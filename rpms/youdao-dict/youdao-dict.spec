# https://aur.archlinux.org/packages/youdao-dict
# http://fedoraproject.org/wiki/Packaging:Python#Byte_compiling
# http://fedoraproject.org/wiki/Packaging:Python_Appendix#Manual_byte_compilation

# Manual byte compilation for python 3(__pycache__)
%global __python %{__python3}

Name:    youdao-dict
Version: 1.1.0
Release: 2%{?dist}
Summary: Youdao Dict
Summary(zh_CN): 有道词典

License: GPLv3 and Proprietary
URL:     http://cidian.youdao.com/index-linux.html
Group:   Applications/System
Source0: http://codown.youdao.com/cidian/linux/%{name}_%{version}-0-ubuntu_amd64.deb
Source1: http://codown.youdao.com/cidian/linux/%{name}_%{version}-0-ubuntu_i386.deb
Patch0:  youdao-dict-1.1.0-dbus-register-object.patch

BuildRequires: dpkg
BuildRequires: python3-devel
Requires: python3-dbus
Requires: python3-lxml
Requires: python3-requests
Requires: python3-pillow
Requires: python3-pyxdg
Requires: python3-qt5
Requires: python3-qt5-webkit
Requires: python3-xlib
Requires: libappindicator-gtk3
Requires: qt5-qtquickcontrols
Requires: qt5-qtgraphicaleffects
Requires: tesseract-langpack-chi_sim
Requires: tesseract-langpack-chi_tra

%description
Youdao Dict

%description -l zh_CN
有道词典

%prep
# Extract DEB package
%ifarch x86_64
dpkg-deb -x %{SOURCE0} %{_builddir}/%{name}-%{version}
%else
dpkg-deb -x %{SOURCE1} %{_builddir}/%{name}-%{version}
%endif

# Fix dbus register object
pushd %{_builddir}/%{name}-%{version}%{_datadir}
%patch0 -p1 -b .dbus-register-object

%build

%install
pushd %{_builddir}/%{name}-%{version}%{_datadir}

# data files
install -d %{buildroot}%{_datadir}/
cp -r %{name} %{buildroot}%{_datadir}/
cp -r icons %{buildroot}/%{_datadir}/
cp -r dbus-1 %{buildroot}%{_datadir}/
cp -r applications %{buildroot}%{_datadir}/
cp -r doc %{buildroot}%{_datadir}/

# bin file
install -d %{buildroot}%{_bindir}
ln -sfv %{_datadir}/%{name}/main.py %{buildroot}%{_bindir}/%{name}

%post
if [ $1 -eq 1 ]; then
    ln -s %{_datadir}/applications/%{name}-autostart.desktop \
      %{_sysconfdir}/xdg/autostart/ &>/dev/null ||:
fi
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%preun
if [ $1 -eq 0 ];then
    rm -f %{_sysconfdir}/xdg/autostart/%{name}-autostart.desktop
    pkill %{name} &>/dev/null ||:
fi

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/doc/%{name}/
%{_datadir}/applications/*.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/icons/hicolor/*/apps/%{name}*

%changelog
* Sun Dec 11 2016 mosquito <sensor.wen@gmail.com> - 1.1.0-2
- fix dbus register object
* Sun Jan 17 2016 mosquito <sensor.wen@gmail.com> - 1.1.0-1
- release 1.1.0
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 1.0.2-2
- remove some command
* Sat May 09 2015 mosquito <sensor.wen@gmail.com> - 1.0.2-1
- initial version 1.0.2
