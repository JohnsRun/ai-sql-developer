# AI Agent for PL/SQL Best Practices (VS Code)

## #1 When To Use
1. Requirements Alignment
2. Context Management
3. Security & Compliance
4. Progressive Code Generation
5. Knowledge Management (Indexing)
6. Legacy Modernization & Maintenance
7. Quality & Compliance (Testing)

## #2 Config Files

.github/ is the path for Copilot config files. There are 2 subfolders, `./instructions` and `./skills` in it.

### Use a `.github/copilot-instructions.md` file

Automatically applies to all chat requests in the workspace. VS Code automatically detects a `.github/copilot-instructions.md` Markdown file in the root of your workspace.

Use `copilot-instructions.md` for:

- Coding style and naming conventions that apply across the project
- Technology stack declarations and preferred libraries
- Architectural patterns to follow or avoid
- Security requirements and error handling approaches
- Documentation standards

Use `/init` can generate or update this file.

### Use `.instructions.md` files

You can create file-based instructions with `*.instructions.md` Markdown files that are applied dynamically based on the files or tasks the agent is working on. The path should be `/instructions/*.instructions.md files`.

Use `.instructions.md` files for:

- Different conventions for frontend vs. backend code
- Language-specific guidelines in a monorepo
- Framework-specific patterns for specific modules
- Specialized rules for test files or documentation

### Use `SKILL.md` Files

Agent Skills are folders of instructions, scripts, and resources that GitHub Copilot can load when relevant to perform specialized tasks. Skills are stored in directories (defined as `[skill-name]`) with a `SKILL.md` file that defines the skill's behavior. The path should be `./skills/[skill-name]/SKILL.md`.

**Reference**:
- [Use custom instructions in VS Code](https://code.visualstudio.com/docs/copilot/customization/custom-instructions#_use-instructionsmd-files)
- [Use Agent Skills in VS Code](https://code.visualstudio.com/docs/copilot/customization/agent-skills)

---

## #2 In Github Copilot Enterprise version, I hope to input a file to provide context which is about the program language, the requirement and the output format, etc. What's the best practises?

Create your context file.

```
# Project Context

### Programming Language
- Language: Python 3.x
- Key libraries: OpenAI client, os module
- Code style: PEP 8

### Requirements
- Specific business rules
- Integration points (APIs, databases)
- Error handling expectations

### Output Format
- Function signatures
- Return types
- Example outputs

```

**Remark:** Good: "Generate code following the specs in /docs/requirements.md and language guidelines in /docs/language-standards.md"

# How Guide Copilot towards helpful outputs

- 1.Provide Copilot with helpful context: open relevant files and close irrelevant files.

# How to Handle Line Number Drift?

Use Agent mode and GPT-5.3-Codex.

![image.png](attachment:image.png)

# How to reduce rework in Agent usage?

1. Archive agent sessions: Archiving/Hiding a session doesn't delete it but moves it out of the active sessions list. At any time, you can unarchive a session to restore it to the active sessions list.

![image.png](attachment:image.png)

2. Use Agent skills (`/skills`) to maintain reusable workflows.

![image-2.png](attachment:image-2.png)
