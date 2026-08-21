# Topos Integrity Pipeline — Codex Edition

Codex uses one global instruction file, `~/.codex/AGENTS.md`. The installer
copies `codex/AGENTS.md` there and mirrors the five canonical Gemini role
prompts to `~/.codex/agentic-pipeline/roles/`.

Codex does not need project-local `AGENTS.md` files for this pipeline. Its
global adapter directs the active agent to load the appropriate role prompt
before each pipeline stage:

```text
Archon → Ontos → Pragma → Dokimos → Hermon
```

The role bodies are shared with the Gemini implementation because both use
sequential role switching. Claude Code remains the multi-agent implementation
and uses the Markdown definitions in `claude/`.

## Deployment

Run the deployer's global pipeline step after `agy`, Claude Code, and Codex are
installed:

```bash
bash /root/deployer/scripts/ubuntu/setup-pipeline.sh
```

The deployer validates that this repository contains all canonical sources
before changing any runtime configuration. It does not create a local
`AGENTS.md` in a project.
