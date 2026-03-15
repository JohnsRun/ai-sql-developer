---
name: sql-lineage
description: You are an expert in Oracle SQL. Parse PL/SQL stored procedures or an entire package to trace the lineage of a specific field or variable — showing its upstream sources, transformation steps, and downstream destinations as an ASCII graph. Supports two modes: single-SP mode (SP name + field + package file) or whole-package mode (field + package file). LLM base model temperature should be 0.
argument-hint: Input [Field/Variable Name] and optionally [SP Name], then attach [Package File]
version: 2.0
---

# Skill Instructions

## Mode Detection (Step 0 — Mandatory)

Before any analysis, determine the operating mode from what the user provides:

| User provides | Mode |
|---|---|
| Field/variable name + SP name + package file | **Single-SP mode** — trace the field within that one procedure only |
| Field/variable name + package file (no SP name) | **Whole-package mode** — follow the field across every SP/function that references it |

If **no package file is attached**, stop immediately and ask:
> "Please attach the PL/SQL package file you want to analyze."

If **no field or variable name is given**, stop immediately and ask:
> "Please provide the field or variable name you want to trace (e.g., `v_salary`)."

Do NOT guess filenames. Do NOT search the workspace unless the user explicitly asks.

---

## Investigation Steps


### Step 1 — Locate all occurrences of the target field/variable

Search within the analysis scope (single SP body or entire package body) for every occurrence of the target name. Classify each occurrence into one of these roles:

| Role | Description | Examples |
|---|---|---|
| **ASSIGNED FROM** | The variable receives a value | `v_x := expr`, `SELECT col INTO v_x FROM …`, `v_x := func(…)`, IN parameter binding |
| **PASSED TO** | The variable is passed as an argument to another SP/function | `other_sp(v_x)`, `func(v_x)` |
| **WRITTEN TO TABLE** | The variable's value is written to a DB table | `INSERT … VALUES(v_x)`, `UPDATE … SET col = v_x` |
| **USED IN CONDITION** | The variable is used in a WHERE / IF / CASE expression (analysis only, do not render in final output) | `WHERE col = v_x`, `IF v_x > 0` |
| **RETURNED** | The variable is an OUT/RETURN value | `p_out := v_x`, `RETURN v_x` |

Record for every occurrence:
- Role (from table above)
- The exact expression/statement involved
- Line number in the file

---

### Step 2 — Identify upstream sources (where the value comes FROM)

For each **ASSIGNED FROM** occurrence found in Step 1, trace one level back to determine the ultimate source:

- **DB table column** → record as `TABLE_NAME.COLUMN_NAME` with the SELECT/cursor statement and line number
- **Input parameter** → record as `PARAM_NAME (IN parameter)` with the procedure signature line
- **Another variable** → record as `VAR_NAME` and note whether that variable itself has an upstream source (chain one more level if it is also assigned via SELECT or parameter)
- **Literal / expression** → record as the literal value or expression (e.g., `SYSDATE`, `'Y'`, `v_a + v_b`)
- **Function return** → record as `FUNC_NAME()` return value

---

### Step 3 — Identify downstream destinations (where the value FLOWS TO)

For each **PASSED TO**, **WRITTEN TO TABLE**, and **RETURNED** occurrence found in Step 1, identify the destination:

- **DB table column** → record as `TABLE_NAME.COLUMN_NAME` with the INSERT/UPDATE statement and line number
- **Another SP/function parameter** → record as `SP_NAME(PARAM_NAME)` and note which parameter position it maps to
- **OUT parameter / RETURN** → record as the output parameter name or RETURN type
- **Intermediate variable** → record as the target variable name and follow one level forward if it subsequently flows to a table or OUT parameter

---

### Step 4 — Build ASCII Lineage Graph

Represent the full lineage chain rendered inside a fenced ` ```text ` block so spacing is preserved.

**Format:**

```text
[1] source_node
    |
    | (L:042 SELECT INTO)
    v
[2] intermediate_node
    |
    | (L:118 UPDATE SET)
    v
[3] destination_node
```

Alignment rules:
- Use a vertical flow only (`|` and `v`) for readability.
- Use sequential numeric node labels: `[1]`, `[2]`, `[3]`, ...
- Keep long SQL statements out of the graph; put full statements in occurrence tables.
- Line numbers are always zero-padded to 3 digits (e.g., `L:042`).
- If no upstream sources exist, start the graph with `[-- origin unknown --]`.
- If no downstream destinations exist, end the graph with `[-- terminal --]`.
- Do **not** include join-condition-only hops in the graph (e.g., `ON a.id = b.id`) unless they also perform true value movement (assignment, write, pass, return).

**Whole-package mode:** produce one fenced graph per SP under a `#### SP_NAME` sub-header. If an SP has no occurrences of the target field, skip it silently.

---

### Step 5 — Final Validation Pass (mandatory)

Before writing output:

- Re-verify every line number in every arrow label and every clickable reference against the actual file.
- Confirm that every upstream source actually assigns to the target variable (not merely reads it).
- Confirm that every downstream destination actually receives the target variable's value.
- Confirm graph edges do not include join-condition-only links.
- Confirm `--None--` or `[-- origin unknown --]` entries have no line numbers appended.
- Confirm the ASCII graph is internally consistent with the occurrence list from Step 1.

---

## Output Structure

Assemble results using **exactly** these section headers, in this order:

---

### `# #1 Field Lineage Graph: <FIELD_NAME>`

*(Fenced `text` code block as described in Step 4)*

Graph rendering rules for this section:

```text
[1] source_node
    |
    | (L:NNN OPERATION)
    v
[2] intermediate_node
    |
    | (L:NNN OPERATION)
    v
[3] destination_node
```

- Keep node text concise in the graph; put full SQL in `#2` tables.
- Exclude pure join-condition edges from this graph.

One-line summary immediately after the code block (plain text, no heading):
> **`<FIELD_NAME>`** originates from `<source(s)>` and flows to `<destination(s)>`.

---

### `# #2 Occurrence Detail`

Two sub-sections, each as a markdown table:

#### Upstream — ASSIGNED FROM

| # | Line | Statement | Source |
|---|---|---|---|
| 1 | [L:NN](path#LNN) | `SELECT col INTO v_field FROM TABLE_A WHERE …` | `TABLE_A.COL` |
| 2 | [L:NN](path#LNN) | `v_field := p_in_param` | `IN param p_in_param` |

#### Downstream — WRITTEN TO / PASSED TO / RETURNED

| # | Line | Statement | Destination |
|---|---|---|---|
| 1 | [L:NN](path#LNN) | `UPDATE TABLE_X SET col = v_field WHERE …` | `TABLE_X.COL` |
| 2 | [L:NN](path#LNN) | `other_sp(v_field)` | `SP_Y(p_arg)` |

Use workspace-relative paths for all line links. If a sub-section has no rows, replace the table with `--None--`.

---

## Best Practices

- ✓ Search the entire SP body — including cursors, subqueries, CTEs, BULK COLLECT, FORALL, and exception handlers
- ✓ Resolve variable aliases and record fields (e.g., `rec.salary` when tracing `salary`)
- ✓ One level of chaining is sufficient — trace one step back for upstream and one step forward for downstream; do not recurse infinitely
- ✓ Work exclusively from the attached file — do not search the workspace unless asked
- ✓ Line-number accuracy is non-negotiable; re-verify before writing output
- ✓ Graph should show value movement only; do not render pure join-condition links
- ✓ `--None--` entries must never have line numbers or links appended
- ✓ Avoid adding commentary or descriptions outside the defined output sections
- ✓ If any uncertainty arises during output assembly, check the example file content in .github/skills/sql-lineage/examples/Output_bill_line_id.md 