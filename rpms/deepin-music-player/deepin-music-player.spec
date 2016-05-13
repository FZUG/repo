%global debug_package %{nil}
%global project deepin-music
%global repo %{project}

# commit
%global _commit c43b01d5457f9a31c14c81e28247ad72d3b4ee0e
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global option_plugins 1
%global bd_repo dmusic-plugin-baidumusic
%global bd_commit ad7dbfc25690c9f7a585c156a9a2a9b5d66e6900
%global bd_scommit %(c=%{bd_commit}; echo ${c:0:7})
%global nm_repo dmusic-plugin-NeteaseCloudMusic
%global nm_commit f10a4bcae8a7cd29f8a488bb5ee134b603eea091
%global nm_scommit %(c=%{nm_commit}; echo ${c:0:7})

Name:		deepin-music-player
Version:	2.3.0
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Deepin Music Player
Summary(zh_CN):	深度音乐播放器

License:	GPLv3
Group:		Applications/Multimedia
Url:		https://github.com/linuxdeepin/deepin-music
Source0:	https://github.com/linuxdeepin/deepin-music/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source1:	https://github.com/sumary/dmusic-plugin-baidumusic/archive/%{bd_commit}/%{bd_repo}-%{bd_scommit}.tar.gz
Source2:	https://github.com/wu-nerd/dmusic-plugin-NeteaseCloudMusic/archive/%{nm_commit}/%{nm_repo}-%{nm_scommit}.tar.gz

BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	desktop-file-utils
BuildRequires:	hicolor-icon-theme
BuildRequires:	gettext
Requires:	deepin-ui
Requires:	scipy
Requires:	pygtk2
Requires:	python-xlib
Requires:	python-pillow
Requires:	python-CDDB
Requires:	python-pycurl
Requires:	python-pyquery
Requires:	python-chardet
Requires:	python-mutagen
Requires:	python-keybinder
Requires:	gstreamer-python
Requires:	gstreamer-plugins-good
Requires:	gstreamer-plugins-bad
Requires:	gstreamer-ffmpeg
Requires:	gstreamer-plugins-ugly
%if 0%{?option_plugins}
Requires:	pyjavascriptcore
%endif

%description
Deepin Music Player with brilliant and tweakful UI Deepin-UI based,
gstreamer front-end, with features likes search music by pinyin,
quanpin, colorful lyrics supports, and more powerful functions
you will found.

%description -l zh_CN
深度音乐播放器界面基于 Deepin-UI , 后端使用 gstreamer ,
其他特性如音乐搜索, 丰富多彩的歌词支持, 更多功能等待您发现.

%prep
%setup -q -b0 -n %{repo}-%{_commit}
%if 0%{?option_plugins}
%setup -q -a1 -a2 -n %{repo}-%{_commit}
%endif

%build

%install
install -d %{buildroot}%{_datadir}/{applications,icons,%{name}}
install -m 644 %{name}.desktop %{buildroot}%{_datadir}/applications/
cp -r {app_theme,image,plugins,skin,src,wizard} %{buildroot}%{_datadir}/%{name}

# generate locale
pushd locale
for i in `ls *.po`
 do
    mkdir -p %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/
    msgfmt $i -o %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/%{name}.mo
 done
popd

# install icons
for i in 16x16 24x24 48x48 64x64 96x96; do
  install -D image/hicolor/$i/apps/%{name}.png \
    %{buildroot}%{_datadir}/icons/hicolor/$i/apps/%{name}.png
done
install -D image/hicolor/scalable/apps/%{name}.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# link exec file
install -d %{buildroot}%{_bindir}
ln -sfv %{_datadir}/%{name}/src/main.py %{buildroot}%{_bindir}/%{name}
chmod 755 %{buildroot}%{_datadir}/%{name}/src/*.py

# install plugins
%if 0%{?option_plugins}
cp -r %{bd_repo}-%{bd_commit}/baidumusic %{buildroot}%{_datadir}/%{name}/plugins/
cp -r %{nm_repo}-%{nm_commit}/neteasecloudmusic %{buildroot}%{_datadir}/%{name}/plugins/
%endif

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md ChangeLog
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/%{name}
%{_bindir}/%{name}

%changelog
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
