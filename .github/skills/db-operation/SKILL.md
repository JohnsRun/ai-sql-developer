---
name: db-operation
description: Use Oracle MCP to answer database questions and perform database operations, including read-only queries and approved DDL/DML changes. This skill must not be invoked automatically.
argument-hint: Describe the database query or operation in natural language
user-invocable: true
---

# Skill Instructions

## Purpose

Use Oracle MCP to answer user questions from Oracle database data and to perform database operations when the user explicitly chooses to use this skill.

## Invocation Rules (Mandatory)

1. Do not invoke this skill automatically.
2. Use this skill only when either:
   - the user explicitly invokes `/db-operation`, or
   - the assistant asks the user whether they want to use `/db-operation` and the user explicitly agrees.
3. If a database operation request appears in a normal chat without explicit invocation or confirmation, do not execute anything. Ask the user whether they want to use `/db-operation`.

## Hard Safety Rules (Mandatory)

1. Run exactly one SQL statement per request. Reject multi-statement SQL.
2. Keep SQL compatible with Oracle syntax.
3. Never hide or silently transform a destructive operation into something broader than the user asked for.
4. For read-only requests, only run statements that begin with `SELECT` or `WITH`.
5. For any non-read-only operation, do not execute immediately. First show the exact SQL and ask for explicit approval.
6. Treat the following as approval-required operations:
   - DML: `INSERT`, `UPDATE`, `DELETE`, `MERGE`
   - DDL: `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `RENAME`, `COMMENT`
   - TCL: `COMMIT`, `ROLLBACK`, `SAVEPOINT`
   - DCL: `GRANT`, `REVOKE`
   - PL/SQL execution: `BEGIN`, `DECLARE`, `CALL`, `EXEC`, `EXECUTE`
   - Session/system operations: `SET`, `SHOW`, `HOST`
7. Explicit approval must be clear and current, for example: `approve`, `approved`, `yes, run it`, or equivalent confirmation after the SQL preview.
8. If approval is not explicit, do not execute the statement.
9. If the request is ambiguous or risky, ask a focused clarification question before producing executable SQL.

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
8. Use Oracle MCP SQL execution tools only for the single SQL statement being handled.
9. Return concise, evidence-based answers from execution results.

## Query And Operation Rules

1. Prefer explicit column names. Avoid `SELECT *` unless the user explicitly requests all columns.
2. Apply reasonable row limits for exploration (for example `FETCH FIRST 50 ROWS ONLY`) unless the user asks for full output.
3. Use deterministic ordering when showing top-N query results.
4. Validate object names and schema assumptions with safe metadata queries when needed.
5. For write or schema-changing requests, prefer a safe preview step before execution when practical, such as:
   - a `SELECT` preview of affected rows for DML
   - metadata inspection for DDL targets
6. When previewing an approval-required operation, show:
   - the target connection
   - the exact SQL to be executed
   - a brief impact statement if it can be determined safely
   - a request for explicit approval
7. After approval, execute only the exact approved SQL. If the SQL must change, ask for approval again.

## Response Behavior

1. For read-only queries, run the safe query and output query results only in markdown table format.
2. For approval-required operations before approval, do not execute. Output only:
   - the exact SQL in a fenced `sql` block
   - a one-line approval request
3. For approval-required operations after approval, execute the exact SQL and return only the execution result, kept concise.
4. If blocked because the skill was not explicitly invoked or confirmed, output only: `CONFIRM_DB_OPERATION_SKILL: ASK_USER_TO_USE_DB_OPERATION`
5. If blocked because approval is missing for a non-read-only operation, output only: `APPROVAL_REQUIRED: NON_READ_ONLY_SQL_NOT_EXECUTED`

## Allowed Examples

- "Use /db-operation to show the top 10 departments by employee count."
- "Use /db-operation to insert one audit row into AUDIT_LOG."
- "Use /db-operation to alter table EMPLOYEES add column NOTES varchar2(200)."

## Disallowed Examples

- Automatically running a write operation because it seems helpful.
- Executing DDL or DML without first showing the exact SQL and getting approval.
- Running a modified version of previously approved SQL without asking again.