# https://github.com/WizTeam/WizQTClient/blob/master/src/WizDef.h
%global __strip_shared %(test $(rpm -E%?fedora) -ge 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}
%global repo WizQTClient

%global commit 10a9fe20b49cfc4b3d14177806d265ad001d6fb9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global with_llvm 0

Name:    wiznote
Version: 2.5.6
Release: 1.git%{shortcommit}%{?dist}
Summary: Cross platform cloud based note-taking application
Summary(zh_CN): 为知笔记 Qt 客户端
Group:   Applications/Editors
License: GPLv3
URL:     https://github.com/WizTeam/WizQTClient
Source0: %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%if 0%{?with_llvm}
BuildRequires: clang
%endif
BuildRequires: cmake(Qt5)
BuildRequires: cmake(Qt5LinguistTools)
BuildRequires: pkgconfig(Qt5WebEngine)
BuildRequires: pkgconfig(Qt5WebSockets)
BuildRequires: pkgconfig(Qt5WebChannel)
BuildRequires: pkgconfig(cryptopp)
BuildRequires: pkgconfig(zlib)
BuildRequires: boost-devel
BuildRequires: quazip-devel

%description
WizNote is an opensource cross-platform cloud based note-taking client.
This is a release version.

Support following platforms:
1. windows xp/vista/7/8
2. Mac OSX
3. Linux
3. Android/IOs
4. Web

Please refer to WizNote home for more detailed info:
- http://www.wiznote.com
- http://www.wiz.cn

%description -l zh_CN
为知笔记是一款基于云技术的开源跨平台笔记软件.
此包为稳定版.

%prep
%setup -q -n %{repo}-%{commit}

# fix missing head
sed -i '8a#include <QMutex>' src/sync/WizKMSync.h

# dynamic library (crypt|zip|json)
sed -i 's|add_subdirectory|find_package|' lib/CMakeLists.txt
sed -i 's|cryptlib|cryptopp|' src/CMakeLists.txt

# GCC version
gcc_version=$((LANG=c;gcc --version)|awk 'gsub(/\./,""){print $3;exit}')
if [ $gcc_version -ge '490' ]; then
#issue 307: https://github.com/WizTeam/WizQTClient/issues/307
sed -i '1a#define CRYPTOPP_DISABLE_SSE2' lib/cryptopp/config.h
fi

%if 0%{?rhel} == 6
#sed -i '/QT_VERSION/s|504|540|g' src/wizCategoryViewItem.cpp
%endif

# change library path
%ifarch x86_64
sed -i 's|lib/wiznote/plugins|lib64/%{name}/plugins|' \
    lib/aggregation/CMakeLists.txt \
    lib/extensionsystem/CMakeLists.txt
%endif

%build
# fixed "/usr/lib64/lib64/libboost_date_time.a" but this file does not exist.
# BOOL Boost_NO_BOOST_CMAKE "Enable fix for FindBoost.cmake"
%{cmake} \
%if 0%{?rhel} == 6
    -DBoost_NO_BOOST_CMAKE=ON \
%endif
%if 0%{?with_llvm}
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
%endif
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DCMAKE_BUILD_TYPE=Release
%make_build

%install
%make_install

# change exec filename
mv %{buildroot}%{_bindir}/{WizNote,%{name}}

# change desktop
sed -i 's|Exec=WizNote|Exec=%{name}|' \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

rm -rf %{buildroot}%{_datadir}/licenses/
rm -rf %{buildroot}%{_datadir}/icons/hicolor/8x8

# stripe shared files
%{__strip_shared}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Mon Sep 11 2017 mosquito <sensor.wen@gmail.com> - 2.5.6-1.git10a9fe2
- Update to 2.5.6
* Fri May 26 2017 mosquito <sensor.wen@gmail.com> - 2.5.1-1.gitf1b53cb
- Update to 2.5.1
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.4.2-1.git812ec4b
- Update to 2.4.2-1.git812ec4b
* Sun Dec 20 2015 mosquito <sensor.wen@gmail.com> - 2.3.1-1.gitfdd16c9
- Update version to 2.3.1-1.gitfdd16c9
* Sun Dec 06 2015 mosquito <sensor.wen@gmail.com> - 2.2.5-1.git56bca7d
- Update version to 2.2.5-1.git56bca7d
- Strip shared files
* Mon Aug 31 2015 mosquito <sensor.wen@gmail.com> - 2.2.3-1.git7bcf616
- Update version to 2.2.3-1.git7bcf616
* Mon Jul 13 2015 mosquito <sensor.wen@gmail.com> - 2.2.1-1.git1c186f3
- Update version to 2.2.1-1.git1c186f3
- use clang with build test
- dynamic link library
* Mon May 18 2015 mosquito <sensor.wen@gmail.com> - 2.1.18-1.git8addfa1
- Update version to 2.1.18-1.git8addfa1
* Wed Mar 04 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150215-1
- Update version to 2.1.15git20150215
* Thu Nov 20 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141119-1
- Branch (v2.1.14) code has been frozen.
* Fri Oct 17 2014 mosquito <sensor.wen@gmail.com> - 2.1.13git20140926-2
- Modify the package name, consistent with debian
- Adjust the library path
* Sat Sep 27 2014 mosquito <sensor.wen@gmail.com> - 2.1.13git20140926-1
- update version 2.1.13git20140926(PreRelease)
* Tue Sep 23 2014 mosquito <sensor.wen@gmail.com> - 2.1.13git20140923-2
- Change script
* Tue Sep 23 2014 mosquito <sensor.wen@gmail.com> - 2.1.13git20140923-1
- update version 2.1.13git20140923
- Changelog see: https://github.com/WizTeam/WizQTClient/commits/v2.1.13
* Thu Sep 11 2014 mosquito <sensor.wen@gmail.com> - 2.1.13-1
- update version 2.1.13
* Wed Sep 10 2014 i@marguerite.su
- update version 2.1.12
* Sat Mar 22 2014 i@marguerite.su
- initial version 2.1.2
