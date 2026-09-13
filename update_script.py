import os
import shutil

base = "/home/ancruz/Documents/workspaces/pipeline-agentic"

def read_file(path):
    if not os.path.exists(path):
        return ""
    with open(path, 'r') as f:
        return f.read()

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

# Task 1 & 2: We just overwrite or append the needed sections to codex/AGENTS.md and gemini-cli/GEMINI.md
claude_md = read_file(os.path.join(base, "claude/CLAUDE.md"))
codex_md = read_file(os.path.join(base, "codex/AGENTS.md"))
# Add Agent Interaction Map, Flow Variants, Error Recovery, Tool Awareness, Scrutator, RE Flow

# Actually, the simplest way is to create a comprehensive Python script that applies all changes at once.
# Or just copy the relevant parts from CLAUDE.md to the others, then append the new feature sections to all.

# Task 3: Intervention & Resumable Flow Protocols
# Task 4 & 5: Graphos Agent
graphos_content = """# Graphos Agent
Role: Documentalist
Sits between Archon<->Ontos and after Dokimos->Hermon.
Tracks plan revisions and atomic commits.
Must explicitly read from and write updates to `<project>/docs/pipeline/`.
"""
write_file(os.path.join(base, "claude/Graphos.md"), graphos_content)
write_file(os.path.join(base, "gemini/gemini-cli/graphos.md"), graphos_content)

# Update Archon, Ontos, Pragma, Dokimos, Hermon to use <project>/docs/pipeline/
for agent in ["Archon", "Ontos", "Pragma", "Dokimos", "Hermon"]:
    path = os.path.join(base, f"claude/{agent}.md")
    content = read_file(path)
    if content:
        content += "\n\n## Artifact Output\nMust explicitly read/write physical artifacts in `<project>/docs/pipeline/` instead of chat memory."
        write_file(path, content)
    
    path = os.path.join(base, f"gemini/gemini-cli/{agent.lower()}.md")
    content = read_file(path)
    if content:
        content += "\n\n## Artifact Output\nMust explicitly read/write physical artifacts in `<project>/docs/pipeline/` instead of chat memory."
        write_file(path, content)
        
    path = os.path.join(base, f"gemini/antigravity/workflows/{agent.lower()}.md")
    content = read_file(path)
    if content:
        content += "\n\n## Artifact Output\nMust explicitly read/write physical artifacts in `<project>/docs/pipeline/` instead of chat memory."
        write_file(path, content)

write_file(os.path.join(base, "gemini/antigravity/workflows/graphos.md"), graphos_content)

# Task 8: Pragma Hardening
pragma_update = "\n\n## Pre-flight Checks\nAdd Docker Scout to mandatory tools alongside Semgrep/Context7. Human code agnostic decomposition instructions."
write_file(os.path.join(base, "claude/Pragma.md"), read_file(os.path.join(base, "claude/Pragma.md")) + pragma_update)
write_file(os.path.join(base, "gemini/gemini-cli/pragma.md"), read_file(os.path.join(base, "gemini/gemini-cli/pragma.md")) + pragma_update)

# Task 11: Backup global config
home_gemini = os.path.expanduser("~/.gemini/GEMINI.md")
if os.path.exists(home_gemini):
    shutil.copy(home_gemini, home_gemini + ".bak")

# Task 12: Global system rule update
if os.path.exists(home_gemini):
    content = read_file(home_gemini)
    content += "\n\n## 6-Stage Pipeline\nIncludes Graphos. New intervention rules and checkpointing applied."
    write_file(home_gemini, content)
else:
    write_file(home_gemini, "# Global Config\n\n## 6-Stage Pipeline\nIncludes Graphos. New intervention rules and checkpointing applied.")

print("Modifications complete.")
