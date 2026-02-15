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
}

echo "== Two-way Git + file operations verification =="
run "git status -sb"
run "git remote -v"
run "git branch --show-current"

# Ensure upstream exists, otherwise set it to REMOTE/BRANCH.
if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} >/dev/null 2>&1; then
  echo "No upstream configured for current branch. Setting upstream to ${REMOTE}/${BRANCH}."
  run "git branch --set-upstream-to=${REMOTE}/${BRANCH} ${BRANCH}"
fi

run "git rev-parse --abbrev-ref --symbolic-full-name @{u}"

run "git fetch ${REMOTE} --prune"
run "git rev-list --left-right --count ${REMOTE}/${BRANCH}...${BRANCH}"

run "sha256sum test-file.txt test-file-2.txt"
run "git show ${REMOTE}/${BRANCH}:test-file.txt | sha256sum"
run "git show ${REMOTE}/${BRANCH}:test-file-2.txt | sha256sum"

run_may_fail "git push --dry-run ${REMOTE} ${BRANCH}"
run_may_fail "git pull --ff-only --dry-run ${REMOTE} ${BRANCH}"

run "mkdir -p checks"
run "printf 'probe-line-1\\n' > checks/io-probe.txt"
run "cat checks/io-probe.txt"
run "printf 'probe-line-2\\n' >> checks/io-probe.txt"
run "cp checks/io-probe.txt checks/io-probe.copy.txt"
run "mv checks/io-probe.copy.txt checks/io-probe.moved.txt"
run "wc -l checks/io-probe.txt checks/io-probe.moved.txt"
run "rm -f checks/io-probe.txt checks/io-probe.moved.txt"
run "rmdir checks"

run "git config --global --get credential.helper"
run "test -f ~/.git-credentials && echo credentials_file_present=yes || echo credentials_file_present=no"
run "git status -sb"

echo "\n== Verification complete =="
