%global commit 3ab1c65cabf80cab3e8ae5d045500601b2bffcc9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-menu
Version:        3.1.5
Release:        1.git%{shortcommit}%{?dist}
Summary:        Deepin menu service

Group:          Development/Libraries
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-menu
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  deepin-tool-kit-devel
BuildRequires:  deepin-qt-dbus-factory-devel
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtx11extras-devel
Requires:       python-qt5

%description
Deepin menu service for building beautiful menus.

%prep
%setup -q -n %{name}-%{commit}

# Remove python shebang
find -iname "*.py" | xargs sed -i '/env python/d'

# Modify lib path to reflect the platform
sed -i 's|/usr/bin|%{_libexecdir}|' data/com.deepin.menu.service \
    deepin-menu.desktop deepin-menu.pro

# Fix setup.py install path
sed -i '/data_files/s|list_files.*)|"")|' setup.py

%build
%{__python2} setup.py build
%{qmake_qt5} DEFINES+=QT_NO_DEBUG_OUTPUT
%{make_build}

%install
%{__python2} setup.py install -O1 --skip-build --prefix=%{_prefix} --root=%{buildroot}
%{make_install} INSTALL_ROOT="%{buildroot}"

install -d %{buildroot}%{_datadir}/dbus-1/services/
install -m644 data/*.service %{buildroot}%{_datadir}/dbus-1/services/

install -d %{buildroot}%{_datadir}/applications/
desktop-file-install --remove-key=OnlyShowIn --mode=644 \
    --dir=%{buildroot}%{_datadir}/applications deepin-menu.desktop

install -d %{buildroot}/etc/xdg/autostart/
ln -sfv %{_datadir}/applications/%{name}.desktop \
    %{buildroot}%{_sysconfdir}/xdg/autostart/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_libexecdir}/%{name}
%{python_sitelib}/deepin_menu*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/com.deepin.menu.service

%changelog
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
