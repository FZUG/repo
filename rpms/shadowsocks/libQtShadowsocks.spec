%global soname QtShadowsocks

Name:    libqtshadowsocks
Version: 2.1.0
Release: 1%{?dist}
Summary: A lightweight and ultra-fast shadowsocks library written in C++/Qt
License: LGPLv3+
URL:     https://github.com/librehat/libQtShadowsocks
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: qt5-qttools
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(botan-2)

%description
%{summary}.

%package devel
Summary: %{name} header files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files of %{name}.

%prep
%setup -q -n lib%{soname}-%{version}

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%doc README.md
%license LICENSE
%{_bindir}/shadowsocks-libqss
%{_libdir}/lib%{soname}.so.2*

%files devel
%{_libdir}/lib%{soname}.so
%{_libdir}/pkgconfig/%{soname}.pc
%{_includedir}/%{soname}/

%changelog
* Sun Dec 30 2018 mosquito <sensor.wen@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.10.0-1
- Update to 1.10.0 [8795845]

* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 1.9.0-1
- Update to 1.9.0 [c60df46]

* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 1.8.4-2
- Rebuild for botan and Qt 5.6.0

* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 1.8.4-1
- Update to 1.8.4 [d2c76c5]

* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 1.8.2-1
- Update to 1.8.2 [3c3aa83]

* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 1.6.1-1
- Update to 1.6.1 [7b71ee0]

* Tue Jun 02 2015 mosquito <sensor.wen@gmail.com> - 1.6.1-1
- Initial build
