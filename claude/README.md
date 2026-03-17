# Topos Integrity Pipeline

A five-stage agentic development pipeline for Claude Code that enforces structural integrity on every change through ontological validation, automated testing, and traceable version control.

## Architecture

```mermaid
flowchart TD
    R([Request]) --> A

    subgraph PLAN ["Stage 1 — Plan"]
        A["`**Archon** · opus
        Execution plan`"]
    end

    subgraph AUDIT ["Stage 2 — Audit"]
        O["`**Ontos** · opus
        Structural audit`"]
    end

    subgraph EXECUTE ["Stage 3 — Execute"]
        P["`**Pragma** · sonnet
        Code generation`"]
        S7["semgrep · context7"]
    end

    subgraph VERIFY ["Stage 4 — Verify"]
        D["`**Dokimos** · sonnet
        Test orchestration`"]
        TT["test runner · coverage"]
        SC["`**Scrutator** · sonnet
        Log trace _(optional)_`"]
    end

    subgraph COMMIT ["Stage 5 — Commit"]
        H["`**Hermon** · sonnet
        Version control`"]
        CC["conventional commits
        semver · changelog"]
    end

    A --> O
    O -->|APPROVED| P
    O -->|BLOCKED| A
    P --> S7
    P --> D
    P -->|structural blocker| O
    D --> TT
    D -.->|log trace needed| SC
    SC -.->|findings| D
    D -->|VERIFIED| H
    D -->|LOGIC_ERROR| P
    D -.->|PLAN_GAP| A
    D -->|DEPENDENCY_ISSUE·breaking| A
    D -->|DEPENDENCY_ISSUE·misuse| P
    H --> CC
    H --> DONE([Done])

    style A fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style O fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style P fill:#E6F1FB,stroke:#185FA5,color:#042C53
    style D fill:#EAF3DE,stroke:#3B6D11,color:#173404
    style SC fill:#FFF8E1,stroke:#F9A825,color:#4A3800
    style H fill:#E1F5EE,stroke:#0F6E56,color:#04342C
    style S7 fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style TT fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style CC fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style R fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style DONE fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
```

## Agents

| Agent | Stage | Model | Purpose |
|-------|-------|-------|---------|
| **Archon** | 1 — Plan | opus | Produces the execution plan. Identifies stack, provisions skills/tools, builds a dependency-aware task list. Never writes code. |
| **Ontos** | 2 — Audit | opus | Validates the plan across four dimensions: vertical coherence (layer integrity), horizontal coherence (peer effects), systemic coherence (ecosystem impact), and omission gap detection. |
| **Pragma** | 3 — Execute | sonnet | Transforms the validated plan into code. Runs abstract dry run, generates code, verifies with Semgrep + Context7, applies fix-first resolution. |
| **Dokimos** | 4 — Verify | sonnet | Provisions test toolchain, generates ontological test suites (vertical/horizontal/systemic), executes them, performs RCA on failures, and routes defects appropriately. |
| **Scrutator** | 4.1 — Log Trace | sonnet | Sub-step of Dokimos. Truncates logs, reads Docker/application output after test execution, parses errors/warnings/anomalies. Fail-open: Dokimos continues without log trace if Scrutator fails. |
| **Hermon** | 5 — Commit | sonnet | Constructs atomic commits following Conventional Commits v1.0.0, GitKraken best practices, and TM Forum traceability. Manages branches, push, and changelog. |

## Agent Interaction Map

Each agent has a defined set of inputs, outputs, and routing targets. The orchestrator (CLAUDE.md) mediates all inter-agent communication — agents never invoke each other directly.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR (CLAUDE.md)                     │
│                   Routes all inter-agent messages                   │
└─────────┬───────────┬───────────┬───────────┬───────────┬──────────┘
          │           │           │           │           │
          ▼           ▼           ▼           ▼           ▼
    ┌──────────┐┌──────────┐┌──────────┐┌──────────┐┌──────────┐
    │  ARCHON  ││  ONTOS   ││  PRAGMA  ││ DOKIMOS  ││  HERMON  │
    │  Plan    ││  Audit   ││ Execute  ││  Verify  ││  Commit  │
    └──────────┘└──────────┘└──────────┘└──────────┘└──────────┘

Routing table:
  Archon  ──plan──►  Ontos
  Ontos   ──APPROVED──►  Pragma
  Ontos   ──BLOCKED──►  Archon  (remediation items)
  Pragma  ──report──►  Dokimos
  Pragma  ──blocker──►  Ontos  (structural issue)
  Dokimos ──VERIFIED──►  Hermon
  Dokimos ──LOGIC_ERROR──►  Pragma  (fix specification)
  Dokimos ──PLAN_GAP──►  Archon  (full restart)
  Dokimos ──DEP_ISSUE·breaking──►  Archon
  Dokimos ──DEP_ISSUE·misuse──►  Pragma
  Dokimos ─ ─log trace─ ─►  Scrutator  (optional sub-step)
  Scrutator ─ ─findings─ ─►  Dokimos
  Hermon  ──done──►  Orchestrator  (pipeline complete)
  Hermon  ──conflict──►  User  (manual resolution)
```

## Agent Workflow Details

### Archon — Planning Workflow

```mermaid
flowchart TD
    R([User Request]) --> CI[Context Ingestion]
    CI --> RE{External source?}
    RE -->|yes| RET2[RE Triage:<br/>Map topology +<br/>Ontological assessment]
    RET2 --> CV{Compatible?}
    CV -->|INCOMPATIBLE| INC[Plan: isolation dir<br/>+ agnostic extraction<br/>+ blueprint.md via SDD]
    CV -->|COMPATIBLE| COM[Plan: cherry-pick<br/>+ coupling validation<br/>+ selective merge]
    INC --> SP
    COM --> SP
    RE -->|no| SP[Skill Provisioning<br/>Tool Awareness Cascade]
    SP --> IR[Investigative Recon]
    IR --> PC[Plan Construction<br/>Dependency Classification<br/>dep · interdep · co-dep]
    PC --> RET[Return to Orchestrator]
    PG([PLAN_GAP from Dokimos]) --> CI

    style R fill:#F1EFE8,stroke:#5F5E5A
    style CI fill:#FAECE7,stroke:#993C1D
    style RE fill:#FFF8E1,stroke:#F9A825
    style RET2 fill:#FAECE7,stroke:#993C1D
    style CV fill:#FFF8E1,stroke:#F9A825
    style INC fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style COM fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
    style SP fill:#FAECE7,stroke:#993C1D
    style IR fill:#FAECE7,stroke:#993C1D
    style PC fill:#FAECE7,stroke:#993C1D
    style RET fill:#FAECE7,stroke:#993C1D
    style PG fill:#FFF8E1,stroke:#F9A825
```

### Ontos — Audit Workflow

```mermaid
flowchart TD
    P([Plan Received]) --> VC[Vertical Coherence]
    VC --> HC[Horizontal Coherence]
    HC --> SC[Systemic Coherence]
    SC --> OGD[Omission Gap Detection]
    OGD --> DRA[Dependency Relationship<br/>Classification Audit<br/>dep · interdep · co-dep]
    DRA --> TAC[Tool Awareness Compliance]
    TAC --> REA{RE tasks?}
    REA -->|yes| REP[RE Plan Audit:<br/>compatibility justified?<br/>isolation/coupling adequate?]
    REP --> GCC[Gap Cascade Check]
    REA -->|no| GCC
    GCC --> V{Verdict}
    V -->|APPROVED| APR([To Pragma])
    V -->|BLOCKED| BLK([Back to Archon])

    style P fill:#F1EFE8,stroke:#5F5E5A
    style VC fill:#FAECE7,stroke:#993C1D
    style HC fill:#FAECE7,stroke:#993C1D
    style SC fill:#FAECE7,stroke:#993C1D
    style OGD fill:#FAECE7,stroke:#993C1D
    style DRA fill:#FAECE7,stroke:#993C1D
    style TAC fill:#FAECE7,stroke:#993C1D
    style REA fill:#FFF8E1,stroke:#F9A825
    style REP fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style GCC fill:#FAECE7,stroke:#993C1D
    style V fill:#FFF8E1,stroke:#F9A825
    style APR fill:#EAF3DE,stroke:#3B6D11
    style BLK fill:#FFE0E0,stroke:#CC3333
```

### Pragma — Execution Workflow

```mermaid
flowchart TD
    A([APPROVED Plan]) --> REC{RE tasks?}
    REC -->|yes| RE05[Phase 0.5: RE Execution]
    RE05 --> REM{re_mode?}
    REM -->|incompatible| ISO[Isolation dir<br/>+ AST analysis<br/>+ agnostic extraction<br/>+ blueprint.md SDD]
    REM -->|compatible| CHP[Cherry-pick extract<br/>+ coupling validation<br/>+ interface adapt<br/>+ selective merge]
    ISO --> DR
    CHP --> CODEP{co-dep?}
    CODEP -->|yes| STOP([STOP → Ontos re-audit])
    CODEP -->|no| DR
    REC -->|no| DR[Phase 1: Abstract Dry Run]
    DR --> CG[Phase 2: Code Generation]
    CG --> SV[Phase 3: Static Verification<br/>Semgrep + Context7<br/>via Tool Awareness Cascade]
    SV --> FF[Phase 4: Fix-First Resolution]
    FF --> ER[Execution Report]
    ER --> DOK([To Dokimos])
    FIX([Fix Spec from Dokimos]) --> DR
    BLK([Structural Blocker]) --> ONT([Back to Ontos])

    style A fill:#F1EFE8,stroke:#5F5E5A
    style REC fill:#FFF8E1,stroke:#F9A825
    style RE05 fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style REM fill:#FFF8E1,stroke:#F9A825
    style ISO fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style CHP fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
    style CODEP fill:#FFE0E0,stroke:#CC3333
    style STOP fill:#FFE0E0,stroke:#CC3333
    style DR fill:#E6F1FB,stroke:#185FA5
    style CG fill:#E6F1FB,stroke:#185FA5
    style SV fill:#E6F1FB,stroke:#185FA5
    style FF fill:#E6F1FB,stroke:#185FA5
    style ER fill:#E6F1FB,stroke:#185FA5
    style DOK fill:#EAF3DE,stroke:#3B6D11
    style FIX fill:#FFF8E1,stroke:#F9A825
    style BLK fill:#FFE0E0,stroke:#CC3333
    style ONT fill:#FAECE7,stroke:#993C1D
```

### Dokimos — Verification Workflow

```mermaid
flowchart TD
    ER([Execution Report]) --> EP[Phase 0: Environment Provisioning<br/>Tool Awareness Cascade]
    EP --> TG[Phase 1: Test Generation]
    TG --> VT[Vertical Tests<br/>+ ontological: dep · interdep · co-dep]
    TG --> HT[Horizontal Tests<br/>+ ontological: peer · mutual · cycle]
    TG --> ST[Systemic Tests<br/>+ ontological: infra · ordering · deploy]
    VT --> TE[Phase 2: Test Execution]
    HT --> TE
    ST --> TE
    TE --> LAP[Phase 3: Local Approximation]
    LAP --> PASS{All Pass?}
    PASS -->|Yes| VER([VERIFIED → Hermon])
    PASS -->|No| RCA[Phase 4: RCA]
    RCA -.->|log trace| SCR[Scrutator<br/>Mode 1 or 2]
    SCR -.-> RCA
    RCA --> CLS{Classify}
    CLS -->|LOGIC_ERROR| PRA([Fix Spec → Pragma])
    CLS -->|PLAN_GAP| ARC([Evidence → Archon])
    CLS -->|DEP_ISSUE| DEP{Severity}
    DEP -->|breaking| ARC
    DEP -->|misuse| PRA

    style ER fill:#F1EFE8,stroke:#5F5E5A
    style EP fill:#EAF3DE,stroke:#3B6D11
    style TG fill:#EAF3DE,stroke:#3B6D11
    style VT fill:#EAF3DE,stroke:#3B6D11
    style HT fill:#EAF3DE,stroke:#3B6D11
    style ST fill:#EAF3DE,stroke:#3B6D11
    style TE fill:#EAF3DE,stroke:#3B6D11
    style LAP fill:#EAF3DE,stroke:#3B6D11
    style RCA fill:#EAF3DE,stroke:#3B6D11
    style SCR fill:#FFF8E1,stroke:#F9A825
    style VER fill:#E1F5EE,stroke:#0F6E56
    style PRA fill:#E6F1FB,stroke:#185FA5
    style ARC fill:#FAECE7,stroke:#993C1D
```

### Hermon — Commit Workflow

```mermaid
flowchart TD
    VER([VERIFIED Report]) --> DA[Phase 1: Diff Analysis]
    DA --> BV[Phase 2: Branch Verification]
    BV --> CC[Phase 3: Conflict Check]
    CC --> CONF{Conflicts?}
    CONF -->|Yes| USR([Report to User])
    CONF -->|No| CS[Commit Construction<br/>Conventional Commits]
    CS --> PP[Phase 4: Push Protocol]
    PP -.->|optional| SCR[Post-Commit Gate<br/>Scrutator Mode 3]
    SCR -.-> PP
    PP --> CL[Phase 5: Changelog<br/>if release-worthy]
    CL --> DONE([Pipeline Complete])

    style VER fill:#F1EFE8,stroke:#5F5E5A
    style DA fill:#E1F5EE,stroke:#0F6E56
    style BV fill:#E1F5EE,stroke:#0F6E56
    style CC fill:#E1F5EE,stroke:#0F6E56
    style CS fill:#E1F5EE,stroke:#0F6E56
    style PP fill:#E1F5EE,stroke:#0F6E56
    style CL fill:#E1F5EE,stroke:#0F6E56
    style SCR fill:#FFF8E1,stroke:#F9A825
    style USR fill:#FFE0E0,stroke:#CC3333
    style DONE fill:#F1EFE8,stroke:#5F5E5A
```

### Reverse Engineering — Decision Flow

```mermaid
flowchart TD
    USR([User provides external source]) --> ORC[Orchestrator loads context]
    ORC --> ARC[Archon: RE Triage]
    ARC --> MAP[Map external topology<br/>modules · deps · stack]
    MAP --> ONT[Ontological compatibility<br/>assessment per module]
    ONT --> CLS{Classification}
    CLS -->|dep A→B| OK[Valid coupling]
    CLS -->|interdep A↔B| OK2[Valid with contract]
    CLS -->|co-dep| FAIL[Automatic INCOMPATIBLE]
    OK --> AGG{Aggregate}
    OK2 --> AGG
    FAIL --> AGG
    AGG -->|any co-dep or axiom violation| INC

    subgraph INC ["INCOMPATIBLE Path"]
        I1[Create isolation dir<br/>_re/source-name/]
        I2[AST + flow analysis]
        I3[Agnostic logic extraction]
        I4[blueprint.md generation<br/>SDD: Specify→Plan→Tasks→Validate]
        I1 --> I2 --> I3 --> I4
    end

    AGG -->|all valid| CMP

    subgraph CMP ["COMPATIBLE Path"]
        C1[Cherry-pick extraction<br/>skill-swarm cherry_pick_context]
        C2[Ontological coupling validation<br/>efferent · afferent index]
        C3{co-dep in extraction?}
        C4[Interface adaptation<br/>conventions · namespaces · APIs]
        C5[Selective merge into project]
        C1 --> C2 --> C3
        C3 -->|no| C4 --> C5
        C3 -->|yes| STOP([STOP → Ontos re-audit])
    end

    INC --> ONTOS[Ontos: audit RE plan<br/>horizontal coherence]
    CMP --> ONTOS
    ONTOS --> PRA[Pragma: Phase 0.5 execution]
    PRA --> DOK[Dokimos: ontological dep tests]
    DOK --> HER([Hermon: commit])

    style USR fill:#F1EFE8,stroke:#5F5E5A
    style ORC fill:#F1EFE8,stroke:#5F5E5A
    style ARC fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style MAP fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style ONT fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style OK fill:#EAF3DE,stroke:#3B6D11
    style OK2 fill:#EAF3DE,stroke:#3B6D11
    style FAIL fill:#FFE0E0,stroke:#CC3333
    style I1 fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style I2 fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style I3 fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style I4 fill:#F3E5F5,stroke:#7B1FA2,color:#4A0072
    style C1 fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
    style C2 fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
    style C3 fill:#FFF8E1,stroke:#F9A825
    style C4 fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
    style C5 fill:#E8F5E9,stroke:#2E7D32,color:#1B5E20
    style STOP fill:#FFE0E0,stroke:#CC3333
    style ONTOS fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style PRA fill:#E6F1FB,stroke:#185FA5,color:#042C53
    style DOK fill:#EAF3DE,stroke:#3B6D11,color:#173404
    style HER fill:#E1F5EE,stroke:#0F6E56,color:#04342C
```

## Ontological Foundation

The pipeline operates under the **Topos Integrity Protocol**: every change is a node in a dependency graph, and a change is valid only if the graph remains coherent after it.

Three tracing dimensions apply at every stage:

- **Vertical trace** — data flow integrity across layers: storage → data access → business logic → API → consumer.
- **Horizontal trace** — peer modules that share imports, exports, state, or events with the changed module.
- **Systemic trace** — CI/CD pipelines, env vars, secrets, config maps, container images, Helm values, K8s manifests.

A critical invariant: **gap cascade prevention**. Fixing gap X1 must not create gap X2. If resolving X2 would reintroduce X1, the fix is structurally invalid and escalates to Archon for replanning.

## Feedback Loops

The pipeline has three feedback loops, each with a max iteration limit of **3 cycles** before escalating to the user:

### Archon ↔ Ontos (plan revision)
When Ontos returns `BLOCKED`, remediation items go back to Archon. Archon revises the plan and resubmits for audit. This loop catches planning omissions before any code is written.

### Pragma ↔ Dokimos (code fix)
When Dokimos returns `DEFECTIVE (LOGIC_ERROR)`, a Fix Specification goes to Pragma. Pragma applies the fix and resubmits for verification. This loop catches implementation bugs without replanning.

### Dokimos → Archon (plan gap escalation)
When Dokimos returns `DEFECTIVE (PLAN_GAP)`, the entire pipeline restarts from Archon. This catches requirements that only surface at test time — the plan itself was incomplete.

## Scrutator: Log Trace Sub-Step

Scrutator has three operational modes (RCA Trace, Plan-Requested Trace, Post-Commit Gate) defined canonically in CLAUDE.md. See the canonical definition there for trigger conditions, decision authority, and fail semantics per mode.

Summary:
- **Mode 1 (RCA Trace):** Dokimos-initiated, fail-open. Default mode for test failure analysis.
- **Mode 2 (Plan-Requested):** Archon-specified, fail-closed for documentation. Targets specific log patterns.
- **Mode 3 (Post-Commit Gate):** Orchestrator-initiated, fail-open. OFF by default. Checks logs after Hermon commits.

## Model Selection Rationale

**Opus** for Archon and Ontos — these are the stages where the cost of error is highest and the reasoning is open-ended. Planning from ambiguous requirements and detecting omissions in a dependency graph require deep multi-dimensional analysis. False negatives at these stages cascade through the entire pipeline.

**Sonnet** for Pragma, Dokimos, Hermon, and Scrutator — these stages operate within well-defined constraints (a validated plan, a known stack, deterministic protocols). The plan provides sufficient scaffolding that Opus-level reasoning adds cost without proportional benefit. Sonnet is faster, cheaper, and equally effective for pattern-driven execution.

## Dokimos: Test Philosophy

Dokimos provisions its own test environment by detecting the project stack and mapping it to the appropriate toolchain. It integrates with Context7 for API validation and Semgrep for static analysis as a second verification layer (Pragma runs them first during code generation).

### Local Approximation Protocol

Not everything can be tested locally. Dokimos classifies conditions into three tiers:

- **Replicable** — pure logic, DB via test containers, HTTP via mocks.
- **Approximation required** — cloud APIs, payment processing, OAuth → mocked with fixtures. Documented with confidence level.
- **Non-replicable** — production data distribution, multi-region latency, real cert chains → flagged with a `PROJECTION` block documenting the production risk.

### Ontological Test Model

Tests follow the same three dimensions as the audit:

- **Vertical tests** — unit (isolated function), integration (cross-layer), contract (API schemas).
- **Horizontal tests** — import/export validation, shared state, event chains.
- **Systemic tests** — env var existence, config coherence, dependency conflicts.

## Hermon: Commit Standards

Hermon enforces three standards simultaneously:

- **Conventional Commits v1.0.0** — structured commit messages with type, scope, description, body, and footers.
- **GitKraken best practices** — branch naming, commit hygiene, merge strategy.
- **TM Forum traceability** — every commit footer includes `Plan-ID`, `Audit-ID`, and `Verified-By` references linking back through the pipeline.

Commits are ordered by dependency layer: infrastructure first, then migrations, then shared modules, then business logic, then tests. At any commit in the sequence, the repository is in a valid state.

## Agent Capability Matrix

| Agent | Model | permissionMode | disallowedTools | maxTurns |
|-------|-------|----------------|-----------------|----------|
| Archon | opus | plan | NotebookEdit | 30 |
| Ontos | opus | plan | NotebookEdit | 25 |
| Pragma | sonnet | acceptEdits | (none) | 50 |
| Dokimos | sonnet | acceptEdits | NotebookEdit | 50 |
| Hermon | sonnet | default | NotebookEdit | 20 |
| Scrutator | sonnet | default | NotebookEdit, Write, Edit | 15 |

## File Structure

```
├── CLAUDE.md      # Orchestrator — invokes and routes between all agents
├── Archon.md      # Stage 1 — strategic planner
├── Ontos.md       # Stage 2 — structural auditor
├── Pragma.md      # Stage 3 — execution engine
├── Dokimos.md     # Stage 4 — verification engine
└── Hermon.md      # Stage 5 — version control engine
```

> **Convention:** Agent prompt files (*.md in this directory except
> README.md) use ASCII art for pipeline diagrams to minimize token
> consumption when loaded as agent context. README.md uses Mermaid
> diagrams for GitHub rendering. CLAUDE.md uses ASCII art
> (it is loaded as orchestrator context).

> **Naming:** Agent files use PascalCase (Archon.md, Ontos.md)
> matching the `name` field in YAML frontmatter. This differs from
> the Gemini variant (lowercase) per CLI conventions. Claude variant
> uses PascalCase as rendered agent identity in the CLI.

## Usage

The orchestrator (CLAUDE.md) handles all routing automatically. To use the pipeline:

1. Describe your task to the Claude Code CLI.
2. The orchestrator invokes Archon to plan.
3. Ontos audits the plan (loops with Archon if blocked).
4. Pragma generates code (with Semgrep + Context7 verification).
5. Dokimos tests the code (with optional Scrutator log tracing). Loops with Pragma on logic errors, escalates to Archon on plan gaps.
6. Hermon commits and pushes on verification success.

For questions, reviews, or discussions that don't modify files, the orchestrator responds directly — no pipeline invocation needed.

## Error Recovery

| Scenario | Action |
|----------|--------|
| Archon cannot resolve ambiguity | Surface to user |
| Ontos BLOCKED after 3 revisions | Escalate to user with findings |
| Pragma hits structural blocker | Return to Ontos |
| Dokimos DEFECTIVE after 3 fix cycles | Escalate to user with RCA |
| Dokimos discovers plan gap | Full restart from Archon |
| Hermon detects merge conflicts | Report to user |
| Scrutator fails or times out | Dokimos continues without log trace (fail-open) |

## License

Internal tooling — adapt to your project's license.
