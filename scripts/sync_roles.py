#!/usr/bin/env python3
"""Propagate role bodies from claude/<Role>.md (canonical source) to every platform copy.

Usage (from the repository root):
    python3 scripts/sync_roles.py [--check] [role ...]

    --check   Write nothing; list files that differ and exit 1 if any do.
    role      archon graphos ontos pragma dokimos hermon (default: all)

Body extraction (claude/<Role>.md):
    frontmatter  = leading '---' ... '---' block (only when line 1 is '---')
    body         = text after the frontmatter, up to the claude-only memory marker
    memory tail  = from '<!-- claude-only:' to EOF (never propagated)

Targets:
    codex/roles/<role>.md                   body only
    gemini/gemini-cli/<role>.md             body only
    gemini/antigravity/workflows/<role>.md  own frontmatter + body + own '***' trigger block
    .agents/<role>/agent.json               "system_prompt" replaced; other keys and format kept

Rollback: the source (claude/) is never written. To undo a propagation run:
    git checkout HEAD -- codex/roles gemini .agents
"""
import json
import sys
from pathlib import Path

ROLES = ["archon", "graphos", "ontos", "pragma", "dokimos", "hermon"]
REPO = Path(__file__).resolve().parent.parent
MEMORY_MARKER = "<!-- claude-only:"
TRIGGER_MARKER = "***\n### Interactive Workflow Trigger"


def split_frontmatter(text):
    """Return (frontmatter, rest). Frontmatter only exists when line 1 is '---'."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[: i + 1]), "".join(lines[i + 1:])
    return "", text


def claude_body(role):
    text = (REPO / "claude" / f"{role.capitalize()}.md").read_text(encoding="utf-8")
    _, rest = split_frontmatter(text)
    body = rest.split(MEMORY_MARKER, 1)[0]
    return body.strip("\n") + "\n"


def render_antigravity(path, body):
    existing = path.read_text(encoding="utf-8")
    fm, rest = split_frontmatter(existing)
    idx = rest.find(TRIGGER_MARKER)
    trigger = rest[idx:] if idx != -1 else ""
    out = (fm + "\n" if fm else "") + body
    if trigger:
        out += "\n" + trigger
    return out


def render_agent_json(path, body):
    raw = path.read_text(encoding="utf-8")
    data = json.loads(raw)
    data["system_prompt"] = body
    out = json.dumps(data, indent=2, ensure_ascii=True)
    return out + ("\n" if raw.endswith("\n") else "")


def apply(path, content, check):
    current = path.read_text(encoding="utf-8") if path.exists() else None
    if current == content:
        return False
    print(("DIFFERS  " if check else "UPDATED  ") + str(path.relative_to(REPO)))
    if not check:
        path.write_text(content, encoding="utf-8")
    return True


def sync(role, check):
    body = claude_body(role)
    changed = False
    changed |= apply(REPO / "codex" / "roles" / f"{role}.md", body, check)
    changed |= apply(REPO / "gemini" / "gemini-cli" / f"{role}.md", body, check)
    ag = REPO / "gemini" / "antigravity" / "workflows" / f"{role}.md"
    changed |= apply(ag, render_antigravity(ag, body), check)
    js = REPO / ".agents" / role / "agent.json"
    changed |= apply(js, render_agent_json(js, body), check)
    return changed


def main(argv):
    check = "--check" in argv
    roles = [a for a in argv if a != "--check"] or ROLES
    unknown = sorted(set(roles) - set(ROLES))
    if unknown:
        sys.exit(f"unknown role(s): {', '.join(unknown)}")
    changed = False
    for role in roles:
        changed |= sync(role, check)
    if check:
        print("CHECK FAILED: copies differ from claude/ source" if changed else "CHECK PASSED")
        return 1 if changed else 0
    print("Done." if changed else "Nothing to update.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
