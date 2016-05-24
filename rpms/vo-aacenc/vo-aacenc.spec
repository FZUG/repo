Name:       vo-aacenc
Version:    0.1.2
Release:    2%{?dist}
Summary:    VisualOn AAC encoder library
License:    ASL 2.0
URL:        http://opencore-amr.sourceforge.net/
Source0:    http://sourceforge.net/projects/opencore-amr/files/%{name}/%{name}-%{version}.tar.gz

%description
This library contains an encoder implementation of the Advanced Audio
Coding (AAC) audio codec. The library is based on a codec implementation
by VisualOn as part of the Stagefright framework from the Google
Android project.

This package is in the 'tainted' section because the AAC encoding
standard is covered by patents.

%package devel
Summary:    Development files for %{name}
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure --disable-static
%make_build

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.la' -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README NOTICE
%license COPYING
%{_libdir}/lib%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*.h
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue May 24 2016 mosquito <sensor.wen@gmail.com> - 0.1.2-2
- Rebuilt for fedora 24

* Thu May 17 2012 David Vasquez <davidjeremias82 AT gmail DOT com> - 0.1.2-1
- Initial build
