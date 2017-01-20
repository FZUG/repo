%global project dde-file-manager
%global repo %{project}

%global _commit f1915f87b341ded5eef75f1637367be720792ba9
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-file-manager
Version:        1.3.7
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin File Manager
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-file-manager
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  atk-devel
BuildRequires:  deepin-tool-kit-devel
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
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel
Requires:       deepin-shortcut-viewer
Provides:       %{repo}%{?_isa} = %{version}-%{release}
Obsoletes:      %{repo}%{?_isa} < %{version}-%{release}
# deepin-file-manager-backend

%description
Deepin File Manager

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}

%prep
%setup -q -n %{repo}-%{_commit}
sed -i 's|-0-2||g' dde-file-manager*/dde-file-manager*.pro
sed -i 's|lrelease|lrelease-qt5|g' dde-file-manager-lib/generate_translations.sh
sed -i 's|qmake|qmake-qt5|g' vendor/prebuild

# Fix broken icon link
sed -i '/Icon/s|dde|system|' %{repo}/%{repo}.desktop

%build
%qmake_qt5 PREFIX=%{_prefix} QMAKE_CFLAGS_ISYSTEM=
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_sysconfdir}/xdg/autostart/%{repo}*.desktop
%{_bindir}/dde-*
%{_libdir}/lib%{repo}.so.*
%{_datadir}/applications/%{repo}.desktop
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/%{repo}/
%{_datadir}/dman/%{repo}/
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%{_datadir}/polkit-1/actions/*.policy

%files devel
%{_includedir}/%{repo}/*.h
%{_libdir}/pkgconfig/%{repo}.pc
%{_libdir}/lib%{repo}.so

%changelog
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
