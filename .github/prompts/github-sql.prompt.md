---
name: github-sql
description: "Use GitHub MCP to work on Oracle SQL tasks in JohnsRun/ai-sql-developer using agent mode and GPT-5.3-Codex."
argument-hint: "Describe the SQL task to run on the GitHub repository"
agent: agent
model: GPT-5.3-Codex
---
Use GitHub MCP to complete the user's SQL task against this repository:
- https://github.com/JohnsRun/ai-sql-developer

Execution requirements:
- Treat `JohnsRun/ai-sql-developer` as the default repository target.
- Use GitHub MCP tools for repository reads/updates when possible.
- Keep work focused on Oracle SQL and PL/SQL assets (`.sql`, `.pkb`, `.pks`, `.pkg`).
- If proposing or making code changes, keep edits minimal and precise.
- If creating or editing executable Oracle scripts, ensure a standalone trailing `/` delimiter exists; if missing, add it and explicitly report the fix.

Response format:
- `Repository:` owner/repo and branch used
- `Task:` one-line interpretation of the request
- `Actions:` key MCP actions performed
- `Result:` concise outcome with changed file paths
- `Notes:` risks, assumptions, or required follow-up
