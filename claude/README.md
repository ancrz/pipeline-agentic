<div align="center">
# Claude Code Harness: Topos Protocol
**Implementing the 6-stage Topos Pipeline in Claude Code**
</div>


## 🌟 Status: Source of Truth
The Claude structure represents the most mature and complete implementation of the Topos Pipeline. Its multi-agent paradigm, featuring strict YAML frontmatter and explicit model mapping (e.g., `sonnet` for heavy logic, `haiku` for documentation/version control), serves as the **Canonical Source of Truth**. This architecture has been successfully replicated and adapted across all other role-based harnesses (Codex, Antigravity) while respecting their specific form factors.

## 📌 Implementation
Claude Code relies on global context markdown instructions. This harness utilizes the `CLAUDE.md` master file to dictate the orchestration behavior.

```mermaid
flowchart LR
    C[Claude Code] -->|Loads| M[CLAUDE.md]
    M -->|Enforces| A(Archon)
    A --> G1(Graphos G1)
    G1 --> O(Ontos)
    O --> P(Pragma)
    P --> D(Dokimos)
    D --> G2(Graphos G2)
    G2 --> H(Hermon)
    O -.BLOCKED.-> G1
    D -.ERROR.-> G2
    
    style C fill:#8B5CF6,stroke:#6D28D9,color:#fff
    style M fill:#3B82F6,stroke:#2563EB,color:#fff
```


## 🏗️ Agent Formatting (Source of Truth)
In Claude Code, subagents are NOT just standard markdown files. To be recognized as an invocable, routable subagent, the file **MUST** contain a YAML frontmatter block at the very top.

**Format Pattern (`<Agent>.md`):**
```markdown
---
name: <AgentName>
description: <Short description of what the agent does and when to route to it>
model: sonnet  # or sonnet, etc.
permissionMode: autonomous         # or acceptEdits, default
---

# <AgentName> Agent
Role: ...
[Your markdown instructions here...]
```
If an agent lacks this YAML block, it is effectively invisible to the routing table and cannot be spawned as a subagent.

## 🚀 Setup
Deploy the master rules to your global configuration:
```bash
cp claude/CLAUDE.md ~/.claude/CLAUDE.md
```