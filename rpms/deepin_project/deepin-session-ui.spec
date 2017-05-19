%global project dde-session-ui
%global repo %{project}

%global _commit 1511ccf4dcf911a1f4e8d224eb58f4d5b9c63c14
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-session-ui
Version:        4.0.6
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin desktop-environment - Session UI module
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-session-ui
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  deepin-qt-dbus-factory-devel
BuildRequires:  gsettings-qt-devel
BuildRequires:  gtk2-devel
BuildRequires:  lightdm-qt5-devel
BuildRequires:  pam-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  systemd-devel
Requires:       deepin-control-center
Requires:       deepin-daemon
Requires:       startdde
Requires:       lightdm
Provides:       %{repo}%{?_isa} = %{version}-%{release}
Provides:       lightdm-deepin-greeter%{?_isa} = %{version}-%{release}

%description
Deepin desktop-environment - Session UI module

%prep
%setup -q -n %{repo}-%{_commit}
sed -i 's|lrelease|lrelease-qt5|g' translate_generation.sh

sed -i 's|lib|libexec|' \
    misc/applications/deepin-toggle-desktop.desktop* \
    dde-osd/com.deepin.dde.osd.service \
    dde-offline-upgrader/dde-offline-upgrader.pro \
    dde-wallpaper-chooser/dde-wallpaper-chooser.pro \
    dde-suspend-dialog/dde-suspend-dialog.pro \
    dde-lowpower/dde-lowpower.pro \
    dde-osd/dde-osd.pro \
    dde-zone/dde-zone.pro \
    dde-zone/mainwindow.h

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
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/com.deepin.dde.lock.conf
%{_bindir}/dde-*
%{_bindir}/lightdm-deepin-greeter
%{_libexecdir}/deepin-daemon/dde-*
%{_datadir}/%{repo}/
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/xgreeters/lightdm-deepin-greeter.desktop

%changelog
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.0.6-1.git1511ccf
- Update to 4.0.6
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.0.27-1.git6a09cb4
- Update to 3.0.27
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.23-1.git9db2f1d
- Update to 3.0.23
* Sun Dec 11 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.22-1
- Initial package build
