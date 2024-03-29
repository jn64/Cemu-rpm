# Build with clang by default (preferred by upstream)
# Use `--with toolchain_gcc` to build with gcc
%bcond toolchain_gcc 0
# Note: Copr builds will use gcc on F38 for now as
# clang 16 builds crash with multi-core recompiler.
# <https://github.com/cemu-project/Cemu/issues/781>

%if %{with toolchain_gcc}
%global toolchain gcc
%else
%global toolchain clang
%endif

# Build with Discord RPC support by default
# Use `--without discord_rpc` to disable
%bcond discord_rpc 1

# Build with Wayland support by default
# Use `--without wayland` to disable
%bcond wayland 1

# Build with GameMode support by default
# Use `--without gamemode` to disable
%bcond gamemode 1

# https://github.com/cemu-project/Cemu/releases
%global commit        f1c200a01675714e51548137f2365ab2a1a9977b
%global commit_date   20230708
%global short_commit  %(c=%{commit}; echo ${c:0:7})
%global snapshot      %{commit_date}git%{short_commit}

# https://github.com/ocornut/imgui/commit/8a44c31c95c8e0217f6e1fc814cbbbcca4981f14
%global im_name       imgui
%global im_url        https://github.com/ocornut/%{im_name}
%global im_commit     f65bcf481ab34cd07d3909aab1479f409fa79f2f
%global im_date       20230323
%global im_short      %(c=%{im_commit}; echo ${c:0:7})
%global im_snapshot   %{im_date}git%{im_short}

# https://github.com/Exzap/ZArchive/commit/d2c717730092c7bf8cbb033b12fd4001b7c4d932
%global za_name       ZArchive
%global za_url        https://github.com/Exzap/%{za_name}
%global za_commit     d2c717730092c7bf8cbb033b12fd4001b7c4d932

%global rdns info.cemu.Cemu

Name:           Cemu
Version:        2.0^%{snapshot}
Release:        1%{?dist}
Summary:        A Nintendo Wii U emulator
License:        MPL-2.0
URL:            https://cemu.info

Source0:        https://github.com/cemu-project/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:        https://github.com/ocornut/%{im_name}/archive/%{im_commit}/%{im_name}-%{im_commit}.tar.gz
Source2:        https://github.com/Exzap/%{za_name}/archive/%{za_commit}/%{za_name}-%{za_commit}.tar.gz

# Use fmt in non-header-only mode
# Not applicable to upstream which uses vcpkg fmt
Patch0:         0001-Use-fmt-in-non-header-only-mode.patch
# Disable auto-update checkboxes and menu item
# Not applicable to upstream
Patch1:         0002-Disable-auto-update-checkboxes-and-menu-item.patch

# Keep this section in sync with upstream build instructions
# <https://github.com/cemu-project/Cemu/blob/1cf72265cd31a15a8c6afce140463dac9917b9fb/BUILD.md#for-fedora-and-derivatives>
%if %{with toolchain_gcc}
BuildRequires:  gcc gcc-c++
%else
BuildRequires:  clang
%endif
BuildRequires:  cmake >= 3.21.1
#BuildRequires:  git
BuildRequires:  kernel-headers
BuildRequires:  nasm
BuildRequires:  ninja-build
BuildRequires:  perl
# Only needed for vcpkg's wxWidgets <https://github.com/cemu-project/Cemu/issues/24>
#BuildRequires:  systemd-devel
BuildRequires:  cmake(cubeb)
BuildRequires:  pkgconfig(glut)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(libgcrypt)
BuildRequires:  pkgconfig(libsecret-1)
BuildRequires:  pkgconfig(zlib)

# This section replaces vcpkg / other bundled libs
BuildRequires:  boost-devel
BuildRequires:  glslang-devel
BuildRequires:  libzip-tools
BuildRequires:  vulkan-headers
BuildRequires:  wxGTK-devel >= 3.2
BuildRequires:  cmake(glm)
BuildRequires:  pkgconfig(fmt) >= 9.1
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  pkgconfig(libzip)
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(pugixml)
BuildRequires:  pkgconfig(RapidJSON)
BuildRequires:  pkgconfig(sdl2)
%if %{with wayland}
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-protocols)
%endif

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
BuildRequires:  sed

# Workaround for missing glslangConfig.cmake file (1/2)
# Only for F37 Copr build
# This breaks local builds. You can comment out this BR
# and manually insert the file into the build chroot if using mock.
%if 0%{?fedora} == 37
BuildRequires:  Cemu-glslang-cmake-workaround
%endif

%if %{with gamemode}
Recommends:     gamemode
%endif

Provides:       cemu = %{version}-%{release}

# Bundled libs (all not available in Fedora)
Provides:       bundled(ZArchive) = 0.1.2
# 1.89.5 WIP
Provides:       bundled(imgui) = 1.89.5~%{im_snapshot}
%if %{with discord_rpc}
# <https://github.com/discord/discord-rpc/commit/963aa9f3e5ce81a4682c6ca3d136cddda614db33>
Provides:       bundled(discord-rpc) = 3.4.0^20200921git963aa9f
%endif
# ih264d from Android Open Source Project, modified by Cemu
# <https://github.com/cemu-project/Cemu/tree/2c81d240a5b065d8cf4c555754c4bfeaf42c826c/dependencies/ih264d>
Provides:       bundled(ih264d) = 0^20221207git2c81d24


%description
Cemu is a cross-platform emulator for the Nintendo Wii U game console.
It is able to run most Wii U games and homebrew in a playable state.

%prep
%autosetup -n %{name}-%{commit} -p1

# imgui "submodule"
rm -rf dependencies/%{im_name}
tar -xzf %{SOURCE1} -C dependencies
mv dependencies/%{im_name}-%{im_commit} dependencies/%{im_name}

# ZArchive "submodule"
rm -rf dependencies/%{za_name}
tar -xzf %{SOURCE2} -C dependencies
mv dependencies/%{za_name}-%{za_commit} dependencies/%{za_name}

# Remove unused bundled libs
rm -rf dependencies/{DirectX_2010,Vulkan-Headers,cubeb,vcpkg,vcpkg_overlay_ports,vcpkg_overlay_ports_linux}
%if %{without discord_rpc}
rm -rf dependencies/discord-rpc
%endif
%if %{without gamemode}
rm -rf dependencies/gamemode
%endif

# Set Cemu version to the package snapshot version
# CMake can't get the hash using git at build time
# because the source tarball doesn't include the .git dir.
sed -i -e 's/${GIT_HASH}/%{snapshot}/' CMakeLists.txt
# Also patch the cli --version
_pattern='versionStr = fmt::format("{}.{}-{}{}", EMULATOR_VERSION_LEAD, EMULATOR_VERSION_MAJOR, EMULATOR_VERSION_MINOR, EMULATOR_VERSION_SUFFIX);'
_replace='versionStr = fmt::format("{}.{}-{}{}", EMULATOR_VERSION_LEAD, EMULATOR_VERSION_MAJOR, "%{snapshot}", EMULATOR_VERSION_SUFFIX);'
sed -i -e "s/${_pattern}/${_replace}/" src/config/LaunchSettings.cpp

# Fix game list icon width
# <https://aur.archlinux.org/cgit/aur.git/commit/PKGBUILD?h=cemu&id=88db93c8671856964b35308046bf015ee3f7712a>
sed -i -e '/InsertColumn/s/kListIconWidth/&+8/;/SetColumnWidth/s/last_col_width/&-1/' src/gui/components/wxGameList.cpp

%build
# Workaround for missing glslangConfig.cmake file (2/2)
%if 0%{?fedora} == 37
glslang_DIR=%{_libdir}/cmake
export glslang_DIR
%endif

# Fix building as PIE
# Got a hint from <https://github.com/Tatsh/tatsh-overlay/issues/168#issuecomment-1328259491>
%global optflags %{optflags} -fPIC
%global build_ldflags %{build_ldflags} -pie

# BUILD_SHARED_LIBS=OFF is to fix this error:
#    At least one of these targets is not a STATIC_LIBRARY. Cyclic dependencies are allowed only among static libraries.
%cmake \
    -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo \
    -DENABLE_VCPKG:BOOL=OFF \
    -DENABLE_WAYLAND:BOOL=%{?with_wayland:ON}%{!?with_wayland:OFF} \
    -DENABLE_DISCORD_RPC:BOOL=%{?with_discord_rpc:ON}%{!?with_discord_rpc:OFF} \
    -DENABLE_FERAL_GAMEMODE:BOOL=%{?with_gamemode:ON}%{!?with_gamemode:OFF} \
    -DEXPERIMENTAL_VERSION:STRING=999999 \
    -DPORTABLE:BOOL=OFF \
    -DBUILD_SHARED_LIBS:BOOL=OFF

%cmake_build

%install
# The binary is suffixed with build type in lowercase, i.e.
# if CMAKE_BUILD_TYPE=Release, then bin/Cemu_release
# if CMAKE_BUILD_TYPE=RelWithDebInfo, then bin/Cemu_relwithdebinfo
install -Dpm 0755 bin/%{name}_relwithdebinfo %{buildroot}%{_bindir}/%{name}

# Install bin/gameProfiles and bin/resources to /usr/share/Cemu
# Don't install bin/shaderCache as it's unused in non-portable mode
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -rp -t %{buildroot}%{_datadir}/%{name} bin/gameProfiles bin/resources

# Desktop-related files
install -Dpm 0644 -t %{buildroot}%{_datadir}/icons/hicolor/128x128/apps dist/linux/%{rdns}.png
install -Dpm 0644 -t %{buildroot}%{_metainfodir} dist/linux/%{rdns}.metainfo.xml
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    dist/linux/%{rdns}.desktop

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{rdns}.metainfo.xml

%files
%license LICENSE.txt
%doc README.md bin/shaderCache/info.txt
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{rdns}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{rdns}.png
%{_metainfodir}/%{rdns}.metainfo.xml

%changelog
* Sun Jul 09 2023 Justin Koh <j@ustink.org> - 2.0^20230708gitf1c200a-1
- Update to f1c200a / 2.0-44 (Experimental)

* Fri Jul 07 2023 Justin Koh <j@ustink.org> - 2.0^20230706gitea86c77-1
- Update to ea86c77 / 2.0-43 (Experimental)

* Sun Jun 25 2023 Justin Koh <j@ustink.org> - 2.0^20230625git9499870-1
- Update to 9499870 / 2.0-42 (Experimental)

* Sat Jun 17 2023 Justin Koh <j@ustink.org> - 2.0^20230617gitfd3b5b7-1
- Update to fd3b5b7 / 2.0-41 (Experimental)

* Fri Jun 16 2023 Justin Koh <j@ustink.org> - 2.0^20230615git633e5c0-1
- Update to 633e5c0 / 2.0-40 (Experimental)

* Sun May 28 2023 Justin Koh <j@ustink.org> - 2.0^20230528git4ae5b4f-2
- Add BRs for wayland-{client,scanner,protocols}

* Sun May 28 2023 Justin Koh <j@ustink.org> - 2.0^20230528git4ae5b4f-1
- Update to 4ae5b4f - New logging system, Wayland viewporter

* Thu May 11 2023 Justin Koh <j@ustink.org> - 2.0^20230511giteda4cf4-1
- Update to eda4cf4 / 2.0-39 (Experimental) - updated translations

* Thu May 11 2023 Justin Koh <j@ustink.org> - 2.0^20230511git1bcdb35-1
- Update to 1bcdb35 / 2.0-38 (Experimental) - adds GameMode support

* Thu May 11 2023 Justin Koh <j@ustink.org> - 2.0^20230510gitb74ae21-1
- Update to b74ae21 / 2.0-37 (Experimental)

* Wed May 03 2023 Justin Koh <j@ustink.org> - 2.0^20230426gitd56bc80-1
- Update to d56bc80
- Add bconds for toolchain, discord

* Thu Apr 20 2023 Justin Koh <j@ustink.org> - 2.0^20230420gitf48ad6a-1
- Update to f48ad6a / 2.0-36 (Experimental)

* Wed Apr 19 2023 Justin Koh <j@ustink.org> - 2.0^20230417gite3e167b-2
- Use gcc on F38. See <https://github.com/jn64/Cemu-rpm/issues/13>

* Wed Apr 19 2023 Justin Koh <j@ustink.org> - 2.0^20230417gite3e167b-1
- Update to e3e167b / 2.0-34 (Experimental)
- Patch to fix icon column width

* Sat Apr 15 2023 Justin Koh <j@ustink.org> - 2.0^20230415gita6e9481-1
- Update to a6e9481 / 2.0-33 (Experimental)

* Sat Apr 01 2023 Justin Koh <j@ustink.org> - 2.0^20230330gitcb9570e-1
- Update to cb9570e
- Fixes "Disable screen saver" option (#726)

* Wed Mar 29 2023 Justin Koh <j@ustink.org> - 2.0^20230329gitaa63a6a-1
- Update to aa63a6a / 2.0-30 (Experimental)

* Wed Mar 15 2023 Justin Koh <j@ustink.org> - 2.0^20230311git3acdd47-1
- Update to 3acdd47 / 2.0-29 (Experimental)

* Sat Feb 25 2023 Justin Koh <j@ustink.org> - 2.0^20230224git4c697d3-1
- Update to 4c697d3 - Add setting to inhibit screensaver

* Thu Feb 23 2023 Justin Koh <j@ustink.org> - 2.0^20230222git80b1c50-1
- Update to 80b1c50 / 2.0-28 (Experimental)

* Sun Feb 19 2023 Justin Koh <j@ustink.org> - 2.0^20230219git6d75776-1
- Update to 6d75776
- Fixes #666 - Clicking main window hides shader progress dialog

* Sat Feb 18 2023 Justin Koh <j@ustink.org> - 2.0^20230218gitcbb79fd-1
- Update to cbb79fd / 2.0-27 (Experimental)

* Tue Jan 31 2023 Justin Koh <j@ustink.org> - 2.0^20230129gitf3ff919-1
- Update to f3ff919

* Sat Jan 28 2023 Justin Koh <j@ustink.org> - 2.0^20230127git9a4f945-1
- Update to 9a4f945 / 2.0-26 (Experimental)
- Improvements to DS VC, Unity-based games, BotW performance (#631)

* Fri Jan 13 2023 Justin Koh <j@ustink.org> - 2.0^20230113git9d55f46-1
- Update to 9d55f46
- Declare bundled libs
- Patch to disable auto-update (which was non-functional)

* Wed Jan 11 2023 Justin Koh <j@ustink.org> - 2.0^20230106git1cf7226-1
- Update to 1cf7226
- Patch to show package version in cli --version
- Use pkgconfig/cmake provides where possible

* Tue Jan 03 2023 Justin Koh <j@ustink.org> - 2.0^20221228git33bd10b-2
- Add conditionals so same spec file can be used for F37 and rawhide/F38

* Tue Jan 03 2023 Justin Koh <j@ustink.org> - 2.0^20221228git33bd10b-1
- Update to 33bd10b
- Build with Discord RPC (can be toggled in Cemu's General Settings)
- Package glslang workaround so this can be built on Copr

* Tue Dec 27 2022 Justin Koh <j@ustink.org> - 2.0^20221226git0c6f18a-1
- Update to 0c6f18a

* Thu Dec 15 2022 Justin Koh <j@ustink.org> - 2.0^20221215gitfcab8f8-1
- Update to fcab8f8

* Mon Dec 12 2022 Justin Koh <j@ustink.org> - 2.0^20221212gitc78b3da-1
- Update to c78b3da
- Fix building as PIE

* Sat Dec 10 2022 Justin Koh <j@ustink.org> - 2.0^20221209git4491560-1
- Switch to snapshot versioning
