---
name: create-md-ToC
description: Generate or repair clickable markdown table of contents for .md files using a collapsible details block, stable anchors, and renderer-safe formatting.
argument-hint: Provide the markdown file path and mode (create, refresh, or fix links)
user-invocable: true
---

# Create Markdown ToC Skill

## Purpose

Process markdown files to create or repair a clickable Table of Contents that is safe across common renderers.

## When To Use

Use this skill when the user asks to:

- add a TOC to a markdown file
- make TOC links clickable
- fix broken section jumps
- convert plain list headings into a clickable contents block

## Default Output Style

Use this structure unless the user requests another style:

```html
<details open>
<summary>Table of Contents (click to expand/collapse)</summary>

- [Section A](#section-a)
- [Section B](#section-b)
- [Section C](#section-c)

</details>
```

Then place stable anchors before each target heading:

```html
<a id="section-a" name="section-a"></a>
## Section A
```

## Processing Rules

1. Target files:
- Only process files with `.md` extension.

2. Heading scope:
- Include major content headings by default (`#`, `##`, `###`), excluding headings inside fenced code blocks.
- Skip duplicate headings by suffixing slugs (`-2`, `-3`, ...).

3. Slug generation:
- Lowercase text.
- Replace spaces with `-`.
- Remove punctuation except `-` and `_`.
- Collapse repeated `-`.
- Trim leading and trailing `-`.

4. Anchor compatibility:
- Always add both `id` and `name` attributes on anchor tags for wider compatibility.
- Keep anchor immediately above the heading.

5. TOC placement:
- Insert TOC at file top, ahead of all markdown content (including any top title).
- If a TOC details block already exists, refresh it in place instead of duplicating.
- Default to expanded TOC using `<details open>` unless the user asks for collapsed by default.

6. Clickability safeguards:
- Do not indent TOC list items with 4 spaces or tabs, which turns them into a code block in many parsers.
- Keep one blank line between summary and list, and between list and `</details>`.
- Do not wrap TOC list in fences.

7. Preservation:
- Preserve all original body content order.
- Do not rewrite unrelated sections.
- Keep existing heading text unchanged unless user explicitly requests normalization.

## Validation Checklist

After editing, verify:

1. TOC entries are rendered as links, not code text.
2. Each TOC link maps to an existing anchor.
3. No duplicate anchor ids remain.
4. Markdown preview supports expand/collapse and section jumps.

## Response Behavior

When this skill completes, report:

1. file processed
2. whether TOC was created, refreshed, or fixed
3. number of headings indexed
4. any headings skipped and why

## Out Of Scope

- Do not generate site-level navigation across multiple files unless requested.
- Do not install markdown plugins or dependencies.
