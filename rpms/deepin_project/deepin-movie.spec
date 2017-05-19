%global _commit a1ba8c318a3a16440adb2677dae5145737f7e038
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-movie
Version:        2.2.13
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Movie based on QtAV
Summary(zh_CN): 深度影音

License:        GPLv3
Group:          Applications/Multimedia
URL:            https://github.com/linuxdeepin/deepin-movie
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  gettext
BuildRequires:  deepin-gettext-tools
BuildRequires:  desktop-file-utils

Requires:       dbus-python
Requires:       mediainfo
Requires:       python-qt5
Requires:       python-xpyb
Requires:       python-magic
Requires:       python2-ass
Requires:       python2-pysrt
Requires:       python2-peewee
Requires:       python2-requests
Requires:       python2-bottle
Requires:       python2-pyopengl
Requires:       qtav-qml-module

Requires:       python2-xpybutil
Requires:       python2-deepin-utils
Requires:       deepin-menu
Requires:       deepin-qml-widgets
Requires:       deepin-qml-dbus-factory
Requires:       deepin-qt5integration
Recommends:     deepin-manual

%description
Deepin movie with linuxdeepin desktop environment.

%description -l zh_CN
深度影音播放器, 后端基于QtAV, 支持解码大多数视频格式.

%prep
%setup -q -n %{name}-%{_commit}
# fix python version
find -iname "*.py" | xargs sed -i '1s|python$|python2|'

%build
%{__python2} configure.py
deepin-generate-mo locale/locale_config.ini

%install
%make_install PREFIX="%{_prefix}"

# Fix cannot register existing type 'GdkDisplayManager'
# https://bbs.archlinux.org/viewtopic.php?id=214147&p=2
rm -f %{buildroot}%{_bindir}/%{name}
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
QT_QPA_PLATFORMTHEME=deepin %{_datadir}/%{name}/main.py
EOF

chmod 0755 %{buildroot}%{_bindir}/%{name} \
    %{buildroot}%{_datadir}/%{name}/main.py

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*

%changelog
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 2.2.13-1.gita1ba8c3
- Update to 2.2.13
* Sat Jan 28 2017 mosquito <sensor.wen@gmail.com> - 2.2.11-2.git7896696
- Fix cannot register existing type 'GdkDisplayManager'
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.2.11-1.git7896696
- Update to 2.2.11
* Thu Jul 16 2015 mosquito <sensor.wen@gmail.com> - 2.2.2-2.git53adfc6
- python-peewee(>=2.3.0,<=2.4.4)
- remove some depends
* Sat Jul  4 2015 mosquito <sensor.wen@gmail.com> - 2.2.2-1.git53adfc6
- Initial build
