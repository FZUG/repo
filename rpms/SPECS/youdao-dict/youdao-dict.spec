%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global debug_package %{nil}

Name:		youdao-dict
Version:	1.0.2
Release:	2%{?dist}
Summary:	Youdao Dict
Summary(zh_CN):	有道词典

License:	Proprietary
URL:		http://cidian.youdao.com/index-linux.html
Group:		Applications/System
Source0:	http://codown.youdao.com/cidian/linux/%{name}_%{version}~ubuntu_amd64.deb
Source1:	http://codown.youdao.com/cidian/linux/%{name}_%{version}~ubuntu_i386.deb

BuildRequires:	dpkg
BuildRequires:	python3-devel
Requires:	python3-qt5
Requires:	python3-requests
Requires:	python3-xlib
Requires:	python3-pillow
Requires:	python3-lxml
Requires:	python3-pyxdg
Requires:	python3-dbus
Requires:	libappindicator-gtk3
Requires:	qt5-qtquickcontrols
Requires:	qt5-qtgraphicaleffects
Requires:	tesseract-langpack-chi_sim
Requires:	tesseract-langpack-chi_tra

%description
Youdao Dict

%description -l zh_CN
有道词典

%prep
# Extract DEB package
%ifarch x86_64
dpkg-deb -X %{SOURCE0} %{_builddir}/%{name}-%{version}
%else
dpkg-deb -X %{SOURCE1} %{_builddir}/%{name}-%{version}
%endif

%build

%install
pushd %{_builddir}/%{name}-%{version}

# data files
install -d %{buildroot}{%{_datadir},%{_bindir}}
cp -r usr/share/* %{buildroot}%{_datadir}/

# python files
install -d %{buildroot}%{python3_sitelib}
mv %{buildroot}%{_datadir}/%{name} %{buildroot}%{python3_sitelib}/
chmod 0755 %{buildroot}%{python3_sitelib}/%{name}/*.py

# bin file
ln -sfv %{python3_sitelib}/%{name}/main.py %{buildroot}%{_bindir}/%{name}

# autostart
cp etc/xdg/autostart/* %{buildroot}%{_datadir}/applications/

# fix path
sed -i 's|/usr/share|%{python3_sitelib}|' \
  %{buildroot}%{_datadir}/dbus-1/services/com.youdao.backend.service \
  %{buildroot}%{_datadir}/dbus-1/services/com.youdao.indicator.service

%post
# install
if [ "$1" -eq "1" ]; then
    ln -s %{_datadir}/applications/%{name}-autostart.desktop \
      %{_sysconfdir}/xdg/autostart/ &>/dev/null ||:
fi
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%preun
# uninstall
if [ "$1" -eq "0" ];then
    rm -rf %{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop
    pkill %{name} &>/dev/null ||:
fi

%postun
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{python3_sitelib}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/
%{_datadir}/doc/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}*

%changelog
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 1.0.2-2
- remove some command
* Sat May 09 2015 mosquito <sensor.wen@gmail.com> - 1.0.2-1
- initial version 1.0.2
