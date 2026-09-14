<div align="center">
# Codex Harness: Topos Protocol
**Enforcing Orchestration in Codex**
</div>

## 📌 Implementation
Codex utilizes rule engines and global text policies. We inject the Topos constraints directly into its global space.

```mermaid
flowchart LR
    C[Codex] -->|Reads| A[AGENTS.md]
    A -->|Applies Guardrails| E[Execution]
    
    style C fill:#F59E0B,stroke:#D97706,color:#fff
    style A fill:#3B82F6,stroke:#2563EB,color:#fff
```

## 🚀 Setup
Deploy to the Codex root:
```bash
cp codex/AGENTS.md ~/.codex/AGENTS.md
```