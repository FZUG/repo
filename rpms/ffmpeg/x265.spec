%global debug_package %{nil}

Summary: H.265/HEVC encoder
Name: x265
Version: 1.7
Release: 1%{?dist}
URL: http://x265.org
Source0: http://ftp.videolan.org/pub/videolan/x265/x265_%{version}.tar.gz
Patch4: x265-detect_cpu_armhfp.patch
# source/Lib/TLibCommon - BSD
# source/Lib/TLibEncoder - BSD
# everything else - GPLv2+
License: GPLv2+ and BSD
BuildRequires: cmake
BuildRequires: yasm
BuildRequires: numactl-devel
# Test !
#%ifarch x86_64
#Provides: libx265.so.51()(64bit)
#%else
#Provides: libx265.so.51()(32bit)
#%endif

%description
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the command line encoder.

%package libs
Summary: H.265/HEVC encoder library

%description libs
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library.

%package devel
Summary: H.265/HEVC encoder library development files
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The primary objective of x265 is to become the best H.265/HEVC encoder
available anywhere, offering the highest compression efficiency and the
highest performance on a wide variety of hardware platforms.

This package contains the shared library development files.

%prep
%setup -q -n x265_%{version}
%patch4 -p1 -b .armhfp

%build
%cmake -G "Unix Makefiles" \
 -DCMAKE_SKIP_RPATH:BOOL=YES \
 -DENABLE_PIC:BOOL=ON \
 -DENABLE_SHARED:BOOL=ON \
 -DENABLE_TESTS:BOOL=ON \
 -DHIGH_BIT_DEPTH:BOOL=ON \
 source
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}%{_libdir}/libx265.a
install -Dpm644 COPYING %{buildroot}%{_pkgdocdir}/COPYING

%ifnarch %{arm}
%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} test/TestBench
%endif

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%{_bindir}/x265

%files libs
%dir %{_pkgdocdir}
%{_pkgdocdir}/COPYING
%{_libdir}/libx265.so.*

%files devel
%doc doc/*
%{_includedir}/x265.h
%{_includedir}/x265_config.h
%{_libdir}/libx265.so
%{_libdir}/pkgconfig/x265.pc

%changelog
* Tue Aug  4 2015 mosquito <sensor.wen@gmail.com> 1.7-1
- update to 1.7

* Wed Apr 15 2015 Dominik Mierzejewski <rpm@greysector.net> 1.6-1
- update to 1.6 (ABI bump, rfbz#3593)
- release tarballs are now hosted on videolan.org
- drop obsolete patches

* Thu Dec 18 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-6
- fix build on armv7l arch (partially fix rfbz#3361, patch by Nicolas Chauvet)
- don't run tests on ARM for now (rfbz#3361)

* Sun Aug 17 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-5
- don't include contributor agreement in doc
- make sure /usr/share/doc/x265 is owned
- add a comment noting which files are BSD-licenced

* Fri Aug 08 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-4
- don't create bogus soname (patch by Xavier)

* Thu Jul 17 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-3
- fix tr call to remove DOS EOL
- build the library with -fPIC on arm and i686, too

* Sun Jul 13 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-2
- use version in source URL
- update License tag
- fix EOL in drag-uncrustify.bat
- don't link test binaries with shared binary on x86 (segfault)

* Thu Jul 10 2014 Dominik Mierzejewski <rpm@greysector.net> 1.2-1
- initial build
- fix pkgconfig file install location
- link test binaries with shared library
