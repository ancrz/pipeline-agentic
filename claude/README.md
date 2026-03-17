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
    D -->|VERIFIED| H
    D -->|LOGIC_ERROR| P
    D -->|PLAN_GAP| A
    H --> CC
    H --> DONE([Done])

    style A fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style O fill:#FAECE7,stroke:#993C1D,color:#4A1B0C
    style P fill:#E6F1FB,stroke:#185FA5,color:#042C53
    style D fill:#EAF3DE,stroke:#3B6D11,color:#173404
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
| **Hermon** | 5 — Commit | sonnet | Constructs atomic commits following Conventional Commits v1.0.0, GitKraken best practices, and TM Forum traceability. Manages branches, push, and changelog. |

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

## Model Selection Rationale

**Opus** for Archon and Ontos — these are the stages where the cost of error is highest and the reasoning is open-ended. Planning from ambiguous requirements and detecting omissions in a dependency graph require deep multi-dimensional analysis. False negatives at these stages cascade through the entire pipeline.

**Sonnet** for Pragma, Dokimos, and Hermon — these stages operate within well-defined constraints (a validated plan, a known stack, deterministic protocols). The plan provides sufficient scaffolding that Opus-level reasoning adds cost without proportional benefit. Sonnet is faster, cheaper, and equally effective for pattern-driven execution.

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

## File Structure

```
├── CLAUDE.md      # Orchestrator — invokes and routes between all agents
├── Archon.md      # Stage 1 — strategic planner
├── Ontos.md       # Stage 2 — structural auditor
├── Pragma.md      # Stage 3 — execution engine
├── Dokimos.md     # Stage 4 — verification engine
└── Hermon.md      # Stage 5 — version control engine
```

## Usage

The orchestrator (CLAUDE.md) handles all routing automatically. To use the pipeline:

1. Describe your task to the Claude Code CLI.
2. The orchestrator invokes Archon to plan.
3. Ontos audits the plan (loops with Archon if blocked).
4. Pragma generates code (with Semgrep + Context7 verification).
5. Dokimos tests the code (loops with Pragma on logic errors, escalates to Archon on plan gaps).
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

## License

Internal tooling — adapt to your project's license.
