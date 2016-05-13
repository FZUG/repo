%global debug_package %{nil}
%global _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/fcitx.conf
%{!?gtk2_binary_version: %global gtk2_binary_version %(pkg-config --variable=gtk_binary_version gtk+-2.0)}
%{!?gtk3_binary_version: %global gtk3_binary_version %(pkg-config --variable=gtk_binary_version gtk+-3.0)}

Name:    fcitx
Version: 4.2.9.1
Release: 1%{?dist}
Summary: An input method framework
Summary(zh_CN): 一个轻量级输入法框架
License: GPLv2+
Group:   User Interface/Desktops
URL:     https://fcitx-im.org/wiki/Fcitx
Source0: http://download.fcitx-im.org/fcitx/%{name}-%{version}_dict.tar.xz
Source1: xinput-%{name}

BuildRequires: pango-devel, dbus-devel, opencc-devel
BuildRequires: wget, intltool, chrpath, sysconftool
BuildRequires: cmake, libtool, doxygen, libicu-devel
BuildRequires: qt4-devel, gtk3-devel, gtk2-devel
BuildRequires: xorg-x11-proto-devel, xorg-x11-xtrans-devel
BuildRequires: gobject-introspection-devel, libxkbfile-devel
BuildRequires: enchant-devel, iso-codes-devel
BuildRequires: libX11-devel, dbus-glib-devel, dbus-x11
BuildRequires: desktop-file-utils, libxml2-devel
BuildRequires: lua-devel, extra-cmake-modules
Requires: %{name}-data = %{version}-%{release}
Requires: imsettings
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-gtk3 = %{version}-%{release}
Requires: %{name}-gtk2 = %{version}-%{release}
Requires(post): %{_sbindir}/alternatives
Requires(postun): %{_sbindir}/alternatives

%description
Fcitx is an input method framework with extension support. Currently it
supports Linux and Unix systems like FreeBSD.

Fcitx tries to provide a native feeling under all desktop as well as a light
weight core. You can easily customize it to fit your requirements.

%description -l zh_CN
Fcitx 是一个支持扩展的输入法框架. 目前支持 Linux 和 Unix 系统 (如 FreeBSD).

Fcitx 致力于为所有桌面环境提供一致的操作体验, 这一切都基于其轻量级的内核.
您可以轻松地进行定制以符合您的需求.

%package data
Summary: Data files of Fcitx
Summary(zh_CN): Fcitx 数据文件
Group: System Environment/Libraries
BuildArch: noarch
Requires: hicolor-icon-theme
Requires: dbus

%description data
The %{name}-data package provides shared data for Fcitx.

%description data -l zh_CN
此 %{name}-data 包为 Fcitx 提供数据文件.

%package libs
Summary: Shared libraries for Fcitx
Summary(zh_CN): Fcitx 共享库
Group: System Environment/Libraries
Provides: %{name}-keyboard = %{version}-%{release}
Obsoletes: %{name}-keyboard =< 4.2.3

%description libs
The %{name}-libs package provides shared libraries for Fcitx

%description libs -l zh_CN
此 %{name}-libs 包为 Fcitx 提供应用程序库.

%package devel
Summary: Development files for Fcitx
Summary(zh_CN): Fcitx 开发文件
Group: Development/Libraries
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: libX11-devel

%description devel
The %{name}-devel package contains libraries and header files necessary for
developing programs using Fcitx libraries.

%description devel -l zh_CN
此 %{name}-devel 包包含使用 Fcitx 库开发应用程序,
所必须使用的程序库和头文件.

%package table-chinese
Summary: Chinese table of Fcitx
Summary(zh_CN): Fcitx 中文码表
Group: System Environment/Libraries
BuildArch: noarch
Requires: %{name}-table = %{version}-%{release}

%description table-chinese
The %{name}-table-chinese package provides other Chinese table for Fcitx.

%description table-chinese -l zh_CN
此 %{name}-table-chinese 包为 Fcitx 提供其他中文码表.

%package gtk2
Summary: Fcitx IM module for gtk2
Summary(zh_CN): Fcitx gtk2 输入模块
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description gtk2
This package contains Fcitx IM module for gtk2.

%description gtk2 -l zh_CN
此包包含 Fcitx gtk2 输入模块.

%package gtk3
Summary: Fcitx IM module for gtk3
Summary(zh_CN): Fcitx gtk3 输入模块
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: imsettings-gnome

%description gtk3
This package contains Fcitx IM module for gtk3.

%description gtk3 -l zh_CN
此包包含 Fcitx gtk3 输入模块.

%package qt4
Summary: Fcitx IM module for qt4
Summary(zh_CN): Fcitx qt4 输入模块
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description qt4
This package contains Fcitx IM module for qt4.

%description qt4 -l zh_CN
此包包含 Fcitx qt4 输入模块.

%package pinyin
Summary: Pinyin Engine for Fcitx
Summary(zh_CN): Fcitx 拼音引擎
URL: https://fcitx-im.org/wiki/Built-in_Pinyin
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-data = %{version}-%{release}

%description pinyin
This package contains pinyin engine for Fcitx.

%description pinyin -l zh_CN
此包包含 Fcitx 拼音引擎.

%package qw
Summary: Quwei Engine for Fcitx
Summary(zh_CN): Fcitx 区位引擎
URL: https://fcitx-im.org/wiki/QuWei
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-data = %{version}-%{release}

%description qw
This package contains Quwei engine for Fcitx.

%description qw -l zh_CN
此包包含 Fcitx 区位引擎.

%package table
Summary: Table Engine for Fcitx
Summary(zh_CN): Fcitx 码表引擎
URL: https://fcitx-im.org/wiki/Table
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: %{name}-data = %{version}-%{release}
Requires: %{name}-pinyin = %{version}-%{release}

%description table
This package contains table engine for Fcitx.

%description table -l zh_CN
此包包含 Fcitx 码表引擎.

%prep
%setup -q

%build
mkdir build
pushd build
%cmake .. \
       -DENABLE_GTK3_IM_MODULE=On \
       -DENABLE_QT_IM_MODULE=On \
       -DENABLE_OPENCC=On \
       -DENABLE_LUA=On \
       -DENABLE_GIR=On \
       -DENABLE_XDGAUTOSTART=Off
make VERBOSE=1 %{?_smp_mflags}

%install
%make_install INSTALL="install -p" -C build
find %{buildroot}%{_libdir} -name '*.la' -delete -print

install -pm 644 -D %{SOURCE1} %{buildroot}%{_xinputconf}

# patch fcitx4-config to use pkg-config to solve libdir to avoid multiarch
# confilict
sed -i -e 's:%{_libdir}:`pkg-config --variable=libdir fcitx`:g' \
  %{buildroot}%{_bindir}/fcitx4-config

chmod +x %{buildroot}%{_datadir}/%{name}/data/env_setup.sh

%find_lang %{name}

desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}-skin-installer.desktop

desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}-configtool.desktop

desktop-file-install --delete-original \
  --dir %{buildroot}%{_datadir}/applications \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
%{_sbindir}/alternatives --install %{_sysconfdir}/X11/xinit/xinputrc xinputrc %{_xinputconf} 55 || :
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ "$1" = "0" ]; then
  %{_sbindir}/alternatives --remove xinputrc %{_xinputconf} || :
  # if alternative was set to manual, reset to auto
  [ -L %{_sysconfdir}/alternatives/xinputrc -a "`readlink %{_sysconfdir}/alternatives/xinputrc`" = "%{_xinputconf}" ] && %{_sbindir}/alternatives --auto xinputrc || :
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%post data
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun data
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans data
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%post gtk2
%{_bindir}/update-gtk-immodules %{_host} || :

%postun gtk2
%{_bindir}/update-gtk-immodules %{_host} || :

%post gtk3
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :

%postun gtk3
%{_bindir}/gtk-query-immodules-3.0-%{__isa_bits} --update-cache || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog THANKS TODO
%license COPYING
%config %{_xinputconf}
%{_bindir}/fcitx-*
%{_bindir}/fcitx
%{_bindir}/createPYMB
%{_bindir}/mb2org
%{_bindir}/mb2txt
%{_bindir}/readPYBase
%{_bindir}/readPYMB
%{_bindir}/scel2org
%{_bindir}/txt2mb
%{_datadir}/applications/%{name}-skin-installer.desktop
%dir %{_datadir}/%{name}/dbus/
%{_datadir}/%{name}/dbus/daemon.conf
%{_datadir}/applications/%{name}-configtool.desktop
%{_datadir}/applications/%{name}.desktop
%{_datadir}/mime/packages/x-fskin.xml
%{_docdir}/%{name}/
%{_mandir}/man1/createPYMB.1*
%{_mandir}/man1/fcitx-remote.1*
%{_mandir}/man1/fcitx.1*
%{_mandir}/man1/mb2org.1*
%{_mandir}/man1/mb2txt.1*
%{_mandir}/man1/readPYBase.1*
%{_mandir}/man1/readPYMB.1*
%{_mandir}/man1/scel2org.1*
%{_mandir}/man1/txt2mb.1*

%files libs
%defattr(-,root,root,-)
%license COPYING
%{_libdir}/libfcitx*.so.*
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/%{name}-[!pqt]*.so
%{_libdir}/%{name}/%{name}-punc.so
%{_libdir}/%{name}/%{name}-quickphrase.so
%{_libdir}/%{name}/qt/
%{_libdir}/%{name}/libexec/
%dir %{_libdir}/girepository-1.0/
%{_libdir}/girepository-1.0/Fcitx-1.0.typelib

%files data
%defattr(-,root,root,-)
%license COPYING
%{_datadir}/icons/hicolor/16x16/apps/*.png
%{_datadir}/icons/hicolor/22x22/apps/*.png
%{_datadir}/icons/hicolor/24x24/apps/*.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/*.svg
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/skin/
%dir %{_datadir}/%{name}/addon
%{_datadir}/%{name}/addon/%{name}-[!pqt]*.conf
%{_datadir}/%{name}/addon/%{name}-punc.conf
%{_datadir}/%{name}/addon/%{name}-quickphrase.conf
%{_datadir}/%{name}/data/
%{_datadir}/%{name}/spell/
%dir %{_datadir}/%{name}/imicon/
%dir %{_datadir}/%{name}/inputmethod/
%dir %{_datadir}/%{name}/configdesc/
%dir %{_datadir}/%{name}/table/
%{_datadir}/%{name}/configdesc/[!ft]*.desc
%{_datadir}/%{name}/configdesc/fcitx-[!p]*.desc
%{_datadir}/dbus-1/services/org.fcitx.Fcitx.service

%files devel
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog THANKS TODO
%license COPYING
%{_bindir}/fcitx4-config
%{_libdir}/libfcitx*.so
%{_libdir}/pkgconfig/fcitx*.pc
%{_includedir}/fcitx*
%{_datadir}/cmake/%{name}/
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Fcitx-1.0.gir

%files table-chinese
%defattr(-,root,root,-)
%{_datadir}/%{name}/table/*
%{_datadir}/%{name}/imicon/[!ps]*.png

%files pinyin
%defattr(-,root,root,-)
%{_datadir}/%{name}/inputmethod/pinyin.conf
%{_datadir}/%{name}/inputmethod/shuangpin.conf
%{_datadir}/%{name}/pinyin/
%{_datadir}/%{name}/configdesc/fcitx-pinyin.desc
%{_datadir}/%{name}/configdesc/fcitx-pinyin-enhance.desc
%{_datadir}/%{name}/addon/fcitx-pinyin.conf
%{_datadir}/%{name}/addon/fcitx-pinyin-enhance.conf
%{_datadir}/%{name}/imicon/pinyin.png
%{_datadir}/%{name}/imicon/shuangpin.png
%{_libdir}/%{name}/%{name}-pinyin.so
%{_libdir}/%{name}/%{name}-pinyin-enhance.so
%{_datadir}/%{name}/py-enhance/

%files qw
%defattr(-,root,root,-)
%{_datadir}/%{name}/inputmethod/qw.conf
%{_libdir}/%{name}/%{name}-qw.so
%{_datadir}/%{name}/addon/fcitx-qw.conf

%files table
%defattr(-,root,root,-)
%{_datadir}/%{name}/configdesc/table.desc
%{_libdir}/%{name}/%{name}-table.so
%{_datadir}/%{name}/addon/fcitx-table.conf

%files gtk2
%defattr(-,root,root,-)
%{_libdir}/gtk-2.0/%{gtk2_binary_version}/immodules/im-fcitx.so

%files gtk3
%defattr(-,root,root,-)
%{_libdir}/gtk-3.0/%{gtk3_binary_version}/immodules/im-fcitx.so

%files qt4
%defattr(-,root,root,-)
%{_libdir}/qt4/plugins/inputmethods/qtim-fcitx.so

%changelog
* Sun Jan 17 2016 mosquito <sensor.wen@gmail.com> - 4.2.9.1-1
- Update to 4.2.9.1

* Mon Aug 31 2015 mosquito <sensor.wen@gmail.com> - 4.2.9-1
- Update to 4.2.9

* Wed Feb 04 2015 mosquito <sensor.wen@gmail.com> - 4.2.8.5git20150203-1
- Update version to 4.2.8.5git20150203

* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 4.2.8.5git20141209-1
- Update version to 4.2.8.5git20141209

* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 4.2.8.5git20141127-1
- Update version to 4.2.8.5git20141127

* Thu Nov 6 2014 mosquito <sensor.wen@gmail.com> - 4.2.8.5git20141105-1
- update to 4.2.8.5git20141105

* Wed Nov 5 2014 mosquito <sensor.wen@gmail.com> - 4.2.8.5git20140928-1
- update to 4.2.8.5git20140928

* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 4.2.8.5git20140918-1
- update to 4.2.8.5git20140918
- rebuild for rhel 7

* Sun Sep 14 2014 mosquito <sensor.wen@gmail.com> - 4.2.8.4git20140912-1
- rebuild for rhel 7

* Tue Sep 09 2014 Rex Dieter <rdieter@fedoraproject.org> 4.2.8.4-6
- update scriptlets (mime mostly), tighten subpkg deps, BR: qt4-devel

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 4.2.8.4-5
- rebuild for ICU 53.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 4.2.8.4-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Robin Lee <cheeselee@fedoraproject.org> - 4.2.8.4-1
- Update to 4.2.8.4

* Fri Feb 14 2014 Parag Nemade <paragn AT fedoraproject DOT org> - 4.2.8.3-2
- Rebuild for icu 52

* Tue Oct 29 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.8.3-1
- Update to 4.2.8.3
- Update summary of fcitx package
- Other minor spell fixes

* Fri Aug 23 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.8-3
- Own some missed directories
- Update URL's and Source0 URL
- Revise description following upstream wiki

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul  2 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.8-1
- Update to 4.2.8 (https://www.csslayer.info/wordpress/fcitx-dev/fcitx-4-2-8/)
- Add scriptlets to update icon cache (BZ#980309)

* Fri Jun 21 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-6
- Move fcitx4-config to devel package and patch it to use pkg-config to solve
  libdir
- devel subpackage explicitly requires pkgconfig

* Fri Jun 21 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-5
- Move fcitx4-config to base package to solve multiarch devel subpackage conflict

* Wed Jun 19 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-4
- BR: lua-devel (BZ#974729)
- Move %%{_datadir}/gir-1.0/Fcitx-1.0.gir %%{_bindir}/fcitx4-config to devel
  subpackage (BZ#965914)
- Co-own %%{_datadir}/gir-1.0/, %%{_libdir}/girepository-1.0/
- Own %%{_libdir}/%%{name}/qt/, %%{_libdir}/%%{name}/
- Other minor cleanup

* Mon Apr 29 2013 Robin Lee <cheeselee@fedoraproject.org> - 4.2.7-3
- Fix gtk2 subpackage description (#830377)

* Sat Mar 23 2013 Liang Suilong <liangsuilong@gmail.com> - 4.2.7-2
- Fix to enable Lua support

* Fri Feb 01 2013 Liang Suilong <liangsuilong@gmail.com> - 4.2.7-1
- Upstream to fcitx-4.2.7

* Sat Jan 26 2013 Kevin Fenzi <kevin@scrye.com> 4.2.6.1-3
- Rebuild for new icu

* Mon Nov 26 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.6.1-2
- Disable xdg-autostart

* Wed Oct 31 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.6.1-1
- Upstream to fcitx-4.2.6.1

* Sun Jul 22 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.5-1
- Upstream to fcitx-4.2.5

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.4-2
- Drop fcitx-keyboard
- Divide Table Engine into fcitx-table
- Move GIR Binding into fcitx-libs

* Tue Jun 05 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.4-1
- Upgrade to fcitx-4.2.4
- Fix the ownership conflict on fcitx and fcitx-data
- Divide Pinyin engine into fcitx-pinyin
- Divide Quwei engine into fcitx-qw
- Divide XKB integration into fcitx-keyboard

* Mon May 07 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.3-1
- Upgrade to fcitx-4.2.3

* Thu Apr 26 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.2-2
- Upgrade to fcitx-4.2.2

* Sun Apr 22 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.2-1
- Upgrade to fcitx-4.2.2

* Sat Feb 04 2012 Liang Suilong <liangsuilong@gmail.com> - 4.2.0-1
- Upgrade to fcitx-4.2.0

* Sun Dec 25 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.2-3
- Fix the spec

* Sun Dec 25 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.2-2
- Fix the spec

* Sun Dec 25 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.2-1
- Update to 4.1.2
- move fcitx4-config to devel

* Fri Sep 09 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.1-2
- Update xinput-fcitx
- Add fcitx-gtk3 as fcitx requires

* Fri Sep 09 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.1-1
- Upstream to fcitx-4.1.1

* Fri Sep 09 2011 Liang Suilong <liangsuilong@gmail.com> - 4.1.0-1
- Upstream to fcitx-4.1.0
- Add fcitx-gtk2 as FCITX im module for gtk2
- Add fcitx-gtk3 as FCITX im module for gtk3
- Add fcitx-qt4 as FCITX im module for qt4

* Tue Aug 02 2011 Liang Suilong <liangsuilong@gmail.com> - 4.0.1-5
- Fix that %%files lists a wrong address
- Separate fcitx-libs again

* Tue Aug 02 2011 Liang Suilong <liangsuilong@gmail.com> - 4.0.1-4
- Separates varieties of tables from FCITX
- Merge fcitx-libs into fcitx

* Sun Jul 03 2011 Liang Suilong <liangsuilong@gmail.com> - 4.0.1-3
- Support GNOME 3 tray icon
- Fix that main window is covered by GNOME Shell

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 19 2010 Chen Lei <supercyper@163.com> - 4.0.0-1
- Update to 4.0.0

* Mon Jun 14 2010 Chen Lei <supercyper@163.com> - 3.6.3-5.20100514svn_utf8
- Remove BR:libXext-devel

* Fri May 14 2010 Chen Lei <supercyper@163.com> - 3.6.3-4.20100514svn_utf8
- svn 365

* Sun Apr 18 2010 Chen Lei <supercyper@163.com> - 3.6.3-3.20100410svn_utf8
- Exclude xpm files

* Sat Apr 17 2010 Chen Lei <supercyper@163.com> - 3.6.3-2.20100410svn_utf8
- Update License tag
- Add more explanation for UTF-8 branch

* Mon Apr 12 2010 Chen Lei <supercyper@163.com> - 3.6.3-1.20100410svn_utf8
- Initial Package
