%global debug_package %{nil}
%global cefurl https://github.com/linuxdeepin/cef-binary
%global cefcom 059a0c9cef4e289a50dc7a2f4c91fe69db95035e

Name:           qcef
Version:        1.1.4.5
Release:        1%{?dist}
Summary:        Qt5 binding of CEF
License:        GPLv3
URL:            https://github.com/linuxdeepin/qcef
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{cefurl}/archive/%{cefcom}/cef-binary-%{cefcom}.tar.gz
Patch0:         %{name}_remove_demo.patch
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5WebChannel)
BuildRequires:  pkgconfig(Qt5X11Extras)

%description
%{summary}.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q -a1
%patch0 -p1 -b .remove_demo
mv -T cef-binary-%{cefcom} cef

%build
cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} \
      -DQCEF_INSTALL_PATH=%{_libdir} \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_VERBOSE_MAKEFILE=ON
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}
chmod +s %{buildroot}%{_libdir}/%{name}/chrome-sandbox

%files
%doc README.md
%license LICENSE
%{_libdir}/lib%{name}.so.1*
%{_libdir}/%{name}/

%files devel
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc
%{_includedir}/%{name}/

%changelog
* Mon Dec 31 2018 mosquito <sensor.wen@gmail.com> - 1.1.4.5-1
- Initial package build
