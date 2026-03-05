#!/usr/bin/env bash
set -e

FILE="$1"

if [ -z "$FILE" ]; then
  echo "Usage: publish.sh <markdown file>"
  exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
STAMP_SCRIPT="$REPO_ROOT/.tools/stamp.sh"

echo "Signing + timestamping..."
"$STAMP_SCRIPT" "$FILE"

echo "Adding files to git..."
git add "$FILE"
git add _timestamps/

echo "Committing..."
git commit -m "publish: $(basename "$FILE")"

echo "Pushing..."
git push

echo "Done."
