# https://github.com/memeco/osd-lyrics/blob/master/fedora/osdlyrics.spec
%global debug_package %{nil}
%global project osdlyrics
%global repo %{project}

%global _commit 33f67b4217241e10f7accbb7a7e3514e04be342c
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    osdlyrics
Version: 0.4.3
Release: 1.git%{_shortcommit}%{?dist}
Summary: A third-party lyrics display program

Group:   Applications/Multimedia
License: GPLv3
Url:     https://github.com/PedroHLC/osdlyrics
Source0: https://github.com/PedroHLC/osdlyrics/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: automake
BuildRequires: pkgconfig
BuildRequires: gtk2-devel
BuildRequires: libX11-devel
BuildRequires: dbus-glib-devel
BuildRequires: libcurl-devel
BuildRequires: libnotify-devel
BuildRequires: sqlite-devel
BuildRequires: libmpd-devel
BuildRequires: xmms2-devel
BuildRequires: libappindicator-devel
BuildRequires: intltool libtool
BuildRequires: gettext-devel

%description
OSD Lyrics is a lyrics show compatible with various media players.
It is not a plugin but a standalone program. OSD Lyrics shows lyrics
on your desktop, in the style similar to KaraOK. It also provides
another displaying style, in which lyrics scroll from bottom to top.
OSD Lyrics can download lyrics from the network automatically.

Support players:
  Amarok, Audacious, Banshee, Clementine, Deadbeef
  Deciber, Exaile, Guayadeque, Gmusicbrowser, Juk
  Listen, MOC, Muine, Qmmp, Quod Libet, Rhythmbox
  Songbird, VLC, XMMS2

%description -l zh_CN
OSD Lyrics 是一款独立的第三方歌词显示程序. 它支持多款音乐播放器,
可以在您的桌面上以竖排或卡拉OK效果显示歌词. 支持自动从网络下载歌词.

%prep
%setup -q -n %repo-%{_commit}

%build
autoreconf --install
%configure
make %{?_smp_mflags}

%install
%make_install

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog README* NEWS
%license COPYING
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/*/%{name}*
%{_datadir}/%{name}/

%changelog
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 0.4.3-1.git33f67b4
- Update version to 0.4.3-1.git33f67b4

* Tue Nov  4 2014 mosquito <sensor.wen@gmail.com> - 0.4.3git20141101-1
- Update version to 0.4.3git20141101

* Wed Sep 24 2014 mosquito <sensor.wen@gmail.com> - 0.4.3git20130927-1
- Rebuild for fedora

* Fri Nov 16 2012 aj@suse.de
- Fix missing include (add patch patches/osdlyrics-includes.patch).

* Mon Jun  4 2012 hillwood@linuxfans.org
- update to 0.4.3
  * Player support:
  - Add cmus support, thanks to alepulver (not enable)
  * Bug fix:
  - Dir is not closed in _prepend_subdirs (ol_app_info.c)
  - Show player chooser if connected player quits in 1 minute

* Thu Mar  1 2012 hillwood@linuxfans.org
- add xmms2 spport
- split the translations in a lang subpackage
- rename patch file
- fixed some RPMLINT report warnings

* Mon Feb 13 2012 coolo@suse.com
- patch license to follow spdx.org standard

* Thu Jan 19 2012 hillwood@linuxfans.org
- update to 0.4.2
  * UI improvements:
  - Player choose dialog redesigned
  - Fade out on the edge of lyric text in OSD mode if it is too long
  - Drag-to-seek in scrolling mode
  * Player support:
  - Bring back support for Rhythmbox prior to 0.13
  - Support RhythmCat
  - Auto-detect the launch command for Audacious 2 and 3
  - Do not require root privilege to launch MPD
  * Bug fixes:
  - Blurring in OSD mode will not cause a frame around lyrics
  - Fix compilation issue in BDS systems.
  - Fix track duration in MPRIS support
  - Deal with player launch commands with %%f or %%U as arguments
  - ttPlayer engine can search lyrics with ' in the title
  - CUE sheets are supported now
  - Don't show invalid search result of Xiami engine

* Fri Dec  9 2011 hillwood@linuxfans.org
- Fix %%post* , change the license to "GPL-3.0".

* Sun Nov 13 2011 hillwood@linuxfans.org
- support openSUSE 12.1

* Mon Jul 18 2011 hillwood@linuxfans.org
- Uptate to 0.4.1
- Choose player if no supported player running on launch
- Outline blur on OSD mode
- Support all MPRIS-compatible players
- New lyrics search site: xiami.com
- Fix ttPlayer search
- Search lyrics from more than one sites
- All files with the name of osd-lyrics are replaced to osdlyrics

* Sat Jul  9 2011 hillwood@linuxfans.org
- rewrite description.

* Mon Jun 27 2011 hillwood@linuxfans.org
- rename the package name.

* Sun Jun 26 2011 hillwood@linuxfans.org
- add support for Fedora and Mandriva.

* Fri Jun 10 2011 hillwood@linuxfans.org
- Uptate to 0.4.0

* Sun May 29 2011 hillwood@linuxfans.org
- Uptate to 0.4.0b1

* Wed Apr 20 2011 hillwood@linuxfans.org
- Rebuild package for opensuse and SLE.

* Sun Jun 13 2010 Robin Lee <robinlee.sysu@gmail.com> - 0.3.20100604-2
- Spec file massive rewritten
- Updated to 0.3.20100604

* Wed Jun 09 2010 Liang Suilong <liangsuilong@gmail.com> - 0.3.20100604-1
- Add Juk and Qmmp support
- Add app indicator support for Ubuntu 10.04
- Add singleton detection
- Honor MPD_HOST and MPD_PORT environment variables for MPD
- The `mouse click through' feature is back for GTK+ 2.20 users
- The appearance under a window manager without compositing support is correct now
- It won't crash now when you open the lyric assign dialog more than once
- The first line of lyric will not be lost when there is a BOM of utf-8 in the file.
- Fix that the last lyric doesn't get its progress with Rhythmbox.

* Wed Mar 31 2010 Liang Suilong <liangsuilong@gmail.com> - 0.3.20100330-1
- Download lyrics from MiniLyrics
- Player control on background panel of OSD Window
- Encoding detection of LRC files
- Display player icon in notification
- FIX: Can not hide OSD Window
- FIX: Advance/delay offset doesn't work from popup menu
- Some minor fixes
- Drop amarok-1.4 support

* Fri Feb 12 2010 Liang Suilong <liangsuilong@gmail.com> - 0.3.20100212-1
- Choose which lyric to download if there are more than one candidates
- Search lyrics manually
- Adjust lyric delay
- Support Quod Libet
- Display track infomation on tooltip of the trayicon
- Show notification of track infomation on track change
- Launch prefered player if no supported player is running
- A more graceful background on OSD Window
- Use themeable icons
- FIX: Crashes when hiding OSD Window under some distribution

* Tue Feb 02 2010 Liang Suilong <liangsuilong@gmail.com> - 0.2.20100201-1
- FIX The program will not crash when DNS lookup timeout
  on searching or downloading lyrics

* Sat Jan 09 2010 Liang Suilong <liangsuilong@gmail.com> - 0.2.20100109-1
- Add MOC support
- Fix dowloading fails when title or artist is not set

* Wed Dec 30 2009 Liang Suilong <liangsuilong@gmail.com> - 0.2.20091227-1
- Add mpd support
- Add BR: libmpd-devel
- Enable Amarok 1.4 support

* Tue Sep 22 2009 Liang Suilong <liangsuilong@gmail.com> - 0.2.20090919-2
- Add gettext-devel as BuildRequires

* Sat Sep 19 2009 Liang Suilong <liangsuilong@gmail.com> - 0.2.20090919-1
- Inital package for Fedora
