# <https://github.com/cemu-project/Cemu/tree/445b0afa9545c9ae7ed30f025bb2f3da2ee1a5f9>
%global forgeurl https://github.com/cemu-project/Cemu
%global commit 445b0afa9545c9ae7ed30f025bb2f3da2ee1a5f9
%forgemeta

# imgui submodule
# <https://github.com/ocornut/imgui/tree/8a44c31c95c8e0217f6e1fc814cbbbcca4981f14>
%global imgui_name imgui
%global imgui_url https://github.com/ocornut/%{imgui_name}
%global imgui_commit 8a44c31c95c8e0217f6e1fc814cbbbcca4981f14

# ZArchive submodule
# <https://github.com/Exzap/ZArchive/tree/d2c717730092c7bf8cbb033b12fd4001b7c4d932>
%global zarchive_name ZArchive
%global zarchive_url https://github.com/Exzap/%{zarchive_name}
%global zarchive_commit d2c717730092c7bf8cbb033b12fd4001b7c4d932

%global toolchain clang
%global rdns info.cemu.Cemu

Name:           Cemu
Version:        2.0
Release:        1%{?dist}
Summary:        Wii U emulator

License:        MPL-2.0
URL:            %{forgeurl}
Source0:        %{forgesource}
Source1:        https://github.com/ocornut/%{imgui_name}/archive/%{imgui_commit}/%{imgui_name}-%{imgui_commit}.tar.gz
Source2:        https://github.com/Exzap/%{zarchive_name}/archive/%{zarchive_commit}/%{zarchive_name}-%{zarchive_commit}.tar.gz
Patch0:         00-Cemu-fmt.patch
Patch1:         01-Cemu-no-strip-debug.patch

# Keep this section in sync with upstream build instructions
# <https://github.com/cemu-project/Cemu/blob/445b0afa9545c9ae7ed30f025bb2f3da2ee1a5f9/BUILD.md#for-fedora-and-derivatives>
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

%description
Cemu is a cross-platform emulator for the Nintendo Wii U game console.
It is written in C/C++, and is able to run most Wii U games and
homebrew in a playable state.

Cemu is actively developed with new features and fixes to increase
compatibility, convenience, and usability.

%prep
%forgesetup

# Remove dependencies/imgui, and extract imgui from the tarball to replace it
rm -rf dependencies/%{imgui_name}
tar -xzf %{SOURCE1} -C dependencies
mv dependencies/%{imgui_name}-%{imgui_commit} dependencies/%{imgui_name}

# Same for dependencies/zarchive
rm -rf dependencies/%{zarchive_name}
tar -xzf %{SOURCE2} -C dependencies
mv dependencies/%{zarchive_name}-%{zarchive_commit} dependencies/%{zarchive_name}

%patch0
%patch1

%build
glslang_DIR=%{_libdir}/cmake
export glslang_DIR

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
# Install bin/Cemu_release to /usr/bin/Cemu
install -Dpm 0755 bin/%{name}_release %{buildroot}%{_bindir}/%{name}

# Install bin/gameProfiles/* to /usr/share/Cemu/gameProfiles
install -dm 0755 %{buildroot}%{_datadir}/%{name}/gameProfiles
cp -r --preserve=timestamps -t %{buildroot}%{_datadir}/%{name}/gameProfiles bin/gameProfiles/*

# Install bin/resources/* to /usr/share/Cemu/resources
install -dm 0755 %{buildroot}%{_datadir}/%{name}/resources
cp -r --preserve=timestamps -t %{buildroot}%{_datadir}/%{name}/resources bin/resources/*

desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    --set-key=PrefersNonDefaultGPU \
    --set-value=true \
    dist/linux/%{rdns}.desktop

install -Dpm 0644 -t %{buildroot}%{_datadir}/icons/hicolor/128x128/apps dist/linux/%{rdns}.png
install -Dpm 0644 -t %{buildroot}%{_metainfodir} dist/linux/%{rdns}.metainfo.xml

%check
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{rdns}.metainfo.xml

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{rdns}.desktop
%{_datadir}/icons/hicolor/128x128/apps/%{rdns}.png
%{_metainfodir}/%{rdns}.metainfo.xml

%changelog
* Wed Dec 07 2022 Justin Koh <j@ustink.org> - 2.0-1.20221205git445b0af
- Initial build
