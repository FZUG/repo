Name:           dtkwidget
Version:        2.0.9.2
Release:        1%{?dist}
Summary:        Deepin tool kit widget modules
License:        GPLv3
URL:            https://github.com/linuxdeepin/dtkwidget
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-static
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Concurrent)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Multimedia)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(dtkcore)
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(gsettings-qt)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xrender)
Provides:       deepin-tool-kit%{_isa} = %{version}-%{release}
Obsoletes:      deepin-tool-kit%{_isa} < %{version}-%{release}

%description
DtkWidget is Deepin graphical user interface for deepin desktop development.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q
sed -i 's|/lib|/libexec|' tools/svgc/svgc.pro

%build
%qmake_qt5 PREFIX=%{_prefix} LIB_INSTALL_DIR=%{_libdir} DBUS_VERSION_0_4_2=YES
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_libdir}/lib%{name}.so.*
%{_libexecdir}/dtk2/dtk-svgc
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/translations/

%files devel
%{_includedir}/libdtk-*/
%{_qt5_archdatadir}/mkspecs/modules/*.pri
%{_libdir}/cmake/DtkWidget/DtkWidgetConfig.cmake*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%changelog
* Fri Aug 10 2018 mosquito <sensor.wen@gmail.com> - 2.0.9.2-1
- Update to 2.0.9.2

* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 2.0.9.1-1
- Update to 2.0.9.1

* Tue Mar 20 2018 mosquito <sensor.wen@gmail.com> - 2.0.7.2-1
- Update to 2.0.7.2

* Tue Feb 20 2018 mosquito <sensor.wen@gmail.com> - 2.0.6.1-1
- Update to 2.0.6.1

* Mon Feb 19 2018 Rex Dieter <rdieter@fedoraproject.org> - 2.0.5.3-3
- rebuild (qt5)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 28 2017 mosquito <sensor.wen@gmail.com> - 2.0.5.3-1
- Update to 2.0.5.3

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 2.0.5.2-1
- Update to 2.0.5.2

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 2.0.4.1-1
- Update to 2.0.4.1

* Mon Oct 23 2017 mosquito <sensor.wen@gmail.com> - 2.0.1-2
- Fix DAboutDialog icon not supporting hidpi

* Tue Oct 17 2017 mosquito <sensor.wen@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Thu Aug 24 2017 mosquito <sensor.wen@gmail.com> - 2.0.0-2
- Dont depend a specific version of Qt

* Sun Aug 20 2017 mosquito <sensor.wen@gmail.com> - 2.0.0-1
- Update to 2.0.0

* Sat Jul 29 2017 mosquito <sensor.wen@gmail.com> - 0.3.3-1
- Initial package build
