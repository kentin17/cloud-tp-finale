#!/usr/bin/env bash
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
BUILD="$HERE/build"

rm -rf "$BUILD"
mkdir -p "$BUILD"
cp "$HERE/handler.py" "$BUILD/"
pip3 install --quiet --target "$BUILD" \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.11 \
  --only-binary=:all: \
  -r "$HERE/requirements.txt"
echo "Build lambda pret dans $BUILD"
