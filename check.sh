#!/usr/bin/bash

# Check for upstream changes

readonly remote='https://github.com/cemu-project/Cemu.git'

echo 'Latest upstream commit:'
git ls-remote --heads "${remote}"

echo
echo 'Last 5 upstream tags (might be wrong! naively sorted):'
# Assume that the 2nd field is refs/tags/...
# We take the 11th character (expected 'v' after the second '/') to the end of the field
# and sort using version sort (sort -V, whatever that means).
git ls-remote --tags "${remote}" | grep -E 'refs/tags/v2.0-[[:digit:]]+' | LC_COLLATE=C sort -k2.11bV | tail -5

echo
echo 'Current packaged commit:'
grep -Po '^%global commit +\K.+' Cemu.spec
