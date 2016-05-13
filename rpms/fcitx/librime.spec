%global debug_package %{nil}
%global project librime
%global repo %{project}

# commit
%global _commit 1da0c637d98c6381f755b24d15bb2ec358246348
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           librime
Version:        1.2
Release:        9.git%{_shortcommit}%{?dist}
Summary:        Rime Input Method Engine Library
Summary(zh_CN): Rime 输入法引擎应用程序库

License:        BSD
URL:            https://github.com/rime/librime
Source0:        https://github.com/rime/librime/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  cmake, opencc-devel
BuildRequires:  boost-devel >= 1.46
BuildRequires:  zlib-devel
BuildRequires:  glog-devel, gtest-devel
BuildRequires:  yaml-cpp-devel, kyotocabinet-devel
BuildRequires:  gflags-devel
BuildRequires:  marisa-devel
BuildRequires:  leveldb-devel

#Fixes arm build
#Patch1:         librime-fixes-misaligned-address.patch

%description
Rime Input Method Engine Library

Support for shape-based and phonetic-based input methods,
including those for Chinese dialects.

A selected dictionary in Traditional Chinese,
powered by opencc for Simplified Chinese output.

%description -l zh_CN
Rime 输入法引擎应用程序库

支持拼音和字形输入法, 包括汉语中的方言.

输入方案基于繁体中文, 简体中文通过 opencc 支持.

%package        devel
Summary:        Development files for %{name}
Summary(zh_CN): %{name} 开发文件
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%description    devel -l zh_CN
%{name}-devel 包含使用 %{name} 开发应用所需的程序库和头文件.

%package        tools
Summary:        Tools for %{name}
Summary(zh_CN): %{name} 工具
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
The %{name}-tools package contains tools for %{name}.

%description    tools -l zh_CN
%{name}-tools 包含 %{name} 工具.

%prep
%setup -q -n %{repo}-%{_commit}

%build
%cmake \
%if 0%{?fedora} > 21
  -DBOOST_USE_CXX11=ON \
%endif
  -DCMAKE_BUILD_TYPE=Release
make VERBOSE=1 %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot} INSTALL="install -p"
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md ChangeLog
%license LICENSE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/rime.pc
%dir %{_datadir}/cmake/rime
%{_datadir}/cmake/rime/RimeConfig.cmake

%files tools
%defattr(-,root,root,-)
%{_bindir}/rime_deployer
%{_bindir}/rime_dict_manager

%changelog
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 1.2-9.git1da0c63
- Update to 1.2-9.git1da0c63

* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 1.2-8.git4eade83
- Update to 1.2-8.git4eade83

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 1.2-7
- Rebuilt for Boost 1.59

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 1.2-5
- rebuild for Boost 1.58

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 04 2015 Kalev Lember <kalevlember@gmail.com> - 1.2-3
- Rebuilt for GCC 5 C++11 ABI change

* Wed Feb 04 2015 mosquito <sensor.wen@gmail.com> - 1.2git20150131-1
- Update version to 1.2git20150131

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 1.2-2
- Rebuild for boost 1.57.0

* Sun Jan 25 2015 mosquito <sensor.wen@gmail.com> - 1.2git20150125-1
- Update version to 1.2git20150125

* Wed Jan 07 2015 mosquito <sensor.wen@gmail.com> - 1.2git20150106-1
- Update version to 1.2git20150106

* Tue Jan  6 2015 Peng Wu <pwu@redhat.com> - 1.2-1
- Update to 1.2

* Sat Jan 03 2015 mosquito <sensor.wen@gmail.com> - 1.2git20141231-1
- Update version to 1.2git20141231

* Wed Dec 31 2014 mosquito <sensor.wen@gmail.com> - 1.2git20141229-1
- Update version to 1.2git20141229

* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 1.2git20141224-1
- Update version to 1.2git20141224

* Mon Dec 08 2014 mosquito <sensor.wen@gmail.com> - 1.2git20141205-1
- Update version to 1.2git20141205

* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 1.2git20141201-1
- Update version to 1.2git20141201

* Wed Nov 19 2014 mosquito <sensor.wen@gmail.com> - 1.2git20141119-1
- Update version to 1.2git20141119

* Wed Nov 5 2014 mosquito <sensor.wen@gmail.com> - 1.2git20141103-1
- Update version to 1.2git20141103

* Mon Sep 15 2014 mosquito <sensor.wen@gmail.com> - 1.2git20140730-1
- Rebuild for rhel/centos 7

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 1.1-4
- Rebuild for boost 1.55.0

* Thu May 22 2014 Brent Baude <baude@us.ibm.com> - 1.1-3
- FTBFS on all arches due to missing gflags.h
- Adding BR for gflags-devel

* Mon Dec 30 2013 Peng Wu <pwu@redhat.com> - 1.1-2
- Update arm patch

* Fri Dec 27 2013 Peng Wu <pwu@redhat.com> - 1.1-1
- Update to 1.1

* Mon Dec  9 2013 Peng Wu <pwu@redhat.com> - 1.0-1
- Update to 1.0

* Mon Nov 25 2013 Peng Wu <pwu@redhat.com> - 0.9.9-1
- Update to 0.9.9

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 27 2013 pmachata@redhat.com - 0.9.8-4
- Rebuild for boost 1.54.0

* Mon Jul 15 2013 Peng Wu <pwu@redhat.com> - 0.9.8-3
- Fixes arm build

* Thu May 16 2013 Peng Wu <pwu@redhat.com> - 0.9.8-2
- Improves the spec

* Thu May  9 2013 Peng Wu <pwu@redhat.com> - 0.9.8-1
- The Initial Version
