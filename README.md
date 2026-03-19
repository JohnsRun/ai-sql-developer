# AI-Powered SQL Developer Workflow  
### Next-Level SQL Development Efficiency with AI

> A high-efficiency SQL development workflow powered by AI — from natural language to optimized queries with automated validation and feedback loops.

- [Connect Your Database to VS Code](Docs_EN/01Connect_Your_Database_to_VSCode.sqlnb)
- Notebooks are all you need
- AI Coding with GitHub Copilot
- Skills are the key.

## 1. Folder Information

### Key Folders
- `.github/`: Config files for AI Agent behavior in VS Code (instructions, prompts, and skills).
- `01Context_Docs/`: Business and project background documents.
- `03Agent_Memory/`: AI-generated outputs and notes.
- `Docs_EN/`: English documentation notebooks and images.

### Current Folder Structure
```text
.
├── README.md
├── skills-lock.json
├── .github/
│   ├── copilot-instructions.md
│   ├── prompts/
│   │   ├── save-output.prompt.md
│   │   └── sp-analysis-markdown.prompt.md
│   └── skills/
│       ├── find-skills/
│       │   └── SKILL.md
│       ├── sp-analysis/
│       │   ├── SKILL.md
│       │   └── examples/
│       │       └── examples_output.md
│       └── sql-lineage/
│           ├── SKILL.md
│           └── examples/
│               └── Output_bill_line_id.md
├── 01Context_Docs/
│   ├── Business_Requirement.md
│   ├── Project_Context.md
│   └── Test_Plan.md
├── 03Agent_Memory/
└── Docs_EN/
    ├── 01Connect_Your_Database_to_VSCode.sqlnb
    ├── 02Notebook_is_what_your_need.sqlnb
    └── AI_Agent_4PLSQL_Best_Practices.ipynb
```

# 2. Use Cases

## 1) Agent Skills
- [/sp-analysis](.github/skills/sp-analysis/SKILL.md): Input an SP name and attach Oracle package content to analyze dependency flow and mechanism.
- [/sql-lineage](.github/skills/sql-lineage/SKILL.md): Trace PL/SQL field or variable lineage, including upstream sources, transformation steps, and downstream destinations as an ASCII graph. Supports single-SP mode and whole-package mode.

## 2) Agent Prompts
- [/save-output](.github/prompts/save-output.prompt.md): Save previous output as a markdown file under `03Agent_Memory/`.
- [/sp-analysis-markdown](.github/prompts/sp-analysis-markdown.prompt.md): Analyze target SP and produce markdown output.

# 3. Notes
- [AI Agent for PL/SQL Best Practices (Notebook)](Docs_EN/AI_Agent_4PLSQL_Best_Practices.ipynb)

## Reference
[Using SQL Developer for VS Code](https://docs.oracle.com/en/database/oracle/sql-developer-vscode/25.3/sqdnx/using-sql-developer-vs-code.html)

