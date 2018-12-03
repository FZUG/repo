# https://github.com/WizTeam/WizQTClient/blob/master/src/WizDef.h
%global repo        WizQTClient
%global commit      862b6376ad7da27f5a97b41c8e39a42b35f5d800
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%global with_llvm   0

Name:           wiznote
Version:        2.6.6
Release:        1%{?dist}
Summary:        Cross platform cloud based note-taking application
Summary(zh_CN): 为知笔记 Qt 客户端
License:        GPLv3
URL:            https://github.com/WizTeam/WizQTClient
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
# patch for CryptoPP::ProcessLastBlock parameter
Patch0:         %{name}_fix_type.patch

%if 0%{?with_llvm}
BuildRequires:  clang
%endif
BuildRequires:  gcc-c++
BuildRequires:  cmake(Qt5)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5WebEngine)
BuildRequires:  pkgconfig(Qt5WebSockets)
BuildRequires:  pkgconfig(Qt5WebChannel)
BuildRequires:  pkgconfig(cryptopp)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  boost-devel
BuildRequires:  quazip-devel
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
WizNote is an opensource cross-platform cloud based note-taking client.

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

%prep
%autosetup -p1 -n %{repo}-%{commit}

# dynamic library
sed -i 's|add_subdirectory|find_package|' lib/CMakeLists.txt
sed -i 's|cryptlib|cryptopp|; /static-libstdc++/d' src/CMakeLists.txt
rm -rf lib/{cryptopp,openssl,quazip,zlib}

# remove icon, change name
sed -i '/ICON_SIZE/s|8||; /LICENSE/d' src/CMakeLists.txt
sed -i '/Exec/s|WizNote|%{name}|' build/common/%{name}.desktop

# change library path
%ifarch x86_64
sed -i 's|lib/wiznote/plugins|lib64/%{name}/plugins|' \
    lib/aggregation/CMakeLists.txt \
    lib/extensionsystem/CMakeLists.txt
%endif

%build
%{cmake} \
%if 0%{?with_llvm}
    -DCMAKE_C_COMPILER=clang \
    -DCMAKE_CXX_COMPILER=clang++ \
%endif
    -DCMAKE_BUILD_TYPE=Release
%make_build

%install
%make_install

desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md CHANGELOG.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Sun Dec 02 2018 mosquito <sensor.wen@gmail.com> - 2.6.6-1
- Update to 2.6.6

* Thu Oct 19 2017 Zamir SUN <sztsian@gmail.com> - 2.5.6-2.git10a9fe2
- Bump version to force rebuild

* Mon Sep 11 2017 mosquito <sensor.wen@gmail.com> - 2.5.6-1.git10a9fe2
- Update to 2.5.6

* Fri May 26 2017 mosquito <sensor.wen@gmail.com> - 2.5.1-1.gitf1b53cb
- Update to 2.5.1

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.4.2-1.git812ec4b
- Update to 2.4.2-1.git812ec4b

* Sun Dec 20 2015 mosquito <sensor.wen@gmail.com> - 2.3.1-1.gitfdd16c9
- Update to 2.3.1-1.gitfdd16c9

* Sun Dec 06 2015 mosquito <sensor.wen@gmail.com> - 2.2.5-1.git56bca7d
- Update to 2.2.5-1.git56bca7d
- Strip shared files

* Mon Aug 31 2015 mosquito <sensor.wen@gmail.com> - 2.2.3-1.git7bcf616
- Update to 2.2.3-1.git7bcf616

* Mon Jul 13 2015 mosquito <sensor.wen@gmail.com> - 2.2.1-1.git1c186f3
- Update to 2.2.1-1.git1c186f3
- use clang with build test
- dynamic link library

* Mon May 18 2015 mosquito <sensor.wen@gmail.com> - 2.1.18-1.git8addfa1
- Update to 2.1.18-1.git8addfa1

* Wed Mar 04 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150215-1
- Update to 2.1.15git20150215

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
