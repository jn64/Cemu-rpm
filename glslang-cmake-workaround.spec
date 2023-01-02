Name:           glslang-cmake-workaround
Version:        1
Release:        1%{?dist}
Summary:        Provides missing glslangConfig.cmake for this Cemu build

License:        BSD
Source0:        glslangConfig.cmake

%description
%{summary}

%prep

%build

%install
install -Dpm 0644 -t %{buildroot}%{_libdir}/cmake %{SOURCE0}

%files
%{_libdir}/cmake/glslangConfig.cmake

%changelog
* Mon Jan 02 2023 Justin Koh <j@ustink.org> - 1-1
- Create package for glslang workaround
