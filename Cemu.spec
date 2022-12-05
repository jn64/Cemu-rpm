%global forgeurl https://github.com/cemu-project/Cemu
# <https://github.com/cemu-project/Cemu/commit/445b0afa9545c9ae7ed30f025bb2f3da2ee1a5f9>
%global commit 445b0afa9545c9ae7ed30f025bb2f3da2ee1a5f9
%forgemeta

%global toolchain clang
%global rdns info.cemu.Cemu

Name:           Cemu
Version:        2.0
Release:        1%{?dist}
Summary:        Wii U emulator

License:        MPLv2.0
URL:            %{forgeurl}
Source0:        %{forgesource}

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

# Upstream uses vcpkg for these deps:
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

Requires:       boost-atomic
Requires:       boost-filesystem
Requires:       boost-nowide
Requires:       boost-program-options
Requires:       cubeb
Requires:       SDL2
Requires:       wxGTK
Requires:       wxGTK-gl

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


%build
%configure
%make_build


%install
# Install bin/Cemu_release to /usr/bin/Cemu
install -Dpm 0755 bin/%{name}_release %{buildroot}%{_bindir}/%{name}
# Create /usr/share/Cemu
install -m 755 -d %{buildroot}%{_datadir}/%{name}
# Copy everything from bin/ except the binary to /usr/share/Cemu
GLOBIGNORE=bin/%{name}_release
cp -pr bin/* %{buildroot}%{_datadir}/%{name}
unset GLOBIGNORE

# TODO use desktop-file-install instead https://docs.fedoraproject.org/en-US/packaging-guidelines/#_desktop_file_install_usage
install -Dpm 0644 -t %{buildroot}%{_datadir}/applications dist/linux/%{rdns}.desktop
install -Dpm 0644 -t %{buildroot}%{_datadir}/icons/hicolor/128x128/apps dist/linux/%{rdns}.png
install -Dpm 0644 -t %{buildroot}%{_metainfodir} dist/linux/%{rdns}.metainfo.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{rdns}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_metainfodir}/%{rdns}.metainfo.xml

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/%{name}/gameProfiles
%{_datadir}/%{name}/resources
# shaderCache should be deleted instead?
%{_datadir}/%{name}/shaderCache
%{_datadir}/applications/%{rdns}.desktop
%{_datadir}/icons/hicolor/hicolor/128x128/apps/%{rnds}.png
%{_metainfodir}/%{rdns}.metainfo.xml

%changelog
* Mon Dec 05 2022 Justin Koh <j@ustink.org> - 2.0-1
- Initial build
