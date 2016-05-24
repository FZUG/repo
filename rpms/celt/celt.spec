Name:          celt
Version:       0.11.3
Release:       2%{?dist}
Summary:       An audio codec for use in low-delay speech and audio communication

Group:         System Environment/Libraries
License:       BSD
URL:           http://www.celt-codec.org/
Source0:       http://downloads.us.xiph.org/releases/%{name}/%{name}-%{version}.tar.gz

BuildRequires: libtool
BuildRequires: pkgconfig(ogg)

%description
CELT (Constrained Energy Lapped Transform) is an ultra-low delay audio
codec designed for realtime transmission of high quality speech and audio.
This is meant to close the gap between traditional speech codecs
(such as Speex) and traditional audio codecs (such as Vorbis).

%package devel
Summary:  Development package for celt
Group:    Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig(ogg)

%description devel
Files for development with celt.

%prep
%setup -q

%build
autoreconf --force --install --verbose
%configure --enable-custom-modes --disable-static

# Remove rpath as per https://fedoraproject.org/wiki/Packaging/Guidelines#Beware_of_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/*.la

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README TODO
%license COPYING
%{_bindir}/celtenc
%{_bindir}/celtdec
%{_libdir}/libcelt0.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/celt
%{_libdir}/pkgconfig/celt.pc
%{_libdir}/libcelt0.so

%changelog
* Tue May 24 2016 mosquito <sensor.wen@gmail.com> - 0.11.3-2
- Rebuild for fedora 24

* Fri Jan 23 2015 David Vásquez <davidjeremias82 AT gmail DOT com> 0.11.3-2
- Upstream

* Thu Feb  6 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.3-1
- 0.11.3 release

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 20 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-2
- add --enable-custom-modes

* Wed Feb 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> 0.11.1-1
- New 0.11.1 release

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.10.0-1
- New 0.10.0 release

* Wed Sep 29 2010 jkeating - 0.8.1-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-1
- New 0.8.1 release

* Fri Jul  2 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.0-2
- Cleanup the spec file and update lib names

* Fri Jul  2 2010 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.0-1
- New 0.8.0 upstream release

* Fri Oct 30 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.7.0-1
- New 0.7.0 upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul  6 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.6.0-1
- New 0.6.0 upstream release

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.2-1
- New upstream release, remove note about license as fix upstream

* Mon Feb 2 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-2
- Updates for package review

* Mon Jan 5 2009 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.1-1
- Initial package
