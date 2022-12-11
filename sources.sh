#!/usr/bin/bash

# ./sources.sh
# Download all SourceN URLs from the spec file

readonly specfile='Cemu.spec'

# The sed command prints only SourceN values starting with http or ftp
wget -nc $(rpmspec --parse "${specfile}" | sed -En "s/^Source[[:digit:]]+:\s*(http|ftp)/\1/p")
