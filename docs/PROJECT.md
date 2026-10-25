# PROJECT — Topos Pipeline Agentic Framework

> Maintained by the Graphos role (Project Documentation Duty). Facts derive from the
> repository and `git log`; inferences are marked as assumptions.

## Premise / intent

A harness-agnostic, prompt-and-config definition of a six-agent software-engineering
pipeline (the **Topos Integrity Protocol**). The same six roles — Archon (plan), Graphos
(weave/record), Ontos (audit), Pragma (execute), Dokimos (verify), Hermon (commit) — are
expressed for four harnesses from one canonical source:

| Harness | Orchestrator | Role bodies |
|---------|--------------|-------------|
| Claude Code (**canonical**) | `claude/CLAUDE.md` | `claude/<Role>.md` |
| Codex | `codex/AGENTS.md` | `codex/roles/<role>.md` |
| Antigravity | `gemini/gemini-cli/GEMINI.md` + `.agents/<role>/agent.json` | `gemini/antigravity/workflows/<role>.md` |
| Gemini CLI | `gemini/gemini-cli/GEMINI.md` | `gemini/gemini-cli/<role>.md` |

Role bodies are identical across harnesses; `claude/` is the source of truth and
`scripts/sync_roles.py` propagates changes (run `--check` to verify).

## Operating premises (PRIORITY)

- **P0 — Agentic Pipeline:** the pipeline returns a validated artifact + report; the user
  owns design/architecture decisions, the agents own deterministic work. Hand-written code
  is a `<USER_CODE_PROPOSAL>` re-validated by the pipeline.
- **P1 — Tool Reach:** each agent inventories its tools and chooses a standard or
  non-conventional path *within granted authorization*, declaring the blast radius. Privilege
  changes are user-gated and never a path choice.
- **P2 — Pipeline Modes:** Full (all six) or Short (Archon + Ontos dropped; orchestrator plans
  inline) to control budget.

## Canonical topology

`Archon(1) → Graphos G1(2) → Ontos(3) → Pragma(4) → Dokimos(5) → Graphos G2(2) → Hermon(6)`,
orchestrator-mediated, with feedback loops routed through Graphos. See the orchestrator files
for the authoritative diagram.

## Architecture decisions (owned by the user)

- Claude Code is the canonical source; other harnesses are mirrors.
- Model mapping per harness: Claude Code uses `sonnet` for reasoning roles and `haiku` for
  Graphos/Hermon; Antigravity/Gemini use `pro`/`flash`/`flash_lite`.
- Deployment is manual (`cp` into `~/.claude`, `~/.codex`, `~/.gemini`); the repo is
  authoritative on divergence.

## Open questions / assumptions

- **`enable_shell_tools`** (Antigravity `agent.json`): present only on `dokimos`; not
  confirmed in official Antigravity docs. Not added to Pragma/Hermon speculatively — see
  `gemini/README.md`.
- Harness compaction knobs (`model_auto_compact_token_limit`, `model.compressionThreshold`,
  Antigravity ~135k auto) were verified against vendor sources in 2026-10 and may change.

## Sync

`./sync.sh` (repo root) is the single entry point: `auto` (default) resolves to `global`
(`~/.claude`, `~/.codex`, `~/.gemini`, via `scripts/agent_inject_harnesses.py`) or `local`
(project overrides `.claude/`, `.codex/`, `.gemini/`, `.agents/`). It propagates role bodies,
validates `agent.json`, syncs only detected harnesses and only changed files.

## Verify

No build/test runner (prompt/config repo). Integrity checks:
- `python3 scripts/sync_roles.py --check` — role bodies in sync with `claude/`.
- `python3 -m json.tool .agents/*/agent.json` — agent manifests valid.
- `./sync.sh --check` — installed harness files match the repository (exit 1 on drift).
