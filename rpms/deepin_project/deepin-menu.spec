Name:           deepin-menu
Version:        3.3.10
Release:        1%{?dist}
Summary:        Deepin menu service
License:        GPLv3+
URL:            https://github.com/linuxdeepin/deepin-menu
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Widgets)

%description
Deepin menu service for building beautiful menus.

%prep
%setup -q

# Modify lib path to reflect the platform
sed -i 's|/usr/bin|%{_libexecdir}|' data/com.deepin.menu.service \
    deepin-menu.desktop deepin-menu.pro

%build
%qmake_qt5 DEFINES+=QT_NO_DEBUG_OUTPUT
%make_build

%install
%make_install INSTALL_ROOT="%{buildroot}"

%files
%doc README.md
%license LICENSE
%{_libexecdir}/%{name}
%{_datadir}/dbus-1/services/com.deepin.menu.service

%changelog
* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 3.3.10-1
- Update to 3.3.10

* Sat Mar 24 2018 mosquito <sensor.wen@gmail.com> - 3.3.2-1
- Update to 3.3.2

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 3.1.7-1
- Update to 3.1.7

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 3.1.6-1
- Update to 3.1.6

* Wed Jul 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.5-1
- Update to 3.1.5

* Thu Jul 20 2017 mosquito <sensor.wen@gmail.com> - 3.1.5-1.git3ab1c65
- Update to 3.1.5

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.4-1.gita4c0bf8
- Update to 3.1.4

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.1.2-1.git3aee346
- Update to 3.1.2

* Tue Feb 21 2017 mosquito <sensor.wen@gmail.com> - 3.0.10-1.git3750b2f
- Update to 3.0.10

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.7-1.git6038c51
- Update to 3.0.7

* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 2.90.0-1.git7557d46
- Update version to 2.90.0-1.git7557d46

* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 1.1git20141202-1
- Update version to 1.1git20141202

* Mon Dec 01 2014 mosquito <sensor.wen@gmail.com> - 1.1git20141124-1
- Update version to 1.1git20141124

* Tue Nov 18 2014 mosquito <sensor.wen@gmail.com> - 1.1git20141113-1
- Update version to 1.1git20141113

* Tue Nov 4 2014 mosquito <sensor.wen@gmail.com> - 1.1git20141028-1
- Update version to 1.1git20141028

* Thu Oct 9 2014 mosquito <sensor.wen@gmail.com> - 1.1git20140923-2
- Fixed depends

* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 1.1git20140923-1
- Initial build
