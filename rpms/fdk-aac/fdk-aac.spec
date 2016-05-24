Name:           fdk-aac
Version:        0.1.4
Release:        2%{?dist}
Summary:        Fraunhofer FDK AAC Codec Library
License:        Apache License v2.0
URL:            http://sourceforge.net/projects/opencore-amr
Source0:        https://github.com/mstorsjo/fdk-aac/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  pkgconfig
BuildRequires:  libtool

%description
The Fraunhofer FDK AAC Codec Library ("FDK AAC Codec") is software that
implements the MPEG Advanced Audio Coding ("AAC") encoding and decoding
scheme for digital audio.

For further information, read:
http://wiki.hydrogenaud.io/Fraunhofer_FDK_AAC

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
libtoolize
aclocal
automake --add-missing
autoreconf --verbose
%configure --enable-shared --disable-static
# make gcc5/gcc6 happy
make CXXFLAGS='%{optflags} -std=c++11 -Wno-narrowing' V=1 %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name '*.la' -delete -print

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog NOTICE
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root,-)
%doc documentation/*.pdf
%dir %{_includedir}/fdk-aac
%{_includedir}/fdk-aac/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue May 24 2016 mosquito <sensor.wen@gmail.com> - 0.1.4-2
- Rebuild for fedora 24

* Tue Feb 23 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.1.4-2
- Rebuilt

* Fri Oct 30 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.1.4-1
- Initial build
