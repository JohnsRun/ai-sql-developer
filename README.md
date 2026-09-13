# AI-Powered SQL Development 

Use GitHub Copilot as a controlled Oracle SQL workspace. The repository's `.github` configuration provides specialized agents that translate focused requests into database actions, enforce safety rules, and return consistent results without exposing connection credentials.

## Start With An Agent

Choose the agent that matches the job. Each agent uses only its dedicated connection script and supports DEV or UAT; production routing is not supported.

| Agent | Use it for | Safety behavior | Example request |
| --- | --- | --- | --- |
| [`DB_Query_Agent`](.github/agents/DB_Query_Agent.agent.md) | Read-only `SELECT`, `WITH`, `SHOW`, and `DESC` requests | Executes one read-only statement and returns the CLI Markdown output | `Show the first 10 rows from STAFF` |
| [`DB_Edit_Agent`](.github/agents/DB_Edit_Agent.agent.md) | Read-only requests plus approved `INSERT`, `UPDATE`, `DELETE`, and `MERGE` | Previews every DML statement and waits for explicit approval before execution | `Update STAFF wage for staff 1001 to 8000` |
| [`DB_DDL_AGENT`](.github/agents/DB_DDL_AGENT.agent.md) | Exporting an Oracle package body | Accepts one `PACKAGE_NAME.pkb`, saves the complete DDL locally, and returns a 10-line preview | `PKG_PAYROLL.pkb` |

### How To Invoke Them

Open Copilot Chat and select the matching agent, or invoke the agent by name. Requests default to DEV. Prefix a request with `UAT|` to use UAT, for example:

```text
UAT|Show STAFF
```

The agents validate input before execution. They reject multi-statement requests, unsupported SQL, ambiguous object names, unsafe unfiltered `UPDATE` or `DELETE` statements, and attempts to bypass approval. `DB_Edit_Agent` commits each approved DML statement as part of its CLI execution; it does not support separate `COMMIT` or `ROLLBACK` commands.

## Supporting Copilot Tools

The `.github` folder also contains reusable prompt modes and skills:

- `/db-select`: Oracle MCP read-only mode for `SELECT` and `WITH` queries.
- `/db-operation`: Oracle MCP operation mode with an exact-SQL preview and explicit approval for non-read-only work.
- `/db-query`, `/db-action`, and `/db-audit`: database-specific guidance and read-only auditing workflows.
- `/sql-lineage` and `pkg-analysis`: trace field flow or stored-procedure dependencies in PL/SQL.
- `/mermaid-lite`: create text-only Mermaid diagrams for database and workflow documentation.

The agent definitions live in [.github/agents](.github/agents), prompts in [.github/prompts](.github/prompts), and skills in [.github/skills](.github/skills). Read the relevant definition before extending an agent or changing its execution contract.

## Guides In 00Guidelines


### #1 [ Connect Your Database to VS Code](00Guidelines/01Connect_Your_Database_to_VSCode.md)
Set up the VS Code database extension, create a connection, and prepare a safe Oracle user for notebook work.

### #2 [Notebook Is What You Need](/00Guidelines/02Notebook_is_what_your_need.md)
Demonstrates how SQL notebooks combine markdown, Oracle SQL, script execution, and shell commands in one workflow.

### #3 [Customize Copilot: Specialize AI to Work for You](00Guidelines/03Customize_Copilot_Specialize_AI_to_Work_for_You.md)
Explains Copilot customization files, prompt files, skills, and MCP usage in this repository.

### #4 [Vibe Coding](https://johnsrun.github.io/sql-vibe-coding/)
Notebook placeholder for future workflow notes or experiments.










