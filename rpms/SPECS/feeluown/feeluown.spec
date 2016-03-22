%global debug_package %{nil}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global project FeelUOwn
%global repo %{project}

# commit
%global _commit a6d4cde2419d662c4e2bdb15c2c4d5a284f16102
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    feeluown
Version: 8.0
Release: 0.1.git%{_shortcommit}%{?dist}
Summary: Net Ease Music for Linux
Summary(zh_CN): 网易云音乐 for Linux

Group:   Applications/Multimedia
License: GPLv3
URL:     https://github.com/cosven/FeelUOwn
Source0: https://github.com/cosven/FeelUOwn/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

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
find -size 0 ! -name "*.py" -exec rm -rf '{}' \;
sed -i '/icons/s|\.\./||g' \
    feeluown/themes/mac.qss \
    feeluown/themes/default.qss \
    feeluown/constants.py

%build

%install
install -d %{buildroot}%{_datadir}/%{name}/icons
cp -r %{name}/* %{buildroot}%{_datadir}/%{name}/
cp -r icons/*.{png,bmp} %{buildroot}%{_datadir}/%{name}/icons/

# icon file
install -Dm644 icons/FeelUOwn.png \
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
python3 %{_datadir}/%{name}/main.py
EOF

%post
if [ $1 -eq 1 ]; then
    /usr/bin/pip3 install -U -q 'quamash==0.5.3' &>/dev/null ||:
fi
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /usr/bin/pip3 uninstall -y -q quamash &>/dev/null ||:
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc README.md docs/*
%license LICENSE
%{_datadir}/%{name}
%attr(0755,-,-) %{_bindir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Tue Mar 22 2016 mosquito <sensor.wen@gmail.com> - 8.0-0.1.gita6d4cde
- Pre-release 8.0a
* Sun Feb 28 2016 mosquito <sensor.wen@gmail.com> - 7.1-0.1.git166205e
- Pre-release 7.1a
* Sat Feb  6 2016 mosquito <sensor.wen@gmail.com> - 7.0-0.1.git4fae2af
- Initial build
