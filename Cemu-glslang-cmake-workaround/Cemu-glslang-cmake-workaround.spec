Name:           Cemu-glslang-cmake-workaround
Version:        1
Release:        2%{?dist}
Summary:        DO NOT INSTALL. Only for Copr jn64/Cemu build

URL:            https://github.com/jn64/Cemu-rpm
License:        BSD
Source0:        glslangConfig.cmake

%description
Provides missing glslangConfig.cmake file for Copr jn64/Cemu build for F37.
You should not install this package locally unless you are working on this Copr.

%prep

%build

%install
install -Dpm 0644 -t %{buildroot}%{_libdir}/cmake %{SOURCE0}

%files
%{_libdir}/cmake/glslangConfig.cmake

%changelog
* Tue Jan 03 2023 Justin Koh <j@ustink.org> - 1-2
- Rename package to avoid unintentional installs of 'glslang*'

* Mon Jan 02 2023 Justin Koh <j@ustink.org> - 1-1
- Create package for glslang workaround
