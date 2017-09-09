%global commit e730f1cddf5f97a0e5e122d648327572600bddf6
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:    moonplayer
Version: 1.1.7
Release: 1.git%{shortcommit}%{?dist}
Summary: Video player that can play online videos
Summary(zh_CN): 一款可点播优酷, 土豆等网站在线视频的视频播放器

Group:   Applications/Multimedia
License: GPLv3
URL:     https://github.com/coslyk/moonplayer
Source0: %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
# https://code.google.com/p/moonplayer/wiki/PluginTutorial
# http://forum.ubuntu.org.cn/viewtopic.php?f=74&t=456351
Source1: plugin_56.py
Source2: plugin_funshion.py
Source3: plugin_iqiyi.py
Source4: plugin_sohu.py

BuildRequires: python-devel
BuildRequires: pkgconfig(Qt5)
BuildRequires: pkgconfig(qtermwidget5)
BuildRequires: mpv-libs-devel
Requires: mplayer
Requires: mencoder

%description
Video player that can play online videos from youku, tudou etc.

%description -l zh_CN
一款可点播优酷, 土豆等网站在线视频的视频播放器.

%prep
%setup -q -n %{name}-%{commit}

%build
pushd src/
%qmake_qt5
%make_build

%install
pushd src/
%make_install INSTALL_ROOT=%{buildroot}
install -m 0755 %{name} %{buildroot}%{_bindir}
install -m 0644 %{S:1} %{buildroot}%{_datadir}/%{name}/plugins/
install -m 0644 %{S:2} %{buildroot}%{_datadir}/%{name}/plugins/
install -m 0644 %{S:3} %{buildroot}%{_datadir}/%{name}/plugins/
install -m 0644 %{S:4} %{buildroot}%{_datadir}/%{name}/plugins/

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

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.png

%changelog
* Sat Sep  9 2017 mosquito <sensor.wen@gmail.com> - 1.1.7-1.gite730f1c
- Update to 1.1.7

* Sat Mar 11 2017 mosquito <sensor.wen@gmail.com> - 0.75-1.git17140ab
- Update to 0.75

* Sat Feb 11 2017 mosquito <sensor.wen@gmail.com> - 0.73-1.git8b5e5f8
- Update to 0.73

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.69-1.gita418dc5
- Update version to 0.69-1.gita418dc5

* Tue Jan  3 2017 mosquito <sensor.wen@gmail.com> - 0.68-1.git7334b70
- Update version to 0.68-1.git7334b70

* Fri Sep  2 2016 mosquito <sensor.wen@gmail.com> - 0.66-1.git0ee65e5
- Update version to 0.66-1.git0ee65e5

* Mon Aug  1 2016 mosquito <sensor.wen@gmail.com> - 0.64-1.git3505479
- Update version to 0.64-1.git3505479

* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 0.63-1.git2f5c721
- Update version to 0.63-1.git2f5c721

* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 0.62-1.git704fc3e
- Update version to 0.62-1.git704fc3e

* Fri Jun  3 2016 mosquito <sensor.wen@gmail.com> - 0.61-1.git0b43fc7
- Update version to 0.61-1.git0b43fc7

* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 0.60-1.gitbc97d11
- Update version to 0.60-1.gitbc97d11

* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 0.59.1-1.gitc443df9
- Update version to 0.59.1-1.gitc443df9

* Tue Mar 22 2016 mosquito <sensor.wen@gmail.com> - 0.58-1.git7b465e3
- Update version to 0.58-1.git7b465e3

* Sat Feb 27 2016 mosquito <sensor.wen@gmail.com> - 0.57-1.gitb221910
- Update version to 0.57-1.gitb221910

* Thu Jan 28 2016 mosquito <sensor.wen@gmail.com> - 0.55-1.gitdbba642
- Update version to 0.55-1.gitdbba642

* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 0.54-1.gita2005f2
- Update version to 0.54-1.gita2005f2

* Sun Dec  6 2015 mosquito <sensor.wen@gmail.com> - 0.49-1.gitbbf096e
- Update version to 0.49-1.gitbbf096e

* Wed Jul 15 2015 mosquito <sensor.wen@gmail.com> - 0.34-1.gitc052050
- Update version to 0.34-1.gitc052050

* Wed Jul  1 2015 mosquito <sensor.wen@gmail.com> - 0.32-1.gitbc16926
- Update version to 0.32-1.gitbc16926

* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 0.29.1git20150117-1
- Update version to 0.29.1git20150117

* Thu Jan 15 2015 mosquito <sensor.wen@gmail.com> - 0.29git20150113-1
- Update version to 0.29git20150113

* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 0.28git20141226-1
- Update version to 0.28git20141226
- Add chinese summary

* Thu Nov 27 2014 mosquito <sensor.wen@gmail.com> - 0.27.1git20141126-1
- Update version to 0.27.1git20141126

* Sun Nov 16 2014 mosquito <sensor.wen@gmail.com> - 0.27git20141115-1
- update to 0.27git20141115

* Mon Oct 27 2014 mosquito <sensor.wen@gmail.com> - 0.26-2
- add depends

* Mon Oct 27 2014 mosquito <sensor.wen@gmail.com> - 0.26-1
- update to 0.26

* Sat Dec 28 2013 gcell <ph.linfan@gmail.com> - 0.17.2-1
- software rename to moonplayer && update

* Sat Dec 28 2013 gcell <ph.linfan@gmail.com> - 0.15.1-1
- update to 0.15.1

* Fri Dec 13 2013 gcell <ph.linfan@gmail.com> - 0.15-1
- The Initial Version
