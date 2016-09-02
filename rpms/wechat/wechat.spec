%global debug_package %{nil}
%global project electronic-wechat
%global repo %{project}
%global __provides_exclude (npm)
%global __requires_exclude (npm|0.12)

# commit
%global _commit c0c466706f18a32e20c49fc34a290c717c3cf64d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    wechat
Version: 1.4.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: An Electron application for WeChat

Group:   Applications/Internet
License: MIT
URL:     https://github.com/geeeeeeeeek/wechat-electron/
Source0: %{url}archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

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
%{_bindir}/electron %{_libdir}/%{name}/src/main.js \$*
EOF

find {src,assets,node_modules} -type f -exec \
    install -Dm644 '{}' '%{buildroot}%{_libdir}/%{name}/{}' \;

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
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Fri Sep  2 2016 mosquito <sensor.wen@gmail.com> - 1.4.0-1.gitc0c4667
- Release 1.4.0
* Wed Jun 29 2016 mosquito <sensor.wen@gmail.com> - 1.3.0-3.git5058348
- Change datadir to libdir for binary file
- Remove some npm dependences
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
