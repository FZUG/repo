Name:           deepin-movie
Version:        2.2.14
Release:        2%{?dist}
Summary:        Deepin Movie based on QtAV
Summary(zh_CN): 深度影音
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-movie
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
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
Deepin movie for deepin desktop environment.

%description -l zh_CN
深度影音播放器, 后端基于QtAV, 支持解码大多数视频格式.

%prep
%setup -q

%build
%{__python2} configure.py
deepin-generate-mo locale/locale_config.ini
chmod 0755 src/main.py

# Make python shebang uniq
find -iname "*.py" | xargs sed -i '1s@^#!/usr/bin/python@#!/usr/bin/python2@'
find -iname "*.py" | xargs sed -i '1s@^#!/usr/bin/env python@#!/usr/bin/python2@'
sed -i '1s@^#! /usr/bin/env python@#!/usr/bin/python2@' src/utils/misc.py

for lib in $(find -iname "*.py" -perm 644) ; do
 sed '1{\@^#!/usr/bin/python2@d}' $lib > $lib.new &&
 touch -r $lib $lib.new &&
 mv $lib.new $lib
done

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
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*

%changelog
* Sun Aug 06 2017 Zamir SUN <sztsian@gmail.com> - 2.2.14-2
- Remove group tag
- Fix rpmlint shebang error

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 2.2.14-1.git69123ed
- Update to 2.2.14

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
