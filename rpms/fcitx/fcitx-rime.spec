%global debug_package %{nil}
%global project fcitx-rime
%global repo %{project}

# commit
%global _commit a54a4505ef493db2a272005528095ad00b233343
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           fcitx-rime
Version:        0.3.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Rime input engine support for Fcitx
Summary(zh_CN): 使 Fcitx 输入框架支持 Rime 输入引擎

License:        GPLv3
Group:          System Environment/Libraries
Url:            https://github.com/fcitx/fcitx-rime
Source0:        https://github.com/fcitx/fcitx-rime/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  fcitx-data
BuildRequires:  fcitx-devel
BuildRequires:  fcitx-qt5-devel
BuildRequires:  brise
BuildRequires:  librime-devel
BuildRequires:  fdupes
BuildRequires:  hicolor-icon-theme
BuildRequires:  intltool
BuildRequires:  pkgconfig
Requires:  brise

%description
Rime is an Traditional Chinese input method engine.
Its idea comes from ancient Chinese brush and carving art.
Mainly it's about to express your thinking with your keystrokes.

This package is the Fcitx implentation of RIME.

%description -l zh_CN
中州韵是一个繁体中文输入法引擎. 灵感来源于中国古代印刷和雕刻艺术.

此包使 Fcitx 输入法框架支持 RIME 输入法.

%prep
%setup -q -n %{repo}-%{_commit}

%build
%cmake -DCMAKE_BUILD_TYPE=Release
make %{?_smp_mflags}

%install
%make_install

%find_lang %{name}
fdupes -nqr %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README.md
%license COPYING
%{_libdir}/fcitx/%{name}.so
%{_libdir}/fcitx/qt/libfcitx-rime-config-gui.so
%{_datadir}/fcitx/addon/%{name}.conf
%{_datadir}/fcitx/imicon/rime.png
%{_datadir}/fcitx/inputmethod/rime.conf
%{_datadir}/fcitx/skin/default/rime-*.png
%{_datadir}/icons/hicolor/48x48/apps/*.png
%{_datadir}/icons/hicolor/128x128/apps/fcitx-rime.png
%{_datadir}/icons/hicolor/scalable/status/*.svg

%changelog
* Fri May 10 2019 Zamir SUN <sztsian@gmail.com> -  0.3.2-1.git54a4505
- Update to git commit a54a4505ef493db2a272005528095ad00b233343

* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 0.3.1-2.git9351313
- Update to 0.3.1-2.git9351313
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 0.3.1-1.gitb716234
- Update to 0.3.1-1.gitb716234
* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141209-1
- Update version to 0.3.1git20141209
* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141209-1
- Update Translation
* Mon Sep 15 2014 mosquito <sensor.wen@gmail.com> - 0.3.1-1
- update version 0.3.1
- build for rhel/centos 7 and fedora 20/21/rawhide
* Mon Nov 18 2013 i@marguerite.su
- update version 0.3.0
  * compatibility for rime 1.0 release.
* Sat Jul 13 2013 i@marguerite.su
- update version 0.2.2
  * Fix Issue 11
  * Fix Issue 12
  * Update icon artwork
  * Add License
- remove patch: fcitx-rime-0.2.1-Caplocks_never_response_second_request.patch
  * got upstreamed
* Fri Jul  5 2013 i@marguerite.su
- add patch: fcitx-rime-0.2.1-Caplocks_never_response_second_request.patch
  * Phenomenon: When inputing Chinese, users hit Capslock to enter
    Capital letters, then fcitx-rime will enter ASCII mode. But
    the second or further Capslock won't change ASCII mode back
    to Chinese pinyin mode unless users hit Shift.
  * Cause: Rime reads bitmask FcitxKeyState_CapsLock to detect
    whether CapsLock is on, but fcitx-rime frontend didn't
    provide such use.
* Sat Jun 22 2013 i@marguerite.su
- update version 0.2.1
  * fixes some bug and add some manual syncing feature,
    and implement redeploy properly
* Fri Feb  1 2013 i@marguerite.su
- explicitly requires: brise.
  it is librime's data file, without it, fcitx-rime is a skeleton.
* Sat Jan 26 2013 i@marguerite.su
- update version 0.2.0
  * re-deploy support
* Thu Oct 11 2012 i@marguerite.su
- update version 0.1.2
  * build with librime 0.9.4
* Sat Sep 15 2012 i@marguerite.su
- update version 0.1.1
  * brise path fix. thanks to Marguerite Su.
* Mon Aug 13 2012 i@marguerite.su
- update source to include COPYING, fix #bnc775644
* Wed Jul 25 2012 i@marguerite.su
- auto detect brise.
* Mon Jul 23 2012 jzheng@suse.com
- add fcitx-rime-paralled-build.patch to enable parallel build
- remove LIB_INSTALL_DIR to clear the unused variable warning
* Sat Jul 21 2012 i@marguerite.su
- initial version 0.1.0
