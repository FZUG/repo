%global __strip_shared %(test $(rpm -E%?fedora) -eq 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}
%global project WizQTClient
%global repo %{project}

# commit
%global _commit 56bca7d81e7586e06ec26a86f9740076f7743e14
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global with_llvm 0

Name:		wiznote
Version:	2.2.5
Release:	1.git%{_shortcommit}%{?dist}
Summary:	WizNote QT Client
Summary(zh_CN):	为知笔记 Qt 客户端

Group:		Applications/Editors
# https://raw.githubusercontent.com/WizTeam/WizQTClient/master/LICENSE
License:	GPLv3
URL:		https://github.com/WizTeam/WizQTClient
Source0:	https://github.com/WizTeam/WizQTClient/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	cmake >= 2.8.4
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qttools-devel
BuildRequires:	qt5-qtwebkit-devel
BuildRequires:	boost-devel
BuildRequires:	cryptopp-devel
BuildRequires:	quazip-devel
BuildRequires:	zlib-devel
%if 0%{?with_llvm}
BuildRequires:	clang
%endif
Obsoletes:	wiz-note <= 2.1.13git20140926

# qt4 build requires
#BuildRequires:	qt-devel
#BuildRequires:	qtwebkit-devel

%description
WizNote is an opensource cross-platform cloud based note-taking client.
This is a release version.
.
Support following platforms:
1. windows xp/vista/7/8
2. Mac OSX
3. Linux
3. Android/IOs
4. Web
.
Please refer to WizNote home for more detailed info:
- http://www.wiznote.com
- http://www.wiz.cn

%description -l zh_CN
为知笔记是一款基于云技术的开源跨平台笔记软件.
此包为稳定版.

%prep
%setup -q -n %repo-%{_commit}

%build
# dynamic library (crypt|zip|json)
sed -i -r '/crypt/d' lib/CMakeLists.txt
sed -i -e '/cryptlib/az' -e 's|cryptlib|cryptopp|' src/CMakeLists.txt

# GCC version
gcc_version=$((LANG=c;gcc --version)|awk 'gsub(/\./,""){print $3;exit}')
if [ $gcc_version -ge '490' ]; then
#issue 307: https://github.com/WizTeam/WizQTClient/issues/307
sed -i '1a#define CRYPTOPP_DISABLE_SSE2' lib/cryptopp/config.h
fi

%if 0%{?rhel} == 6
sed -i '/QT_VERSION/s|504|540|g' src/wizCategoryViewItem.cpp
%endif

# change library path
%ifarch x86_64
sed -i 's|lib/wiznote/plugins|lib64/%{name}/plugins|' \
	src/main.cpp \
	src/plugins/coreplugin/CMakeLists.txt \
	src/plugins/helloworld/CMakeLists.txt \
	src/plugins/markdown/CMakeLists.txt \
	lib/aggregation/CMakeLists.txt \
	lib/extensionsystem/CMakeLists.txt \
	CMakeLists.txt
%endif

mkdir dist
pushd dist
# fixed "/usr/lib64/lib64/libboost_date_time.a" but this file does not exist.
# BOOL Boost_NO_BOOST_CMAKE "Enable fix for FindBoost.cmake"
%{cmake} .. \
%if 0%{?rhel} == 6
	-DBoost_NO_BOOST_CMAKE=ON \
%endif
%if 0%{?with_llvm}
	-DCMAKE_C_COMPILER=clang \
	-DCMAKE_CXX_COMPILER=clang++ \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DWIZNOTE_USE_QT5=ON \
	-DCMAKE_BUILD_TYPE=Release
make %{?_smp_mflags}

%install
%make_install -C dist

# change exec filename
mv %{buildroot}%{_bindir}/WizNote %{buildroot}%{_bindir}/%{name}

# change desktop
sed -i 's|Exec=WizNote|Exec=%{name}|' \
   %{buildroot}%{_datadir}/applications/%{name}.desktop

# export library path
install -d %{buildroot}/etc/ld.so.conf.d/
echo "%{_libdir}/%{name}/plugins/" > %{buildroot}/etc/ld.so.conf.d/%{name}.conf

rm -rf %{buildroot}%{_datadir}/licenses/
rm -rf %{buildroot}%{_datadir}/icons/hicolor/{512x512,8x8}

# stripe shared files
%{__strip_shared}

%post
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
ldconfig

%postun
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
ldconfig

%files
%defattr(-,root,root,-)
%doc README.md CHANGELOG.md
%license LICENSE
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_libdir}/%{name}/plugins/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}/*

%changelog
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
