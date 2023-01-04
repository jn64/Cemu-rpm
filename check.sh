#!/usr/bin/bash

# Check for upstream changes

echo 'Latest upstream commit:'
git ls-remote --heads https://github.com/cemu-project/Cemu.git

echo 'Current packaged commit:'
grep -Po '^%global commit \K.+' Cemu.spec
