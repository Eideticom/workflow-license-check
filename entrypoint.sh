#!/usr/bin/env bash
# SPDX-License-Identifer: Apache-2.0
# Copyright (c) 2022, Eidetic Communications Inc.

set -e

echo "Start..."
echo "Workflow: $GITHUB_WORKFLOW"
echo "Action: $GITHUB_ACTION"
echo "Actor: $GITHUB_ACTOR"
echo "Repository: $GITHUB_REPOSITORY"
echo "Event-name: $GITHUB_EVENT_NAME"
echo "Event-path: $GITHUB_EVENT_PATH"
echo "Workspace: $GITHUB_WORKSPACE"
echo "SHA: $GITHUB_SHA"
echo "REF: $GITHUB_REF"
echo "HEAD-REF: $GITHUB_HEAD_REF"
echo "BASE-REF: $GITHUB_BASE_REF"
pwd

# Get PR number
PR=${GITHUB_REF#"refs/pull/"}
PRNUM=${PR%"/merge"}

# Github REST API endpoints
BODY_URL="https://api.github.com/repos/${GITHUB_REPOSITORY}/issues/${PRNUM}/comments"

git config --global --add safe.directory $(pwd)

git fetch --no-tags --progress --no-recurse-submodules \
	--depth=1 origin "$GITHUB_BASE_REF"

LOG="spdx_review.log"
REVIEW_ARGS=(-l "$LOG" -g "origin/$GITHUB_BASE_REF" "origin/$GITHUB_HEAD_REF")

echo "Run spdx_review.py" "${REVIEW_ARGS[@]}"
python3 /spdx_review.py "${REVIEW_ARGS[@]}" || EXIT_CODE=$?
if [ "$EXIT_CODE" != "" -a "$EXIT_CODE" != 1 ]; then
	echo "FAILURE ($EXIT_CODE)"
	exit 1
fi

if [[ -s "$LOG" ]]; then
    SPDX_RESULT=$(cat "$LOG")
    fmt_body="{ \"body\": \"${SPDX_RESULT//$'\n'/\\n}\" }"

    curl "${BODY_URL}" -s \
        -H "Authorization: token ${GITHUB_TOKEN}" \
        -H "Content-Type: application/json" \
        -X POST --data "$fmt_body"
fi
