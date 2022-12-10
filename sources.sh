#!/usr/bin/bash

# ./sources.sh
# Download all SourceN URLs from the spec file
#
# Does not check for URL validity (if you have any Sources that are not URLs)

readonly specfile='Cemu.spec'

wget -nc $(rpmspec --parse "${specfile}" | sed -nE "s/^Source[[:digit:]]+:\s*//p")
