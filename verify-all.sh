#!/usr/bin/env bash
set -euo pipefail

BRANCH="${1:-work}"
REMOTE="${2:-origin}"

run() {
  echo "\n$ $*"
  eval "$*"
}

run_may_fail() {
  echo "\n$ $*"
  set +e
  eval "$*"
  rc=$?
  set -e
  if [ $rc -ne 0 ]; then
    echo "WARNING: command failed with exit code $rc"
  fi
  return 0
}

echo "== Two-way Git + file operations verification =="
run "git status -sb"
run "git remote -v"
run "git branch --show-current"

REMOTE_AVAILABLE=1
if ! git remote get-url "${REMOTE}" >/dev/null 2>&1; then
  REMOTE_AVAILABLE=0
  echo "WARNING: remote '${REMOTE}' is not configured. Remote checks will be skipped."
fi

REMOTE_BRANCH_AVAILABLE=0
if [ "$REMOTE_AVAILABLE" -eq 1 ]; then
  run_may_fail "git fetch ${REMOTE} --prune"
  if git show-ref --verify --quiet "refs/remotes/${REMOTE}/${BRANCH}"; then
    REMOTE_BRANCH_AVAILABLE=1
  else
    echo "WARNING: remote branch '${REMOTE}/${BRANCH}' does not exist yet."
  fi
fi

# Ensure upstream exists when remote branch is available.
if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
    echo "No upstream configured for current branch. Setting upstream to ${REMOTE}/${BRANCH}."
    run_may_fail "git branch --set-upstream-to=${REMOTE}/${BRANCH} ${BRANCH}"
  else
    echo "WARNING: upstream not configured and ${REMOTE}/${BRANCH} unavailable; skipping upstream setup."
  fi
fi

run_may_fail "git rev-parse --abbrev-ref --symbolic-full-name @{u}"

if [ "$REMOTE_BRANCH_AVAILABLE" -eq 1 ]; then
  run "git rev-list --left-right --count ${REMOTE}/${BRANCH}...${BRANCH}"

  run "sha256sum test-file.txt test-file-2.txt"
  run "git show ${REMOTE}/${BRANCH}:test-file.txt | sha256sum"
  run "git show ${REMOTE}/${BRANCH}:test-file-2.txt | sha256sum"

  run_may_fail "git push --dry-run ${REMOTE} ${BRANCH}"
  run_may_fail "git pull --ff-only --dry-run ${REMOTE} ${BRANCH}"
else
  run "sha256sum test-file.txt test-file-2.txt"
fi

run "mkdir -p checks"
run "printf 'probe-line-1\n' > checks/io-probe.txt"
run "cat checks/io-probe.txt"
run "printf 'probe-line-2\n' >> checks/io-probe.txt"
run "cp checks/io-probe.txt checks/io-probe.copy.txt"
run "mv checks/io-probe.copy.txt checks/io-probe.moved.txt"
run "wc -l checks/io-probe.txt checks/io-probe.moved.txt"
run "rm -f checks/io-probe.txt checks/io-probe.moved.txt"
run "rmdir checks"

run_may_fail "git config --global --get credential.helper"
run_may_fail "test -f ~/.git-credentials && echo credentials_file_present=yes || echo credentials_file_present=no"
run "git status -sb"

echo "\n== Verification complete =="
