#!/usr/bin/env bash
set -euo pipefail

BRANCH="${1:-work}"
REMOTE="${2:-origin}"

run() {
  echo "\n$ $*"
  eval "$*"
}

echo "== Two-way Git + file operations verification =="
run "git status -sb"
run "git remote -v"
run "git branch --show-current"
run "git rev-parse --abbrev-ref --symbolic-full-name @{u}"

run "git fetch ${REMOTE} --prune"
run "git rev-list --left-right --count ${REMOTE}/${BRANCH}...${BRANCH}"

run "sha256sum test-file.txt test-file-2.txt"
run "git show ${REMOTE}/${BRANCH}:test-file.txt | sha256sum"
run "git show ${REMOTE}/${BRANCH}:test-file-2.txt | sha256sum"

run "git push --dry-run ${REMOTE} ${BRANCH}"
run "git pull --ff-only --dry-run ${REMOTE} ${BRANCH}"

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
