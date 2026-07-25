#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
PROJECT_ROOT="$REPO_ROOT/MinusLock_BigHarvest_EA_V2"
SOURCE_BASE="4413a05bd785cbef398fc418ad12b008fa090a00"
SOURCE_COMMIT="11ae620f717cf011436db52cf4b3b76d0015c606"
FORBIDDEN_PATTERN='^MinusLock_BigHarvest_EA_V2/Include/(StateMachine|TradeEngine|PositionUtils|SimulationEngine|HybridPartialFarPreview|BrokerMoneyModel|Types|Config)\.mqh$'

match_forbidden_paths() {
  grep -E "$FORBIDDEN_PATTERN"
}

check_forbidden_files() {
  local base_sha="$1" source_sha="$2" log_file="$3"
  local changed_files diff_status forbidden_files

  if ! git -C "$REPO_ROOT" cat-file -e "${base_sha}^{commit}" 2>/dev/null; then
    { printf 'FORBIDDEN_FILES_GUARD_ERROR\nREASON=SOURCE_BASE_NOT_FOUND\nSOURCE_BASE=%s\n' "$base_sha"; } | tee "$log_file"
    return 2
  fi
  if ! git -C "$REPO_ROOT" cat-file -e "${source_sha}^{commit}" 2>/dev/null; then
    { printf 'FORBIDDEN_FILES_GUARD_ERROR\nREASON=SOURCE_COMMIT_NOT_FOUND\nSOURCE_COMMIT=%s\n' "$source_sha"; } | tee "$log_file"
    return 3
  fi

  set +e
  changed_files="$(git -C "$REPO_ROOT" diff --name-only "$base_sha" "$source_sha" 2>&1)"
  diff_status=$?
  set -e
  if (( diff_status != 0 )); then
    {
      printf 'FORBIDDEN_FILES_GUARD_ERROR\nREASON=GIT_DIFF_FAILED\nGIT_DIFF_EXIT_STATUS=%d\n' "$diff_status"
      printf 'GIT_DIFF_OUTPUT_BEGIN\n%s\nGIT_DIFF_OUTPUT_END\n' "$changed_files"
    } | tee "$log_file"
    return 4
  fi

  forbidden_files="$(printf '%s\n' "$changed_files" | match_forbidden_paths || true)"
  if [[ -n "$forbidden_files" ]]; then
    {
      printf 'FORBIDDEN_FILES_FOUND\nSOURCE_BASE=%s\nSOURCE_COMMIT=%s\nFILES_BEGIN\n' "$base_sha" "$source_sha"
      printf '%s\nFILES_END\n' "$forbidden_files"
    } | tee "$log_file"
    return 1
  fi
  {
    printf 'FORBIDDEN_FILES_EMPTY\nSOURCE_BASE=%s\nSOURCE_BASE_EXISTS=1\n' "$base_sha"
    printf 'SOURCE_COMMIT=%s\nSOURCE_COMMIT_EXISTS=1\nGIT_DIFF_EXIT_STATUS=0\n' "$source_sha"
  } | tee "$log_file"
  return 0
}

run_guard_self_tests() {
  local passed=0 failed=0 status tmp
  tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' RETURN
  set +e
  check_forbidden_files 0000000000000000000000000000000000000000 "$SOURCE_COMMIT" "$tmp/01.log" >/dev/null; status=$?
  set -e
  if (( status == 2 )) && grep -q 'REASON=SOURCE_BASE_NOT_FOUND' "$tmp/01.log"; then ((passed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-01|PASS'; else ((failed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-01|FAIL'; fi
  set +e
  check_forbidden_files "$SOURCE_BASE" 0000000000000000000000000000000000000000 "$tmp/02.log" >/dev/null; status=$?
  set -e
  if (( status == 3 )) && grep -q 'REASON=SOURCE_COMMIT_NOT_FOUND' "$tmp/02.log"; then ((passed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-02|PASS'; else ((failed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-02|FAIL'; fi
  set +e
  check_forbidden_files "$SOURCE_BASE" "$SOURCE_COMMIT" "$tmp/03.log" >/dev/null; status=$?
  set -e
  if (( status == 0 )) && grep -q '^FORBIDDEN_FILES_EMPTY$' "$tmp/03.log"; then ((passed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-03|PASS'; else ((failed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-03|FAIL'; fi
  if printf '%s\n' 'MinusLock_BigHarvest_EA_V2/Include/StateMachine.mqh' | match_forbidden_paths >/dev/null; then ((passed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-04|PASS'; else ((failed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-04|FAIL'; fi
  if ! printf '%s\n' 'MinusLock_BigHarvest_EA_V2/Docs/STAGE_1_2_4_1_EVIDENCE_RU.md' | match_forbidden_paths >/dev/null; then ((passed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-05|PASS'; else ((failed+=1)); echo 'FORBIDDEN_GUARD_SELF_TEST|SELF-GUARD-05|FAIL'; fi
  printf 'FORBIDDEN_GUARD_SELF_TEST|SUMMARY|Passed=%d|Failed=%d\n' "$passed" "$failed"
  (( failed == 0 ))
}

if [[ "${1:-}" == "--self-test-forbidden-guard" ]]; then
  run_guard_self_tests
  exit $?
fi

OUTPUT_DIR="${1:-$REPO_ROOT/.stage_1_2_4_1_evidence}"
BRANCH="${EVIDENCE_BRANCH_NAME:-$(git -C "$REPO_ROOT" branch --show-current)}"
CI_COMMIT="${EVIDENCE_BRANCH_SHA:-$(git -C "$REPO_ROOT" rev-parse HEAD)}"
ORIGIN_WORK_SHA="$(git -C "$REPO_ROOT" rev-parse origin/work 2>/dev/null || printf 'NOT_AVAILABLE')"
overall_status=0 guard_status=5 self_test_status=1
mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_DIR"/*.log "$OUTPUT_DIR/evidence_manifest.txt" "$OUTPUT_DIR/SHA256SUMS.txt"

run_logged() {
  local log_name="$1"; shift
  set +e; "$@" 2>&1 | tee "$OUTPUT_DIR/$log_name"; local status=${PIPESTATUS[0]}; set -e
  (( status == 0 )) || overall_status=1
  return 0
}

if [[ -n "${EXPECTED_BRANCH_NAME:-}" && "$BRANCH" != "$EXPECTED_BRANCH_NAME" ]]; then
  printf 'UNEXPECTED_BRANCH\nEXPECTED_BRANCH=%s\nACTUAL_BRANCH=%s\n' "$EXPECTED_BRANCH_NAME" "$BRANCH"
  overall_status=1
fi

run_logged 01_py_compile.log python3 -m py_compile "$PROJECT_ROOT"/Tests/HybridSplitBig/*.py
run_logged 02_dimension_contract.log python3 -m pytest -q "$PROJECT_ROOT/Tests/HybridSplitBig/test_catchup_full_dimension_contract.py"
run_logged 03_hybrid_split_big.log python3 -m pytest -q "$PROJECT_ROOT/Tests/HybridSplitBig"
run_logged 04_all_tests.log python3 -m pytest -q "$PROJECT_ROOT/Tests"
run_logged 05_big_move_levels_check.log python3 "$PROJECT_ROOT/Tests/big_move_levels_check.py"
run_logged 06_validate_v2_static.log python3 "$PROJECT_ROOT/Tests/validate_v2_static.py"

set +e; check_forbidden_files "$SOURCE_BASE" "$SOURCE_COMMIT" "$OUTPUT_DIR/07_forbidden_files.log"; guard_status=$?; set -e
(( guard_status == 0 )) || overall_status=1
run_logged 09_forbidden_guard_self_tests.log bash "$PROJECT_ROOT/Tests/run_stage_1_2_4_1_source_validation.sh" --self-test-forbidden-guard
grep -q 'SUMMARY|Passed=5|Failed=0' "$OUTPUT_DIR/09_forbidden_guard_self_tests.log" && self_test_status=0 || { self_test_status=1; overall_status=1; }

base_exists=0; source_exists=0
git -C "$REPO_ROOT" cat-file -e "${SOURCE_BASE}^{commit}" 2>/dev/null && base_exists=1
git -C "$REPO_ROOT" cat-file -e "${SOURCE_COMMIT}^{commit}" 2>/dev/null && source_exists=1
{
  printf 'REPOSITORY=%s\nBRANCH=%s\nHEAD=%s\nORIGIN_WORK=%s\n' "$(git -C "$REPO_ROOT" remote get-url origin)" "$BRANCH" "$(git -C "$REPO_ROOT" rev-parse HEAD)" "$ORIGIN_WORK_SHA"
  printf 'SOURCE_BASE=%s\nSOURCE_BASE_EXISTS=%d\nSOURCE_COMMIT=%s\nSOURCE_COMMIT_EXISTS=%d\nCI_COMMIT=%s\n' "$SOURCE_BASE" "$base_exists" "$SOURCE_COMMIT" "$source_exists" "$CI_COMMIT"
  printf 'WORKFLOW_RUN_ID=%s\nWORKFLOW_RUN_ATTEMPT=%s\nGITHUB_EVENT_NAME=%s\nGITHUB_REPOSITORY=%s\n' "${WORKFLOW_RUN_ID_VALUE:-LOCAL}" "${WORKFLOW_RUN_ATTEMPT_VALUE:-LOCAL}" "${GITHUB_EVENT_NAME_VALUE:-LOCAL}" "${GITHUB_REPOSITORY_VALUE:-LOCAL}"
  printf 'CHANGED_FILES_BEGIN\n'; git -C "$REPO_ROOT" diff --name-only "$SOURCE_COMMIT" HEAD; printf 'CHANGED_FILES_END\n'
} 2>&1 | tee "$OUTPUT_DIR/08_git_metadata.log"

cat > "$OUTPUT_DIR/evidence_manifest.txt" <<EOF
STAGE=1.2.4.1
EVIDENCE_STAGE=1.2.4.2.1
REPOSITORY=$(git -C "$REPO_ROOT" remote get-url origin)
BRANCH=$BRANCH
SOURCE_BASE=$SOURCE_BASE
SOURCE_BASE_EXISTS=$base_exists
SOURCE_COMMIT=$SOURCE_COMMIT
SOURCE_COMMIT_EXISTS=$source_exists
CI_COMMIT=$CI_COMMIT
ORIGIN_WORK_SHA=$ORIGIN_WORK_SHA
WORKFLOW_RUN_ID=${WORKFLOW_RUN_ID_VALUE:-LOCAL}
WORKFLOW_RUN_ATTEMPT=${WORKFLOW_RUN_ATTEMPT_VALUE:-LOCAL}
GITHUB_EVENT_NAME=${GITHUB_EVENT_NAME_VALUE:-LOCAL}
GITHUB_REPOSITORY=${GITHUB_REPOSITORY_VALUE:-LOCAL}
UTC_TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
PYTHON_VERSION=$(python3 --version 2>&1)
PYTEST_VERSION=$(python3 -m pytest --version 2>&1 | head -n 1)
OPERATING_SYSTEM=$(uname -a)
CHANGED_FILES=$(git -C "$REPO_ROOT" diff --name-only "$SOURCE_COMMIT" HEAD | paste -sd, -)
TEST_COMMANDS=py_compile;dimension_contract_pytest;HybridSplitBig_pytest;all_project_pytest;big_move_levels_check;validate_v2_static;forbidden_files_guard;forbidden_guard_self_tests
EXIT_STATUS=$overall_status
FORBIDDEN_GUARD_STATUS=$guard_status
SELF_TEST_STATUS=$self_test_status
ARTIFACT_CONTENTS=01_py_compile.log,02_dimension_contract.log,03_hybrid_split_big.log,04_all_tests.log,05_big_move_levels_check.log,06_validate_v2_static.log,07_forbidden_files.log,08_git_metadata.log,09_forbidden_guard_self_tests.log,evidence_manifest.txt,SHA256SUMS.txt
EOF

(
  cd "$OUTPUT_DIR"
  sha256sum 01_py_compile.log 02_dimension_contract.log 03_hybrid_split_big.log 04_all_tests.log 05_big_move_levels_check.log 06_validate_v2_static.log 07_forbidden_files.log 08_git_metadata.log 09_forbidden_guard_self_tests.log evidence_manifest.txt > SHA256SUMS.txt
)
set +e; (cd "$OUTPUT_DIR" && sha256sum -c SHA256SUMS.txt); checksum_status=$?; set -e
(( checksum_status == 0 )) || overall_status=1
if (( overall_status != 0 )); then sed -i 's/^EXIT_STATUS=.*/EXIT_STATUS=1/' "$OUTPUT_DIR/evidence_manifest.txt"; fi
printf 'SOURCE_VALIDATION_SUMMARY|ExitStatus=%d|Evidence=%s\n' "$overall_status" "$OUTPUT_DIR"
exit "$overall_status"
