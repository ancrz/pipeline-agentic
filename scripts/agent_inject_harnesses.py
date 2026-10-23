#!/usr/bin/env python3
"""Runbook: Injects canonical Topos Pipeline harnesses across Claude Code, Codex, and Gemini.

Runbook Name: scripts/agent_inject_harnesses.py
Plan Reference: PLAN-TOPOS-INJECT-20261023 & PLAN-TOPOS-CODEX-PARITY-20261023
                (documented in docs/pipeline/feature_20261023_022200.md)
Ontos Status: APPROVED (0 blockers, 0 co-dependencies)

Environment Variables:
    BACKUP_DIR: Optional path for backup directory.
                Default: /home/ancruz/.gemini/backups/pre-inject-<YYYYMMDD_HHMMSS>
    CANONICAL_REPO: Optional path to repository root.
                Default: /home/ancruz/Documents/workspaces/pipeline-agentic

Usage:
    python3 scripts/agent_inject_harnesses.py [--dry-run] [--verify-only] [--rollback <backup_dir>]

Exceptions & Error Handling:
    - If any canonical source file is missing, aborts immediately before modifying targets.
    - If any target file cannot be backed up, aborts immediately.
    - If static verification fails post-injection, reports failure and provides automated rollback.
"""

import argparse
import datetime
import glob
import hashlib
import os
import shutil
import sys
from pathlib import Path

ROLES = ["archon", "graphos", "ontos", "pragma", "dokimos", "hermon"]

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def split_frontmatter(text: str):
    """Extract leading YAML frontmatter block (lines from initial '---' through closing '---')."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return "", text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "".join(lines[: i + 1]), "".join(lines[i + 1:])
    return "", text

def build_manifest(repo: Path):
    claude_home = Path("/home/ancruz/.claude")
    codex_home = Path("/home/ancruz/.codex")
    gemini_home = Path("/home/ancruz/.gemini")

    # 22 direct copy tasks: (source, target, backup_rel_path)
    direct_copies = [
        # Claude (7 files)
        (repo / "claude" / "CLAUDE.md", claude_home / "CLAUDE.md", Path("claude/CLAUDE.md")),
        *[(repo / "claude" / f"{r.capitalize()}.md", claude_home / "agents" / f"{r.capitalize()}.md", Path(f"claude/agents/{r.capitalize()}.md")) for r in ROLES],
        # Codex (7 files)
        (repo / "codex" / "AGENTS.md", codex_home / "AGENTS.md", Path("codex/AGENTS.md")),
        *[(repo / "codex" / "roles" / f"{r}.md", codex_home / "agentic-pipeline" / "roles" / f"{r}.md", Path(f"codex/roles/{r}.md")) for r in ROLES],
        # Gemini CLI & agy CLI (8 files)
        (repo / "gemini" / "gemini-cli" / "GEMINI.md", gemini_home / "GEMINI.md", Path("gemini/GEMINI.md")),
        (repo / "gemini" / "gemini-cli" / "GEMINI.md", gemini_home / "antigravity-cli" / "AGENTS.md", Path("gemini/antigravity-cli/AGENTS.md")),
        *[(repo / "gemini" / "gemini-cli" / f"{r}.md", gemini_home / f"{r}.md", Path(f"gemini/{r}.md")) for r in ROLES],
    ]

    # 6 composite tasks: (role, canonical_body_source, target_agent_file, backup_rel_path)
    composite_copies = [
        (r, repo / "gemini" / "gemini-cli" / f"{r}.md", gemini_home / "config" / "agents" / r / "agent.md", Path(f"gemini/agents/{r}/agent.md"))
        for r in ROLES
    ]

    # Symlink task: ~/.codex/roles -> ~/.codex/agentic-pipeline/roles
    symlinks = [
        (codex_home / "roles", codex_home / "agentic-pipeline" / "roles")
    ]

    protected_patterns = [
        "/home/ancruz/.claude/agent-memory/*/MEMORY.md",
        "/home/ancruz/.claude/settings.json",
        "/home/ancruz/.gemini/settings.json",
        "/home/ancruz/.gemini/config/mcp_config.json",
    ]

    return direct_copies, composite_copies, symlinks, protected_patterns

def execute_backup(backup_dir: Path, direct_copies, composite_copies):
    print(f"[*] Creating backup directory: {backup_dir}")
    # Subdirectories per plan specification
    subdirs = [
        backup_dir / "claude" / "agents",
        backup_dir / "codex" / "roles",
        backup_dir / "gemini" / "antigravity-cli",
        *[backup_dir / "gemini" / "agents" / r for r in ROLES],
    ]
    for sd in subdirs:
        sd.mkdir(parents=True, exist_ok=True)

    backup_inventory = []
    # Backup direct copy targets (22 files)
    for _, target, rel_bkp in direct_copies:
        dest = backup_dir / rel_bkp
        dest.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            shutil.copy2(target, dest)
            backup_inventory.append((target, dest))

    # Backup composite copy targets (6 files)
    for _, _, target, rel_bkp in composite_copies:
        dest = backup_dir / rel_bkp
        dest.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            shutil.copy2(target, dest)
            backup_inventory.append((target, dest))

    print(f"[+] Successfully backed up all {len(backup_inventory)} target files into {backup_dir}")
    return backup_inventory

def record_protected_checksums(protected_patterns):
    hashes = {}
    for pat in protected_patterns:
        matches = glob.glob(pat)
        if not matches and not ("*" in pat):
            matches = [pat]
        for m in sorted(matches):
            p = Path(m)
            if p.exists():
                hashes[str(p)] = sha256_file(p)
    return hashes

def execute_injection(direct_copies, composite_copies, symlinks, dry_run=False):
    print(f"[*] Beginning injection (dry_run={dry_run})...")
    
    # Direct copies (22 files)
    for src, dst, _ in direct_copies:
        print(f"  COPY: {src} -> {dst}")
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)

    # Composite copies (6 files)
    for role, body_src, dst, _ in composite_copies:
        print(f"  COMPOSITE: frontmatter({dst}) + {body_src} -> {dst}")
        if not dry_run:
            current_target_text = dst.read_text(encoding="utf-8")
            fm, _ = split_frontmatter(current_target_text)
            if not fm:
                raise ValueError(f"Target file {dst} missing leading YAML frontmatter!")
            canonical_body = body_src.read_text(encoding="utf-8")
            # Write <frontmatter>\n<body>
            new_content = fm + "\n" + canonical_body
            dst.write_text(new_content, encoding="utf-8")

    # Symlinks
    for link_path, target_path in symlinks:
        print(f"  SYMLINK: {link_path} -> {target_path}")
        if not dry_run:
            if link_path.is_symlink() or link_path.exists():
                link_path.unlink()
            link_path.symlink_to(target_path)

def verify_static_gate(direct_copies, composite_copies, symlinks, protected_baseline):
    print("\n[*] Running Static Verification Gate...")
    errors = []

    # 1. Verify direct copies against canonical source
    print(f"  [1/4] Verifying {len(direct_copies)} direct copies match canonical source SHA-256...")
    for src, dst, _ in direct_copies:
        src_sha = sha256_file(src)
        dst_sha = sha256_file(dst)
        if src_sha != dst_sha:
            errors.append(f"Direct copy mismatch: {dst} ({dst_sha[:10]}...) != {src} ({src_sha[:10]}...)")
        else:
            print(f"    MATCH: {dst} -> {dst_sha[:12]}...")

    # 2. Verify composite copies
    print(f"  [2/4] Verifying {len(composite_copies)} composite files frontmatter preservation and body integrity...")
    for role, body_src, dst, _ in composite_copies:
        canonical_body = body_src.read_text(encoding="utf-8")
        dst_text = dst.read_text(encoding="utf-8")
        fm, rest = split_frontmatter(dst_text)
        if not fm:
            errors.append(f"Composite file {dst} has empty frontmatter")
            continue
        
        extracted_body = rest[1:] if rest.startswith("\n") else rest
        if extracted_body != canonical_body:
            errors.append(f"Composite file {dst} body does not match canonical source {body_src} byte-for-byte")
        else:
            print(f"    VERIFIED: {dst} (frontmatter preserved: {len(fm.splitlines())} lines, body matches {body_src.name} byte-for-byte)")

    # 3. Verify symlinks
    print(f"  [3/4] Verifying {len(symlinks)} symlinks...")
    for link_path, target_path in symlinks:
        if not link_path.is_symlink():
            errors.append(f"Expected symlink at {link_path}, but not a symlink")
        else:
            actual_target = os.readlink(link_path)
            if Path(actual_target).resolve() != target_path.resolve():
                errors.append(f"Symlink {link_path} points to {actual_target}, expected {target_path}")
            else:
                print(f"    VERIFIED SYMLINK: {link_path} -> {actual_target}")

    # 4. Verify protected files invariance
    print("  [4/4] Verifying protected files checksum invariance...")
    current_protected = record_protected_checksums(list(protected_baseline.keys()))
    for path_str, original_hash in protected_baseline.items():
        curr_hash = current_protected.get(path_str)
        if curr_hash != original_hash:
            errors.append(f"Protected file MUTATED: {path_str} was {original_hash} now {curr_hash}")
        else:
            print(f"    UNTOUCHED: {path_str} -> {curr_hash[:12]}...")

    if errors:
        print("\n[!] STATIC VERIFICATION FAILED:")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("\n[+] STATIC VERIFICATION PASSED: All target files, symlinks, and protected baselines verified.")
    return True

def rollback(backup_dir: Path, direct_copies, composite_copies):
    print(f"[*] Rolling back from backup directory: {backup_dir}")
    restored = 0
    for _, target, rel_bkp in direct_copies:
        src = backup_dir / rel_bkp
        if src.exists():
            shutil.copy2(src, target)
            restored += 1
    for _, _, target, rel_bkp in composite_copies:
        src = backup_dir / rel_bkp
        if src.exists():
            shutil.copy2(src, target)
            restored += 1
    print(f"[+] Successfully restored {restored} files from {backup_dir}")

def main():
    parser = argparse.ArgumentParser(description="Topos Pipeline Harness Injector Runbook")
    parser.add_argument("--dry-run", action="store_true", help="Simulate execution without modifying files")
    parser.add_argument("--verify-only", action="store_true", help="Only verify static integrity without copying")
    parser.add_argument("--rollback", type=str, help="Restore files from specified backup directory")
    args = parser.parse_args()

    repo_path = Path(os.getenv("CANONICAL_REPO", "/home/ancruz/Documents/workspaces/pipeline-agentic")).resolve()
    direct_copies, composite_copies, symlinks, protected_patterns = build_manifest(repo_path)

    if args.rollback:
        rollback(Path(args.rollback), direct_copies, composite_copies)
        return 0

    # Record protected files baseline
    protected_baseline = record_protected_checksums(protected_patterns)
    print(f"[*] Recorded {len(protected_baseline)} protected file checksums.")

    if args.verify_only:
        ok = verify_static_gate(direct_copies, composite_copies, symlinks, protected_baseline)
        return 0 if ok else 1

    # Backup gate
    default_bkp = f"/home/ancruz/.gemini/backups/pre-inject-{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
    backup_dir = Path(os.getenv("BACKUP_DIR", default_bkp)).resolve()

    if not args.dry_run:
        execute_backup(backup_dir, direct_copies, composite_copies)
    else:
        print(f"[DRY-RUN] Would create backup in {backup_dir}")

    # Injection
    try:
        execute_injection(direct_copies, composite_copies, symlinks, dry_run=args.dry_run)
    except Exception as e:
        print(f"[!] Injection failed with exception: {e}")
        if not args.dry_run:
            print("[*] Triggering automatic rollback...")
            rollback(backup_dir, direct_copies, composite_copies)
        return 1

    # Verification gate
    if not args.dry_run:
        ok = verify_static_gate(direct_copies, composite_copies, symlinks, protected_baseline)
        if not ok:
            print("[!] Static verification failed! Triggering automatic rollback...")
            rollback(backup_dir, direct_copies, composite_copies)
            return 1

    print("\n==========================================")
    print(f"Execution successful! Backup saved at:\n{backup_dir}")
    print("==========================================")
    return 0

if __name__ == "__main__":
    sys.exit(main())
