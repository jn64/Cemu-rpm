%global forgeurl https://github.com/cemu-project/Cemu

# <https://github.com/cemu-project/Cemu/commit/c1afa4cad0e6092325ae796f9b0c9ed9a686be0f>
%global commit c1afa4cad0e6092325ae796f9b0c9ed9a686be0f

%forgemeta

Name:           Cemu
Version:        2.0
Release:        1%{?dist}
Summary:        Wii U emulator

License:        MPLv2.0
URL:            %{forgeurl}
Source0:        %{forgesource}

BuildRequires:  
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
