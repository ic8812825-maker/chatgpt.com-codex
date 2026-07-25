#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_ROOT="$REPO_ROOT/MinusLock_BigHarvest_EA_V2"
OUTPUT_DIR="${1:-$REPO_ROOT/.stage_1_2_4_1_evidence}"
SOURCE_BASE="4413a05bd785cbef398fc418ad12b008fa090a00"
SOURCE_COMMIT="11ae620f717cf011436db52cf4b3b76d0015c606"
EVIDENCE_BRANCH_NAME="${EVIDENCE_BRANCH_NAME:-$(git -C "$REPO_ROOT" branch --show-current)}"
EVIDENCE_BRANCH_SHA="${EVIDENCE_BRANCH_SHA:-$(git -C "$REPO_ROOT" rev-parse HEAD)}"
FORBIDDEN_PATTERN='MinusLock_BigHarvest_EA_V2/Include/(StateMachine|TradeEngine|PositionUtils|SimulationEngine|HybridPartialFarPreview|BrokerMoneyModel|Types|Config)\.mqh'
overall_status=0

mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR"/*.log "$OUTPUT_DIR/evidence_manifest.txt" "$OUTPUT_DIR/SHA256SUMS.txt"

run_logged() {
  local log_name="$1"
  shift
  set +e
  "$@" 2>&1 | tee "$OUTPUT_DIR/$log_name"
  local status=${PIPESTATUS[0]}
  set -e
  if (( status != 0 )); then
    overall_status=1
  fi
  return 0
}

run_logged 01_py_compile.log \
  python3 -m py_compile "$PROJECT_ROOT"/Tests/HybridSplitBig/*.py
run_logged 02_dimension_contract.log \
  python3 -m pytest -q "$PROJECT_ROOT/Tests/HybridSplitBig/test_catchup_full_dimension_contract.py"
run_logged 03_hybrid_split_big.log \
  python3 -m pytest -q "$PROJECT_ROOT/Tests/HybridSplitBig"
run_logged 04_all_tests.log \
  python3 -m pytest -q "$PROJECT_ROOT/Tests"
run_logged 05_big_move_levels_check.log \
  python3 "$PROJECT_ROOT/Tests/big_move_levels_check.py"
run_logged 06_validate_v2_static.log \
  python3 "$PROJECT_ROOT/Tests/validate_v2_static.py"

set +e
forbidden_files="$(git -C "$REPO_ROOT" diff --name-only "$SOURCE_BASE" "$SOURCE_COMMIT" | grep -E "$FORBIDDEN_PATTERN")"
forbidden_status=$?
set -e
{
  printf 'SOURCE_BASE=%s\nSOURCE_COMMIT=%s\n' "$SOURCE_BASE" "$SOURCE_COMMIT"
  if [[ -n "$forbidden_files" ]]; then
    printf 'FORBIDDEN_FILES_FOUND\n%s\n' "$forbidden_files"
    overall_status=1
  elif (( forbidden_status == 0 )); then
    printf 'FORBIDDEN_FILES_EMPTY\n'
  else
    printf 'FORBIDDEN_FILES_EMPTY\n'
  fi
} 2>&1 | tee "$OUTPUT_DIR/07_forbidden_files.log"

{
  printf 'REPOSITORY=%s\n' "$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || printf 'NOT_AVAILABLE')"
  printf 'BRANCH=%s\n' "$EVIDENCE_BRANCH_NAME"
  printf 'CI_COMMIT=%s\n' "$EVIDENCE_BRANCH_SHA"
  printf 'SOURCE_BASE=%s\nSOURCE_COMMIT=%s\n' "$SOURCE_BASE" "$SOURCE_COMMIT"
  printf 'CHANGED_FILES_BEGIN\n'
  git -C "$REPO_ROOT" diff --name-only "$SOURCE_COMMIT" HEAD
  printf 'CHANGED_FILES_END\n'
} 2>&1 | tee "$OUTPUT_DIR/08_git_metadata.log"

cat > "$OUTPUT_DIR/evidence_manifest.txt" <<EOF
STAGE=1.2.4.1
EVIDENCE_STAGE=1.2.4.2
REPOSITORY=$(git -C "$REPO_ROOT" remote get-url origin 2>/dev/null || printf 'NOT_AVAILABLE')
BRANCH=$EVIDENCE_BRANCH_NAME
SOURCE_COMMIT=$SOURCE_COMMIT
SOURCE_BASE=$SOURCE_BASE
CI_COMMIT=$EVIDENCE_BRANCH_SHA
UTC_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
PYTHON_VERSION=$(python3 --version 2>&1)
PYTEST_VERSION=$(python3 -m pytest --version 2>&1 | head -n 1)
OPERATING_SYSTEM=$(uname -a)
CHANGED_FILES=$(git -C "$REPO_ROOT" diff --name-only "$SOURCE_COMMIT" HEAD | paste -sd, -)
TEST_COMMANDS=py_compile;dimension_contract_pytest;HybridSplitBig_pytest;all_project_pytest;big_move_levels_check;validate_v2_static;forbidden_files_guard
EXIT_STATUS=$overall_status
ARTIFACT_CONTENTS=01_py_compile.log,02_dimension_contract.log,03_hybrid_split_big.log,04_all_tests.log,05_big_move_levels_check.log,06_validate_v2_static.log,07_forbidden_files.log,08_git_metadata.log,evidence_manifest.txt,SHA256SUMS.txt
EOF

(
  cd "$OUTPUT_DIR"
  sha256sum ./*.log evidence_manifest.txt > SHA256SUMS.txt
)

printf 'SOURCE_VALIDATION_SUMMARY|ExitStatus=%d|Evidence=%s\n' "$overall_status" "$OUTPUT_DIR"
exit "$overall_status"
