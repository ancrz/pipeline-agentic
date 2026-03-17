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
