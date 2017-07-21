%global project dde-control-center
%global repo %{project}

%global commit 21d68b62443fa54907db82e2d998a0c9cefbac37
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-control-center
Version:        4.2.4
Release:        1.git%{shortcommit}%{?dist}
Summary:        New control center for linux deepin
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-control-center
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  deepin-dock-devel
BuildRequires:  deepin-qt-dbus-factory-devel
BuildRequires:  gsettings-qt-devel
BuildRequires:  GeoIP-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  desktop-file-utils
Requires:       deepin-account-faces
Requires:       deepin-api
Requires:       deepin-daemon
Requires:       GeoIP-GeoLite-data
Requires:       GeoIP-GeoLite-data-extra
Requires:       startdde
Requires:       gtk-murrine-engine
Provides:       %{repo}%{?_isa} = %{version}-%{release}

%description
New control center for linux deepin

%prep
%setup -q -n %{repo}-%{commit}
sed -i 's|lrelease|lrelease-qt5|g' translate_generation.sh

sed -i -E '/target.path|utils.path/s|lib|%{_lib}|' plugins/*/*.pro
sed -i 's|lib|%{_lib}|' frame/pluginscontroller.cpp
sed -i -E '/QProcess|target.path/s|lib|libexec|' modules/update/updatemodule.cpp \
    dialogs/reboot-reminder-dialog/reboot-reminder-dialog.pro

%build
%qmake_qt5 PREFIX=%{_prefix} \
    QMAKE_CFLAGS_ISYSTEM= \
    WITH_MODULE_GRUB=NO \
    WITH_MODULE_REMOTE_ASSIST=NO \
    WITH_MODULE_SYSINFO_UPDATE=NO \
    DISABLE_SYS_UPDATE=YES
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%doc README.md
%license LICENSE
%{_bindir}/%{repo}
%{_libdir}/%{repo}/plugins/
%{_libexecdir}/%{repo}/reboot-reminder-dialog
%{_datadir}/applications/%{repo}.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{repo}/

%changelog
* Thu Jul 20 2017 mosquito <sensor.wen@gmail.com> - 4.2.4-1.git21d68b6
- Update to 4.2.4
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.2.3-1.git2f420f2
- Update to 4.2.3
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.1.2-1.git4d3827b
- Update to 4.1.2
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 4.0.7-1.git10c3be2
- Update to 4.0.7
* Sat Jan 21 2017 mosquito <sensor.wen@gmail.com> - 3.0.24-1.git481255b
- Downgrade to 3.0.24 for end user
* Sat Jan 21 2017 mosquito <sensor.wen@gmail.com> - 4.0.2-2.git8b1a736
- Fix can not start
* Thu Jan 19 2017 mosquito <sensor.wen@gmail.com> - 4.0.2-1.git8b1a736
- Update to 4.0.2
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 4.0.1-1.gitd1c1c9a
- Update to 4.0.1
* Tue Dec 27 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.24-2
- Bump to newer release because of copr signature
* Fri Dec 09 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.24-1
- Upgrade to 3.0.24
* Sun Oct 09 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.21-1
- Initial package build
