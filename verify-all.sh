#!/usr/bin/env bash
set -euo pipefail

# ========= COLORS =========
if [ -t 1 ]; then
  RED="\033[31m"
  GREEN="\033[32m"
  YELLOW="\033[33m"
  BLUE="\033[34m"
  RESET="\033[0m"
else
  RED=""
  GREEN=""
  YELLOW=""
  BLUE=""
  RESET=""
fi

log()   { printf "%b== %s ==%b\n" "${BLUE}" "$*" "${RESET}"; }
ok()    { printf "%b%s%b\n" "${GREEN}" "$*" "${RESET}"; }
warn()  { printf "%bWARNING: %s%b\n" "${YELLOW}" "$*" "${RESET}"; }
fail()  { printf "%bERROR: %s%b\n" "${RED}" "$*" "${RESET}"; }

# ========= CI SAFE =========
export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=/bin/true
export GIT_SSH_COMMAND="ssh -oBatchMode=yes"
export GIT_CONFIG_NOSYSTEM=1

# ========= ARGUMENTS =========
ARG_BRANCH="${1:-}"
PRIMARY_REMOTE="${2:-origin}"
REMOTES=("${PRIMARY_REMOTE}" "upstream" "backup")

CURRENT_BRANCH="$(git symbolic-ref --quiet --short HEAD || true)"
if [ -z "${CURRENT_BRANCH}" ]; then
  fail "Detached HEAD or unborn branch"
  exit 1
fi

if [ -n "${ARG_BRANCH}" ] && [ "${ARG_BRANCH}" != "${CURRENT_BRANCH}" ]; then
  fail "arg branch '${ARG_BRANCH}' != current '${CURRENT_BRANCH}'"
  exit 1
fi

log "Two-way Git verification (branch: ${CURRENT_BRANCH})"

run() {
  printf "\n$"
  printf " %q" "$@"
  printf "\n"
  "$@"
}

run_may_fail() {
  printf "\n$"
  printf " %q" "$@"
  printf "\n"
  set +e
  "$@"
  rc=$?
  set -e
  if [ $rc -ne 0 ]; then
    warn "command failed with exit code $rc"
  fi
  return 0
}

# ========= BASIC STATE =========
run git status -sb
run git remote -v
run git branch --show-current

# ========= FIND WORKING REMOTE =========
WORKING_REMOTE=""
REMOTE_BRANCH_AVAILABLE=0

for r in "${REMOTES[@]}"; do
  if git remote get-url "${r}" >/dev/null 2>&1; then
    log "Checking remote: ${r}"
    if git fetch "${r}" "+refs/heads/${CURRENT_BRANCH}:refs/remotes/${r}/${CURRENT_BRANCH}" >/dev/null 2>&1; then
      if git show-ref --verify --quiet "refs/remotes/${r}/${CURRENT_BRANCH}"; then
        WORKING_REMOTE="${r}"
        REMOTE_BRANCH_AVAILABLE=1
        ok "Using remote: ${WORKING_REMOTE}"
        break
      fi
    fi
  fi
done

if [ -z "${WORKING_REMOTE}" ]; then
  warn "No remote branch found. Remote checks limited."
fi

# ========= UPSTREAM =========
UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)"
EXPECTED_UPSTREAM="${WORKING_REMOTE}/${CURRENT_BRANCH}"
if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
  if [ -z "$UPSTREAM" ] || [ "$UPSTREAM" != "$EXPECTED_UPSTREAM" ]; then
    run_may_fail git branch --set-upstream-to="$EXPECTED_UPSTREAM" "$CURRENT_BRANCH"
    UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || true)"
  fi
fi
[ -n "$UPSTREAM" ] && ok "Upstream: $UPSTREAM" || warn "No upstream configured"

# ========= ULTRA PARANOID AUDIT =========
log "Ultra-paranoid audit"
if git rev-parse HEAD >/dev/null 2>&1; then
  run git rev-parse HEAD
  run git rev-parse "$CURRENT_BRANCH"
  run git cat-file -p HEAD

  TREE_HASH="$(git rev-parse HEAD^{tree})"
  ok "Tree hash: ${TREE_HASH}"

  run bash -lc 'git ls-tree -r --full-tree HEAD | sha256sum'

  if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
    REMOTE_HEAD="$(git rev-parse --verify "${WORKING_REMOTE}/${CURRENT_BRANCH}" 2>/dev/null || true)"
    if [ -n "$REMOTE_HEAD" ]; then
      ok "Remote HEAD: ${REMOTE_HEAD}"
      run git rev-list --left-right --count "${WORKING_REMOTE}/${CURRENT_BRANCH}...${CURRENT_BRANCH}"

      log "Compare commit hashes"
      if [ "${REMOTE_HEAD}" = "$(git rev-parse HEAD)" ]; then
        ok "Local and remote HEAD identical"
      else
        warn "Local and remote differ"
      fi
    else
      warn "Cannot resolve remote HEAD for ${WORKING_REMOTE}/${CURRENT_BRANCH}"
    fi
  fi
else
  warn "Repository has no commits yet"
fi

# ========= FILE HASH CHECK =========
log "File integrity"
FILES=("test-file.txt" "test-file-2.txt")
for f in "${FILES[@]}"; do
  if [ -L "$f" ]; then
    warn "File is symlink: $f"
  fi

  if [ -f "$f" ]; then
    run sha256sum "$f"
    run git hash-object "$f"
    if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
      run_may_fail bash -lc "git show '${WORKING_REMOTE}/${CURRENT_BRANCH}:${f}' | sha256sum"
    fi
  else
    warn "File not found locally: $f (skipping hash check)"
  fi
done

# ========= PUSH / PULL DRY RUN =========
if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
  run_may_fail git push --dry-run "$WORKING_REMOTE" "$CURRENT_BRANCH"
  run_may_fail git pull --ff-only --dry-run "$WORKING_REMOTE" "$CURRENT_BRANCH"
fi

# ========= FILE I/O =========
log "Filesystem verification"
run mkdir -p checks
run bash -lc "printf 'probe-line-1\\n' > checks/io-probe.txt"
run bash -lc "printf 'probe-line-2\\n' >> checks/io-probe.txt"
run cp checks/io-probe.txt checks/io-probe.copy.txt
run mv checks/io-probe.copy.txt checks/io-probe.moved.txt
run wc -l checks/io-probe.txt checks/io-probe.moved.txt
run rm -f checks/io-probe.txt checks/io-probe.moved.txt
run rmdir checks

# ========= CREDENTIAL =========
log "Credential check"
run_may_fail git config --global --get credential.helper
run_may_fail test -f ~/.git-credentials
if test -f ~/.git-credentials; then
  ok "credentials_file_present=yes"
else
  warn "credentials_file_present=no"
fi

run git status -sb
ok "Verification complete"
