%global debug_package %{nil}
%global project OpenCC
%global repo %{project}

# commit
%global _commit b19714d74675cb0cbaf80187d4b4f6f9cbd9b961
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		opencc
Version:	1.0.2
Release:	3.git%{_shortcommit}%{?dist}
Summary:	Libraries for Simplified-Traditional Chinese Conversion
Summary(zh_CN):	简体-繁体中文转换库
License:	ASL 2.0
Group:		System Environment/Libraries
URL:		https://github.com/BYVoid/OpenCC
Source0:	https://github.com/BYVoid/OpenCC/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Patch1:		opencc-fixes-cmake.patch

BuildRequires:	gettext
BuildRequires:	cmake
BuildRequires:	doxygen

# provide libopencc.so.1
%ifarch x86_64
Provides:	libopencc.so.1()(64bit)
%else
Provides:	libopencc.so.1
%endif

%description
OpenCC is a library for converting characters and phrases between
Traditional Chinese and Simplified Chinese.

%description -l zh_CN
OpenCC 程序库可以将字符和短语在简体中文和繁体中文之间进行转换.


%package doc
Summary:	Documentation for OpenCC
Summary(zh_CN):	OpenCC 文档
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description doc
Doxygen generated documentation for OpenCC.

%description doc -l zh_CN
使用 doxygen 生成的 OpenCC 文档.


%package tools
Summary:	Command line tools for OpenCC
Summary(zh_CN):	OpenCC 命令行工具
Group:		Applications/Text
Requires:	%{name} = %{version}-%{release}

%description tools
Command line tools for OpenCC, including tools for conversion via CLI and
for building dictionaries.

%description tools -l zh_CN
OpenCC 命令行工具, 包含转换和构建字典的命令行工具.


%package devel
Summary:	Development files for OpenCC
Summary(zh_CN):	OpenCC 开发文件
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description devel -l zh_CN
%{name}-devel 包含使用 %{name} 开发应用所需的程序库和头文件.


%prep
%setup -q -n %{repo}-%{_commit}
%patch1 -p1 -b .cmake

%build
%cmake . \
	-DENABLE_GETTEXT:BOOL=ON \
	-DBUILD_DOCUMENTATION:BOOL=ON
make VERBOSE=1 %{?_smp_mflags}

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.a

# error path
#install -d %{buildroot}%{_datadir}/%{name}
#mv %{buildroot}/usr/shareopencc/* %{buildroot}%{_datadir}/%{name}
#rm -rf %{buildroot}/usr/shareopencc/

# error lib path
#%ifarch x86_64
#  mv %{buildroot}%{_exec_prefix}/lib/* %{buildroot}%{_libdir}
#  rm -rf %{buildroot}%{_exec_prefix}/lib
#  sed -i 's|libdir=/usr/lib/|libdir=%{_libdir}|g' %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
#%endif

# provide libopencc.so.2.0.0 -> so.2 -> so
rm -rf %{buildroot}%{_libdir}/libopencc.so{,.2}
mv %{buildroot}%{_libdir}/libopencc.so.1.0.0 %{buildroot}%{_libdir}/libopencc.so.2.0.0
ln -sfv %{_libdir}/libopencc.so.2.0.0 %{buildroot}%{_libdir}/libopencc.so.2
ln -sfv %{_libdir}/libopencc.so.2 %{buildroot}%{_libdir}/libopencc.so

# link libopencc.so.1.0.0
ln -sfv %{_libdir}/libopencc.so.2.0.0 %{buildroot}%{_libdir}/libopencc.so.1.0.0
ln -sfv %{_libdir}/libopencc.so.2.0.0 %{buildroot}%{_libdir}/libopencc.so.1

%check
ctest

%post
if [ "0$1" -eq "2" ]; then
    LIB1="%{_libdir}/libopencc.so.1"
    LIB2="%{_libdir}/libopencc.so.2.0.0"
    if [ ! -L "$LIB1" ]; then
	ln -sf "$LIB2" "$LIB1"
    fi
fi
ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS LICENSE README.md NEWS.md
%{_libdir}/lib*.so.*
%{_datadir}/opencc/
%exclude %{_datadir}/opencc/doc

%files doc
%defattr(-,root,root,-)
%{_datadir}/opencc/doc

%files tools
%defattr(-,root,root,-)
%{_bindir}/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc


%changelog
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 1.0.2-3
- Rename version name

* Tue Feb 03 2015 mosquito <sensor.wen@gmail.com> - 1.0.2git20150203-1
- Update version to 1.0.2git20150203

* Mon Jan 19 2015 Peng Wu <pwu@redhat.com> - 1.0.2-2
- Fixes postun script

* Mon Jan 12 2015 mosquito <sensor.wen@gmail.com> - 1.0.2git20150112-1
- Update version to 1.0.2git20150112

* Mon Jan 12 2015 mosquito <sensor.wen@gmail.com> - 1.0.2git20150106-1
- Update version to 1.0.2git20150106

* Tue Jan  6 2015 Peng Wu <pwu@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Tue Dec 30 2014 mosquito <sensor.wen@gmail.com> - 1.0.2git20141212-3
- Provide libopencc.so.1 library

* Mon Dec 29 2014 mosquito <sensor.wen@gmail.com> - 1.0.2git20141212-2
- Add post scrpit

* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 1.0.2git20141212-1
- Update version to 1.0.2git20141212

* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 1.0.2git20141127-2
- Rebuild

* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 1.0.2git20141127-1
- Update version to 1.0.2git20141127

* Thu Nov 6 2014 mosquito <sensor.wen@gmail.com> - 1.0.2git20141108-1
- Update version to 1.0.2git20141108

* Thu Nov 6 2014 mosquito <sensor.wen@gmail.com> - 1.0.1git20141105-1
- Update version to 1.0.1git20141105

* Wed Nov 5 2014 mosquito <sensor.wen@gmail.com> - 1.0.1git20141020-1
- Update version to 1.0.1git20141020

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Peng Wu <pwu@redhat.com> - 0.4.3-1
- Update to 0.4.3

* Mon Mar  4 2013 Peng Wu <pwu@redhat.com> - 0.4.0-1
- Update to 0.4.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 22 2012  Peng Wu <pwu@redhat.com> - 0.3.0-4
- Fixes Download URL

* Mon Jul 23 2012  Peng Wu <pwu@redhat.com> - 0.3.0-3
- Fixes cmake

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012  Peng Wu <pwu@redhat.com> - 0.3.0-1
- Update to 0.3.0, and fixes ctest

* Wed Feb  1 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.2.0-6
- Drop unnessary ExclusiveArch directive

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011  Peng Wu <pwu@redhat.com> - 0.2.0-4
- Change i386 to i686

* Wed Nov 30 2011  Peng Wu <pwu@redhat.com> - 0.2.0-3
- Only build for i386 and x86_64

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Dec 25 2010 BYVoid <byvoid.kcp@gmail.com> - 0.2.0-1
- Upstream release.
- Use CMake instead of autotools.

* Wed Sep 29 2010 jkeating - 0.1.2-2
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.2-1
- Upstream release.

* Thu Aug 12 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.1-1
- Upstream release.

* Thu Jul 29 2010 BYVoid <byvoid.kcp@gmail.com> - 0.1.0-1
- Upstream release.

* Fri Jul 16 2010 BYVoid <byvoid.kcp@gmail.com> - 0.0.4-1
- Initial release of RPM.

