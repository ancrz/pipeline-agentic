---
description: "Archon — Strategic Planner. Role 1 of 5. Assume at the start of every task, feature, fix, refactor, or config change. Produces the Execution Plan with dependency classification (dep/interdep/co-dep), RE triage for external sources, and Tool Awareness Cascade provisioning."

---

> **DEPRECATED**: Use native `.agents/agent.json` invocation via `invoke_subagent` instead of this workflow.


Read the file ~/.gemini/archon.md. Assume the Archon role
and produce an Execution Plan for the following task:

${input}

Follow the Topos Integrity Protocol. Classify all cross-module
relationships using the Dependency Relationship Classification
(GEMINI.md). If the task involves an external source, perform
RE Triage (step 3) to assess ontological compatibility.

Output the plan in the structured format defined in archon.md.
If a project-level override exists at .gemini/archon.md, use that instead.


## Artifact Output
Must explicitly read/write physical artifacts in `<project>/docs/pipeline/` instead of chat memory.
