#!/usr/bin/bash

# Create git tag with normalised version-release

readonly specfile='Cemu.spec'

# shellcheck disable=SC2155
readonly vr="$(rpmspec -q --qf '%{version}-%{release}\n' "${specfile}" | head -1)"
readonly vr_nodist="${vr%.fc*}"

# Normalises the following to - (hyphen-minus):
#   space ~ ^ : ? *
# shellcheck disable=SC2155
readonly vr_nodist_norm="$(sed -E -e 's@[ ~^:?*]@-@g' <<<"${vr_nodist}")"

printf '%-25s:  %s\n' \
	'Version-Release (no dist)' "${vr_nodist}" \
	'Normalised for git' "${vr_nodist_norm}"

echo 'Tagging HEAD...'
if git tag "${vr_nodist_norm}"; then
	# Copy to clipboard
	xclip -selection clipboard -rmlastnl <<<"${vr_nodist_norm}"
	echo 'Copied to clipboard. Use it for GitHub release title and filenames.'
	echo 'Remember to git push the tag too.'
fi
