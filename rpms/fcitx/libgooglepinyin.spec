%global debug_package %{nil}

Name:    libgooglepinyin
Version: 0.1.2
Release: 3%{?dist}
Summary: A fork from google pinyin on android
License: Apache-2.0
Group:   System Environment/Libraries
Url:     https://code.google.com/p/libgooglepinyin
Source0: https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/libgooglepinyin/%{name}-%{version}.tar.bz2

BuildRequires: cmake
BuildRequires: intltool
BuildRequires: cairo-devel
BuildRequires: gtk2-devel
BuildRequires: pango-devel

%description
libgooglepinyin is an input method fork from google pinyin on android

%package devel
Summary:  Development files for libgooglepinyin
Group:    Development/Libraries
Requires: python-libs
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The libgooglepinyin-devel package includes the header files
for the googlepinyin package.

%prep
%setup -q -n %{name}-%{version}

%build
%{cmake}
make %{?_smp_mflags} VERBOSE=1

%install
make DESTDIR=%{buildroot} install

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/%{name}.so.*
%{_libdir}/googlepinyin/

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/googlepinyin.pc
%{_includedir}/googlepinyin/

%changelog
* Mon Mar 28 2016 mosquito <sensor.wen@gmail.com> 0.1.2-3
- Rebuild for fedora 23
* Tue Sep 16 2014 mosquito <sensor.wen@gmail.com> 0.1.2-2
- copr need python
* Mon Sep 15 2014 mosquito <sensor.wen@gmail.com> 0.1.2-1
- Rebuild for rhel/centos 7 and fedora 20/21/rawhide
* Mon Sep 17 2012 hillwood@linuxfans.org
- Fix ibus-googlepinyin working in 64bit for openSUSE
* Sun Jun 24 2012 i@marguerite.su
- fix builds on fedora.
* Fri Jan 27 2012 i@marguerite.su
- Update Source to latest git
  Fix builds, merge changelog
* Wed Sep  7 2011 hillwood@linuxfans.org
- first build
