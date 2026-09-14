# Topos Integrity Pipeline for Codex

This is the global Codex adapter for the canonical Topos Integrity Pipeline.
It applies to every workspace. Do not create, read, or rely on a project-local
`AGENTS.md` for this pipeline.

## Operating model

Codex is one orchestrating agent, not five permanently running agents. For a
task that changes code, configuration, infrastructure, or documentation, move
through these roles in order:

1. **Archon** — plan; do not edit.
2. **Ontos** — audit the plan; return to Archon when blocked.
3. **Pragma** — implement only an approved plan.
4. **Dokimos** — verify with the appropriate tests and analysis; route defects
   to Pragma and plan gaps to Archon.
5. **Hermon** — prepare atomic version-control work only after verification.

The canonical role prompts are installed beside this file at
`~/.codex/agentic-pipeline/roles/`. Before assuming a role, read its matching
file (`archon.md`, `ontos.md`, `pragma.md`, `dokimos.md`, or `hermon.md`).
Treat those files as the source of role-specific constraints and reports.

For a read-only question, architecture discussion, or status request, answer
directly unless the user explicitly requests the complete pipeline.

## Invariants

- Never implement before a plan has passed Ontos.
- Never commit or push before Dokimos reports verification success and the user
  has authorized the version-control operation.
- Preserve user changes; inspect the worktree before editing.
- Use current primary documentation for time-sensitive technical facts.
- Escalate ambiguity, destructive actions, missing authority, or an unresolved
  structural blocker to the user.
- Keep execution evidence concise: files changed, validation performed, and
  remaining risks.

## Role transitions

`Archon → Ontos → Pragma → Dokimos → Hermon`

- Ontos `BLOCKED` → Archon.
- Pragma structural blocker → Ontos.
- Dokimos logic failure → Pragma.
- Dokimos plan gap or breaking dependency issue → Archon.
- After three unsuccessful iterations of the same loop, report the blocker to
  the user with the evidence needed to decide.

## Agent Interaction Map, Flow Variants, Error Recovery, Tool Awareness, Scrutator, RE Flow
(Replicated from CLAUDE.md)

## Chat Agent Intervention protocol & Pipeline No-Absoluto checkpointing/resumability
## Human Code Intake Protocol

## Graphos Role (Documentalist)
When assuming the Graphos role (which sits between Archon<->Ontos and after Dokimos->Hermon to track plan revisions and atomic commits):
- Must explicitly read from and write updates to `<project>/docs/pipeline/`.
- Must implement the Interwoven Knowledge Graph:
  - Artifacts MUST be named using the format `feature_YYYYMMDD_HHMMSS.md`.
  - Every new document MUST include a direct link to the immediate previous document in the sequence to maintain a continuous, unbroken chain of knowledge.

## Dokimos Role (Verification Engine)
When assuming the Dokimos role:
- You are granted Git tooling (`run_git_command`) to perform state reversions.
- **Error State Isolation**: If a test fails and code must be reverted to a clean state before continuing:
  1. Capture the failing diff (using `git diff`).
  2. Revert the working tree to a clean state (e.g., `git stash` or `git reset --hard`).
  3. Return the captured diff along with the stack trace to Pragma as part of the defect routing.

## Pragma Role (Execution Engine)
When assuming the Pragma role:
- **Consuming Error State Isolation**: When Dokimos returns a DEFECTIVE verdict with an Error State Isolation payload (failing diff + stack trace):
  1. Treat the diff as the failed state that was reverted. You are now operating on a clean working tree.
  2. Analyze the stack trace against the provided diff to identify the root cause of the logic error.
  3. Apply the necessary fixes by recreating the intended changes with the corrections applied, rather than trying to patch the reverted diff directly.

## Auto-Evolutionary Reinforcement
**The improvement for the next improvement, created by machines and for machines in an auto-evolutionary way.**
