%global debug_package %{nil}
%global project WizQTClient
%global repo %{project}

# commit
%global _commit 88992f4252b13aa78eabb75a87fb99b7328d6149
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global with_llvm 0

Name:		wiznote-beta
Version:	2.2.2
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
Obsoletes:	wiznote-beta <= 2.1.18git20150430

# qt4 build requires
#BuildRequires:	qt-devel
#BuildRequires:	qtwebkit-devel

%description
WizNote is an opensource cross-platform cloud based note-taking client.
This is a development version.

%description -l zh_CN
为知笔记是一款基于云技术的开源跨平台笔记软件.
此包为开发版.

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
%else
sed -i 's|lib/wiznote/plugins|lib/%{name}/plugins|' \
	src/main.cpp \
	src/plugins/coreplugin/CMakeLists.txt \
	src/plugins/helloworld/CMakeLists.txt \
	src/plugins/markdown/CMakeLists.txt \
	lib/aggregation/CMakeLists.txt \
	lib/extensionsystem/CMakeLists.txt \
	CMakeLists.txt
%endif

# change share path
sed -i 's|share/wiznote|share/%{name}|' \
	src/utils/pathresolve.cpp \
	src/main.cpp \
	src/CMakeLists.txt \
	src/plugins/markdown/markdown.cpp

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
popd

%install
pushd dist
make install DESTDIR=%{buildroot}
popd

# change exec filename
mv %{buildroot}%{_bindir}/WizNote %{buildroot}%{_bindir}/%{name}-run
mv %{buildroot}%{_datadir}/applications/wiznote.desktop \
   %{buildroot}%{_datadir}/applications/%{name}.desktop

# change desktop
sed -i -e 's|Name=WizNote|Name=WizNote Develop|' \
       -e '/Name\[zh\_*/s|为知笔记|为知笔记开发版|' \
       -e 's|Exec=WizNote|Exec=%{name}|' \
       -e 's|Icon=wiznote|Icon=%{name}|' \
   %{buildroot}%{_datadir}/applications/%{name}.desktop

# change icon filename
for i in `ls %{buildroot}%{_datadir}/icons/hicolor/`; do
   mv %{buildroot}%{_datadir}/icons/hicolor/${i}/apps/wiznote.png \
      %{buildroot}%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done

# export library path
#install -d %%{buildroot}/etc/ld.so.conf.d/
#echo "%%{_libdir}/%%{name}/plugins/" > %%{buildroot}/etc/ld.so.conf.d/%%{name}.conf

cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
LD_LIBRARY_PATH=%{_libdir}/%{name}/plugins %{name}-run
EOF
chmod 0755 %{buildroot}%{_bindir}/%{name}

rm -rf %{buildroot}%{_datadir}/licenses/
rm -rf %{buildroot}%{_datadir}/icons/hicolor/{512x512,8x8}

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
%doc LICENSE README.md CHANGELOG.md
#%%{_sysconfdir}/ld.so.conf.d/%%{name}.conf
%{_libdir}/%{name}/plugins/*
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/%{name}/*
#%%exclude %%{_datadir}/licenses/

%changelog
* Mon Jul 13 2015 mosquito <sensor.wen@gmail.com> - 2.2.2-1.git88992f4
- Update version to 2.2.2-1.git88992f4
- use clang with build test
- dynamic link library
* Mon Jun 29 2015 mosquito <sensor.wen@gmail.com> - 2.2.1-1.git020d933
- Version release
* Fri May 22 2015 mosquito <sensor.wen@gmail.com> - 2.2.1-1.git8c58446
- Build on linux
* Mon May 18 2015 mosquito <sensor.wen@gmail.com> - 2.2.1-1.git4bf03fa
- Update version to 2.2.1
* Tue May 05 2015 mosquito <sensor.wen@gmail.com> - 2.1.18-1.git8addfa1
- Rename version name
* Mon May 04 2015 mosquito <sensor.wen@gmail.com> - 2.1.18git20150430-1
- Update version to 2.1.18git20150430
- Fixed issue 307: https://github.com/WizTeam/WizQTClient/issues/307
* Wed Mar 04 2015 mosquito <sensor.wen@gmail.com> - 2.1.16git20150215-1
- Update version to 2.1.16git20150215
* Tue Feb 03 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150203-1
- Update version to 2.1.15git20150203
* Thu Jan 29 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150127-1
- Update version to 2.1.15git20150127
* Mon Jan 26 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150126-1
- Update version to 2.1.15git20150126
* Fri Jan 23 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150123-1
- Update version to 2.1.15git20150123
* Wed Jan 21 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150121-1
- Update version to 2.1.15git20150121
* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150116-1
- Update version to 2.1.15git20150116
* Thu Jan 15 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150115-1
- Update version to 2.1.15git20150115
* Mon Jan 12 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150109-1
- Update version to 2.1.15git20150109
* Wed Jan 07 2015 mosquito <sensor.wen@gmail.com> - 2.1.15git20150106-1
- Update version to 2.1.15git20150106
* Tue Dec 30 2014 mosquito <sensor.wen@gmail.com> - 2.1.15git20141230-1
- Update version to 2.1.15git20141230
* Fri Dec 26 2014 mosquito <sensor.wen@gmail.com> - 2.1.15git20141225-1
- Update version to 2.1.15git20141225
* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> - 2.1.15git20141222-1
- Update version to 2.1.15git20141222
* Mon Dec 08 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141205-1
- Update version to 2.1.14git20141205
* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141202-1
- Update version to 2.1.14git20141202
* Thu Nov 27 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141127-1
- Update version to 2.1.14git20141127
* Thu Nov 20 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141120-1
- Update version to 2.1.14git20141120
* Wed Nov 19 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141119-1
- Update version to 2.1.14git20141119
* Tue Nov 18 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141118-1
- Update version 2.1.14git20141118
* Fri Nov 14 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141114-1
- Update version 2.1.14git20141114
* Wed Nov 12 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141112-1
- Update version 2.1.14git20141112
* Wed Nov 12 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141111-1
- Update version 2.1.14git20141111
* Mon Nov 10 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141110-1
- Update version 2.1.14git20141110
* Wed Nov 5 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141105-1
- Update version 2.1.14git20141105
* Fri Oct 17 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141017-1
- Update version 2.1.14git20141017
* Thu Oct 16 2014 mosquito <sensor.wen@gmail.com> - 2.1.14git20141015-1
- Development version 2.1.14git20141015
