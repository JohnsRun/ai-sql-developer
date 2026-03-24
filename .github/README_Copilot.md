# .github Introduction

This folder defines how the agent should work in this Oracle SQL workspace.

## Purpose
- Keep agent behavior consistent, focused, and evidence-based.
- Separate global rules, reusable prompts, and deep domain skills.
- Make maintenance easier by organizing instructions by responsibility.

## Structure

### 1) `copilot-instructions.md`
Global operating rules for this repository.

Current focus includes:
- Oracle SQL expert behavior
- Limited-context analysis policy (precision over broad discovery)
- Preferred project paths and folder usage

Use this file to define baseline behavior that should apply broadly.

### 2) `prompts/`
Reusable task prompts for repeatable workflows.

Current prompts:
- `save-output.prompt.md`
  - Saves generated output to `03Agent_Memory/Output_[object].md`
  - Returns the saved file path
- `sp-analysis-markdown.prompt.md`
  - Triggers SP analysis workflow
  - Saves analysis result as markdown under `03Agent_Memory/`

Use this folder for task-oriented prompt templates.

### 3) `skills/`
Specialized, high-detail capabilities.

Current skill:
- `sp-analysis/SKILL.md`
  - Stored procedure dependency-chain analysis
  - Upstream/downstream tracing
  - Mechanism analysis
  - Strict line-link validation and output format requirements
- `db-select/SKILL.md`
  - Oracle MCP query skill for natural-language database Q&A
  - Read-only mode (`SELECT`/`WITH` only)
  - Blocks destructive and non-query operations (`DROP`, `DELETE`, `TRUNCATE`, etc.)

Use skills for complex domain logic that requires step-by-step methodology.

### 4) `instructions/`
Reserved for additional instruction modules.

Current status:
- Folder exists and is ready for extension-specific or scenario-specific instruction files.

## When to put content where
- Put **repository-wide behavior** in `copilot-instructions.md`.
- Put **repeatable user intents** in `prompts/`.
- Put **expert workflows with strict procedures** in `skills/`.
- Put **future modular rule sets** in `instructions/`.

## Maintenance Notes
- Keep naming clear and version metadata updated in frontmatter.
- Keep links workspace-relative for markdown navigation in VS Code.
- Prefer narrow, deterministic instructions over broad exploratory guidance.
