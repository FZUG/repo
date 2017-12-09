%global repo dde-launcher

Name:           deepin-launcher
Version:        4.2.7
Release:        1%{?dist}
Summary:        Deepin desktop-environment - Launcher module
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-launcher
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  pkgconfig(dtkcore)
BuildRequires:  pkgconfig(dtkwidget) >= 2.0
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  qt5-linguist
Requires:       deepin-menu
Requires:       deepin-daemon
Requires:       startdde
Requires:       hicolor-icon-theme

%description
Deepin desktop-environment - Launcher module

%prep
%setup -q -n %{repo}-%{version}
sed -i 's|lrelease|lrelease-qt5|g' translate_generation.sh

%build
%qmake_qt5 PREFIX=%{_prefix} WITHOUT_UNINSTALL_APP=1
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%license LICENSE
%{_bindir}/%{repo}
%{_datadir}/%{repo}/
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
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
