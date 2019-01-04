Name:    shadowsocks-qt5
Version: 3.0.1
Release: 1%{?dist}
Summary: A cross-platform shadowsocks GUI client
License: LGPLv3+
URL:     https://github.com/shadowsocks/shadowsocks-qt5
Source0: %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: cmake
BuildRequires: gcc-c++
BuildRequires: qt5-qttools
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(QtShadowsocks)
BuildRequires: pkgconfig(botan-2)
BuildRequires: pkgconfig(libqrencode)
BuildRequires: pkgconfig(zbar)
BuildRequires: desktop-file-utils
Requires:      hicolor-icon-theme

%description
%{summary}.

%prep
%setup -q

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}
desktop-file-validate %{buildroot}%{_datadir}/applications/{name}.desktop

%files
%doc README.md
%license LICENSE
%{_bindir}/ss-qt5
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Sun Dec 30 2018 mosquito <sensor.wen@gmail.com> - 3.0.1-1
- Update to 3.0.1

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.8.0-1
- Update to 2.8.0 [92a51a4]

* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 2.7.0-1
- Update to 2.7.0 [4540be9]

* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 2.6.1-2
- Rebuild for Qt 5.6.0

* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 2.6.1-1
- Update to 2.6.1 [ba70fd1]

* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 2.6.0-1
- Update to 2.6.0 [7ec8a63]

* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 2.4.1-1
- Update to 2.4.1 [6cd4372]

* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 2.4.0-1
- Initial build
