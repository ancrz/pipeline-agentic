# COMPACT — context compaction instruction

> Harness-neutral guidance for `/compact` (Claude Code / Codex), `/compress` (Gemini CLI),
> or automatic compaction (Antigravity). Maintained by Graphos; regenerate at each G2.

Preserve:
- Active pipeline mode (Full / Short) and which agents are in play.
- Active intent and milestone status (see `docs/MILESTONES.md`).
- Files changed this session and why; the canonical-source rule (`claude/` → others via
  `scripts/sync_roles.py`).
- Open defects with their routing; decisions the user made (model change, mode choice).
- The three PRIORITY premises (P0 agentic pipeline, P1 tool reach, P2 modes).
- Next pending actions.

Drop:
- Tool output already summarized; superseded plan drafts; resolved errors.
- Full file contents already written to disk (keep paths, not bodies).

Current pending (2026-10-23): Global harness injection and Codex standalone parity verified (Dokimos 44/44 PASS). Hermon to create atomic commit for `codex/AGENTS.md`, `codex/README.md`, `scripts/agent_inject_harnesses.py`, and pipeline documentation under `docs/pipeline/`; no push without user authorization.
