%global with_plugins_nonfree 1
%if 0%{?with_plugins_freeworld} 
    %global plugins freeworld
%endif
%if 0%{?with_plugins_nonfree}
    %global plugins nonfree
%endif
%global realname sox

Name:           sox%{?plugins:-plugins-%{plugins}}
Summary:        A general purpose sound file conversion tool
Version:        14.4.2
Release:        1%{?dist}
License:        GPLv2+ and LGPLv2+ and MIT

URL:            http://sox.sourceforge.net/
Source: http://downloads.sourceforge.net/%{realname}/%{realname}-%{version}.tar.gz
#Modified source tarball with libgsm license, without unlicensed liblpc10
#Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz

Patch0:         sox-14.4.2-lsx_error.patch
Patch1:         sox-14.4.1-lpc10.patch

BuildRequires: libvorbis-devel
BuildRequires: alsa-lib-devel, libtool-ltdl-devel, libsamplerate-devel
BuildRequires: gsm-devel, wavpack-devel, ladspa-devel, libpng-devel
BuildRequires: flac-devel, libao-devel, libsndfile-devel, libid3tag-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: libtool
# Additional requirements for RPM Fusion
%if 0%{?with_plugins_freeworld}
BuildRequires:  lame-devel ladspa-devel
BuildRequires:  libmad-devel
%endif
%if 0%{?with_plugins_nonfree}
BuildRequires:  amrwb-devel amrnb-devel ladspa-devel
%endif
%if 0%{?with_plugins_freeworld} || 0%{?with_plugins_nonfree}
# Need to require sox
Requires:       sox%{?_isa}
%endif

%description
SoX (Sound eXchange) is a sound file format converter SoX can convert
between many different digitized sound formats and perform simple
sound manipulation functions, including sound effects.

%if 0%{?with_plugins_freeworld}
This package provides the plugin for MPEG-2 audio layer 3 audio (MP3) support.
%endif
%if 0%{?with_plugins_nonfree}
This package provides the plugins for Adaptive Multi-Rate Wideband and
Narrowband codecs.
%endif


%if ! 0%{?with_plugins_freeworld} && ! 0%{?with_plugins_nonfree}
%package -n  sox-devel
Summary: The SoX sound file format converter libraries
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description -n sox-devel
This package contains the library needed for compiling applications
which will use the SoX sound file format converter.
%endif


%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1 -b .lpc
#regenerate scripts from older autoconf to support aarch64
autoreconf -vfi


%build
export CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
%configure  --without-lpc10 \
            --without-gsm \
            --includedir=%{_includedir}/sox \
            --disable-static \
            --with-distro=Fedora \
            --with-dyn-default \
%if 0%{?with_plugins_freeworld}
            --with-mp3=dyn \
            --without-flac \
            --without-amrnb \
            --without-amrwb
%endif
%if 0%{?with_plugins_nonfree}
            --with-amrwb=dyn \
            --with-amrnb=dyn \
            --without-flac \
            --without-mp3
%endif
make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libsox.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/sox/*.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/sox/*.a

# Remove all the plugins execept the one we want.
%if 0%{?with_plugins_freeworld}
find %{buildroot}%{_libdir}/sox -name "*.so" \! -name "*mp3.so" -exec rm -f {} \;
%endif
%if 0%{?with_plugins_nonfree}
find %{buildroot}%{_libdir}/sox -name "*.so" \! -name "*amr*.so" -exec rm -f {} \;
%endif


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%doc AUTHORS ChangeLog COPYING README
%if 0%{?with_plugins_freeworld}
%{_libdir}/sox/libsox_fmt_mp3.so
%endif
%if 0%{?with_plugins_nonfree}
%{_libdir}/sox/libsox_fmt_amr*.so
%endif
%if 0%{?with_plugins_freeworld} || 0%{?with_plugins_nonfree}
%exclude %{_bindir}
%exclude %{_datadir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so*
%exclude %{_libdir}/pkgconfig
%else
%{_bindir}/play
%{_bindir}/rec
%{_bindir}/sox
%{_bindir}/soxi
%{_libdir}/libsox.so.*
%dir %{_libdir}/sox/
%{_libdir}/sox/libsox_fmt_*.so
%{_mandir}/man1/*
%{_mandir}/man7/*

%files -n sox-devel
%{_includedir}/sox
%{_libdir}/libsox.so
%{_libdir}/pkgconfig/sox.pc
%{_mandir}/man3/*
%endif


%changelog
* Thu Jul  2 2015 Richard Shaw <hobbes1069@gmail.com> - 14.4.2-1
- Update to latest upstream release.

* Fri Feb 13 2015 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-7
- patch missing size checks, https://bugzilla.redhat.com/show_bug.cgi?id=1174792

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jul 25 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-4
- removed liblpc10 from source tarball due to licensing uncertainity
- added license file to libgsm
- fixed bogus dates in changelog

* Tue Apr 02 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-3
- added autoreconf to replace old scropts => support aarch64

* Fri Feb 15 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-2
- added sox-mcompand_clipping.patch to prevent integer overflow

* Thu Feb 14 2013 Frantisek Kluknavsky <fkluknav@redhat.com> - 14.4.1-1
- rebase to 14.4.1

* Tue Sep 18 2012 Honza Horak <hhorak@redhat.com> - 14.4.0-3
- Minor spec file fixes
 
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 09 2012 Honza Horak <hhorak@redhat.com> - 14.4.0-1
- updated to upstream version 14.4.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 07 2011 Adam Jackson <ajax@redhat.com> 14.3.2-2
- Rebuild for libpng 1.5

* Sat Mar 19 2011 Felix Kaechele <heffer@fedoraproject.org> - 14.3.2-1
- 14.3.2
- added PulseAudio support

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
