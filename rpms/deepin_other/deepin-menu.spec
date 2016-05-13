%global debug_package %{nil}
%global project deepin-menu
%global repo %{project}

# commit
%global _commit 7557d46600e993aa3ccdb60ce661620f971c7ebb
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		deepin-menu
Version:	2.90.0
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Deepin menu service

Group:		Development/Libraries
License:	GPLv3
URL:		https://github.com/linuxdeepin/deepin-menu
Source0:	https://github.com/linuxdeepin/deepin-menu/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	desktop-file-utils
BuildRequires:	python-setuptools
BuildRequires:	python-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qtdeclarative-devel
BuildRequires:	qt5-qtx11extras-devel
Requires:	python
Requires:	python-qt5

%description
Deepin menu service for building beautiful menus.

%prep
%setup -q -n %repo-%{_commit}

%build
%ifarch x86_64
sed -i 's|lib|lib64|' deepin-menu.pro
%endif
%{__python} setup.py build
%{_qt5_qmake}
make %{?_smp_mflags}

%install
%{__python} setup.py install -O1 --skip-build --prefix=%{_prefix} --root=%{buildroot}
make install INSTALL_ROOT=%{buildroot}

rm -rf %{buildroot}/usr/deepin_menu
cat com.deepin.menu.service <<EOF
[D-BUS Service]
Name=com.deepin.menu
Exec=%{_libdir}/%{name}
EOF
install -Dm 0644 com.deepin.menu.service \
    %{buildroot}%{_datadir}/dbus-1/services/com.deepin.menu.service

install -d %{buildroot}%{_sysconfdir}/xdg/autostart
cat > %{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=Deepin Menu
Exec=%{_libdir}/%{name}
NoDisplay=true
EOF
desktop-file-install -m 644 --dir=%{buildroot}%{_datadir}/applications/ %{name}.desktop
ln -sfv %{_datadir}/applications/%{name}.desktop \
    %{buildroot}%{_sysconfdir}/xdg/autostart/

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{python_sitelib}/deepin_menu*
%{_libdir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/com.deepin.menu.service
%{_sysconfdir}/xdg/autostart/%{name}.desktop

%changelog
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
