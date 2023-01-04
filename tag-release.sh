#!/usr/bin/bash

# Create git tag with normalised version-release

readonly specfile='Cemu.spec'

# shellcheck disable=SC2155
readonly vr="$(rpmspec -q --qf '%{version}-%{release}\n' "${specfile}" | head -1)"
readonly vr_nodist="${vr%.fc*}"

# Normalises the following to - (hyphen-minus):
#   space ~ ^ : ? *
# shellcheck disable=SC2155
readonly git_tag="$(sed -E -e 's@[ ~^:?*]@-@g' <<<"${vr_nodist}")"

printf '%-25s:  %s\n' \
	'Version-Release (no dist)' "${vr_nodist}" \
	'Normalised for git' "${git_tag}"

echo 'Tagging HEAD...'
if git tag "${git_tag}"; then
	# Copy to clipboard
	xclip -selection clipboard -rmlastnl <<<"${git_tag}"
	echo 'Copied tag to clipboard.'
	echo 'Pushing the tag will trigger a rebuild on Copr.'
fi
