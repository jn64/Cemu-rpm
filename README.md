# Cemu rpm package for Fedora

Summary:

- This is a working package of [Cemu](https://github.com/cemu-project/Cemu) for Fedora 37
- The process to build it involves fucking with the mock chroot to patch one file in `/usr` (???)

What this means:

- You can download and use the rpm (at your own risk!)
- You can build the rpm yourself from the spec file
- I cannot proceed to next step of trying to build on Copr until I figure this out

## Build options

This Cemu package is built with these options:

- Portable mode **disabled**
  - Cemu's data files are installed to `/usr/share/Cemu`
  - Your user data will be in `~/.local/share/Cemu` (or `$XDG_DATA_HOME/Cemu`)
  - Your user config will be in `~/.config/Cemu` (or `$XDG_CONFIG_HOME/Cemu`)
  - Your shader cache will be in `~/.cache/Cemu` (or `$XDG_CACHE_HOME/Cemu`)
- Discord Rich Presence **disabled**

## Building from spec file

If you've never used any rpm packaging tools like `rpmbuild`, `mock`, or `fedpkg`, I strongly recommend you do Fedora's [Packaging Tutorial: GNU Hello](https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/) first.

I'm using `fedpkg` because it's a convenient wrapper. Only using it for offline `mockbuild` and not interacting with Fedora infrastructure in any way.

```shell
$ git clone https://github.com/jn64/Cemu-rpm.git
$ cd Cemu-rpm
$ fedpkg --name Cemu --release f37 lint #STEP0
$ mock -r fedora-37-x86_64 --copyin glslangConfig.cmake /usr/lib64/cmake #STEP1
$ fedpkg --name Cemu --release f37 mockbuild --no-clean-all #STEP2
$ fedpkg --name Cemu --release f37 lint #STEP3
```

### STEP0

Lint the spec file to check for errors

### STEP1

Insert the glslangConfig.cmake file into the chroot

### STEP2

Build.

Use `--no-clean-all` (which means `--no-clean` and `--no-cleanup-after`) in case build fails, so you can troubleshoot issues without re-initialising the chroot every time (installing ~700 packages...).

You can repeat this step multiple times. Once you've sorted out all issues, you can change to `--no-clean` so it won't clean before, but it *will* clean (delete) the chroot after building (if you don't want to poke around in it).

buildroot is `/var/lib/mock/fedora-37-x86_64/root/builddir/build/BUILDROOT/Cemu-...`

### STEP3

Lint again, this time it will check the packages as well. Some warnings are expected.

## Issue reporting

If you're not sure, report it here.

If Cemu doesn't start, run it from terminal and report it here.

Only report upstream if you confirm the bug with upstream build (AppImage) or by building it yourself.

## I don't care, just give me rpm

Download the x86_64 rpm from [releases](https://github.com/jn64/Cemu-rpm/releases).

Inspect it first:

```shell
$ rpm -qpi /path/to/rpm
$ rpm -qplv /path/to/rpm
$ rpm -qpRv /path/to/rpm
```

and install with `dnf` (not `rpm`):

```shell
$ sudo dnf install /path/to/rpm
```

Uninstall by package name (not filename):

```shell
$ sudo dnf remove Cemu
```

## License

Cemu is [MPL-2.0](https://spdx.org/licenses/MPL-2.0.html)

The spec file and any original documents in this repo are [0BSD](https://spdx.org/licenses/0BSD.html)

Patches to Cemu source code are MPL-2.0 or the license of the original file
