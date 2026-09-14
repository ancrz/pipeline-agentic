<div align="center">
# Antigravity (Gemini) Harness: Topos Protocol
**True Async Multi-Agent Execution**
</div>

## 📌 Implementation
This harness bridges the gap between legacy CLI Sequential Role-Switching and True Async Orchestration via `.agents/agent.json`.

```mermaid
flowchart TD
    subgraph Antigravity Engine
        CLI[agy CLI]
        GUI[Antigravity 2.0 IDE]
    end
    
    CLI & GUI -->|Priority 1| Local[.agents/agent.json]
    CLI & GUI -->|Fallback| Global[~/.gemini/config/]
    
    style CLI fill:#10B981,stroke:#059669,color:#fff
    style GUI fill:#10B981,stroke:#059669,color:#fff
    style Local fill:#3B82F6,stroke:#2563EB,color:#fff
```

## 🚀 Setup
The `.agents` folder works natively. To deploy the global fallback:
```bash
cp gemini/gemini-cli/GEMINI.md ~/.gemini/GEMINI.md
```