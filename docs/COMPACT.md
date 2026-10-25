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

Current pending (2026-10-24): cross-harness parity remediated (CLAUDE.md / AGENTS.md / GEMINI.md
share Flow Variants with Graphos, Rules 1-12, Scrutator, Error Recovery, Abstract Study,
cascade privilege clause, compaction for 4 harnesses). Claude Code delegation documented as
on-demand by the orchestrator (`description`-driven), `isolation: "worktree"`, nested
sub-agents allowed. Open: Antigravity `enable_shell_tools` still unverified; no push without
user authorization.
