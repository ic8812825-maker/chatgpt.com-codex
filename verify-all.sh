#!/usr/bin/env bash
set -euo pipefail

# ========= COLORS =========
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
RESET="\033[0m"

log()   { echo -e "${BLUE}== $* ==${RESET}"; }
ok()    { echo -e "${GREEN}$*${RESET}"; }
warn()  { echo -e "${YELLOW}WARNING: $*${RESET}"; }
fail()  { echo -e "${RED}ERROR: $*${RESET}"; }

# ========= CI SAFE =========
export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=true
export GIT_SSH_COMMAND="ssh -oBatchMode=yes"

# ========= ARGUMENTS =========
ARG_BRANCH="${1:-}"
PRIMARY_REMOTE="${2:-origin}"
REMOTES=("${PRIMARY_REMOTE}" "upstream" "backup")

CURRENT_BRANCH="$(git branch --show-current)"
if [ -z "${CURRENT_BRANCH}" ]; then
  fail "Detached HEAD detected. Checkout a branch first."
  exit 1
fi

if [ -n "${ARG_BRANCH}" ] && [ "${ARG_BRANCH}" != "${CURRENT_BRANCH}" ]; then
  fail "arg branch '${ARG_BRANCH}' != current '${CURRENT_BRANCH}'"
  exit 1
fi

log "Two-way Git verification (branch: ${CURRENT_BRANCH})"

run() {
  echo -e "\n$ $*"
  eval "$*"
}

run_may_fail() {
  echo -e "\n$ $*"
  set +e
  eval "$*"
  rc=$?
  set -e
  if [ $rc -ne 0 ]; then
    warn "command failed with exit code $rc"
  fi
  return 0
}

# ========= BASIC STATE =========
run "git status -sb"
run "git remote -v"
run "git branch --show-current"

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
if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
  if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
    run_may_fail "git branch --set-upstream-to=${WORKING_REMOTE}/${CURRENT_BRANCH} ${CURRENT_BRANCH}"
  fi
fi
run_may_fail "git rev-parse --abbrev-ref --symbolic-full-name @{u}"

# ========= ULTRA PARANOID AUDIT =========
log "Ultra-paranoid audit"
run "git rev-parse HEAD"
run "git rev-parse ${CURRENT_BRANCH}"
run "git cat-file -p HEAD | head -n 5"
TREE_HASH="$(git rev-parse HEAD^{tree})"
ok "Tree hash: ${TREE_HASH}"
run "git ls-tree -r HEAD | sha256sum"

if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
  REMOTE_HEAD="$(git rev-parse ${WORKING_REMOTE}/${CURRENT_BRANCH})"
  ok "Remote HEAD: ${REMOTE_HEAD}"
  run "git rev-list --left-right --count ${WORKING_REMOTE}/${CURRENT_BRANCH}...${CURRENT_BRANCH}"
  log "Compare commit hashes"
  if [ "${REMOTE_HEAD}" = "$(git rev-parse HEAD)" ]; then
    ok "Local and remote HEAD identical"
  else
    warn "Local and remote differ"
  fi
fi

# ========= FILE HASH CHECK =========
log "File integrity"
FILES=("test-file.txt" "test-file-2.txt")
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    run "sha256sum '$f'"
    if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
      run_may_fail "git show ${WORKING_REMOTE}/${CURRENT_BRANCH}:'$f' | sha256sum"
    fi
  else
    warn "File not found locally: $f (skipping hash check)"
  fi
done

# ========= PUSH / PULL DRY RUN =========
if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
  run_may_fail "git push --dry-run ${WORKING_REMOTE} ${CURRENT_BRANCH}"
  run_may_fail "git pull --ff-only --dry-run ${WORKING_REMOTE} ${CURRENT_BRANCH}"
fi

# ========= FILE I/O =========
log "Filesystem verification"
run "mkdir -p checks"
run "printf 'probe-line-1\n' > checks/io-probe.txt"
run "printf 'probe-line-2\n' >> checks/io-probe.txt"
run "cp checks/io-probe.txt checks/io-probe.copy.txt"
run "mv checks/io-probe.copy.txt checks/io-probe.moved.txt"
run "wc -l checks/io-probe.txt checks/io-probe.moved.txt"
run "rm -f checks/io-probe.txt checks/io-probe.moved.txt"
run "rmdir checks"

# ========= CREDENTIAL =========
log "Credential check"
run_may_fail "git config --global --get credential.helper"
run_may_fail "test -f ~/.git-credentials && echo credentials_file_present=yes || echo credentials_file_present=no"
run "git status -sb"
ok "Verification complete"
