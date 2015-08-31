%global debug_package %{nil}
%global project fcitx-qt5
%global repo %{project}

# commit
%global _commit 73337c53f704f083c8269728ae8912fb47c4282f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		fcitx-qt5
Version:	1.0.4
Release:	2.git%{_shortcommit}%{?dist}
Summary:	Fcitx IM module for Qt5
Summary(zh_CN):	Fcitx QT5 输入模块

# The entire source code is GPLv2+ except
# platforminputcontext/keyserver_x11.h which is LGPLv2+
License:	GPLv2+ and LGPLv2+
Url:		https://github.com/fcitx/fcitx-qt5
Source0:	https://github.com/fcitx/fcitx-qt5/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	cmake
BuildRequires:	libicu-devel
BuildRequires:	fcitx-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	libxkbcommon-devel
BuildRequires:	extra-cmake-modules

%description
A QT5 input context plugin of Fcitx IM Framework.

%description -l zh_CN
Fcitx 输入法框架的 QT5 输入模块.

%package devel
Summary:	Development files for %{name}
Summary(zh_CN):	%{name} 开发文件
Group:		Development/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Development header files for Fcitx input method framework (Qt5).

%description devel -l zh_CN
Fcitx 输入法框架 (Qt5) 的头文件.

%prep
%setup -q -n %repo-%{_commit}

%build
%cmake .
make %{?_smp_mflags}

%install
%make_install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README
%{_libdir}/libFcitxQt5DBusAddons.so.*
%{_libdir}/libFcitxQt5WidgetsAddons.so.*
%dir %{_qt5_plugindir}/platforminputcontexts/
%{_qt5_plugindir}/platforminputcontexts/libfcitxplatforminputcontextplugin.so

%files devel
%defattr(-,root,root,-)
%{_libdir}/libFcitxQt5DBusAddons.so
%{_libdir}/libFcitxQt5WidgetsAddons.so
%{_includedir}/FcitxQt5/*.h
%{_includedir}/FcitxQt5/FcitxQtDBusAddons/*.h
%{_includedir}/FcitxQt5/FcitxQtWidgetsAddons/*.h
%{_libdir}/cmake/FcitxQt5DBusAddons/FcitxQt5DBusAddons*.cmake
%{_libdir}/cmake/FcitxQt5WidgetsAddons/FcitxQt5WidgetsAddons*.cmake

%changelog
* Mon Aug 31 2015 mosquito <sensor.wen@gmail.com> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_22_Mass_Rebuild
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 1.0.4-1
- Update version to 1.0.4
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 1.0.2-1
- Update version to 1.0.2
- Rename version name
* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 1.0.0git20150118-1
- Update version to 1.0.0git20150118
* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 1.0.0git20150115-1
- Update version to 1.0.0git20150115
* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 0.1.2git20141201-1
- Update version to 0.1.2git20141201
* Tue Nov 4 2014 mosquito <sensor.wen@gmail.com> - 0.1.2git20141022-1
- Update version to 0.1.2git20141022
* Wed Oct 1 2014 mosquito <sensor.wen@gmail.com> - 0.1.2git20140828-1
- Rebuild for fedora and rhel 7
* Mon Sep 15 2014 i@marguerite.su
- add baselibs.conf to Source
* Thu Sep 11 2014 hrvoje.senjan@gmail.com
- Fix baselibs requires, and shlib find-requires works
  also with baselibs
* Mon Jun  9 2014 i@marguerite.su
- update version 0.1.2
  * Fix github issue fcitx/fcitx-qt5#2
* Sun Mar  3 2013 i@marguerite.su
- update version 0.1.1
  * fix build and add libfcitx-qt5 for dbus.
- fix Qt5 dependency name from KDE:Qt50 repository.
- add baselibs.conf
  * because there're 32bit applications that needs input method
  * so we have to provide a 32bit input module too
* Tue Apr 17 2012 i@marguerite.su
- initial version 0.1.0
