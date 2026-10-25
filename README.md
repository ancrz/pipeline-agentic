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
    A["Archon: Plan"] --> G1["Graphos G1: Weave"]
    G1 -- "Documented Plan" --> O["Ontos: Audit"]
    O -- "APPROVED" --> P["Pragma: Execute"]
    O -. "BLOCKED" .-> G1
    G1 -. "Remediation" .-> A
    P -. "Structural blocker" .-> O
    P --> D["Dokimos: Verify"]
    D -. "trace" .-> SC(["Scrutator"])
    D -- "verdict" --> G2["Graphos G2: Record"]
    G2 -- "VERIFIED" --> H["Hermon: Commit"]
    G2 -. "LOGIC_ERROR / DEP misuse" .-> P
    G2 -. "PLAN_GAP / DEP breaking" .-> A
    H -- "done" --> DONE(["Done"])
    H -. "conflict" .-> U["User"]
```

The pipeline runs in **Full** mode (all six agents) or **Short** mode (Archon and Ontos
dropped; the orchestrator plans inline and all agents route back to it) to control budget.

### The Roles
1. **Archon**: Analyzes requests and creates deterministic Execution Plans. Sets up concurrent *Worktree Tracks*.
2. **Graphos**: Records every pipeline transition in an interwoven chain (`docs/pipeline/feature_YYYYMMDD_HHMMSS.md`, 5-step rollup) and keeps the project baseline: local git, `README.md` reinforcement graph, `docs/PROJECT.md`, `docs/MILESTONES.md`, `docs/COMPACT.md`.
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
- **Concurrent Worktrees**: Parallel tracks each get an isolated Git worktree — `isolation: "worktree"` on the Agent call in Claude Code, `git worktree add` in Codex / Gemini (sequential there, concurrent in Antigravity).
- **Operating Premises (all harnesses)**: P0 agentic pipeline (validated artifact; design decisions stay with the user), P1 tool reach (standard vs non-conventional path within granted authorization; privilege changes are user-gated), P2 Full / Short modes.
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

## 🔄 Sync (all harnesses)

`./sync.sh` at the repository root installs the pipeline everywhere it applies:

| Command | Effect |
|---|---|
| `./sync.sh` | **auto**: global from this repo; local when run inside another git project or with `--target` |
| `./sync.sh global` | user-level homes `~/.claude`, `~/.codex`, `~/.gemini` (backup + verification + auto-rollback) |
| `./sync.sh local --target <dir>` | project overrides `.claude/`, `.codex/`, `.gemini/`, `.agents/` (root `CLAUDE.md`/`AGENTS.md`/`GEMINI.md` untouched) |
| `--check` / `--dry-run` | report drift without writing (`--check` exits 1 on drift) |
| `--harness claude,codex,gemini` | limit to some harnesses (default: those detected as installed) |
| `--force` | local: overwrite files the project customized (backed up first) |
| `--rollback <dir>` | restore a previous backup |

Before deploying it propagates role bodies from `claude/` (`scripts/sync_roles.py`), refuses
invalid `agent.json`, and writes only files that changed.

## ⚙️ Supported Orchestrators

| Platform | Integration Type | Location |
|---|---|---|
| **Claude Code** | Global instructions + subagents (canonical source) | `claude/CLAUDE.md`, `claude/<Role>.md` |
| **Codex** | Global rule policy + sequential role files | `codex/AGENTS.md`, `codex/roles/<role>.md` |
| **Antigravity** | Native async agents (`agent.json`) + workflows | `.agents/<role>/agent.json`, `gemini/antigravity/workflows/<role>.md` |
| **Gemini CLI** | Global instructions + sequential role files | `gemini/gemini-cli/GEMINI.md`, `gemini/gemini-cli/<role>.md` |

Role bodies are identical across all four harnesses; `claude/` is the canonical source and
`scripts/sync_roles.py` propagates any change to the other copies (`--check` verifies sync).

---
<div align="center">
Built for autonomous engineering.
</div>