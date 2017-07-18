%global project dde-file-manager
%global repo %{project}

%global commit 9308953ef9b3f5ea42caebe3d191340d5392e750
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-file-manager
Version:        4.1.8
Release:        1.git%{shortcommit}%{?dist}
Summary:        Deepin File Manager
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-file-manager
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires:  atk-devel
BuildRequires:  deepin-gettext-tools
BuildRequires:  deepin-tool-kit-devel
BuildRequires:  deepin-dock-devel
BuildRequires:  deepin-qt-dbus-factory-devel
BuildRequires:  dtksettings-devel
BuildRequires:  ffmpegthumbnailer-devel
BuildRequires:  file-devel
BuildRequires:  gtk2-devel
BuildRequires:  gsettings-qt-devel
BuildRequires:  libsecret-devel
BuildRequires:  poppler-cpp-devel
BuildRequires:  polkit-devel
BuildRequires:  polkit-qt5-1-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  xcb-util-wm-devel
# run command by QProcess
Requires:       deepin-shortcut-viewer
Requires:       deepin-manual
Requires:       deepin-terminal
Requires:       file-roller
Requires:       gvfs-client
Requires:       samba
Requires:       xdg-user-dirs

Provides:       %{repo}%{?_isa} = %{version}-%{release}
Obsoletes:      %{repo}%{?_isa} < %{version}-%{release}
Provides:       deepin-desktop%{?_isa} = %{version}-%{release}
Obsoletes:      deepin-desktop%{?_isa} < %{version}-%{release}

%description
Deepin File Manager

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}

%prep
%setup -q -n %{repo}-%{commit}
sed -i 's|-0-2||g' %{repo}*/*.pro usb-device-formatter/usb-device-formatter.pro
sed -i 's|lrelease|lrelease-qt5|' %{repo}*/generate_translations.sh \
  usb-device-formatter/generate_translations.sh \
  dde-desktop/translate_generation.sh
sed -i 's|qmake|qmake-qt5|' vendor/prebuild
sed -i '/target.path/s|lib|%{_lib}|' dde-dock-plugins/disk-mount/disk-mount.pro \
  dde-dock-plugins/trash/trash.pro
sed -i '/deepin-daemon/s|lib|libexec|' dde-zone/mainwindow.h
sed -i 's|lib/gvfs|libexec|' dde-file-manager-lib/gvfs/networkmanager.cpp

%build
%qmake_qt5 PREFIX=%{_prefix} QMAKE_CFLAGS_ISYSTEM=
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_sysconfdir}/xdg/autostart/%{repo}*.desktop
%{_bindir}/dde-*
%{_bindir}/usb-device-formatter*
%{_libdir}/lib%{repo}.so.*
%{_libdir}/dde-dock/plugins/*.so
%{_datadir}/applications/dde-*.desktop
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/%{repo}/
%{_datadir}/dde-desktop/
%{_datadir}/usb-device-formatter/
%{_datadir}/dman/%{repo}/
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/polkit-1/actions/*.policy

%files devel
%{_includedir}/%{repo}/*.h
%{_includedir}/%{repo}/gvfs/*.h
%{_libdir}/pkgconfig/%{repo}.pc
%{_libdir}/lib%{repo}.so

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.1.8-1.git9308953
- Update to 4.1.8
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.1.5-1.git99d7597
- Update to 4.1.5
* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 1.4.1-1.gite303113
- Update to 1.4.1
* Sat Jan 28 2017 mosquito <sensor.wen@gmail.com> - 1.3.8-1.git207000d
- Update to 1.3.8
* Sun Jan 22 2017 mosquito <sensor.wen@gmail.com> - 1.3.7-2.gitf1915f8
- Add Req for run command
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.3.7-1.gitf1915f8
- Update to 1.3.7
* Thu Jan 12 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-3
- Fixed broken icon link noticed by Brenton Horne <brentonhorne77@gmail.com>
* Fri Jan 06 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-2
- Fixed build dependecies
* Fri Dec 30 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.6-1
- Update package to 1.3.6 and rename to deepin-file-manager
* Mon Dec 19 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.4-1
- Update package to 1.3.4
* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.3.3-1
- Update package to 1.3.3
* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.3-1
- Initial package build
