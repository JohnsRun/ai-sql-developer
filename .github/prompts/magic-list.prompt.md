---
agent: Ask
name: magic-list
model: GPT-5.3-Codex
description: List slash commands, agent definitions, and hook-related files under .github and summarize them in a 3-column table (Command names, Description, Path of the file).
version: 1.0
---
When the user runs this command, inspect only the `.github/` directory and produce a concise inventory table.

Scope:
1. Slash commands from `.github/prompts/*.prompt.md`.
2. Agent definitions from `.github/**/*.agent.md`.
3. Hook-related files/configs under `.github/` (any file/path/content indicating hook or hooks).

Extraction rules:
1. For slash commands, read frontmatter `name` and render as `/<name>`.
2. For descriptions, use frontmatter `description` when available; otherwise write a short factual summary.
3. For path, provide the repository-relative file path.
4. If a category has no matches, include a row with:
   - Command names: `N/A`
   - Description: `No entries found for this category.`
   - Path of the file: `N/A`
   and label the category in the description text.

Output format:
1. Return one markdown table with exactly 3 columns:
   - `Command names`
   - `Description`
   - `Path of the file`
2. Keep rows grouped in this order:
   - Slash commands
   - Agents
   - Hooks
3. Do not include extra prose before or after the table unless the user asks for details.
