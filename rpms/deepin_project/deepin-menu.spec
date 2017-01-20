%global _commit 6038c517f2adcd511f13c600423accd0cac38ff7
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-menu
Version:        3.0.7
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin menu service

Group:          Development/Libraries
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-menu
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  python-devel
BuildRequires:  python2-setuptools
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtx11extras-devel
Requires:       python-qt5
Requires:       qt5-qtx11extras

%description
Deepin menu service for building beautiful menus.

%prep
%setup -q -n %{name}-%{_commit}

# fix python version
find -iname "*.py" | xargs sed -i '1s|python$|python2|'

sed -i '/target.path/s|lib|libexec|' deepin-menu.pro

%build
%{__python2} setup.py build
%{qmake_qt5} DEFINES+=QT_NO_DEBUG_OUTPUT
%{make_build}

%install
%{__python2} setup.py install -O1 --skip-build --prefix=%{_prefix} --root=%{buildroot}
%{make_install} INSTALL_ROOT="%{buildroot}"

rm -rf %{buildroot}/usr/deepin_menu
install -d %{buildroot}%{_datadir}/dbus-1/services/
install -d %{buildroot}%{_datadir}/applications/
install -d %{buildroot}/etc/xdg/autostart/

# Modify lib path to reflect the platform
sed -i 's|/usr/lib|%{_libexecdir}|' \
    com.deepin.menu.service deepin-menu.desktop

install -m644 *.service %{buildroot}%{_datadir}/dbus-1/services/
install -m644 *.desktop %{buildroot}%{_datadir}/applications/
ln -sfv %{_datadir}/applications/%{name}.desktop \
    %{buildroot}%{_sysconfdir}/xdg/autostart/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_libexecdir}/%{name}
%{python_sitelib}/deepin_menu*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/com.deepin.menu.service

%changelog
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
