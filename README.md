# Cemu rpm package for Fedora

[Cemu](https://cemu.info/) is a Wii U emulator.
This is an rpm package of Cemu for Fedora Linux.

## For users

[Built packages are available on Copr jn64/Cemu](https://copr.fedorainfracloud.org/coprs/jn64/Cemu/).

Only Fedora 37 builds are available currently. F36 is not supported due to older libs.

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

### Reporting issues

[Report issues with this package here](https://github.com/jn64/Cemu-rpm/issues).

Please include the package version in your report. You can obtain it by running:

```shell
$ dnf -qC rq --installed --nvr Cemu
```

Only [report upstream](https://github.com/cemu-project/Cemu/issues) if you can reproduce the issue with upstream builds (AppImage) or by building it yourself.

## For packagers

TODO: document glslang workaround for Copr. Breaks local builds. See spec file

Automatic rebuilds on Copr are triggered via webhook on branch/tag creation

## License

Cemu is [MPL-2.0](https://spdx.org/licenses/MPL-2.0.html)

The spec file and any original documents in this repo are [0BSD](https://spdx.org/licenses/0BSD.html)

Patches to Cemu source code are MPL-2.0 or the license of the original file

## Links

- [Cemu homepage](https://cemu.info/)
- [Upstream repo](https://github.com/cemu-project/Cemu)
- [Game compatibility](https://compat.cemu.info/)
- [Unofficial Cemu user guide](https://cemu.cfw.guide/)
