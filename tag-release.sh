#!/usr/bin/bash

# Create git tag with normalised version-release

readonly specfile='Cemu.spec'

readonly version_release="$(rpmspec -q --qf '%{version}-%{release}\n' "${specfile}" | head -1)"
readonly without_dist="${version_release%.fc*}"

# Normalises the following to - (hyphen-minus):
#   space ~ ^ : ? *
readonly normalised="$(sed -E -e 's@[ ~^:?*]@-@g' <<<"${without_dist}")"

printf 'Tagging HEAD as:  %s\n' "${normalised}"
git tag "${normalised}" &&
echo 'Use this for GitHub release title, filename etc.'
