# Cemu rpm package for Fedora

[![Copr build status badge](https://copr.fedorainfracloud.org/coprs/jn64/Cemu/package/Cemu/status_image/last_build.png)](https://copr.fedorainfracloud.org/coprs/jn64/Cemu/)

[Cemu](https://cemu.info/) is a Wii U emulator.
This is an rpm package of Cemu for Fedora Linux.

## For users

### Install

```sh
sudo dnf copr enable jn64/Cemu
sudo dnf install Cemu
```

#### Uninstall

```sh
sudo dnf remove Cemu
sudo dnf copr remove jn64/Cemu
```

### Usage

On first run, you will see a _Getting started_ dialog:

- mlc01 path: Recommend leaving this unset
- Game paths: Set this to the folder where you store your game dumps
- Graphic packs: Click the button to download community graphic packs

You may also need to enable your audio device in Cemu:

- Open the menu _Options > General settings_
- Click on the _Audio_ tab
- Under _TV > Device_, choose your audio device e.g. _Built-in Audio Analog Stereo_, and set the volume

### File locations

- Your user data will be in `~/.local/share/Cemu` (or `$XDG_DATA_HOME/Cemu`)
- Your user config will be in `~/.config/Cemu` (or `$XDG_CONFIG_HOME/Cemu`)
- Your shader cache will be in `~/.cache/Cemu` (or `$XDG_CACHE_HOME/Cemu`)

### Reporting issues

[Report issues with this package here](https://github.com/jn64/Cemu-rpm/issues).

Please include the package version in your report. You can obtain it by running:

```shell
$ rpm -q Cemu
```

Only [report upstream](https://github.com/cemu-project/Cemu/issues) if you can reproduce the issue with upstream builds.

## For packagers

Automatic rebuilds on Copr are triggered via webhook on branch/tag creation.
I've set the Copr package's committish to `main` so only tags on main should
trigger it.

Planning to only package stable releases once Cemu reaches 2.1. Switch to rpmautospec as well.

## License

Cemu is [MPL-2.0](https://spdx.org/licenses/MPL-2.0.html)

The spec file and any original documents in this repo are [0BSD](https://spdx.org/licenses/0BSD.html)

Patches to Cemu source code are MPL-2.0 or the license of the original file

## Links

- [Cemu homepage](https://cemu.info/)
- [Upstream repo](https://github.com/cemu-project/Cemu)
- [Game compatibility](https://compat.cemu.info/)
- [Unofficial Cemu user guide](https://cemu.cfw.guide/)
