# https://github.com/cemu-project/Cemu/commit/33bd10b4e0b9c27881fa7d6bf38908791f84d3b2
%global commit 33bd10b4e0b9c27881fa7d6bf38908791f84d3b2
%global commit_date 20221228
%global short_commit %(c=%{commit}; echo ${c:0:7})
%global snapshot %{commit_date}git%{short_commit}

# https://github.com/ocornut/imgui/commit/8a44c31c95c8e0217f6e1fc814cbbbcca4981f14
%global im_name imgui
%global im_url https://github.com/ocornut/%{im_name}
%global im_commit 8a44c31c95c8e0217f6e1fc814cbbbcca4981f14

# https://github.com/Exzap/ZArchive/commit/d2c717730092c7bf8cbb033b12fd4001b7c4d932
%global za_name ZArchive
%global za_url https://github.com/Exzap/%{za_name}
%global za_commit d2c717730092c7bf8cbb033b12fd4001b7c4d932

%global rdns info.cemu.Cemu

%global toolchain clang

Name:           Cemu
Version:        2.0^%{snapshot}
Release:        2%{?dist}
Summary:        Wii U emulator

License:        MPL-2.0
URL:            https://cemu.info

Source0:        https://github.com/cemu-project/%{name}/archive/%{commit}/%{name}-%{commit}.tar.gz
Source1:        https://github.com/ocornut/%{im_name}/archive/%{im_commit}/%{im_name}-%{im_commit}.tar.gz
Source2:        https://github.com/Exzap/%{za_name}/archive/%{za_commit}/%{za_name}-%{za_commit}.tar.gz

# Use fmt in non-header-only mode
# Not applicable to upstream which uses vcpkg fmt
# Patch based on cemu-git Arch package
# <https://aur.archlinux.org/cgit/aur.git/commit/?h=cemu-git&id=af25b06aeeb1c89c09359382ac25266d4bb2859e>
Patch0:         00-Cemu-fmt-not-header-only.patch

# Keep this section in sync with upstream build instructions
# <https://github.com/cemu-project/Cemu/blob/fca7f5dfe4dc6c7293183922c964713b55017fd5/BUILD.md#for-fedora-and-derivatives>
BuildRequires:  clang
BuildRequires:  cmake >= 3.21.1
BuildRequires:  cubeb-devel
BuildRequires:  freeglut-devel
#BuildRequires:  git
BuildRequires:  gtk3-devel
BuildRequires:  kernel-headers
BuildRequires:  libgcrypt-devel
BuildRequires:  libsecret-devel
BuildRequires:  nasm
BuildRequires:  ninja-build
BuildRequires:  perl-core
# Only needed for vcpkg build
#BuildRequires:  systemd-devel
BuildRequires:  zlib-devel

# This section replaces vcpkg
BuildRequires:  SDL2-devel
BuildRequires:  boost-devel
BuildRequires:  fmt-devel >= 9.1
BuildRequires:  glm-devel
BuildRequires:  glslang-devel
BuildRequires:  libcurl-devel
BuildRequires:  libzip-devel
BuildRequires:  libzip-tools
BuildRequires:  libzstd-devel
BuildRequires:  openssl-devel
BuildRequires:  pugixml-devel
BuildRequires:  rapidjson-devel
BuildRequires:  vulkan-headers
BuildRequires:  wxGTK-devel >= 3.2

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

# For the version hash workaround
BuildRequires:  sed

# Workaround for missing glslangConfig.cmake file (1/2)
# Only for F37 Copr build
# Should not be necessary in F38 based on current rawhide build results
# This breaks local builds. You can comment out this BR
# and manually insert the file into the build chroot if using mock.
%if 0%{?fedora} == 37
BuildRequires:  Cemu-glslang-cmake-workaround
%endif

Provides:       cemu = %{version}-%{release}

%description
Cemu is a cross-platform emulator for the Nintendo Wii U game console.
It is written in C/C++, and is able to run most Wii U games and
homebrew in a playable state.

Cemu is actively developed with new features and fixes to increase
compatibility, convenience, and usability.

%prep
%autosetup -n %{name}-%{commit} -p0

# imgui "submodule"
rm -rf dependencies/%{im_name}
tar -xzf %{SOURCE1} -C dependencies
mv dependencies/%{im_name}-%{im_commit} dependencies/%{im_name}

# ZArchive "submodule"
rm -rf dependencies/%{za_name}
tar -xzf %{SOURCE2} -C dependencies
mv dependencies/%{za_name}-%{za_commit} dependencies/%{za_name}

# CMake can't get the hash using git at build time
# because the source tarball doesn't include the .git dir.
sed -i -e 's/${GIT_HASH}/%{snapshot}/' CMakeLists.txt
# Also patch the cli --version
_pattern='versionStr = fmt::format("{}.{}-{}{}", EMULATOR_VERSION_LEAD, EMULATOR_VERSION_MAJOR, EMULATOR_VERSION_MINOR, EMULATOR_VERSION_SUFFIX);'
_replace='versionStr = fmt::format("{}.{}-{}{}", EMULATOR_VERSION_LEAD, EMULATOR_VERSION_MAJOR, "%{snapshot}", EMULATOR_VERSION_SUFFIX);'
sed -i -e "s/${_pattern}/${_replace}/" src/config/LaunchSettings.cpp

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
    -DENABLE_DISCORD_RPC:BOOL=ON \
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
# Set PrefersNonDefaultGPU
# It should benefit the majority of dual-GPU users, but will negatively impact
# a minority whose default GPU is their dGPU instead of iGPU. These users will
# need to override the desktop file to remove/unset the key,
# or run Cemu with the environment variable DRI_PRIME=0.
# Also set a similar KDE-specific key.
# See <https://github.com/ValveSoftware/steam-for-linux/issues/7089>
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    --set-key=PrefersNonDefaultGPU \
    --set-value=true \
    --set-key=X-KDE-RunOnDiscreteGpu \
    --set-value=true \
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
