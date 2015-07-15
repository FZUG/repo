%global debug_package %{nil}
%global project moonplayer
%global repo %{project}

# commit
%global _commit c05205092e8c57f975c33bd2829875f89e83e290
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		moonplayer
Version:	0.34
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Video player that can play online videos
Summary(zh_CN):	一款可点播优酷, 土豆等网站在线视频的视频播放器

Group:		Applications/Multimedia
License:	GPLv3
URL:		https://github.com/coslyk/moonplayer
Source0:	https://github.com/coslyk/moonplayer/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
# https://code.google.com/p/moonplayer/wiki/PluginTutorial
# http://forum.ubuntu.org.cn/viewtopic.php?f=74&t=456351
Source1:	plugin_56.py
Source2:	plugin_funshion.py
Source3:	plugin_iqiyi.py
Source4:	plugin_sohu.py

BuildRequires:	qt-devel
BuildRequires:	python-devel
#BuildRequires:	qt5-qtbase-devel
Requires:	mplayer
Requires:	mencoder

%description
Video player that can play online videos from youku, tudou etc.

%description -l zh_CN
一款可点播优酷, 土豆等网站在线视频的视频播放器.

%prep
%setup -q -n %repo-%{_commit}

%build
#export CPATH="%%{_includedir}/qt5/QtWidgets:$CPATH"
mkdir src/build
pushd src/build
%{_qt4_qmake} ..
make %{?_smp_mflags}
popd

%install
pushd src/build
make install INSTALL_ROOT=%{buildroot}
install -m 0755 %{name} %{buildroot}%{_bindir}
install -m 0644 %{S:1} %{buildroot}%{_datadir}/%{name}/plugins/
install -m 0644 %{S:2} %{buildroot}%{_datadir}/%{name}/plugins/
install -m 0644 %{S:3} %{buildroot}%{_datadir}/%{name}/plugins/
install -m 0644 %{S:4} %{buildroot}%{_datadir}/%{name}/plugins/

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/%{name}.png

%changelog
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
