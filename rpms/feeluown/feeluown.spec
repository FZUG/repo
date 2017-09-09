%global project FeelUOwn
%global repo %{project}

%global commit d9e439a96fd9d2578bf52df48f9552674bf5b28e
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global c_commit e8af87411faacc554079d5718237fccab964fb21
%global c_shortcommit %(c=%{c_commit}; echo ${c:0:7})

Name:    feeluown
Version: 9.5
Release: 0.1.git%{shortcommit}%{?dist}
Summary: Net Ease Music for Linux
Summary(zh_CN): 网易云音乐 for Linux

Group:   Applications/Multimedia
License: GPLv3
URL:     https://github.com/cosven/feeluown
Source0: %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
Source1: %{url}-core/archive/%{c_commit}/%{name}-core-%{c_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: dos2unix
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pytest-runner
BuildRequires: desktop-file-utils
Requires(post): python3-pip
Requires: hicolor-icon-theme
Requires: python3-qt5
Requires: python3-dbus
Requires: python3-xlib
Requires: python3-crypto
Requires: python3-requests
Requires: python3-beautifulsoup4
Requires: python3-marshmallow
Requires: python3-msgpack
Requires: python3-mutagen
Requires: python3-fuzzywuzzy
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
%setup -q -a1 -n %{repo}-%{commit}
dos2unix README.md

%build
%{__python3} setup.py build
pushd %{name}-core-%{c_commit}
sed -i 's|2.13|2.10|' setup.py
%{__python3} setup.py build

%install
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
pushd %{name}-core-%{c_commit}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd

# fix locale
sed -i "2aimport os\nos.environ['LANG'] = 'C'" %{buildroot}%{_bindir}/%{name}

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

%post
if [ $1 -eq 1 ]; then
    /usr/bin/pip3 install -U -q 'quamash>=0.5.5' 'python-Levenshtein>=0.12.0' 'april==0.0.1a4' aiozmq &>/dev/null ||:
fi
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /usr/bin/pip3 uninstall -y -q quamash python-Levenshtein aiozmq april &>/dev/null ||:
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}*
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/applications/%{name}.desktop
%{python3_sitelib}/%{name}*
%{python3_sitelib}/fuocore*
%{python3_sitelib}/mpv.py
%{python3_sitelib}/__pycache__/*

%changelog
* Sat Sep  9 2017 mosquito <sensor.wen@gmail.com> - 9.5-0.1.gitd9e439a
- Release 9.5
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
