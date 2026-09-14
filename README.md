<div align="center">

# Topos Pipeline Agentic Framework

**A multi-agent reference architecture enforcing the Topos Integrity Protocol.**

[![License](https://img.shields.io/badge/License-Apache_2.0-blue?style=flat-square)](#)
[![Agents](https://img.shields.io/badge/Agents-6_Stage-purple?style=flat-square)](#)
[![Framework](https://img.shields.io/badge/Multi--Agent-Architecture-green?style=flat-square)](#)

</div>

---

## 🛑 The Problem

Autonomous AI coding agents tend to jump straight to execution. They write code without auditing structural dependencies, they destroy visual interfaces by guessing logic, and they overwrite their own history during error recovery. 
This results in **context explosion, hallucination cascades, and unmaintainable codebases**.

## 🚀 The Solution: Topos V2

Moving beyond linear scripting, Topos V2 establishes a **True Multi-Agent Concurrent Orchestration System**. It enforces deep reasoning, structural auditing, multi-modal grounding, and strict verification before any code is committed. The AI acts as a *Principal Engineer* rather than a passive assistant.

---

## 🏗️ 6-Stage Architecture

Regardless of the underlying LLM or harness, the pipeline operates through six specialized, asynchronous agent roles. 

```mermaid
flowchart TD
    Req["👤 User Request"] --> A
    
    subgraph Pipeline["Topos Pipeline Orchestration"]
        direction TB
        A["🧠 Archon<br/>Strategic Planner"] --> G1["📝 Graphos<br/>Knowledge Weaver"]
        G1 --> O["🛡️ Ontos<br/>Structural Auditor"]
        O -.->|BLOCKED| A
        O --> P["⚙️ Pragma<br/>Execution Engine"]
        
        P --> D["✅ Dokimos<br/>Verification Engine"]
        D -.->|Logic Error + Diff| P
        D -.->|Plan Gap| A
        
        D --> G2["📝 Graphos<br/>Docs & Rollup"]
        G2 --> H["📦 Hermon<br/>Version Control"]
    end

    style Req fill:#1E293B,stroke:#334155,color:#fff
    style A fill:#8B5CF6,stroke:#6D28D9,color:#fff
    style O fill:#3B82F6,stroke:#2563EB,color:#fff
    style P fill:#10B981,stroke:#059669,color:#fff
    style D fill:#F59E0B,stroke:#D97706,color:#fff
    style G1 fill:#475569,stroke:#64748B,color:#fff
    style G2 fill:#475569,stroke:#64748B,color:#fff
    style H fill:#334155,stroke:#475569,color:#fff
```

### The Roles
1. **Archon**: Analyzes requests and creates deterministic Execution Plans. Sets up concurrent *Worktree Tracks*.
2. **Graphos**: Generates interwoven documentation (`feature_YYYY.md`). Prevents context explosion using a 5-step rollup.
3. **Ontos**: Audits plans against Vertical/Horizontal Tracing. Blocks plans lacking proper Runbook updates.
4. **Pragma**: Generates code and encapsulates repetitive tasks into `agent_*.sh` runbooks.
5. **Dokimos**: Validates execution. Performs **Error State Isolation** (reverts git tree on failure and passes clean error diff back to Pragma).
6. **Hermon**: Packages verified changes into atomic, Semantic Versioning commits.

---

## 🧠 Auto-Evolutionary Capabilities

```mermaid
pie title Protocol Priorities
    "Structural Coherence" : 35
    "Epistemic Verification" : 25
    "Execution Safety" : 25
    "Token Efficiency" : 15
```

- **Epistemic Authority Guardrail**: The human is a strategic navigator, not the absolute truth. Agents MUST refute hallucinated APIs, deprecated tools, or non-existent solutions *by any means necessary*.
- **Concurrent Worktrees**: The Orchestrator spawns subagents (`Workspace: share`) to develop features in parallel via isolated Git worktrees.
- **Multimodal Grounding Protocol**: If visual evidence contradicts text narration, *visual empiricism takes precedence*.
- **Runbook Encapsulation**: Repetitive patterns are automatically extracted into `scripts/agent_*.sh` and static-tested by Dokimos.

---

## 📥 Installation & Prerequisites

This repository serves as the **Canonical Source of Truth** for the Topos V2 Agentic Pipeline. It contains the raw Markdown prompt definitions and configuration files used by various agent orchestrators.

**Prerequisites:**
- `git` must be installed on your system.
- If integrating this pipeline into a broader deployment (like `termux-linux-deployer`), you must clone this repository alongside it, as deployment scripts dynamically parse and inject these `.md` files into the global agent environments.

```bash
git clone https://github.com/ancrz/pipeline-agentic.git
```

## ⚙️ Supported Orchestrators

| Platform | Integration Type | Location |
|---|---|---|
| **Antigravity CLI & GUI** | Native Async Agents | `/.agents/` overrides global |
| **Claude Code** | Global Instructions | `/claude/` |
| **Codex** | Rule Policies | `/codex/` |

---
<div align="center">
Built for autonomous engineering.
</div>