# 2. Use Cases

## 1) Agent Skills
- [/sp-analysis](.github/skills/sp-analysis/SKILL.md): Input an SP name and attach Oracle package content to analyze dependency flow and mechanism.
- [/sql-lineage](.github/skills/sql-lineage/SKILL.md): Trace PL/SQL field or variable lineage, including upstream sources, transformation steps, and downstream destinations as an ASCII graph. Supports single-SP mode and whole-package mode.


## 2) Agent Prompts
- [/save-output](.github/prompts/save-output.prompt.md): Save previous output as a markdown file under 03Agent_Memory/.
- [/sp-analysis-markdown](.github/skills/sp-analysis/examples/examples_output.md): Analyze target SP and produce markdown output.
- [/]

# 3. Notes
- [AI Agent for PL/SQL Best Practices (Notebook)](AI_Agent_4PLSQL_Best_Practices.ipynb)

## 1. Folder Information

## Key Folders
- .github/: Config files for AI Agent behavior in VS Code (instructions and skills).
- 01Context_Docs/: Business and project background documents.
- 02Development_Zone/: Oracle SQL packages and test scripts.
- 03Agent_Memory/: AI-generated outputs and notes.
- 04Agent_Tools/: Tool-specific skill assets and examples.

## Current Folder Structure
```text
.
├── AI_Agent_4PLSQL_Best_Practices.md
├── README.md
├── skills-lock.json
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   └── skills/
├── 01Context_Docs/
│   ├── Business_Requirement.md
│   ├── Project_Context.md
│   └── Test_Plan.md
├── 02Development_Zone/
│   └── Oracle_Package/
│       ├── JTA_Create_Database.sql
│       ├── JTA_Packages.sql
│       └── JTA_Test_Code.sql
├── 03Agent_Memory/
└── 04Agent_Tools/
```