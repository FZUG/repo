%global debug_package %{nil}
%global project electronic-wechat
%global repo %{project}

# commit
%global _commit 5058348258b3a83f26daa417b282763f5cd8800e
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    wechat
Version: 1.3.0
Release: 2.git%{_shortcommit}%{?dist}
Summary: An Electron application for WeChat

Group:   Applications/Internet
License: MIT
URL:     https://github.com/geeeeeeeeek/wechat-electron/
Source0: https://github.com/geeeeeeeeek/wechat-electron/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: /usr/bin/npm
Requires: electron

%description
Electronic WeChat is released by this open source project. While Web WeChat
is a major component in the app, it should be noted that this is a community
release and not an official WeChat release.

%prep
%setup -q -n %repo-%{_commit}

%build
npm install pinyin

%install
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh
%{_bindir}/electron %{_datadir}/%{name}/src/main.js \$*
EOF

find {src,assets,node_modules} -type f -exec \
    install -Dm644 '{}' '%{buildroot}%{_datadir}/%{name}/{}' \;

install -Dm644 assets/icon.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Name=Electronic WeChat
Comment=A better WeChat client on Mac OS X and Linux
Exec=%{name}
Icon=%{name}
Categories=Network;InstantMessaging;Application;
Terminal=false
StartupNotify=true
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
%doc README.md README_zh.md CHANGELOG.md CONTRIBUTING.md
%license LICENSE.md
%attr(755,-,-) %{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Wed Jun 29 2016 mosquito <sensor.wen@gmail.com> - 1.3.0-2.git5058348
- Fix hold splash window
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 1.3.0-1.git5058348
- Release 1.3.0
* Fri Apr 22 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-1.git275edce
- Release 1.2.0
* Mon Mar 21 2016 mosquito <sensor.wen@gmail.com> - 1.1.1-1.git6704050
- Release 1.1.1
* Sun Mar  6 2016 mosquito <sensor.wen@gmail.com> - 1.0.1-1.gitb43c562
- Initial build
