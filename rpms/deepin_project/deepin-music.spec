%global _commit 76f52e97d443a6851fe6439d27194af3190748b9
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global option_plugins 1
%global bd_repo dmusic-plugin-baidumusic
%global bd_commit 319ded887f7944a9bee0339e6d767f6640994b1d
%global bd_scommit %(c=%{bd_commit}; echo ${c:0:7})
%global nm_repo dmusic-plugin-NeteaseCloudMusic
%global nm_commit 503701ce6c2c4d94f1fcd40a158c7a0077861793
%global nm_scommit %(c=%{nm_commit}; echo ${c:0:7})

Name:           deepin-music
Version:        2.3.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Music Player
Summary(zh_CN): 深度音乐播放器

License:        GPLv3
Group:          Applications/Multimedia
Url:            https://github.com/linuxdeepin/deepin-music
Source0:        https://github.com/linuxdeepin/deepin-music/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz
Source1:        https://github.com/sumary/dmusic-plugin-baidumusic/archive/%{bd_commit}/%{bd_repo}-%{bd_scommit}.tar.gz
Source2:        https://github.com/wu-nerd/dmusic-plugin-NeteaseCloudMusic/archive/%{nm_commit}/%{nm_repo}-%{nm_scommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
BuildRequires:  deepin-gettext-tools
BuildRequires:  gettext
Requires:       python2-deepin-ui
Requires:	      scipy
Requires:	      pygtk2
Requires:	      python-xlib
Requires:	      python2-pillow
Requires:	      python-CDDB
Requires:       dbus-python
Requires:	      python-pycurl
Requires:       python-pyquery
Requires:       python-chardet
Requires:       python-mutagen
Requires:       python-keybinder
Requires:       gstreamer-python
Requires:       gstreamer-ffmpeg
Requires:       gstreamer-plugins-good
Requires:       gstreamer-plugins-bad
Requires:       gstreamer-plugins-ugly
%if 0%{?option_plugins}
# Baidu Music
Requires:       python2-javascriptcore
# Netease Cloud Music
Requires:       python2-requests
Requires:       python2-crypto
%endif
Provides:       deepin-music-player = %{version}-%{release}
Obsoletes:      deepin-music-player < %{version}-%{release}

%description
Deepin Music Player with brilliant and tweakful UI Deepin-UI based,
gstreamer front-end, with features likes search music by pinyin,
quanpin, colorful lyrics supports, and more powerful functions
you will found.

%description -l zh_CN
深度音乐播放器界面基于 Deepin-UI , 后端使用 gstreamer ,
其他特性如音乐搜索, 丰富多彩的歌词支持, 更多功能等待您发现.

%prep
%setup -q -n %{name}-%{_commit}
%if 0%{?option_plugins}
%setup -q -a1 -a2 -n %{name}-%{_commit}
%endif

# fix python version
find src -type f | xargs sed -i '1s|python$|python2|'

%build
deepin-generate-mo tools/locale_config.ini

%install
install -d %{buildroot}%{_datadir}/{applications,icons,%{name}}
install -m 644 %{name}-player.desktop %{buildroot}%{_datadir}/applications/
cp -r {app_theme,image,plugins,skin,src,wizard} %{buildroot}%{_datadir}/%{name}/

# generate locale
pushd locale
for i in `ls *.po`
 do
    mkdir -p %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/
    msgfmt $i -o %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/%{name}-player.mo
 done
popd

# install icons
for i in 16x16 24x24 48x48 64x64 96x96; do
  install -D image/hicolor/$i/apps/%{name}-player.png \
    %{buildroot}%{_datadir}/icons/hicolor/$i/apps/%{name}-player.png
done
install -D image/hicolor/scalable/apps/%{name}-player.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}-player.svg

# link exec file
install -d %{buildroot}%{_bindir}
ln -sfv %{_datadir}/%{name}/src/main.py %{buildroot}%{_bindir}/%{name}-player
chmod 755 %{buildroot}%{_datadir}/%{name}/src/*.py

# install plugins
%if 0%{?option_plugins}
cp -r %{bd_repo}-%{bd_commit}/baidumusic %{buildroot}%{_datadir}/%{name}/plugins/
cp -r %{nm_repo}-%{nm_commit}/neteasecloudmusic %{buildroot}%{_datadir}/%{name}/plugins/
%endif

%find_lang %{name}-player

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

%files -f %{name}-player.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING README.md ChangeLog
%{_datadir}/applications/%{name}-player.desktop
%{_datadir}/icons/hicolor/*
%{_datadir}/%{name}
%{_bindir}/%{name}-player

%changelog
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
