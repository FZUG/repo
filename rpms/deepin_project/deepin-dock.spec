%global repo dde-dock

Name:           deepin-dock
Version:        4.5.9.1
Release:        1%{?dist}
Summary:        Deepin desktop-environment - Dock module
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-dock
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  pkgconfig(dtkwidget) = 2.0
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  qt5-linguist
Requires:       deepin-daemon
Requires:       deepin-launcher
Requires:       deepin-menu
Requires:       deepin-qt5integration

%description
Deepin desktop-environment - Dock module.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q -n %{repo}-%{version}
sed -i 's|lrelease|lrelease-qt5|g' translate_generation.sh
sed -i '/target.path/s|lib|%{_lib}|' plugins/*/*.pro
sed -i 's|lib|%{_lib}|' frame/controller/dockpluginloader.cpp

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/%{repo}
%{_libdir}/%{repo}/
%{_datadir}/%{repo}/
%{_datadir}/dbus-1/services/*.service

%files devel
%{_includedir}/%{repo}/

%changelog
* Wed Jan 10 2018 mosquito <sensor.wen@gmail.com> - 4.5.9.1-1
- Update to 4.5.9.1

* Wed Dec 20 2017 mosquito <sensor.wen@gmail.com> - 4.5.9-1
- Update to 4.5.9

* Sat Dec  9 2017 mosquito <sensor.wen@gmail.com> - 4.5.7.1-1
- Update to 4.5.7.1

* Sat Dec  2 2017 mosquito <sensor.wen@gmail.com> - 4.5.7-1
- Update to 4.5.7

* Wed Nov 15 2017 mosquito <sensor.wen@gmail.com> - 4.5.1-1
- Update to 4.5.1

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 4.4.1-1
- Update to 4.4.1

* Sun Aug 20 2017 mosquito <sensor.wen@gmail.com> - 4.3.4-1
- Update to 4.3.4

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.3.3-1.gitbf79f1c
- Update to 4.3.3

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.2.1-1.git42610ae
- Update to 4.2.1

* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 4.1.4-1.gitd772fe2
- Update to 4.1.4

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 4.1.3-1.git26f189d
- Update to 4.1.3

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 4.0.8-1.gita882590
- Update to 4.0.8

* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 4.0.7-1
- Update to version 4.0.7 and renamed to deepin-dock

* Mon Dec 19 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 4.0.6-1
- Update to version 4.0.6

* Sun Dec 04 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 4.0.5-2
- Rebuild with newer deepin-tool-kit

* Sun Oct 02 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 4.0.5-1
- Initial package build
