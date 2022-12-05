Name:           Cemu
Version:        2.0
Release:        1%{?dist}
Summary:        Wii U emulator

License:        MPLv2.0
URL:            https://github.com/cemu-project/Cemu
Source0:        

BuildRequires:  
Requires:       

%description
Cemu is a cross-platform emulator for the Nintendo Wii U game console.
It is written in C/C++, and is able to run most Wii U games and
homebrew in a playable state.

Cemu is actively developed with new features and fixes to increase
compatibility, convenience, and usability.

%prep
%autosetup


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
