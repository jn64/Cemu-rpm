# Cemu rpm package for Fedora

Summary:

- This is a working package of [Cemu](https://github.com/cemu-project/Cemu) for Fedora 37
- The build process involves fucking with the mock chroot to patch one file in `/usr` (???)

What this means:

- You can download and use the rpm (at your own risk!)
- You can build the rpm yourself from the spec file
- I cannot proceed to next step of trying to build on Copr until I figure this out

## Cemu build options

This Cemu package is built with these options (meaning they are set at compile time, and can't be changed by checking a box when you use Cemu):

- Non-portable mode
  - Cemu's data files are installed to `/usr/share/Cemu`
  - Your user data will be in `~/.local/share/Cemu` (or `$XDG_DATA_HOME/Cemu`)
  - Your user config will be in `~/.config/Cemu` (or `$XDG_CONFIG_HOME/Cemu`)
  - Your shader cache will be in `~/.cache/Cemu` (or `$XDG_CACHE_HOME/Cemu`)
- No Discord Rich Presence
- No vcpkg; uses your Fedora system libraries where possible

Everything else *should* be the same as upstream builds, or it's a bug with the package.

## Building from spec file

If you've never used any RPM packaging tools like `rpmbuild`, `mock`, or `fedpkg`, I strongly recommend completing Fedora's [Packaging Tutorial: GNU Hello](https://docs.fedoraproject.org/en-US/package-maintainers/Packaging_Tutorial_GNU_Hello/) first.

### Quick start

```shell
$ git clone https://github.com/jn64/Cemu-rpm.git
$ cd Cemu-rpm
$ ./sources.sh
$ fedpkg --name Cemu --release f37 lint
$ mock -r fedora-37-x86_64 --copyin glslangConfig.cmake /usr/lib64/cmake
$ fedpkg --name Cemu --release f37 mockbuild --no-clean-all
$ fedpkg --name Cemu --release f37 lint
```

### Notes

The building is done with `mock` via `fedpkg mockbuild`, meaning the build dependencies are installed in the mock chroot, not in your normal environment.

`mock --copyin ...` copies the file into the chroot, i.e. to `/var/lib/mock/fedora-37-x86_64/root/usr/lib64/cmake`. For details on this file, see [KhronosGroup/glslang#2570](https://github.com/KhronosGroup/glslang/issues/2570#issue-831123061). I don't know CMake and I'm not able to solve this issue by patching Cemu, so this is an ugly workaround.

Using `fedpkg mockbuild --no-clean-all` allows you to repeat the build without re-initialising the chroot (installing ~700 packages...), in case of any errors. If there are no issues with the build, you can change it to `--no-clean`, which will keep the file inserted in the previous step, but clean up (delete) the chroot after the mockbuild is done.

`fedpkg lint` also lints the build results, unlike using `rpmlint` directly.

#### Other ways to build Cemu

If you prefer, you can build Cemu from source on Fedora in a more manual, but perhaps easier to understand way:

- [Using toolbox (F36+)](https://github.com/cemu-project/Cemu/issues/266#issuecomment-1271873601)
- [Using toolbox, non-vcpkg (F37+)](https://github.com/cemu-project/Cemu/issues/266#issuecomment-1336935816)

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
