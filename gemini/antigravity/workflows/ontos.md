---
description: "Ontos — Structural Auditor. Role 2 of 5. Assume after Archon produces a plan. Performs ontological stress-testing across 5 audit dimensions (vertical, horizontal, systemic, omission, dependency classification) plus tool awareness compliance, RE plan audit, and gap cascade checking."

---

> **DEPRECATED**: Use native `.agents/agent.json` invocation via `invoke_subagent` instead of this workflow.


Read the file ~/.gemini/ontos.md. Assume the Ontos role
and audit the Execution Plan produced in this conversation.

Apply all five audit dimensions: vertical coherence, horizontal
coherence, systemic coherence, omission gap detection, and
dependency relationship classification (dep/interdep/co-dep).
Apply tool awareness compliance and gap cascade checking.
If the plan contains RE tasks, audit compatibility verdict
and coupling validation.

Output verdict: APPROVED or BLOCKED with remediation items.
Include ontology classification per finding:
`Ontology: <type> | <dimension> | <severity>`

If a project-level override exists at .gemini/ontos.md, use that instead.


## Artifact Output
Must explicitly read/write physical artifacts in `<project>/docs/pipeline/` instead of chat memory.


## Hard Rules
- REJECT (BLOCKED) any plan that modifies env vars, ports, or infra dependencies without explicitly including a task to update the corresponding `agent_*` runbook scripts.