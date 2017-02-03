%global project dde-desktop
%global repo %{project}

%global _commit 6468342ea569db307136a451bf7aeb61dfb3327f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-desktop
Version:        4.0.1
Release:        2.git%{_shortcommit}%{?dist}
Summary:        Deepin desktop-environment - Desktop module
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-desktop
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  boost-devel
BuildRequires:  deepin-file-manager-devel
BuildRequires:  deepin-tool-kit-devel
BuildRequires:  gsettings-qt-devel
BuildRequires:  gtk2-devel
BuildRequires:  libqtxdg-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  xcb-util-wm-devel
Requires:       deepin-menu
Requires:       deepin-dock
Requires:       deepin-daemon
Requires:       deepin-qt5integration
Requires:       startdde
#Requires:       deepin-nautilus-properties
Provides:       %{repo}%{?_isa} = %{version}-%{release}

%description
Deepin desktop-environment - Desktop module

%prep
%setup -q -n %{repo}-%{_commit}
sed -i 's|-0-2||g' build.pri
sed -i 's|lrelease|lrelease-qt5|g' app/translate_generation.sh
sed -i 's|/usr/lib|%{_libexecdir}|' app/view/canvasgridview.cpp

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%doc README.md
%{_bindir}/%{repo}
%{_datadir}/%{repo}/
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service

%changelog
* Fri Feb  3 2017 mosquito <sensor.wen@gmail.com> - 4.0.1-2.git6468342
- Fix not work wallpaper choose
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 4.0.1-1.git6468342
- Update to 4.0.1
* Mon Dec 19 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 4.0.0-1
- Update to version 4.0.0
* Sun Dec 04 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.15-2
- Rebuild with newer deepin-tool-kit
* Sun Oct 02 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.15-1
- Initial package build
