Name:           deepin-music
Version:        3.1.8.3
Release:        1%{?dist}
Summary:        Deepin Music Player
Summary(zh_CN): 深度音乐播放器
License:        GPLv3
Url:            https://github.com/linuxdeepin/deepin-music
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python
BuildRequires:  desktop-file-utils
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(dtkcore)
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(icu-uc)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libcue)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Sql)
BuildRequires:  pkgconfig(Qt5Xml)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(Qt5Multimedia)
Provides:       deepin-music-player%{?_isa} = %{version}-%{release}

%description
Deepin Music Player with brilliant and tweakful UI Deepin-UI based,
gstreamer front-end, with features likes search music by pinyin,
quanpin, colorful lyrics supports, and more powerful functions
you will found.

%description -l zh_CN
深度音乐播放器界面基于 Deepin-UI , 后端使用 gstreamer ,
其他特性如音乐搜索, 丰富多彩的歌词支持, 更多功能等待您发现.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q
sed -i 's|lrelease|lrelease-qt5|g' tool/translate_generation.*
sed -i '/%1/s|lib|%{_lib}|' music-player/core/pluginmanager.cpp
sed -i '/target.path/s|lib|%{_lib}|' libdmusic/libdmusic.pro \
    plugin/netease-meta-search/netease-meta-search.pro \
    vendor/src/dbusextended-qt/src/src.pro \
    vendor/src/mpris-qt/src/src.pro

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post
/sbin/ldconfig
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%doc AUTHORS README.md
%license COPYING
%{_bindir}/%{name}
%{_libdir}/lib*.so.*
%{_libdir}/%{name}/plugins/lib*.so.*
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files devel
%{_includedir}/DBusExtended/
%{_includedir}/MprisQt/
%{_qt5_archdatadir}/mkspecs/features/*-qt5.prf
%{_libdir}/lib*.so
%{_libdir}/%{name}/plugins/lib*.so
%{_libdir}/pkgconfig/*-qt5.pc

%changelog
* Fri Jul 20 2018 mosquito <sensor.wen@gmail.com> - 3.1.8.3-1
- Update to 3.1.8.3

* Tue Mar 20 2018 mosquito <sensor.wen@gmail.com> - 3.1.8.1-1
- Update to 3.1.8.1

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 3.1.7.2-1
- Update to 3.1.7.2

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 3.1.6.2-1
- Update to 3.1.6.2

* Thu Sep 21 2017 mosquito <sensor.wen@gmail.com> - 3.1.6-1
- Update to 3.1.6

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 3.1.5-1
- Update to 3.1.5

* Sun Aug 6 2017 Zamir SUN <sztsian@gmail.com> - 3.1.4-2
- Remove group tag

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.4-1.git7c31a72
- Update to 3.1.4

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.1.0-1.git901b8a3
- Update to 3.1.0

* Sat Jan 21 2017 mosquito <sensor.wen@gmail.com> - 3.0.1-1.git5110780
- Update to 3.0.1

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.3.2-1.git76f52e9
- Update to 2.3.2-1.git76f52e9

* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 2.3.0-1.gitc43b01d
- Update version to 2.3.0-1.gitc43b01d

* Wed Dec 31 2014 mosquito <sensor.wen@gmail.com> - 2.0git20141231-1
- Update version to 2.0git20141231

* Mon Dec 15 2014 mosquito <sensor.wen@gmail.com> - 2.0git20141209-1
- Update version to 2.0git20141209

* Thu Nov 27 2014 mosquito <sensor.wen@gmail.com> - 2.0git20141127-1
- Update version to 2.0git20141127

* Tue Nov 18 2014 mosquito <sensor.wen@gmail.com> - 2.0git20141117-1
- Update version to 2.0git20141117

* Wed Nov 5 2014 mosquito <sensor.wen@gmail.com> - 2.0git20141104-1
- Update to 2.0git20141104

* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 2.0git20140922-2
- Update translation

* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 2.0git20140922-1
- Update to 2.0git20140922

* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 2.0git20140916-1
- Rebuild for fedora and rhel

* Sat Jul 5 2014 hillwood@linuxfans.org
- Add python-gstreamer-0_10 as Requires.

* Sun May 25 2014 hillwood@linuxfans.org
- Update to 2.0git20140505.
  Feature update.

* Wed Aug 14 2013 hillwood@linuxfans.org
- add deepin-gsettings as Requires

* Wed Aug 14 2013 hillwood@linuxfans.org
- update to 2.0git20130802
  * upsteam did not provide changlog

* Sun Apr 28 2013 hillwood@linuxfans.org
- update to 1.0.1git20130330(2.0 Alpha)
  * fix bugs

* Tue Mar 19 2013 douglarek@outlook.com
- Bug fix
  * fix bnc#808258

* Sun Feb 24 2013 kaji331@hotmail.com
- fix require python-cddb to python-CDDB

* Tue Feb 5 2013 hillwood@linuxfans.org
- update to 1.0.1git20130125(2.0 Alpha)
  * add plugins support
  * add mini mode
  * more media formats support

* Mon Jan 7 2013 douglarek@outlook.com
- Add runtime dependence: python-gtk

* Wed Sep 26 2012 hillwood@linuxfans.org
- update to 1.0.1git20120911
- fix bnc#778659
- more changlog please see http://goo.gl/WCVGo

* Mon Sep 3 2012 hillwood@linuxfans.org
- license update: GPL-3.0+

* Mon Sep 3 2012 hillwood@linuxfans.org
- add python-chardet , python-imaging and python-xlib as require
  packages.

* Sun Sep 2 2012 hillwood@linuxfans.org
- Initial package 1.0git20120716
  Init.
  Implement logging to tracking events that happen.
  Implement a basic configuration.
  Use listen-music-player play kernel, and thank him for his.
  Determine the Audio file type is supported.
  Add Universal encoding detector of the chardet.
