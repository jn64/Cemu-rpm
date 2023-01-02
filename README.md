# Cemu rpm package for Fedora

Built packages are [available on Copr jn64/Cemu](https://copr.fedorainfracloud.org/coprs/jn64/Cemu/).

Currently only Fedora 37 builds are available. F36 is not supported due to older libs.

## For users

### Installation

```shell
# dnf copr enable jn64/Cemu
# dnf install Cemu
```

### Cemu options

This Cemu package is built with these options:

- Non-portable mode
  - Cemu's data files are installed to `/usr/share/Cemu`
  - Your user data will be in `~/.local/share/Cemu` (or `$XDG_DATA_HOME/Cemu`)
  - Your user config will be in `~/.config/Cemu` (or `$XDG_CONFIG_HOME/Cemu`)
  - Your shader cache will be in `~/.cache/Cemu` (or `$XDG_CACHE_HOME/Cemu`)
- No vcpkg; uses Fedora-packaged libraries where possible

Everything else *should* be the same as upstream builds, or it's a bug with the package.

### Issue reporting

If you're not sure, report it here.

If Cemu doesn't start, run it from terminal and report it here.

Only report upstream if you confirm the bug with upstream build (AppImage) or by building it yourself.

## For packagers

TODO: document glslang workaround for Copr. Breaks local builds.

## License

Cemu is [MPL-2.0](https://spdx.org/licenses/MPL-2.0.html)

The spec file and any original documents in this repo are [0BSD](https://spdx.org/licenses/0BSD.html)

Patches to Cemu source code are MPL-2.0 or the license of the original file
