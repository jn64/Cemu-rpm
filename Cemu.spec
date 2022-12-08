# https://github.com/cemu-project/Cemu/commit/fca7f5dfe4dc6c7293183922c964713b55017fd5
%global forgeurl https://github.com/cemu-project/Cemu
%global commit fca7f5dfe4dc6c7293183922c964713b55017fd5
%forgemeta

# https://github.com/ocornut/imgui/commit/8a44c31c95c8e0217f6e1fc814cbbbcca4981f14
%global im_name imgui
%global im_url https://github.com/ocornut/%{im_name}
%global im_commit 8a44c31c95c8e0217f6e1fc814cbbbcca4981f14

# https://github.com/Exzap/ZArchive/commit/d2c717730092c7bf8cbb033b12fd4001b7c4d932
%global za_name ZArchive
%global za_url https://github.com/Exzap/%{za_name}
%global za_commit d2c717730092c7bf8cbb033b12fd4001b7c4d932

%global toolchain clang

%global rdns info.cemu.Cemu

Name:           Cemu
Version:        2.0
Release:        2%{?dist}
Summary:        Wii U emulator

License:        MPL-2.0
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://github.com/ocornut/%{im_name}/archive/%{im_commit}/%{im_name}-%{im_commit}.tar.gz
Source2:        https://github.com/Exzap/%{za_name}/archive/%{za_commit}/%{za_name}-%{za_commit}.tar.gz
# Use fmt in non-header-only mode
# Not applicable to upstream which uses vcpkg fmt
# Patch based on cemu-git Arch package
# <https://aur.archlinux.org/cgit/aur.git/commit/?h=cemu-git&id=af25b06aeeb1c89c09359382ac25266d4bb2859e>
Patch0:         00-Cemu-fmt.patch
Patch1:         01-Cemu-no-strip-debug.patch

# Keep this section in sync with upstream build instructions
# <https://github.com/cemu-project/Cemu/blob/fca7f5dfe4dc6c7293183922c964713b55017fd5/BUILD.md#for-fedora-and-derivatives>
BuildRequires:  clang
BuildRequires:  cmake
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

# This section replaces vcpkg used by upstream
BuildRequires:  SDL2-devel
BuildRequires:  boost-devel
BuildRequires:  fmt-devel
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
BuildRequires:  wxGTK-devel

BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       hicolor-icon-theme
Requires:       shared-mime-info

Provides:       cemu = %{version}-%{release}

%description
Cemu is a cross-platform emulator for the Nintendo Wii U game console.
It is written in C/C++, and is able to run most Wii U games and
homebrew in a playable state.

Cemu is actively developed with new features and fixes to increase
compatibility, convenience, and usability.

%prep
%forgesetup

# imgui "submodule"
rm -rf dependencies/%{im_name}
tar -xzf %{SOURCE1} -C dependencies
mv dependencies/%{im_name}-%{im_commit} dependencies/%{im_name}

# ZArchive "submodule"
rm -rf dependencies/%{za_name}
tar -xzf %{SOURCE2} -C dependencies
mv dependencies/%{za_name}-%{za_commit} dependencies/%{za_name}

%patch0
%patch1

%build
glslang_DIR=%{_libdir}/cmake
export glslang_DIR

# Fix for error:
# /usr/bin/ld: /usr/lib64/libgtk-3.so: undefined reference to symbol 'wl_proxy_marshal_flags'
# /usr/bin/ld: /usr/lib64/libwayland-client.so.0: error adding symbols: DSO missing from command line
# Based on <https://github.com/libsdl-org/SDL/issues/5088#issue-1076489996>
# Setting it in build_ldflags didn't work, use optflags
%global optflags %{optflags} -lwayland-client

# BUILD_SHARED_LIBS=OFF is to fix this error:
#    At least one of these targets is not a STATIC_LIBRARY. Cyclic dependencies are allowed only among static libraries.
%cmake \
    -DCMAKE_BUILD_TYPE=release \
    -DENABLE_VCPKG=OFF \
    -DENABLE_DISCORD_RPC=OFF \
    -DEXPERIMENTAL_VERSION=999999 \
    -DPORTABLE=OFF \
    -DBUILD_SHARED_LIBS=OFF

%cmake_build

%install
# bin/Cemu_release -> /usr/bin/Cemu
install -Dpm 0755 bin/%{name}_release %{buildroot}%{_bindir}/%{name}

# bin/gameProfiles/* -> /usr/share/Cemu/gameProfiles
install -dm 0755 %{buildroot}%{_datadir}/%{name}/gameProfiles
cp -r --preserve=timestamps -t %{buildroot}%{_datadir}/%{name}/gameProfiles bin/gameProfiles/*

# bin/resources/* -> /usr/share/Cemu/resources
install -dm 0755 %{buildroot}%{_datadir}/%{name}/resources
cp -r --preserve=timestamps -t %{buildroot}%{_datadir}/%{name}/resources bin/resources/*

install -Dpm 0644 -t %{buildroot}%{_datadir}/icons/hicolor/128x128/apps dist/linux/%{rdns}.png
install -Dpm 0644 -t %{buildroot}%{_metainfodir} dist/linux/%{rdns}.metainfo.xml

desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    --set-key=PrefersNonDefaultGPU \
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
* Wed Dec 07 2022 Justin Koh <j@ustink.org> - 2.0-2.20221208gitfca7f5d
- Linux: Add Vulkan support for wayland (Cemu#553)

* Wed Dec 07 2022 Justin Koh <j@ustink.org> - 2.0-1.20221205git445b0af
- Initial build
