%global project dde-control-center
%global repo %{project}

%global _commit 481255b220fca0881ff75e316b90f6f9955125ad
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-control-center
Version:        3.0.24
Release:        1.git%{_shortcommit}%{?dist}
Summary:        New control center for linux deepin
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-control-center
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  deepin-dock-devel
BuildRequires:  deepin-qt-dbus-factory-devel
BuildRequires:  GeoIP-devel
BuildRequires:  gtk2-devel
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
%setup -q -n %{repo}-%{_commit}
sed -i 's|lrelease|lrelease-qt5|g' translate_generation.sh

find -name '*.pro' | xargs sed -i '/target.path/s|lib|%{_lib}|'
sed -i '/%{repo}/s|lib|%{_lib}|' frame/pluginsmanager.cpp
sed -i '/deepin-daemon/s|lib|libexec|' modules/system_info/updatewidget.cpp

%build
%qmake_qt5 PREFIX=%{_prefix} \
    QMAKE_CFLAGS_ISYSTEM= \
    WITH_MODULE_GRUB=NO \
    WITH_MODULE_REMOTE_ASSIST=NO \
    WITH_MODULE_SYSINFO_UPDATE=NO
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%{_bindir}/%{repo}
%{_libdir}/%{repo}/modules/
%{_datadir}/applications/%{repo}.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{repo}/
%{_datadir}/dman/%{repo}/

%changelog
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
