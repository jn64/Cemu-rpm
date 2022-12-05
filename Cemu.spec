%global forgeurl https://github.com/cemu-project/Cemu

# <https://github.com/cemu-project/Cemu/commit/c1afa4cad0e6092325ae796f9b0c9ed9a686be0f>
%global commit c1afa4cad0e6092325ae796f9b0c9ed9a686be0f

%global toolchain clang

%forgemeta

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

Requires:       

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
%make_install


%files
%license add-license-file-here
%doc add-docs-here



%changelog
* Mon Dec 05 2022 Justin Koh <j@ustink.org>
- 
