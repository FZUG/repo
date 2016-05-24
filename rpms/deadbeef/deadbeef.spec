%global _with_restricted 1

Name:          deadbeef
Version:       0.7.2
Release:       3%{?dist}
Summary:       GTK+ audio player
License:       GPLv2
Group:         Applications/Multimedia
Url:           https://github.com/Alexey-Yakovenko/deadbeef
Source0:       https://github.com/Alexey-Yakovenko/deadbeef/archive/0.7.2/%{name}-%{version}.tar.gz
Patch0:        desktop.patch

BuildRequires: bison
BuildRequires: libtool intltool
BuildRequires: turbojpeg-devel
BuildRequires: yasm-devel
BuildRequires: libX11-devel
BuildRequires: pkgconfig(alsa)
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(flac)
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: pkgconfig(gtk+-3.0)
BuildRequires: pkgconfig(imlib2)
BuildRequires: pkgconfig(jansson)
BuildRequires: pkgconfig(libcddb)
BuildRequires: pkgconfig(libcdio)
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libnotify)
BuildRequires: pkgconfig(libpulse)
BuildRequires: pkgconfig(libzip)
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(samplerate)
BuildRequires: pkgconfig(sndfile)
BuildRequires: pkgconfig(vorbis)
BuildRequires: pkgconfig(wavpack)
%if 0%{?_with_restricted}
BuildRequires: faad2-devel
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libmpg123)
BuildRequires: pkgconfig(mad)
%endif
BuildRequires: desktop-file-utils
Requires: desktop-file-utils
Recommends: %{name}-plugins-extra%{?_isa} = %{version}-%{release}

%description
DeaDBeeF is an audio player for GNU/Linux and other UNIX-like systems.
It is written in C with some plugins in C++. It has minimal dependencies,
a native GTK2 GUI, cuesheet support, support for MP3, Ogg, FLAC, and APE,
chiptune formats with subtunes, song-length databases, and more.
It is very fast and lightweight, and extensible using plugins
(DSP, GUI, output, input, etc.). The GUI looks similar to Foobar2000.

%if 0%{?_with_restricted}
%package plugins-extra
License:        LGPLv2
Summary:        Restricted plugins Support for %{name}
Group:          Applications/Multimedia
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description plugins-extra
XMMS2 is an audio framework, but it is not a general multimedia player - it
will not play videos. It has a modular framework and plugin architecture for
audio processing, visualisation and output, but this framework has not been
designed to support video. Also the client-server design of XMMS2 (and the
daemon being independent of any graphics output) practically prevents direct
video output being implemented. It has support for a wide range of audio
formats, which is expandable via plugins. It includes a basic CLI interface
to the XMMS2 framework, but most users will want to install a graphical XMMS2
client (such as gxmms2 or esperanza).
%endif

%package devel
License:        GPLv2
Group:          Development/Libraries
Summary:        Devel files for %name
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package provides headers to develop deadbeef plugins

%prep
%setup -q
%patch0 -p1

%build
./autogen.sh
%configure \
    --enable-src=yes \
%if 0%{?_with_restricted}
    --enable-ffmpeg \
%endif
    --disable-static
%make_build V=1

%install
%make_install
find %{buildroot} -type f -name '*.la' -delete -print
%find_lang %{name}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%postun
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}/
%{_bindir}/%{name}
%{_libdir}/%{name}/
%if 0%{?_with_restricted}
%exclude %{_libdir}/%{name}/aac.so*
%exclude %{_libdir}/%{name}/mp3.so*
%exclude %{_libdir}/%{name}/ddb_ao.so*
%exclude %{_libdir}/%{name}/ffmpeg.so*
%endif
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%if 0%{?_with_restricted}
%files plugins-extra
%defattr(-,root,root,-)
%{_libdir}/%{name}/aac.so*
%{_libdir}/%{name}/mp3.so*
%{_libdir}/%{name}/ddb_ao.so*
%{_libdir}/%{name}/ffmpeg.so*
%endif

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}

%changelog
* Tue May 24 2016 mosquito <sensor.wen@gmail.com> - 0.7.2-3
- Rebuild for fedora 24

* Tue May 3  2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.7.2-20160427-3762995-3
- dropped redundant flags

* Mon May 2  2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.7.2-20160427-3762995-2
- Added scriptlets

* Wed Apr 27 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.2-20160427-3762995-1
- Updated to 0.7.2-20160427-3762995

* Tue Mar 29 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.7.1-20160329-1cfcd8b-1
- Updated to 0.7.1-20160329-1cfcd8b

* Mon Aug 10 2015 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.3.1-20150810-acb0ee4-1
- Initial build
