---
name: db-select
description: Use Oracle MCP to answer database questions with read-only SQL only. Accepts natural-language questions and generates safe SELECT/WITH queries. Rejects any non-query operation.
argument-hint: Input your database question in natural language
user-invocable: true
---

# Skill Instructions

## Purpose

Use Oracle MCP to answer user questions from Oracle database data using read-only SQL.

## Hard Safety Rules (Mandatory)

1. Only run read-only SQL statements that begin with `SELECT` or `WITH`.
2. Never execute any non-query operation, including but not limited to:
   - DML: `INSERT`, `UPDATE`, `DELETE`, `MERGE`
   - DDL: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`, `COMMENT`
   - TCL: `COMMIT`, `ROLLBACK`, `SAVEPOINT`
   - DCL: `GRANT`, `REVOKE`
   - PL/SQL execution: `BEGIN`, `DECLARE`, `CALL`, `EXEC`, `EXECUTE`
   - Session/system operations: `SET`, `SHOW`, `HOST`
3. If the user asks for any operation outside read-only querying, refuse and provide a safe alternative (for example, offer a `SELECT` preview to inspect affected rows).
4. Reject multi-statement SQL. Run one statement per request.
5. Do not use SQLcl command execution tools for this skill. Use query execution only.

## Oracle MCP Usage

1. Resolve requested database/environment names case-insensitively before connecting.
2. Apply alias mapping for common environment names:
   - `DEV` -> `Oracle_DEV`
   - `UAT` -> `Oracle_UAT`
3. If the user does not specify any database/environment, default to `DEV` (resolved connection: `Oracle_DEV`).
4. Treat alias matching as case-insensitive (for example: `dev`, `Dev`, `dEv`, `UAT`, `uat`).
5. If not connected, connect to the resolved saved connection name first.
6. If the resolved connection does not exist in saved connections, ask the user to confirm the exact saved connection name.
7. If the user provides a full connection name directly, use it as-is (connection names are case-sensitive on connect).
8. Execute only read-only queries through Oracle MCP query execution.
9. Return concise, evidence-based answers from query results.
10. For ambiguous requests, ask a focused clarification question before querying.

## Query Construction Rules

1. Prefer explicit column names. Avoid `SELECT *` unless the user explicitly requests all columns.
2. Apply reasonable row limits for exploration (for example `FETCH FIRST 50 ROWS ONLY`) unless the user asks for full output.
3. Use deterministic ordering when showing top-N results.
4. Validate object names and schema assumptions with read-only metadata queries when needed.
5. Keep SQL compatible with Oracle syntax.

## Response Behavior

1. Run the safe read-only query.
2. Output query results only in markdown table format.
3. Do not add explanations, summaries, prefaces, or follow-up suggestions.
4. If no rows are returned, output only the table header (or a single-row table with `NO_DATA`).
5. If blocked by safety rules, output only: `READ_ONLY_MODE: ONLY_SELECT_OR_WITH_ALLOWED`.

## Allowed Examples

- "Show top 10 departments by employee count."
- "List orders created in the last 7 days."
- "Find duplicate customer emails."

## Disallowed Examples

- "Delete old log rows."
- "Drop table EMPLOYEES."
- "Truncate staging table."
- "Update salary by 5%."
