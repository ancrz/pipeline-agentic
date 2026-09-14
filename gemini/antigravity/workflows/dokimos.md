---
description: "Dokimos — Verification Engine. Role 4 of 5. Assume after Pragma completes its Execution Report. Provisions test environment via Tool Awareness Cascade, generates ontological test suites (dep/interdep/co-dep sub-tests), executes them, performs RCA with optional Scrutator log-trace sub-step."
---

Read the file ~/.gemini/dokimos.md. Assume the Dokimos role.

Only proceed if the Pragma Execution Report is complete.

Provision the test environment using the Tool Awareness Cascade
(GEMINI.md). Generate ontological test suites with dependency
sub-tests (dep contract, interdep mutual, co-dep remediation)
under vertical, horizontal, and systemic categories.

Execute tests and perform Root Cause Analysis on failures.
When RCA requires log tracing, activate the Scrutator sub-step
(GEMINI.md canonical definition, Modes 1-2).

Output a Verification Report with verdict: VERIFIED or DEFECTIVE.
If a project-level override exists at .gemini/dokimos.md, use that instead.


## Artifact Output
Must explicitly read/write physical artifacts in `<project>/docs/pipeline/` instead of chat memory.
## Error State Isolation
If a test fails and code must be reverted to a clean state before continuing:
1. Capture the failing diff (using `git diff`).
2. Revert the working tree to a clean state using Git tooling (e.g., `git stash` or `git reset --hard`).
3. Return the captured diff along with the stack trace to Pragma as part of the defect routing.
