%global debug_package %{nil}
%define _xinputconf %{_sysconfdir}/X11/xinit/xinput.d/xsunpinyin.conf
%global project sunpinyin
%global repo %{project}

# commit
%global _commit a8bd8118f3a4e5caf83d3163be9c10cdf946d2f8
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		sunpinyin
Version:	2.0.4
Release:	1.git%{_shortcommit}%{?dist}
Summary:	A statistical language model based Chinese input method engine
Summary(zh_CN):	基于统计语言模型的中文输入法引擎

Group:		System Environment/Libraries
License:	LGPLv2 or CDDL
URL:		https://github.com/sunpinyin/sunpinyin
Source0:	https://github.com/sunpinyin/sunpinyin/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source1:	http://open-gram.googlecode.com/files/lm_sc.3gm.arpa-20140820.tar.bz2
Source2:	http://open-gram.googlecode.com/files/dict.utf8-20131214.tar.bz2

BuildRequires:	sqlite-devel
BuildRequires:	gettext
BuildRequires:	scons
BuildRequires:	perl(Pod::Man)
BuildRequires:	python-devel
BuildRequires:	pkgconfig
Requires:	%{name}-data

%description
Sunpinyin is an input method engine for Simplified Chinese. It is an SLM based
IM engine, and features full sentence input.

SunPinyin has been ported to various input method platforms and operating 
systems. The 2.0 release currently supports iBus, XIM, and Mac OS X.

%description -l zh_CN
SunPinyin 是一个基于 SLM 的简体中文输入法引擎,
支持完整的整句输入功能.

SunPinyin 已被移植到各种输入法平台和操作系统.
2.0 版本目前支持 iBus, XIM 和 Mac OS X.

%package devel
Summary:	Development files for %{name}
Summary(zh_CN):	%{name} 开发文件
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files that allows user
to write their own front-end for sunpinyin.

%description devel -l zh_CN
%{name}-devel 包含程序库和头文件, 允许用户编写自己的 sunpinyin 前端.

%package data
Summary:	Little-endian data files for %{name}
Summary(zh_CN):	%{name} 数据文件
Group:		System Environment/Libraries
License:	CC-BY-SA
Requires:	%{name}
Obsoletes:	%{name}-data-le
Obsoletes:	%{name}-data-be

%description data
The %{name}-data package contains necessary lexicon data and its index data
files needed by the sunpinyin input methods.

%description data -l zh_CN
%{name}-data 包含 sunpinyin 输入模块运行需要的 lexicon 数据和索引数据文件.

%prep
%setup -q -n %repo-%{_commit}
mkdir -p raw
cp %SOURCE1 raw
cp %SOURCE2 raw
pushd raw
tar xf lm_sc.3gm.arpa-20140820.tar.bz2
tar xf dict.utf8-20131214.tar.bz2
popd

%build
scons %{?_smp_mflags} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --datadir=%{_datadir}
export PATH=`pwd`/src:$PATH
pushd raw
ln -sf ../doc/SLM-inst.mk Makefile
make %{?_smp_mflags} VERBOSE=1
popd

%install
rm -rf $RPM_BUILD_ROOT
scons %{?_smp_mflags} \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --datadir=%{_datadir} \
    --install-sandbox=%{buildroot} \
    install
pushd raw
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
popd

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING *.LICENSE README.md TODO
%{_libdir}/libsunpinyin*.so.*
%{_docdir}/%{name}/README

%files devel
%defattr(-,root,root,-)
%{_libdir}/libsunpinyin*.so
%{_libdir}/pkgconfig/sunpinyin*.pc
%{_includedir}/sunpinyin*

%files data
%defattr(-,root,root,-)
%{_datadir}/%{name}
%{_bindir}/*
%{_mandir}/man1/*.1.gz
%{_docdir}/%{name}/SLM-*.mk

%changelog
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 2.0.4-1
- Rename version name

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.0.4-0.13
- Rebuilt for GCC 5 C++11 ABI change

* Sun Nov 16 2014 mosquito <sensor.wen@gmail.com> - 2.0.4git20141114-1
- Update version to 2.0.4git20141114

* Mon Nov 10 2014 mosquito <sensor.wen@gmail.com> - 2.0.4git20141109-1
- Update version to 2.0.4git20141109

* Wed Nov 5 2014 mosquito <sensor.wen@gmail.com> - 2.0.4git20141025-1
- Update version to 2.0.4git20141025

* Tue Sep 16 2014 mosquito <sensor.wen@gmail.com> - 2.0.4git20140820-2
- Update lm_sc.3gm file

* Tue Sep 16 2014 mosquito <sensor.wen@gmail.com> - 2.0.4git20140820-1
- Rebuild for rhel/centos 7

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-0.12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jun 16 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 2.0.4-0.11
- Handle AArch64 as well

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-0.10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-0.9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Liang Suilong <liangsuilong@gmail.com> - 2.0.4-0.8
- Upstream to the latest git snapshot

* Sun Feb 24 2013 Liang Suilong <liangsuilong@gmail.com> - 2.0.4-0.7
- Drop ibus-sunpinyin
- Drop xsunpinyin
- Architecture-dependent data file
- Upstream sunpinyin data file

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-0.6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 28 2012 Liang Suilong <liangsuilong@gmail.com> - 2.0.4-0.5
- Fix the spec file for building fcitx-sunpinyin

* Thu Jul 26 2012 Liang Suilong <liangsuilong@gmail.com> - 2.0.4-0.4
- Upstream to the latest git snapshot

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-0.3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 03 2012 Liang Suilong <liangsuilong@gmail.com> - 2.0.4-0.2
- Upstream to the latest git snapshot

* Sun May 13 2012 Liang Suilong <liangsuilong@gmail.com> - 2.0.4-0.1
- Upstream to the latest git snapshot
- Add BR: python-devel
- Upgrade to the latest SLM Data
- Drop the patch: sunpinyin-fixes-unistd-compile.patch

* Tue Mar 06 2012  Peng Wu <pwu@redhat.com> - 2.0.3-4
- Rebuilt for ibus-1.4.99

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 2.0.3-2
- Rebuild for new libpng

* Fri Feb 18 2011 Howard Ning <mrlhwliberty@gmail.com> - 2.0.3-1
- New upstream

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 26 2010  Peng Wu <pwu@redhat.com> - 2.0.2-4
- Fixes build for ibus 1.4

* Thu Aug 19 2010 Chen Lei <supercyper@163.com> - 2.0.2-3
- Rebuild for Rawhide

* Thu Aug 19 2010 Chen Lei <supercyper@163.com> - 2.0.2-2
- Add seperate license field to data files

* Mon Aug 16 2010 Chen Lei <supercyper@163.com> - 2.0.2-1
- Initial Package
