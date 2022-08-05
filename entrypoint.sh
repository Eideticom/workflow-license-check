#!/usr/bin/env bash

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

git fetch --no-tags --progress --no-recurse-submodules --depth=1 origin "$GITHUB_BASE_REF" 

echo "Run spdx_review.py using args - Workspace: $GITHUB_WORKSPACE before: HEAD-REF: $GITHUB_HEAD_REF after: BASE-REF: $GITHUB_BASE_REF"
python3 /spdx_review.py -g "origin/$GITHUB_BASE_REF" "origin/$GITHUB_HEAD_REF"

