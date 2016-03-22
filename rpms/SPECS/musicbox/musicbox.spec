%global debug_package %{nil}
%global project musicbox
%global repo %{project}

# commit
%global _commit 6ac5ee11c27e7bb1997d7edfb08bf35dd4499afe
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    musicbox
Version: 0.2.1.6
Release: 1.git%{_shortcommit}%{?dist}
Summary: A sexy command line interface musicbox
Summary(zh_CN): 命令行版的网易云音乐

Group:   Applications/Multimedia
License: MIT
URL:     https://github.com/darknessomi/musicbox
Source0: https://github.com/darknessomi/musicbox/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source1: musicbox_logo.png

BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-setuptools
Requires: python-crypto
Requires: python-requests
Requires: python-beautifulsoup4
Requires: mpg123
Recommends: aria2
Recommends: python-keybinder
Recommends: libnotify

%description
A sexy command line interface musicbox.

%description -l zh_CN
命令行版的网易云音乐.

%prep
%setup -q -n %repo-%{_commit}

%build

%install
%{__python} setup.py install \
    -O1 \
    --prefix=%{_prefix} \
    --root=%{buildroot}

# install icon file
install -Dm 0644 %{S:1} %{buildroot}%{_datadir}/icons/%{name}.png

# install desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=MusicBox
Name[zh_CN]=网易云音乐
GenericName=MusicBox
GenericName[zh_CN]=网易云音乐
Comment=Play your cloud music
Comment[zh_CN]=网易云音乐的命令行客户端
Exec=%{name}
Icon=%{name}
Terminal=true
StartupNotify=true
Categories=AudioVideo;Player;
EOF

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

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
%doc README.md
%license LICENSE.txt
%{_bindir}/%{name}
%{python_sitelib}/NEMbox
%{python_sitelib}/NetEase_MusicBox-%{version}-py%{python2_version}.egg-info
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.png

%changelog
* Tue Mar 22 2016 mosquito <sensor.wen@gmail.com> - 0.2.1.6-1.git6ac5ee1
- Update version to 0.2.1.6-1.git6ac5ee1
* Mon Feb 29 2016 mosquito <sensor.wen@gmail.com> - 0.2.1.3-1.gite6428bb
- Update version to 0.2.1.3-1.gite6428bb
* Sat Feb 27 2016 mosquito <sensor.wen@gmail.com> - 0.2.1.2-1.git7e04315
- Update version to 0.2.1.2-1.git7e04315
- Add depends python-crypto, aria2, python-keybinder, libnotify
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 0.2.1.0-1.gitf0d05ae
- Update version to 0.2.1.0-1.gitf0d05ae
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 0.2.0.8-1.git0d67739
- Update version to 0.2.0.8-1.git0d67739
* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 0.1.5.6-1.git65c2742
- Update version to 0.1.5.6-1.git65c2742
* Tue Feb 03 2015 mosquito <sensor.wen@gmail.com> - 0.1.3git20150202-1
- Update version to 0.1.3git20150202
* Thu Jan 29 2015 mosquito <sensor.wen@gmail.com> - 0.1.2git20150128-1
- Update version to 0.1.2git20150128
* Mon Jan 12 2015 mosquito <sensor.wen@gmail.com> - 0.1.2git20150107-1
- Update version to 0.1.2git20150107
* Wed Jan 07 2015 mosquito <sensor.wen@gmail.com> - 0.1.1git20150103-1
- Update version to 0.1.1git20150103
* Sat Jan 03 2015 mosquito <sensor.wen@gmail.com> - 0.1.1git20150102-1
- Update version to 0.1.1git20150102
* Sun Oct 19 2014 mosquito <sensor.wen@gmail.com> - 0.1-1
- Initial build
