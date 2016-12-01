%global debug_package %{nil}
%global __os_install_post %{nil}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global project FeelUOwn
%global repo %{project}

# commit
%global _commit 698ed58c4ab33f78bd1a0700480a066f9c2fbe5b
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    feeluown
Version: 9.3
Release: 0.1.git%{_shortcommit}%{?dist}
Summary: Net Ease Music for Linux
Summary(zh_CN): 网易云音乐 for Linux

Group:   Applications/Multimedia
License: GPLv3
URL:     https://github.com/cosven/FeelUOwn
Source0: %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: dos2unix
BuildRequires: python3-devel
BuildRequires: desktop-file-utils
Requires(post): python3-pip
Requires: hicolor-icon-theme
Requires: python3-qt5
Requires: python3-dbus
Requires: python3-xlib
Requires: python3-requests
Requires: python3-beautifulsoup4
Requires: python3-sqlalchemy
Requires: python3-PyYAML
Requires: gstreamer1-plugins-base
Requires: gstreamer1-plugins-good
Requires: gstreamer1-plugins-ugly
Requires: gstreamer1-libav
Requires: gstreamer-python
Recommends: vlc

%description
Net Ease Music for Linux

%description -l zh_CN
网易云音乐 for Linux

%prep
%setup -q -n %repo-%{_commit}
dos2unix README.md

%build

%install
install -d %{buildroot}%{_datadir}
cp -r %{name} %{buildroot}%{_datadir}/

# icon file
install -Dm644 %{name}/%{name}.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# desktop file
cat > %{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=FeelUOwn
Comment=FeelUOwn Launcher
Exec=%{name}
Icon=%{name}
Categories=AudioVideo;Audio;Player;Qt;
Terminal=false
StartupNotify=true
EOF
desktop-file-install \
    --dir=%{buildroot}%{_datadir}/applications \
    %{name}.desktop

# execution file
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/bash
python3 %{_datadir}/%{name}
EOF

%post
if [ $1 -eq 1 ]; then
    /usr/bin/pip3 install -U -q 'quamash==0.5.5' pycrypto &>/dev/null ||:
fi
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /usr/bin/pip3 uninstall -y -q quamash pycrypto &>/dev/null ||:
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_datadir}/%{name}
%attr(0755,-,-) %{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Thu Dec  1 2016 mosquito <sensor.wen@gmail.com> - 9.3-0.1.git698ed58
- Release 9.3a
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 9.2-0.1.git8ccb1fe
- Release 9.2a
* Tue Mar 22 2016 mosquito <sensor.wen@gmail.com> - 8.0-0.1.gita6d4cde
- Pre-release 8.0a
* Sun Feb 28 2016 mosquito <sensor.wen@gmail.com> - 7.1-0.1.git166205e
- Pre-release 7.1a
* Sat Feb  6 2016 mosquito <sensor.wen@gmail.com> - 7.0-0.1.git4fae2af
- Initial build
