%global debug_package %{nil}

# cmake version
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
   %define _cmake cmake
%else
 %if 0%{?rhel} == 6
   %define _cmake cmake28
 %endif
%endif

Name:		wiznote
Version:	2.1.15git20150215
Release:	1%{?dist}
Summary:	WizNote QT Client
Summary(zh_CN):	为知笔记 Qt 客户端
Group:		Applications/Editors
License:	GPLv3
URL:		https://github.com/WizTeam/WizQTClient
Source:		%{name}-%{version}.tar.xz
BuildRequires:	gcc-c++
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qttools-devel
BuildRequires:	qt5-qtwebkit-devel
BuildRequires:	boost-devel
BuildRequires:	zlib-devel
%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
BuildRequires:	cmake >= 2.8.4
%else
 %if 0%{?rhel} == 6
BuildRequires:	cmake28 >= 2.8.4
 %endif
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
%setup -q

%build
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
%{_cmake} .. \
%if 0%{?rhel} == 6
	-DBoost_NO_BOOST_CMAKE=ON \
%endif
	-DCMAKE_INSTALL_PREFIX=%{_prefix} \
	-DBUILD_STATIC_LIBRARIES=ON \
	-DCLUCENE_BUILD_SHARED_LIBRARIES=ON \
	-DCRYPTOPP_BUILD_SHARED_LIBS=ON \
	-DCRYPTOPP_BUILD_STATIC_LIBS=ON \
	-DWIZNOTE_USE_QT5=ON \
	-DCMAKE_BUILD_TYPE=Release
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd dist
make install DESTDIR=%{buildroot}
popd

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md CHANGELOG.md
%{_sysconfdir}/ld.so.conf.d/%{name}.conf
%{_libdir}/%{name}/plugins/*
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}/*
#@exclude @{_datadir}/licenses/

%changelog
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
