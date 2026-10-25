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

Current pending (2026-10-25): branch `feat/smart-sync` adds `./sync.sh` (auto/global/local,
--check/--dry-run/--harness/--force/--rollback) and runbook `--only` + portable paths. Only
`main` exists on origin (merged branches pruned). Open: push/merge of `feat/smart-sync` awaits
user authorization; Antigravity `enable_shell_tools` unverified.
