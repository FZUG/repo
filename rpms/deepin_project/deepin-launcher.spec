%global repo dde-launcher

Name:           deepin-launcher
Version:        4.4.3
Release:        1%{?dist}
Summary:        Deepin desktop-environment - Launcher module
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-launcher
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(dtkcore)
BuildRequires:  pkgconfig(dtkwidget) >= 2.0
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5X11Extras)
Requires:       deepin-menu
Requires:       deepin-daemon
Requires:       startdde
Requires:       hicolor-icon-theme

%description
%{summary}.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q -n %{repo}-%{version}
sed -i 's|lrelease|lrelease-qt5|' translate_generation.sh

%build
%cmake -DCMAKE_INSTALL_PREFIX=%{_prefix} -DWITHOUT_UNINSTALL_APP=1 .
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%license LICENSE
%{_bindir}/%{repo}
%{_datadir}/%{repo}/
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files devel
%{_includedir}/%{repo}/

%changelog
* Thu Aug  2 2018 mosquito <sensor.wen@gmail.com> - 4.4.3-1
- Update to 4.4.3

* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 4.4.1-1
- Update to 4.4.1

* Tue Mar 20 2018 mosquito <sensor.wen@gmail.com> - 4.3.2-1
- Update to 4.3.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.3.0-2
- Remove obsolete scriptlets

* Wed Dec 20 2017 mosquito <sensor.wen@gmail.com> - 4.3.0-1
- Update to 4.3.0

* Sat Dec  9 2017 mosquito <sensor.wen@gmail.com> - 4.2.7-1
- Update to 4.2.7

* Sat Dec  2 2017 mosquito <sensor.wen@gmail.com> - 4.2.6-1
- Update to 4.2.6

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 4.2.1-1
- Update to 4.2.1

* Mon Oct 23 2017 mosquito <sensor.wen@gmail.com> - 4.1.9-1
- Update to 4.1.9

* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 4.1.8-1
- Update to 4.1.8

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 4.1.7-1
- Update to 4.1.7

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 4.1.6-1
- Update to 4.1.6

* Thu Jul 20 2017 mosquito <sensor.wen@gmail.com> - 4.1.4-1.gitbe7e408
- Update to 4.1.4

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.1.3-1.git1cc701f
- Update to 4.1.3

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.0.11-1.git67081d3
- Update to 4.0.11

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 4.0.7-1.gitf2df6ea
- Update to 4.0.7

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 4.0.4-1.git8b1a2dd
- Update to 4.0.4

* Sun Dec 04 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 4.0.3-1
- Updated to version 4.0.3

* Sat Oct 01 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 4.0.2-1
- Initial package build
