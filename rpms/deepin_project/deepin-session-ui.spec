%global repo dde-session-ui

Name:           deepin-session-ui
Version:        4.4.7
Release:        1%{?dist}
Summary:        Deepin desktop-environment - Session UI module
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-session-ui
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  deepin-gettext-tools
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(liblightdm-qt5-3)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pam-devel
BuildRequires:  qt5-linguist
Requires:       deepin-control-center
Requires:       deepin-daemon
Requires:       startdde
Requires:       lightdm
Provides:       lightdm-deepin-greeter%{?_isa} = %{version}-%{release}
Provides:       deepin-notifications%{?_isa} = %{version}-%{release}
Obsoletes:      deepin-notifications%{?_isa} < %{version}-%{release}

%description
This project include those sub-project:

- dde-shutdown: User interface of shutdown.
- dde-lock: User interface of lock screen.
- dde-lockservice: The back-end service of locking screen.
- lightdm-deepin-greeter: The user interface when you login in.
- dde-switchtogreeter: The tools to switch the user to login in.
- dde-lowpower: The user interface of reminding low power.
- dde-osd: User interface of on-screen display.
- dde-hotzone: User interface of setting hot zone.

%prep
%setup -q -n %{repo}-%{version}
sed -i 's|lrelease|lrelease-qt5|' translate_generation.sh
sed -i 's|default_background.jpg|default.png|' widgets/*.cpp boxframe/*.cpp
sed -i 's|lib|libexec|' \
    misc/applications/deepin-toggle-desktop.desktop* \
    dde-osd/dde-osd_autostart.desktop \
    dde-osd/com.deepin.dde.osd.service \
    dde-osd/dde-osd.pro \
    dde-welcome/com.deepin.dde.welcome.service \
    dde-welcome/dde-welcome.pro \
    dde-warning-dialog/com.deepin.dde.WarningDialog.service \
    dde-warning-dialog/dde-warning-dialog.pro \
    dde-offline-upgrader/dde-offline-upgrader.pro \
    dde-suspend-dialog/dde-suspend-dialog.pro \
    dde-lowpower/dde-lowpower.pro

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

# lightdm.conf
#https://wiki.archlinux.org/index.php/Deepin_Desktop_Environment#Via_a_Display_Manager
install -d %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d
cat > %{buildroot}%{_sysconfdir}/lightdm/lightdm.conf.d/deepin.conf <<EOF
[Seat:*]
greeter-session=lightdm-deepin-greeter
EOF

%files
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/lightdm/lightdm.conf.d/deepin.conf
%{_bindir}/dde-*
%{_bindir}/dmemory-warning-dialog
%{_bindir}/lightdm-deepin-greeter
%{_libexecdir}/deepin-daemon/dde-*
%{_datadir}/%{repo}/
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/xgreeters/lightdm-deepin-greeter.desktop

%changelog
* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 4.4.7-1
- Update to 4.4.7

* Mon Mar 26 2018 mosquito <sensor.wen@gmail.com> - 4.3.5-1
- Update to 4.3.5

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.2.0-2
- Remove obsolete scriptlets

* Wed Dec 20 2017 mosquito <sensor.wen@gmail.com> - 4.2.0-1
- Update to 4.2.0

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 4.1.7-1
- Update to 4.1.7

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 4.0.17-1
- Update to 4.0.17

* Mon Oct 23 2017 mosquito <sensor.wen@gmail.com> - 4.0.15-1
- Update to 4.0.15

* Thu Sep 21 2017 mosquito <sensor.wen@gmail.com> - 4.0.14-1
- Update to 4.0.14

* Sun Aug 20 2017 mosquito <sensor.wen@gmail.com> - 4.0.13.1-1
- Update to 4.0.13.1

* Sun Aug  6 2017 mosquito <sensor.wen@gmail.com> - 4.0.13-1
- Rebuild

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.0.13-1.git4cadab1
- Update to 4.0.13

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.0.6-1.git1511ccf
- Update to 4.0.6

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.0.27-1.git6a09cb4
- Update to 3.0.27

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.23-1.git9db2f1d
- Update to 3.0.23

* Sun Dec 11 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.22-1
- Initial package build
