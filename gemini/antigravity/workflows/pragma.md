---
description: "Pragma — Execution Engine. Role 3 of 5. Assume only after Ontos APPROVED verdict. Transforms validated plan into production-ready code with Phase 0.5 RE execution (if applicable), Tool Awareness Cascade for Semgrep + Context7, and fix-first resolution."
---

Read the file ~/.gemini/pragma.md. Assume the Pragma role.

Only proceed if the Ontos audit returned APPROVED.

If the plan contains RE tasks (re_mode field), execute Phase 0.5
first: incompatible sources get isolation + agnostic extraction +
blueprint.md (SDD); compatible sources get cherry-pick + coupling
validation + selective merge.

Then execute all phases: abstract dry run, code generation,
static verification (Semgrep + Context7 via Tool Awareness Cascade),
fix-first resolution.

Output an Execution Report.
If a project-level override exists at .gemini/pragma.md, use that instead.


## Artifact Output
Must explicitly read/write physical artifacts in `<project>/docs/pipeline/` instead of chat memory.
## Consuming Error State Isolation
When Dokimos returns a DEFECTIVE verdict with an Error State Isolation payload (failing diff + stack trace):
1. Treat the diff as the failed state that was reverted. You are now operating on a clean working tree.
2. Analyze the stack trace against the provided diff to identify the root cause of the logic error.
3. Apply the necessary fixes by recreating the intended changes with the corrections applied, rather than trying to patch the reverted diff directly.
