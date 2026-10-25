#!/usr/bin/env bash
# sync.sh — smart sync of the Topos pipeline into Claude Code, Codex and Gemini/Antigravity.
#
# Modes
#   auto    (default) local if --target is given or you run it from inside another git
#           project; global when run from this repository (or outside any project).
#   global  install into the user-level harness homes (~/.claude, ~/.codex, ~/.gemini) via
#           scripts/agent_inject_harnesses.py (backup + static verification + auto-rollback).
#   local   install into one project as project-level overrides:
#             .claude/CLAUDE.md, .claude/agents/<Role>.md         (Claude Code)
#             .codex/AGENTS.md, .codex/roles/<role>.md            (Codex)
#             .gemini/GEMINI.md, .gemini/<role>.md                (Gemini CLI)
#             .agents/<role>/agent.json                           (Antigravity workspace)
#           Root-level CLAUDE.md / AGENTS.md / GEMINI.md of the project are never touched.
#
# What makes it "smart"
#   - Propagates role bodies from claude/ (canonical) to every copy first (scripts/sync_roles.py)
#     and refuses to deploy invalid agent.json files.
#   - Detects which harnesses are installed and only syncs those (override with --harness).
#   - Writes only files that changed; reports NEW / UPDATE / SAME / SKIP per file.
#   - Local mode tracks the files it installed (state lock under $XDG_STATE_HOME). A file that
#     exists but was not installed by this script, or was edited afterwards, is treated as a
#     project customization and skipped unless --force (it is backed up before overwrite).
#
# Usage
#   ./sync.sh [auto|global|local] [--target DIR] [--harness claude,codex,gemini]
#             [--dry-run] [--check] [--force] [--rollback DIR] [-h|--help]
#
# Exit codes: 0 ok / in sync, 1 drift found (--check) or failure, 2 usage error.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
ROLES=(archon graphos ontos pragma dokimos hermon)
STATE_ROOT="${XDG_STATE_HOME:-$HOME/.local/state}/pipeline-agentic"

MODE="auto"
TARGET=""
HARNESS=""
DRY_RUN=0
CHECK=0
FORCE=0
ROLLBACK=""

info() { printf '[*] %s\n' "$*"; }
ok()   { printf '[+] %s\n' "$*"; }
warn() { printf '[!] %s\n' "$*" >&2; }
die()  { printf '[x] %s\n' "$1" >&2; exit "${2:-1}"; }

usage() { sed -n '2,29p' "$0" | sed 's/^# \{0,1\}//'; }

cap() { printf '%s%s' "$(printf '%s' "${1:0:1}" | tr '[:lower:]' '[:upper:]')" "${1:1}"; }
sha() { sha256sum "$1" | cut -d' ' -f1; }

# ---------------------------------------------------------------- argument parsing
while (($#)); do
  case "$1" in
    auto|global|local) MODE="$1" ;;
    --target)   TARGET="${2:?--target needs a directory}"; shift ;;
    --harness)  HARNESS="${2:?--harness needs a list}"; shift ;;
    --dry-run)  DRY_RUN=1 ;;
    --check)    CHECK=1 ;;
    --force)    FORCE=1 ;;
    --rollback) ROLLBACK="${2:?--rollback needs a backup directory}"; shift ;;
    -h|--help)  usage; exit 0 ;;
    *) usage >&2; die "unknown argument: $1" 2 ;;
  esac
  shift
done
((CHECK)) && DRY_RUN=1   # --check never writes

command -v python3 >/dev/null || die "python3 is required"
command -v sha256sum >/dev/null || die "sha256sum is required"

# ---------------------------------------------------------------- harness detection
detect_harnesses() {
  local found=()
  { command -v claude >/dev/null || [[ -d $HOME/.claude ]]; } && found+=(claude)
  { command -v codex  >/dev/null || [[ -d $HOME/.codex  ]]; } && found+=(codex)
  { command -v gemini >/dev/null || command -v agy >/dev/null || [[ -d $HOME/.gemini ]]; } && found+=(gemini)
  local IFS=,; printf '%s' "${found[*]}"
}

if [[ -z $HARNESS ]]; then
  HARNESS="$(detect_harnesses)"
  [[ -n $HARNESS ]] || die "no harness detected (claude, codex, gemini/agy); use --harness"
  info "Detected harnesses: $HARNESS"
fi
IFS=, read -r -a SELECTED <<<"$HARNESS"
for h in "${SELECTED[@]}"; do
  [[ $h == claude || $h == codex || $h == gemini ]] || die "unknown harness: $h" 2
done
has() { [[ ",$HARNESS," == *",$1,"* ]]; }

# ---------------------------------------------------------------- mode resolution
if [[ $MODE == auto ]]; then
  if [[ -n $TARGET ]]; then
    MODE=local
  else
    top="$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || true)"
    if [[ -n $top && "$(cd "$top" && pwd -P)" != "$REPO" ]]; then
      MODE=local; TARGET="$top"
    else
      MODE=global
    fi
  fi
  info "Auto mode resolved to: $MODE${TARGET:+ ($TARGET)}"
fi
if [[ $MODE == local ]]; then
  [[ -n $TARGET ]] || TARGET="$(git -C "$PWD" rev-parse --show-toplevel 2>/dev/null || pwd -P)"
  [[ -d $TARGET ]] || die "target directory does not exist: $TARGET"
  TARGET="$(cd "$TARGET" && pwd -P)"
  [[ $TARGET != "$REPO" ]] || die "local target is the pipeline repository itself; use global mode"
fi

# ---------------------------------------------------------------- rollback
if [[ -n $ROLLBACK ]]; then
  [[ -d $ROLLBACK ]] || die "backup directory not found: $ROLLBACK"
  if [[ $MODE == global ]]; then
    exec python3 "$REPO/scripts/agent_inject_harnesses.py" --rollback "$ROLLBACK"
  fi
  lock="$STATE_ROOT/$(printf '%s' "$TARGET" | sha256sum | cut -c1-16).lock"
  info "Restoring $TARGET from $ROLLBACK"
  restored="$(mktemp)"
  while IFS= read -r -d '' f; do
    rel="${f#./}"; mkdir -p "$(dirname "$TARGET/$rel")"; cp -p "$ROLLBACK/$rel" "$TARGET/$rel"
    printf '%s\n' "$rel" >>"$restored"
    printf '  RESTORED %s\n' "$rel"
  done < <(cd "$ROLLBACK" && find . -type f -print0)
  # A backup may hold a project customization: restored files stop being pipeline-owned, so a
  # later sync skips them (SKIP) instead of silently overwriting them; --force overrides.
  if [[ -f $lock ]]; then
    tmp="$(mktemp)"
    grep -v -F -f <(sed 's/$/ /' "$restored") "$lock" >"$tmp" || true
    mv "$tmp" "$lock"
  fi
  rm -f "$restored"
  ok "Rollback complete"; exit 0
fi

# ---------------------------------------------------------------- preflight (repo integrity)
preflight() {
  local f
  for f in "$REPO"/.agents/*/agent.json; do
    python3 -m json.tool "$f" >/dev/null 2>&1 || die "invalid JSON, refusing to deploy: ${f#"$REPO"/}"
  done
  if python3 "$REPO/scripts/sync_roles.py" --check >/dev/null; then
    ok "Role copies in sync with claude/ (canonical source)"
  elif ((DRY_RUN)); then
    warn "Role copies differ from claude/; a real run propagates them first (scripts/sync_roles.py)"
    DRIFT=1
  else
    info "Propagating role bodies from claude/ to codex/, gemini/ and .agents/ ..."
    python3 "$REPO/scripts/sync_roles.py" | sed 's/^/    /'
    warn "Repository files were updated by propagation — review and commit them"
  fi
}

# ---------------------------------------------------------------- global mode
global_sync() {
  local runbook="$REPO/scripts/agent_inject_harnesses.py"
  local only="$HARNESS"
  if python3 "$runbook" --verify-only --only "$only" >/dev/null 2>&1 && ((DRIFT == 0)); then
    ok "Global ($only): every installed file already matches the repository — nothing to do"
    return 0
  fi
  if ((CHECK)); then
    warn "Global ($only): installed files differ from the repository"
    python3 "$runbook" --verify-only --only "$only" 2>&1 | grep -E 'mismatch|Missing|MUTATED|FAILED' | sed 's/^/    /' || true
    return 1
  fi
  if ((DRY_RUN)); then
    python3 "$runbook" --dry-run --only "$only"
  else
    python3 "$runbook" --only "$only"
  fi
}

# ---------------------------------------------------------------- local mode
local_map() {   # prints "source<TAB>relative-target" for the selected harnesses
  local r
  if has claude; then
    printf '%s\t%s\n' "claude/CLAUDE.md" ".claude/CLAUDE.md"
    for r in "${ROLES[@]}"; do printf '%s\t%s\n' "claude/$(cap "$r").md" ".claude/agents/$(cap "$r").md"; done
  fi
  if has codex; then
    printf '%s\t%s\n' "codex/AGENTS.md" ".codex/AGENTS.md"
    for r in "${ROLES[@]}"; do printf '%s\t%s\n' "codex/roles/$r.md" ".codex/roles/$r.md"; done
  fi
  if has gemini; then
    printf '%s\t%s\n' "gemini/gemini-cli/GEMINI.md" ".gemini/GEMINI.md"
    for r in "${ROLES[@]}"; do
      printf '%s\t%s\n' "gemini/gemini-cli/$r.md" ".gemini/$r.md"
      printf '%s\t%s\n' ".agents/$r/agent.json" ".agents/$r/agent.json"
    done
  fi
}

local_sync() {
  mkdir -p "$STATE_ROOT"
  local key lock backup src rel dst action owned_sha
  key="$(printf '%s' "$TARGET" | sha256sum | cut -c1-16)"
  lock="$STATE_ROOT/$key.lock"
  backup="$STATE_ROOT/backups/$(basename "$TARGET")-$(date +%Y%m%d_%H%M%S)"
  declare -A OWNED=()
  if [[ -f $lock ]]; then
    while read -r rel owned_sha; do OWNED["$rel"]="$owned_sha"; done <"$lock"
  fi

  local -a plan=()
  local n_new=0 n_upd=0 n_same=0 n_skip=0
  info "Local target: $TARGET"
  while IFS=$'\t' read -r src rel; do
    dst="$TARGET/$rel"
    if [[ ! -e $dst ]]; then
      action=NEW; ((++n_new))
    elif cmp -s "$REPO/$src" "$dst"; then
      action=SAME; ((++n_same))
    elif [[ ${OWNED[$rel]:-} == "$(sha "$dst")" ]]; then
      action=UPDATE; ((++n_upd))
    elif ((FORCE)); then
      action=FORCE; ((++n_upd))
    else
      action=SKIP; ((++n_skip))
    fi
    printf '  %-6s %s\n' "$action" "$rel"
    plan+=("$action"$'\t'"$src"$'\t'"$rel")
  done < <(local_map)

  info "Summary: $n_new new, $n_upd update, $n_same unchanged, $n_skip skipped (project-customized; --force to overwrite)"
  if ((CHECK)); then
    ((n_new + n_upd + n_skip + DRIFT == 0)) && { ok "Local target in sync"; return 0; }
    return 1
  fi
  ((DRY_RUN)) && { info "Dry run: nothing written"; return 0; }
  ((n_new + n_upd == 0)) && { ok "Nothing to write"; }

  local entry wrote=0
  for entry in "${plan[@]}"; do
    IFS=$'\t' read -r action src rel <<<"$entry"
    dst="$TARGET/$rel"
    case $action in
      UPDATE|FORCE)
        mkdir -p "$(dirname "$backup/$rel")"; cp -p "$dst" "$backup/$rel" ;;&
      NEW|UPDATE|FORCE)
        mkdir -p "$(dirname "$dst")"; cp "$REPO/$src" "$dst"
        cmp -s "$REPO/$src" "$dst" || die "verification failed after writing $rel (backup: $backup)"
        wrote=1 ;;
    esac
  done

  # Record every file this script now owns (installed and identical to the repository).
  local tmp; tmp="$(mktemp)"
  while IFS=$'\t' read -r src rel; do
    dst="$TARGET/$rel"
    if [[ -f $dst ]] && cmp -s "$REPO/$src" "$dst"; then
      printf '%s %s\n' "$rel" "$(sha "$dst")"
    elif [[ -n ${OWNED[$rel]:-} ]]; then
      printf '%s %s\n' "$rel" "${OWNED[$rel]}"
    fi
  done < <(local_map) >"$tmp"
  mv "$tmp" "$lock"

  if ((wrote)); then
    if ((n_upd > 0)); then ok "Local sync complete; previous versions backed up in $backup"; else ok "Local sync complete"; fi
  fi
  [[ -d $TARGET/.git ]] && info "Tip: decide whether to commit .claude/ .codex/ .gemini/ .agents/ in $TARGET or add them to .gitignore"
  return 0
}

# ---------------------------------------------------------------- main
DRIFT=0
info "Pipeline repository: $REPO ($(git -C "$REPO" rev-parse --short HEAD 2>/dev/null || echo 'no git'))"
preflight
case $MODE in
  global) global_sync ;;
  local)  local_sync ;;
  *) die "unknown mode: $MODE" 2 ;;
esac
