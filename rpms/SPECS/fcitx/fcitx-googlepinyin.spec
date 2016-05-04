%global debug_package %{nil}
%global project fcitx-googlepinyin
%global repo %{project}

%global _commit 6536e187c6637a866aaf25649d7bf3f0d9a926d3
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    fcitx-googlepinyin
Version: 0.1.6
Release: 3.git%{_shortcommit}%{?dist}
Summary: Googlepinyin module for fcitx
Group:   System Environment/Libraries
License: GPLv3
Url:     https://fcitx-im.org/wiki/Googlepinyin
Source0: https://github.com/fcitx/fcitx-googlepinyin/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: cmake
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: pkgconfig
BuildRequires: fcitx-devel
BuildRequires: libgooglepinyin-devel
BuildRequires: hicolor-icon-theme
Requires: fcitx

%description
fcitx-googlepinyin is a Googlepinyin module for fcitx.

%prep
%setup -q -n %{repo}-%{_commit}
sed -i '/addon/ifcitx_add_inputmethod_conf_file(googlepinyin.conf)' src/CMakeLists.txt

%build
%{cmake}
make %{?_smp_mflags} VERBOSE=1

%install
make install DESTDIR=%{buildroot} INSTALL="install -p"

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_libdir}/fcitx/*.so
%{_datadir}/fcitx/addon/*.conf
%{_datadir}/fcitx/inputmethod/*.conf
%{_datadir}/fcitx/imicon/*.png
%{_datadir}/fcitx/skin/classic/*.png
%{_datadir}/fcitx/skin/default/*.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Wed May  4 2016 mosquito <sensor.wen@gmail.com> 0.1.6-3
- Fix https://github.com/FZUG/repo/issues/71
* Mon Mar 28 2016 mosquito <sensor.wen@gmail.com> 0.1.6-2
- Rebuild for fedora 23
* Mon Sep 15 2014 mosquito <sensor.wen@gmail.com> 0.1.6-1
- Rebuild for rhel/centos 7 and fedora 20/21/rawhide
* Thu Oct 11 2012 i@marguerite.su
- updte 0.1.6
  * a bug fix release
* Mon Jun 25 2012 i@marguerite.su
- fix fedora builds.
* Mon May 28 2012 i@marguerite.su
- bring it into DVD.
* Mon Mar 12 2012 cfarrell@suse.com
- license update: GPL-3.0+
* Fri Mar 9 2012 hillwood@linuxfans.org
- update to 0.4.1
  Portable to run with archive
* Wed Feb 29 2012 i@marguerite.su
- set _service disabled. update source from git.
* Sat Jan 28 2012 i@marguerite.su
- Upstream version 0.1.4git
* Sun Oct 2 2011 hillwood@linuxfans.org
- Update to 0.1.3
  coexistance with latest Fcitx API.
  pre-input text shows Chinese and fixed cursor position.
* Thu Sep 8 2011 hillwood@linuxfans.org
- Update to 0.1.2
* Thu Sep 8 2011 hillwood@linuxfans.org
- First package for 0.1.1
