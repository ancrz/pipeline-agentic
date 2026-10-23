# MILESTONES — per intent and per agent

> Maintained by the Graphos role. `✅` done, `🔄` in progress, `⛔` blocked, `⬜` pending.

## Intent: Graph coherence across all harnesses

```mermaid
flowchart LR
    I["Intent: Graph coherence"] --> M1["M1: defects inventoried ✅"]
    M1 --> M2["M2: role bodies unified + propagated ✅ (Pragma/sync)"]
    M2 --> M3["M3: 3 orchestrators corrected ✅"]
    M3 --> M4["M4: READMEs + diagrams fixed ✅"]
    M4 --> M5["M5: mermaid/json validated ✅ (Dokimos)"]
    M5 --> M6["M6: committed 🔄 (Hermon)"]
```

## Intent: Tool-Reach premise (PRIORITY P1)

```mermaid
flowchart LR
    I["Intent: Tool-Reach premise"] --> M1["M1: premise text authored ✅"]
    M1 --> M2["M2: embedded PRIORITY in 3 orchestrators ✅"]
    M2 --> M3["M3: per-platform tool surfaces documented ✅"]
    M3 --> M4["M4: per-role obligations added to role bodies ✅"]
    M4 --> M5["M5: safety boundary (no privilege escalation) stated ✅"]
```

## Intent: Pipeline Modes (P2) + compaction

```mermaid
flowchart LR
    I["Intent: Modes + compaction"] --> M1["M1: Full/Short modes defined ✅"]
    M1 --> M2["M2: Short-mode routing via orchestrator ✅"]
    M2 --> M3["M3: compaction verified per harness ✅"]
    M3 --> M4["M4: Graphos COMPACT.md duty defined ✅"]
```

## Intent: Graphos project-documentation duty

```mermaid
flowchart LR
    I["Intent: Project documentation"] --> M1["M1: Graphos role rewritten with duty ✅"]
    M1 --> M2["M2: README reinforcement graphs ✅"]
    M2 --> M3["M3: docs/ PROJECT + MILESTONES + COMPACT ✅"]
    M3 --> M4["M4: local git + chain artifacts ✅"]
```

## Per-agent milestone summary

| Agent | Role milestones (reinforcement graph in each role body) |
|-------|---------------------------------------------------------|
| Archon | context+tools inventoried → deps classified → path+blast radius → plan returned |
| Graphos | state recorded → docs/reinforcement graphs → COMPACT.md → chain linked |
| Ontos | traces → omissions/co-dep → tool-reach audit → verdict |
| Pragma | tools declared → dry run → code → static-verify → report |
| Dokimos | env provisioned → suites → executed+RCA → verdict |
| Hermon | diff grouped → atomic commits → dependency order → report |
