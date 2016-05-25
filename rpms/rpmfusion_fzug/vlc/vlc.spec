# https://wiki.videolan.org/Category:Building
%global _commit 45bc33349134f308a1a9a5cc01995adc113ea96f
%global _scommit %(c=%{_commit}; echo ${c:0:7})

%bcond_without bootstrap
%bcond_without workaround_circle_deps
%bcond_without vaapi
%bcond_without vdpau
%bcond_without bluray
%bcond_without opencv
%bcond_without fluidsynth
%bcond_without qt5
%bcond_with    qt4
%bcond_without wayland
%if 0%{?fedora}
%bcond_without freerdp
%bcond_without projectm
%bcond_without schroedinger
%endif
%ifarch x86_64 i686
%bcond_without crystalhd
%endif

# Those are dependencies which are NOT provided in Fedora, mostly for legal reasons.
%if 0%{?!_without_freeworld:1}
%bcond_without a52dec
%bcond_without faad2
%bcond_without fdkaac
%bcond_without ffmpeg
%bcond_without libdca
%bcond_without libdvbpsi
%bcond_without libmad
%bcond_without libmpeg2
%bcond_without live555
%bcond_without twolame
%bcond_without x264
%bcond_without x265
%bcond_without xvidcore
%endif

Summary:       The cross-platform open-source multimedia framework, player and server
Name:          vlc
Version:       3.0.0
Release:       1.git%{_scommit}%{?dist}
License:       GPLv2+ and LGPLv2.1+
Group:         Applications/Multimedia
URL:           http://www.videolan.org
Source0:       https://github.com/videolan/vlc/archive/%{_commit}/%{name}-%{_scommit}.tar.gz

# Base tools
BuildRequires: libtool
BuildRequires: gettext-devel
BuildRequires: pkgconfig(dbus-1)
BuildRequires: pkgconfig(lua) >= 5.1
BuildRequires: pkgconfig(zlib)
%if %{with qt5}
BuildRequires: pkgconfig(Qt5Core) >= 5.2.0
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5X11Extras)
%endif
%if %{with qt4}
BuildRequires: pkgconfig(QtCore) >= 4.8.0
BuildRequires: pkgconfig(QtGui) >= 4.8.0
%endif
BuildRequires: desktop-file-utils
BuildRequires: fdupes
# Images
BuildRequires: libpng-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: pkgconfig(SDL_image) >= 1.2.10
BuildRequires: libtiff-devel
# Access
BuildRequires: libshout-devel
BuildRequires: pkgconfig(libarchive) >= 3.1.0
%if %{with live555}
BuildRequires: live555-devel >= 2015.01.27
%endif
BuildRequires: pkgconfig(libavc1394) >= 0.5.3
BuildRequires: pkgconfig(libdc1394-2) >= 2.1.0
BuildRequires: pkgconfig(libraw1394) >= 2.0.1
BuildRequires: pkgconfig(dvdread) > 4.9.0
BuildRequires: pkgconfig(dvdnav) > 4.9.0
%if %{with bluray}
BuildRequires: pkgconfig(libbluray) >= 0.5.0
%endif
%if %{with opencv}
BuildRequires: pkgconfig(opencv) > 2.0
%endif
BuildRequires: pkgconfig(smbclient)
BuildRequires: pkgconfig(libssh2)
BuildRequires: libnfs-devel
BuildRequires: pkgconfig(libv4l2)
BuildRequires: pkgconfig(libvcdinfo)
BuildRequires: vcdimager-devel >= 0.7.21
BuildRequires: pkgconfig(libcddb) >= 0.9.5
BuildRequires: pkgconfig(libcdio) >= 0.78.2
BuildRequires: pkgconfig(libvncclient) >= 0.9.9
%if %{with freerdp}
BuildRequires: pkgconfig(freerdp) >= 1.0.1
%endif
# Demuxers and Muxers
BuildRequires: pkgconfig(libsidplayfp)
%if %{with libdvbpsi}
BuildRequires: libdvbpsi-devel >= 1.2.0
%endif
BuildRequires: pkgconfig(ogg) >= 1.0
BuildRequires: pkgconfig(shout) >= 2.1
BuildRequires: libmkv-devel
BuildRequires: pkgconfig(libmodplug) >= 0.8.4
BuildRequires: libebml-devel
BuildRequires: libmatroska-devel
BuildRequires: pkgconfig(libgme)
BuildRequires: libmp4v2-devel
# Codecs
BuildRequires: pkgconfig(vorbis) >= 1.1
BuildRequires: pkgconfig(vorbisenc) >= 1.1
BuildRequires: pkgconfig(theoradec) >= 1.0
BuildRequires: pkgconfig(theoraenc)
BuildRequires: pkgconfig(speex)
BuildRequires: pkgconfig(flac)
%if %{with x264}
BuildRequires: x264-devel >= 0.86
%endif
%if %{with x265}
BuildRequires: pkgconfig(x265)
%endif
%if %{with a52dec}
BuildRequires: a52dec-devel
%endif
%if %{with libmpeg2}
BuildRequires: pkgconfig(libmpeg2)
%endif
%if %{with vaapi}
BuildRequires: pkgconfig(libva)
%endif
%if %{with workaround_circle_deps}
BuildRequires: phonon-backend-gstreamer
%endif
BuildRequires: gstreamer1-plugins-base-devel
%if %{with faad2}
BuildRequires: faad2-devel
%endif
BuildRequires: faac-devel
BuildRequires: lame-devel
%if %{with ffmpeg}
BuildRequires: pkgconfig(libavcodec)
BuildRequires: pkgconfig(libavformat)
BuildRequires: pkgconfig(libavutil)
BuildRequires: pkgconfig(libswscale)
BuildRequires: pkgconfig(libpostproc)
%endif
BuildRequires: pkgconfig(mad)
%if %{with schroedinger}
BuildRequires: pkgconfig(schroedinger-1.0) >= 1.0.10
%endif
%if %{with libdca}
BuildRequires: pkgconfig(libdca) >= 0.0.5
%endif
%if %{with twolame}
BuildRequires: pkgconfig(twolame)
%endif
BuildRequires: libmpcdec-devel
BuildRequires: pkgconfig(libass) >= 0.9.8
BuildRequires: gsm-devel
%if %{with fluidsynth}
BuildRequires: pkgconfig(fluidsynth) >= 1.1.2
%endif
BuildRequires: pkgconfig(zvbi-0.2) >= 0.2.28
BuildRequires: pkgconfig(opus) >= 1.0.3
%if %{with xvidcore}
BuildRequires: xvidcore-devel
%endif
BuildRequires: libvpx-devel
%if %{with fdkaac}
BuildRequires: fdk-aac-devel
%endif
BuildRequires: libmpg123-devel
BuildRequires: pkgconfig(kate) >= 0.3.0
BuildRequires: libtiger-devel
%if %{with crystalhd}
BuildRequires: libcrystalhd-devel
%endif
BuildRequires: pkgconfig(dirac)
# Video plugins, X-libs
BuildRequires: libXt-devel
BuildRequires: libXv-devel
BuildRequires: libXxf86vm-devel
BuildRequires: libX11-devel
BuildRequires: libXext-devel
BuildRequires: libXpm-devel
%{!?_without_xcb:
BuildRequires: libxcb-devel
BuildRequires: xcb-util-devel
BuildRequires: pkgconfig(xcb-keysyms) >= 0.3.4
}
BuildRequires: xorg-x11-proto-devel
%if %{with wayland}
BuildRequires: pkgconfig(wayland-scanner)
BuildRequires: pkgconfig(wayland-egl)
%endif
BuildRequires: pkgconfig(gtk+-2.0)
%if %{with vdpau}
BuildRequires: pkgconfig(vdpau) >= 0.6
%endif
BuildRequires: pkgconfig(sdl) >= 1.2.10
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fribidi)
BuildRequires: harfbuzz-devel
BuildRequires: pkgconfig(librsvg-2.0) >= 2.9.0
BuildRequires: aalib-devel
BuildRequires: pkgconfig(caca) >= 0.99.beta14
# Audio plugins
BuildRequires: pkgconfig(libpulse) >= 1.0
BuildRequires: pkgconfig(alsa) >= 1.0.24
BuildRequires: pkgconfig(jack) >= 1.9.7
BuildRequires: pkgconfig(samplerate)
BuildRequires: pkgconfig(libchromaprint) >= 0.6.0
# Others
BuildRequires: libtar-devel
BuildRequires: pkgconfig(ncursesw)
BuildRequires: lirc-devel
%if %{with projectm}
BuildRequires: pkgconfig(libprojectM)
%endif
BuildRequires: pkgconfig(avahi-client) >= 0.6
BuildRequires: pkgconfig(libudev) >= 142
BuildRequires: pkgconfig(libmtp) >= 1.0.0
BuildRequires: pkgconfig(libupnp)
BuildRequires: pkgconfig(libxml-2.0) >= 2.5
BuildRequires: libgcrypt-devel
BuildRequires: pkgconfig(gnutls) >= 3.2.8
BuildRequires: pkgconfig(taglib) >= 1.9
BuildRequires: libgpg-error-devel
BuildRequires: pkgconfig(libnotify)
BuildRequires: kde-filesystem

BuildRequires: cdparanoia-devel
BuildRequires: game-music-emu-devel
BuildRequires: libdv-devel
BuildRequires: minizip-devel
%{?_with_gnomevfs:BuildRequires: gnome-vfs2-devel}
%if 0%{?fedora} < 24
BuildRequires: libmusicbrainz-devel
%endif
BuildRequires: pkgconfig(gl)
BuildRequires: pkgconfig(glu)
BuildRequires: pkgconfig(libidn)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(slang)
BuildRequires: gdk-pixbuf2-devel
BuildRequires: xosd-devel

Provides: %{name}-xorg%{?_isa} = %{version}-%{release}
Requires: %{name}-core%{?_isa} = %{version}-%{release}
Requires: kde-filesystem
Requires: dejavu-sans-fonts
Requires: dejavu-sans-mono-fonts
Requires: dejavu-serif-fonts
# For xdg-sreensaver
Requires: xdg-utils

%description
VLC media player is a highly portable multimedia player and multimedia framework
capable of reading most audio and video formats as well as DVDs, Audio CDs VCDs,
and various streaming protocols.

It can also be used as a media converter or a server to stream in uni-cast or
multi-cast in IPv4 or IPv6 on networks.

%package devel
Summary:       Development files for %{name}
Group:         Development/Libraries
Requires:      %{name}-core%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package core
Summary:       VLC media player core
Group:         Applications/Multimedia
Provides:      %{name}-nox = %{version}-%{release}
Obsoletes:     %{name}-nox < 1.1.5-2
%{?live555_version:Requires: live555%{?_isa} = %{live555_version}}

%description core
VLC media player core components

%package extras
Summary:       VLC media player with extras modules
Group:         Applications/Multimedia
Requires:      %{name}-core%{?_isa} = %{version}-%{release}

%description extras
VLC media player extras modules.

%package plugin-jack
Summary:       JACK audio plugin for VLC
Group:         Applications/Multimedia
Requires:      %{name}-core%{?_isa} = %{version}-%{release}

%description plugin-jack
JACK audio plugin for the VLC media player.

%prep
%setup -q -n %{name}-%{_commit}
%if %{with bootstrap}
rm aclocal.m4 m4/lib*.m4 m4/lt*.m4 || :
./bootstrap
echo '%{version}-git.%{_scommit}' > src/revision.txt
%endif

# fix builddate info
# Remove build time references so build-compare can do its work
BUILDTIME=$(LC_ALL=C date -u '+%%H:%%M')
BUILDDATE=$(LC_ALL=C date -u '+%%b %%e %%Y')
sed -e "s/__TIME__/\"$BUILDTIME\"/" -i modules/gui/qt/dialogs/help.cpp src/config/help.c
sed -e "s/__DATE__/\"$BUILDDATE\"/" -i modules/gui/qt/dialogs/help.cpp src/config/help.c

%build
%configure \
    --disable-dependency-tracking                   \
    --enable-optimizations                          \
    --enable-fast-install                           \
%if 0%{?fedora} >= 22 && %{?_arch} == i686
    --disable-mmx --disable-sse                     \
%endif
    --disable-silent-rules                          \
    --with-pic                                      \
    --disable-rpath                                 \
    --with-binary-version=%{version}                \
    --with-kde-solid=%{_kde4_appsdir}/solid/actions \
    --enable-httpd                                  \
%if ! %{with live555}
    --disable-live555                               \
%endif
    --enable-dvdread                                \
    --enable-dvdnav                                 \
%if ! %{with bluray}
    --disable-bluray                                \
%endif
%if ! %{with opencv}
    --disable-opencv                                \
%endif
    --enable-smbclient                              \
    --enable-sftp                                   \
    --disable-dsm                                   \
    --enable-v4l2                                   \
    --enable-vcd                                    \
    --enable-vcdx                                   \
    --enable-libcddb                                \
    --enable-vnc                                    \
%if ! %{with freerdp}
    --disable-freerdp                               \
%endif
    --enable-realrtsp                               \
%if ! %{with dvbpsi}
    --disable-dvbpsi                                \
%endif
    --enable-ogg                                    \
    --enable-shout                                  \
    --enable-mkv                                    \
    --enable-mod                                    \
    --enable-omxil                                  \
    --enable-omxil-vout                             \
%{?_with_rpi:
    --enable-rpi-omxil                              \
    --enable-mmal-codec                             \
    --enable-mmal-vout                              \
}                                                   \
%if ! %{with libmad}
    --disable-mad                                   \
%endif
%if ! %{with ffmpeg}
    --disable-avcodec --disable-avformat            \
    --disable-swscale --disable-postproc            \
%endif
%if ! %{with vaapi}
    --disable-libva                                 \
%endif
%if ! %{with faad2}
    --disable-faad                                  \
%endif
    --enable-vpx                                    \
%if ! %{with twolame}
    --disable-twolame                               \
%endif
%if %{with fdkaac}
    --enable-fdkaac                                 \
%endif
%if ! %{with a52dec}
    --disable-a52                                   \
%endif
%if ! %{with libdca}
    --disable-dca                                   \
%endif
    --enable-flac                                   \
%if ! %{with libmpeg2}
    --disable-libmpeg2                              \
%endif
    --enable-vorbis                                 \
    --enable-tremor                                 \
    --enable-speex                                  \
    --enable-theora                                 \
%if ! %{with x264}
    --disable-x264                                  \
%endif
%if ! %{with x265}
    --disable-x265                                  \
%endif
    --enable-libass                                 \
    --enable-kate                                   \
    --disable-gles2                                 \
    %{!?_without_xcb:--enable-xcb --enable-xvideo}  \
    %{?_without_xcb:--disable-xcb --disable-xvideo} \
%if ! %{with vdpau}
    --disable-vdpau                                 \
%endif
%if ! %{with wayland}
    --disable-wayland                               \
%endif
    --enable-freetype                               \
    --enable-fribidi                                \
    --enable-svg                                    \
    --enable-svgdec                                 \
    --enable-aa                                     \
    --enable-caca                                   \
    --enable-pulse                                  \
    --enable-alsa                                   \
    --disable-oss                                   \
    --enable-jack                                   \
%if ! %{with qt4}
    --disable-skins2                                \
%endif
    --enable-ncurses                                \
    --enable-lirc

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot} INSTALL="install -p" CPPROG="cp -p"
find %{buildroot} -type f -name "*.la" -delete -print

desktop-file-install --vendor "" \
	--dir %{buildroot}%{_datadir}/applications \
	--delete-original \
	--mode 644 \
	%{buildroot}%{_datadir}/applications/vlc.desktop

mkdir -p %{buildroot}/%{_datadir}/pixmaps
ln -s %{_datadir}/icons/hicolor/48x48/apps/vlc.png %{buildroot}/%{_datadir}/pixmaps/vlc.png

# add missing manfiles
for i in ?vlc; do
    pushd %{buildroot}/%{_mandir}/man1
    ln -s vlc.1 $i.1
    popd
done

%fdupes %{buildroot}%{_datadir}/%{name}
%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
%{_bindir}/update-desktop-database &>/dev/null || :
%{_libdir}/vlc/vlc-cache-gen -f %{_libdir}/vlc &>/dev/null || :

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
    %{_bindir}/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor || :
fi
%{_bindir}/update-desktop-database &>/dev/null || :
%{_libdir}/vlc/vlc-cache-gen -f %{_libdir}/vlc &>/dev/null || :

%posttrans
%{_bindir}/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor || :

%post core -p /sbin/ldconfig

%preun core
if [ $1 -eq 0 ]; then
    rm -f %{_libdir}/vlc/plugins*.dat
fi || :

%postun core -p /sbin/ldconfig

%posttrans core
%{_libdir}/vlc/vlc-cache-gen -f %{_libdir}/vlc &>/dev/null || :

%post extras
if [ $1 -eq 1 ]; then
    %{_libdir}/vlc/vlc-cache-gen -f %{_libdir}/vlc &>/dev/null || :
fi

%postun extras
if [ $1 -eq 0 ]; then
    %{_libdir}/vlc/vlc-cache-gen -f %{_libdir}/vlc &>/dev/null || :
fi

%post plugin-jack
if [ $1 -eq 1 ]; then
    %{_libdir}/vlc/vlc-cache-gen -f %{_libdir}/vlc &>/dev/null || :
fi

%postun plugin-jack
if [ $1 -eq 0 ]; then
    %{_libdir}/vlc/vlc-cache-gen -f %{_libdir}/vlc &>/dev/null || :
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS NEWS README THANKS
%license COPYING COPYING.LIB
%{_bindir}/qvlc
%if %{with qt4}
%{_bindir}/svlc
%{_datadir}/vlc/skins2/
%{_libdir}/vlc/plugins/gui/libqt_plugin.so
%{_libdir}/vlc/plugins/gui/libskins2_plugin.so
%endif
%{_libdir}/vlc/plugins/audio_output/libpulse_plugin.so
%{_libdir}/vlc/plugins/video_output/libaa_plugin.so
%{_libdir}/vlc/plugins/video_output/libcaca_plugin.so
%{!?_without_xcb:
%{_libdir}/vlc/plugins/access/libxcb_screen_plugin.so
%{_libdir}/vlc/plugins/video_output/libxcb_glx_plugin.so
%{_libdir}/vlc/plugins/video_output/libxcb_window_plugin.so
%{_libdir}/vlc/plugins/video_output/libxcb_x11_plugin.so
%{_libdir}/vlc/plugins/video_output/libxcb_xv_plugin.so
}
%if %{with projectm}
%{_libdir}/vlc/plugins/visualization/libprojectm_plugin.so
%endif
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/kde4/apps/solid/actions/vlc-*.desktop
%{_datadir}/icons/hicolor/*/apps/vlc*.png
%{_datadir}/icons/hicolor/*/apps/vlc*.xpm
%{_datadir}/pixmaps/vlc.png

%files core -f %{name}.lang
%defattr(-,root,root,-)
%doc %{_datadir}/doc/%{name}
%{_bindir}/vlc
%{_bindir}/cvlc
%{_bindir}/nvlc
%{_bindir}/rvlc
%{_bindir}/vlc-wrapper
%if %{with qt4}
%exclude %{_datadir}/vlc/skins2/
%exclude %{_libdir}/vlc/plugins/gui/libqt_plugin.so
%exclude %{_libdir}/vlc/plugins/gui/libskins2_plugin.so
%endif
%exclude %{_libdir}/vlc/plugins/access/libaccess_jack_plugin.so
%{?_with_vcdimager:
%exclude %{_libdir}/vlc/plugins/access/libvcd_plugin.so
%exclude %{_libdir}/vlc/plugins/access/libvcdx_plugin.so
%exclude %{_libdir}/vlc/plugins/codec/libsvcdsub_plugin.so
}
%if %{with crystalhd}
%exclude %{_libdir}/vlc/plugins/codec/libcrystalhd_plugin.so
%endif
%if %{with fluidsynth}
%exclude %{_libdir}/vlc/plugins/codec/libfluidsynth_plugin.so
%endif
%{!?_without_xcb:
%exclude %{_libdir}/vlc/plugins/access/libxcb_screen_plugin.so
%if 0%{?fedora} < 17
%exclude %{_libdir}/vlc/plugins/control/libglobalhotkeys_plugin.so
%endif
%exclude %{_libdir}/vlc/plugins/video_output/libaa_plugin.so
%exclude %{_libdir}/vlc/plugins/video_output/libcaca_plugin.so
%exclude %{_libdir}/vlc/plugins/video_output/libxcb_glx_plugin.so
%exclude %{_libdir}/vlc/plugins/video_output/libxcb_x11_plugin.so
%exclude %{_libdir}/vlc/plugins/video_output/libxcb_window_plugin.so
%exclude %{_libdir}/vlc/plugins/video_output/libxcb_xv_plugin.so
}
%if %{with opencv}
%exclude %{_libdir}/vlc/plugins/video_filter/libopencv_example_plugin.so
%exclude %{_libdir}/vlc/plugins/video_filter/libopencv_wrapper_plugin.so
%endif
%if %{with projectm}
%exclude %{_libdir}/vlc/plugins/visualization/libprojectm_plugin.so
%endif
%exclude %{_libdir}/vlc/plugins/audio_output/libjack_plugin.so
%exclude %{_libdir}/vlc/plugins/audio_output/libpulse_plugin.so
%ghost %{_libdir}/vlc/plugins.dat
%{_libdir}/vlc/
%{_libdir}/*.so.*
%{_datadir}/vlc/
%{_mandir}/man1/*vlc*.1*

%files plugin-jack
%defattr(-,root,root,-)
%{_libdir}/vlc/plugins/access/libaccess_jack_plugin.so
%{_libdir}/vlc/plugins/audio_output/libjack_plugin.so
%if %{with fluidsynth}
%{_libdir}/vlc/plugins/codec/libfluidsynth_plugin.so
%endif

%files extras
%defattr(-,root,root,-)
%if %{with opencv}
%{_libdir}/vlc/plugins/video_filter/libopencv_example_plugin.so
%{_libdir}/vlc/plugins/video_filter/libopencv_wrapper_plugin.so
%endif
%{?_with_vcdimager:
%{_libdir}/vlc/plugins/access/libvcd_plugin.so
%{_libdir}/vlc/plugins/access/libvcdx_plugin.so
%{_libdir}/vlc/plugins/codec/libsvcdsub_plugin.so
}
%if %{with crystalhd}
%{_libdir}/vlc/plugins/codec/libcrystalhd_plugin.so
%endif

%files devel
%defattr(-,root,root,-)
%dir %{_includedir}/vlc
%{_includedir}/vlc/*
%{_libdir}/libvlccore.so
%{_libdir}/libvlc.so
%{_libdir}/pkgconfig/libvlc.pc
%{_libdir}/pkgconfig/vlc-plugin.pc
%{_libdir}/vlc/libcompat.a
%if %{with vdpau}
%{_libdir}/vlc/libvlc_vdpau.so
%endif

%changelog
* Wed May 25 2016 mosquito <sensor.wen@gmail.com> - 3.0.0-1.git45bc333
- Update to 3.0.0-git45bc333

* Wed May 11 2016 Adrian Reber <adrian@lisas.de> - 2.2.3-2
- Disable freedrp and projectm on Fedora >= 24; fails compilation

* Wed May 04 2016 Nicolas Chauvet <kwizart@gmail.com> - 2.2.3-1
- Update to 2.2.3

* Sat Feb 06 2016 Nicolas Chauvet <kwizart@gmail.com> - 2.2.2-1
- Update to 2.2.2

* Tue Oct 06 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.2-0.1
- Update to 2.2.2 pre-version

* Sat May 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-6
- Rebuilt for x265

* Wed May 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-5
- Update to current bugfix

* Sat May 09 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-4
- Recreate the plugins cache on post for main - rfbz#3639
- %%ghost the cache plugins

* Sun Apr 26 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-3
- Fix build with freerdp for f22
- Disable optimizations
- Disable mmx and sse on fedora >= 22

* Thu Apr 16 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-2
- Rebuilt for x265

* Mon Apr 13 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.1-1
- Update to 2.2.1
- Enable x265 on armhfp
- Add --with rpi conditional for raspberrypi and mmal

* Fri Feb 27 2015 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-1
- Update to 2.2.0

* Tue Nov 25 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-0.2
- Update to 2.2.0-rc2

* Fri Nov 14 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-0.1
- Update to 2.2.0-rc1

* Sun Sep 28 2014 kwizart <kwizart@gmail.com> - 2.1.5-4
- Allow build with ffmpeg24

* Fri Sep 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.5-3
- Rebuilt for FFmpeg 2.4.x

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 2.1.5-2
- Rebuilt for ffmpeg-2.3

* Sat Jul 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.5-1
- Update to 2.1.5

* Sat Apr 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.4-5
- Rebuilt for libgcrypt

* Sat Mar 29 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.4-4
- Rebuilt for ffmpeg

* Sat Mar 22 2014 Sérgio Basto <sergio@serjux.com> - 2.1.4-3
- Rebuilt for x264

* Thu Mar 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.4-2
- Rebuilt for x264

* Fri Feb 21 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.4-1
- Update to 2.1.4

* Thu Feb 06 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.3-1
- Update to 2.1.3

* Fri Jan 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.1.2-2
- Disable freerdp for f21

* Tue Dec 10 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.2-1
- Update to 2.1.2

* Thu Nov 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.1-2
- Rebuilt for live555

* Thu Nov 14 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.1-1
- Update to 2.1.1

* Tue Nov 05 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-3
- Rebuilt for x264/FFmpeg

* Tue Oct 22 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-2
- Rebuilt for x264

* Tue Oct 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-1
- Update to 2.1.0

* Wed Aug 28 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-0.8.rc1
- Update to 2.1.0-rc1

* Thu Aug 15 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-0.6.pre2
- Rebuilt for FFmpeg 2.0.x

* Fri Jul 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-0.5.pre2
- Update to 2.1.0-pre2

* Sat Jul 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-0.4.pre1
- Rebuilt for x264

* Fri Jul 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-0.3.pre1
- Use Officially tagged 2.1.0-pre1

* Wed Jun 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-0.2.pre1
- Update to 2.1.0-pre1

* Mon Apr 08 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.6-1
- Update to 2.0.6

* Tue Mar 26 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.5-6
- Move %%{_datadir}/vlc/lua/http/.hosts to hosts-sample to avoid
  config file - https://bugzilla.rpmfusion.org/2726

* Sat Feb 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.5-5
- Fix samba4 detection rfbz#2659

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.5-4
- Add new live555 requires

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.5-3
- Rebuilt for ffmpeg/x264

* Wed Jan 02 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.0.5-2
- Fix build with FLAC-1.3.x

* Fri Dec 14 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.5-1
- Update to 2.0.5

* Sat Nov 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.4-3
- Fix build with kernel-3.7

* Fri Nov 23 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.4-2
- Rebuilt for x264

* Fri Oct 19 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.4-1
- Update to 2.0.4
- Enable opus
- Disable x86 loader
- Avoid rpath

* Wed Sep 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.3-3
- Fix --with fluidsynth typo

* Wed Sep 05 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.3-2
- Rebuilt for x264 ABI 125

* Fri Jul 20 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.3-1
- Update to 2.0.3

* Wed Jul 11 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.2-3
- Fix build of xcb
- Switch to pkgconfig(libudev)

* Wed Jul 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.2-2
- Rework BR and RPM conditionals
- Drop support for anything below EL-6 and current Fedora.

* Thu Jun 28 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.2-1
- Update to 2.0.2

* Sun Jun 24 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-3
- Rebuild for FFmpeg/x264

* Mon Jun 18 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-2
- Backport patch for ffmpeg54

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.1-1
- Update to 2.0.1

* Tue Mar 13 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-5
- Rebuilt for x264 ABI 0.120

* Fri Mar 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-4
- Rebuilt for c++ ABI breakage

* Sun Feb 26 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-3
- Reenable skins2 - rfbz#2195
- Disable internal live555 build

* Wed Feb 22 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-2
- Rebuilt for x264/FFmpeg

* Sun Feb 19 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-1
- Update to 2.0.0 (Final)

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0.0-0.9_rc1
- Update to 2.0.0-rc1

* Mon Jan 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-0.7_pre4
- Update to 1.2.0-pre4

* Mon Jan 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-0.6_pre3
- Add BR game-music-emu-devel
- move vcdimager plugin to vlc-extras

* Wed Dec 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-0.5_pre3
- Update to 1.2.0-pre3

* Tue Dec 13 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-0.4_pre2
- Rebuild for libbluray

* Sat Dec 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-0.3_pre2
- Rebuilt with xz to workaround rfbz#2086

* Wed Dec 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.2.0-0.2_pre2
- Update to 1.2.0-pre2
- Reverse build conditional to --without freeworld
  So it can be tested with Fedora only (patches welcomed)
- Disable xcb globalhotkeys in Rawhide/F-17

* Fri Oct 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.12-1
- Update to 1.1.12
- Add 2 already merged patches

* Tue Sep 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.11-2
- Update to current bugfix
- Add patch for FFmpeg-0.8

* Wed Jul 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.11-1
- Update to 1.1.11

* Fri Jul 15 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.10-2
- Rebuilt for x264 ABI 115

* Mon Jun 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.10-1
- Update to 1.1.10
- backport from 1.1-bugfix
- Re-add mozilla-vlc for f15

* Tue May 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.9-2
- Rebuilt for libdvbpsi

* Tue Apr 12 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.9-1
- Update to 1.1.9

* Wed Apr 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.8-2
- Backport youtube lua fix - rfbz#1675

* Thu Mar 24 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.8-1
- Update to 1.1.8

* Fri Mar 11 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.8-0.2.1
- Rebuilt for new x264/FFmpeg

* Mon Mar 07 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.8-0.1.1
- Update to pre-1.1.8 bugfix git from today

* Wed Feb 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.7-1
- Update to 1.1.7

* Sat Jan 29 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.6.1-1
- Update to 1.1.6.1
- Remove merged patches

* Mon Jan 24 2011 Nicolas Chauvet <kwizart@gmail.com> - 1.1.6-2
- Update to 1.1.6
- backport lirc and signal fixes

* Sat Dec 18 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.5-2
-  Clear execstack on dmo and real plugin for i686

* Sun Nov 14 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.5-1
- Update to 1.1.5
- Rename nox subpackage to extras
- Move opencv modules to extras
- Move libnotify module to extras until f15

* Wed Nov 10 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.4-6
- Disable notify by f15 - deprecated upstream
- Fix libProjectM crash once selected.
- Fix default CA file for gnutls module.
- xosd not built by default - deprecated upstream

* Tue Nov 09 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.4-5
- Enable VAAPI

* Sun Oct 24 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.4-4
- Workaround for taglib not been tread safe

* Sun Oct 17 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.4-3
- Explicitely use -fPIC compilation even for dmo plugin
- Silence post scriptlet

* Sun Sep 05 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.4-2
- Adds support for vlc-cache-gen
- Drop support for vlc-handlers.schemas
  (will be handled in .desktop file)

* Sat Aug 28 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.4-1
- Update to 1.1.4
- Fix libnotify build on f14
- Obsoletes ffmpeg4vlc
- Raise selinux requirements that fix rhbz#591854

* Sat Aug 21 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.3-1
- Update to 1.1.3
- move some plugin from core to main

* Thu Aug 05 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.2-1
- Update to 1.1.2

* Thu Jul 01 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Sat Jun 12 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-0.12.rc3
- Update to -rc3

* Tue Jun 08 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-0.11.rc2
- Fix segfault on dlopen

* Mon Jun 07 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-0.10.rc2
- Fix --with a52dec conditional

* Fri Jun 04 2010 Nicolas Chauvet <kwizart@gmail.com> - 1.1.0-0.9.rc2
- Update to 1.1.0-rc2

* Sun May  2 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.0-0.6.pre3
- Update to 1.1.0-pre3
- Add patch from rdieter

* Fri Apr 16 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.1.0-0.3.pre1
- Update to 1.1.0-pre1
- Built for Fedora
- Changed summary and descriptions

* Sat Feb 27 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0.5-2
- Add BR libtiger-devel

* Thu Jan 28 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Tue Jan 26 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0.4-3
- Rebuild

* Sun Jan  3 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0.4-2
- Add vlc-1.0.4-xulrunner-192.patch

* Tue Dec 15 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4
- Drop patch2 - PulseaAudio is tried first from original sources.

* Sat Oct 31 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Sun Oct 25 2009 kwizart < kwizart at gmail.com > - 1.0.3-0.1_rc
- Update to 1.0.3-rc
- Update bugfix to 20091025
- Clean dc1394 sub-package

* Fri Oct 16 2009 kwizart < kwizart at gmail.com > - 1.0.2-2
- Update to 1.0-bugfix 20091016
- Rebuild for x264/ffmpeg

* Sun Sep 27 2009 kwizart < kwizart at gmail.com > - 1.0.2-1.2
- Disable the workaround for the compiler bug. (rhbz#524439)
- Resync with the fonts requirement.

* Sun Sep 20 2009 kwizart < kwizart at gmail.com > - 1.0.2-1.1
- Workaround the compiler bug on x86 x86_64 by disabling optimization.

* Sat Sep 19 2009 kwizart < kwizart at gmail.com > - 1.0.2-1
- Update to 1.0.2

* Wed Aug 12 2009 kwizart < kwizart at gmail.com > - 1.0.1-2
- Conditionalize libass until stabilized ABI.
- Update to 1.0-bugfix 20090812

* Tue Jul 28 2009 kwizart < kwizart at gmail.com > - 1.0.1-1
- Update to 1.0.1 (Final)
- Improve conditionals
- Backport zip qt4 from 1.0-bugfix
- More %%_isa requirement

* Mon Jul  6 2009 kwizart < kwizart at gmail.com > - 1.0.0-1
- Update to 1.0.0 (Final)

* Thu Jul  2 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.14rc4
- Cherry pick from 1.0-bugfix
- Move xcb modules into main
- Move -devel Requirement from main to -core (Mutlilib fix)

* Wed Jun 17 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.12rc4
- Update to 1.0.0-rc4

* Sun Jun  7 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.11rc3
- Update to 1.0.0-rc3

* Fri Jun  5 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.10rc2
- Move some module to avoid dependency
- Remove previous signal-slot connection(s) if any - vlc trac #2818

* Tue Jun  2 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.9rc2
- Update to current bugfix
- Revert b8f23ea716693d8d07dd8bd0cb4c9ba8ed05f568
- Split plugin-jack

* Wed May 27 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.7rc2
- Update to 1.0.0-rc2
- Rebase xulrunner patch for -rc2
- Add GConf2 support for url-handler (based on totem)

* Wed May 13 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.5rc1
- Fix missing XvMC symbols
- Fix export make_URI

* Tue May 12 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.4rc1
- Update to 1.0.0-rc1
- Add 1.0-bugfix patches

* Fri Apr 17 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.3pre2
- Update to 1.0.0-pre2

* Fri Apr 10 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.2pre1
- Re-enable xxmc
- Remove libmpeg2 out

* Fri Mar 27 2009 kwizart < kwizart at gmail.com > - 1.0.0-0.1pre1
- Update to 1.0.0-pre1
- Add mozilla plugin with xulrunner-1.9.1. Patch from Alexey Gladkov
- Disable xxmc

* Fri Mar  6 2009 kwizart < kwizart at gmail.com > - 0.9.9-0.4rc2
- Update to 0.9.9-rc2

* Fri Feb 27 2009 kwizart < kwizart at gmail.com > - 0.9.9-0.3rc
- Rename the Required font package.

* Fri Feb 13 2009 kwizart < kwizart at gmail.com > - 0.9.9-0.1rc
- Update to 0.9.9rc
- Move Xless binaries to the -core subpackage
- Add support for libxul 1.9.1

* Fri Jan 16 2009 kwizart < kwizart at gmail.com > - 0.9.8a-3
- Add libxul 1.9.1 preliminary support
- backport postproc fixes
- Add pending 0.9-bugfix git branch
- Add lua support by default

* Thu Jan 15 2009 kwizart < kwizart at gmail.com > - 0.9.8a-2
- Disable mozilla-vlc because of libxul 1.9.1 WIP
- Rebuild for libcdio

* Fri Dec  5 2008 kwizart < kwizart at gmail.com > - 0.9.8a-1
- Update to 0.9.8a
Security update:
 * Fixed buffer overflow in Real demuxer (SA-0811, CVE-2008-5276)
- Add pulse0071 Patch
- Fix RPM Fusion bugs:
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=201
  https://bugzilla.rpmfusion.org/show_bug.cgi?id=155

* Thu Nov  6 2008 kwizart < kwizart at gmail.com > - 0.9.6-1
- Update to 0.9.6

* Tue Oct 28 2008 kwizart < kwizart at gmail.com > - 0.9.5-3
- Rebuild for dependency

* Mon Oct 27 2008 kwizart < kwizart at gmail.com > - 0.9.5-2
- Fix ppc/ppc64 build

* Fri Oct 24 2008 kwizart < kwizart at gmail.com > - 0.9.5-1
- Update to 0.9.5
- Use non-default rpmbuild options for dirac kate lua
- Split core/nox (nox bundles directfb/svgalib)
- Fix Selinux denials (patches from gentoo).
- Fix spurious perms on qt4 sources.

* Wed Oct  8 2008 kwizart < kwizart at gmail.com > - 0.9.4-1
- Update to 0.9.4

* Mon Sep 29 2008 kwizart < kwizart at gmail.com > - 0.9.3-2
- Add libv4l2 patch from Hans de Goede

* Fri Sep 26 2008 kwizart < kwizart at gmail.com > - 0.9.3-1
- Update to 0.9.3 (final)
- Few others move from core to main

* Mon Sep 15 2008 kwizart < kwizart at gmail.com > - 0.9.2-1
- Update to 0.9.2 (final)

* Sat Aug  2 2008 kwizart < kwizart at gmail.com > - 0.9.0-0.5.20080802git
- Update to 0.9.0-20080802git

* Sun Jul 13 2008 kwizart < kwizart at gmail.com > - 0.9.0-0.4.20080713git
- Update to 0.9.0-20080713git

* Thu Jul  3 2008 kwizart < kwizart at gmail.com > - 0.9.0-0.3.20080703git
- Update to 0.9.0-20080703git
  http://mailman.videolan.org/pipermail/vlc-devel/2008-July/045911.html
- Conditionalize xvmc to exclude ppc

* Thu Jun 12 2008 kwizart < kwizart at gmail.com > - 0.8.6h-2
- Fix libdvdnav (only) use.

* Fri Jun 6 2008 kwizart < kwizart at gmail.com > - 0.8.6h-1
- Update to 0.8.6h
- Use hicolor icons
- Add patch for new_x-content
  http://bugzilla.livna.org/show_bug.cgi?id=2003
- Fix VLC: HTTP access: cannot seek AVI
  http://bugzilla.livna.org/show_bug.cgi?id=2014

* Sun May 18 2008 kwizart < kwizart at gmail.com > - 0.8.6g-2
- Bump for official release

* Wed May 14 2008 kwizart < kwizart at gmail.com > - 0.8.6g-1
- Update to 0.8.6g
Security updates:
 * Removed VLC variable settings from Mozilla and ActiveX (CVE-2007-6683)
 * Removed loading plugins from the current directory (CVE-2008-2147)

Various bugfixes:
 * Fixed various memory leaks, improving stability when running as a server
 * Fixed compilation with recent versions of FFmpeg
 * Correctly parses SAP announcements from MPEG-TS
 * Fixed AAC resampling
 * The Fullscreen Controller appears correctly on Mac OS X,
   if the 'Always-on-top' video option was selected.

* Tue May 13 2008 kwizart < kwizart at gmail.com > - 0.8.6f-6
- Fix ffmpeg-compat with newest ffmpeg interaction

* Mon May 12 2008 kwizart < kwizart at gmail.com > - 0.8.6f-5
- Introduce 180_all_faad.patch
- Re-enable ffmpeg-compat for F-9

* Mon May 12 2008 Thorsten Leemhuis < fedora at leemhuis dot info > - 0.8.6f-4
- disable patch82 temporary

* Fri May  9 2008 kwizart < kwizart at gmail.com > - 0.8.6f-3
- Bugfixes patches for post f version
- Add vlvc 0.8 plugin support
- Add textrel fix from gentoo patch
- Improve libxul patch

* Mon Apr  7 2008 kwizart < kwizart at gmail.com > - 0.8.6f-2
- Fix for wxGTK28 compatibility.
 Patch from Dominique Leuenberger <dominique@leuenberger.net

* Mon Apr  7 2008 kwizart < kwizart at gmail.com > - 0.8.6f-1
- Update to 0.8.6f (Final)
Security updates:
 * Really fixed subtitle buffer overflow (CVE-2007-6681)
 * Fixed Real RTSP code execution problem (CVE-2008-0073)
 * Fixed MP4 integer overflows (CVE-2008-1489)
 * Fixed cinepak integer overflow
Various bugfixes:
 * Fixed crashes in H264 packetizer
 * Close MMS access on network timeout
 * Fix some problems with AAC decoder & packetizer
- Remove java-vlc (will be built externally)
- Add clinkcc conditional/experimental support.

* Mon Feb 25 2008 kwizart < kwizart at gmail.com > - 0.8.6e-1
- Update to 0.8.6e (Final)
Security updates:
 * Subtitle demuxers overflow (CVE-2007-6681)
 * HTTP listener format string injection (CVE-2007-6682)
 * Fixed buffer overflow in the SDL_image library (CVE-2006-4484)
 * Real RTSP overflows (CVE-2008-0225, CVE-2008-0295,
   CVE-2008-0296, VideoLAN-SA-0801)
 * Arbitrary memory overwrite in the MP4 demuxer (CORE-2008-0130,
   VideoLAN-SA-0802)


* Mon Feb 25 2008 kwizart < kwizart at gmail.com > - 0.8.6e-0.3
- Update to svn20080225 from bugfix (pre 0.8.6e)

* Thu Feb 21 2008 kwizart < kwizart at gmail.com > - 0.8.6e-0.2
- Update to svn20080221 from bugfix (pre 0.8.6e)
- Updated merged pulseaudio patch
- Raise PA to be used by default.

* Mon Feb 18 2008 kwizart < kwizart at gmail.com > - 0.8.6e-0.1
- Update to pre0.8.6e
- Add pre PA patch (not merged yet)

* Sat Jan 19 2008 kwizart < kwizart at gmail.com > - 0.8.6d-4
- Patches from Jens Petersen <juhpetersen at gmail.com>
- Add wxGTK28 wip patch
- Conditionalize directfb and dirac
- Change the default font to DejaVuSerif.ttf (dejavu-fonts)
- Add BR missing libmpeg4v2

* Thu Jan 10 2008 kwizart < kwizart at gmail.com > - 0.8.6d-3.1
- Remove BR portaudio arts
- Move skins2 to main vlc package
- Enable libopendaap (included within Fedora)

* Mon Dec  3 2007 kwizart < kwizart at gmail.com > - 0.8.6d-3
- Enable java-vlc (developer use only - java-icedtea).
- Fix arch detection for java headers

* Sat Dec  1 2007 kwizart < kwizart at gmail.com > - 0.8.6d-2
- Improve core/nox split

* Thu Nov 29 2007 kwizart < kwizart at gmail.com > - 0.8.6d-1
- Update to vlc 0.8.6d

* Tue Nov  6 2007 kwizart < kwizart at gmail.com > - 0.8.6c-10
- Split to core/nox package for server use.

* Tue Nov  6 2007 kwizart < kwizart at gmail.com > - 0.8.6c-9
- Raise ESD audio_output to be tried by default
  (used by pulseaudio-esound-compat )

* Tue Nov  6 2007 kwizart < kwizart at gmail.com > - 0.8.6c-8
- Rebuild for libdca and faad2

* Mon Oct 22 2007 kwizart < kwizart at gmail.com > - 0.8.6c-7
- Rebuild for new libdvbpsi5-0.1.6

* Fri Oct 19 2007 kwizart < kwizart at gmail.com > - 0.8.6c-6
- Rebuild with the GPL compatible faad2
- Update the Dirac patch
- Fix livna #1668

* Sun Sep 23 2007 kwizart < kwizart at gmail.com > - 0.8.6c-5
- Prepare svn version
- Drop the python switch default
- Add BR directfb-devel
- Improve timestamp
- Allow faad2 to be 2.5 (license change is known GPL compatible).

* Thu Aug 23 2007 kwizart < kwizart at gmail.com > - 0.8.6c-4
- Change default font to dejavu-lgc/DejaVuLGCSerif.ttf
  http://bugzilla.livna.org/show_bug.cgi?id=1605
- Remove unneeded fonts provided by skins2

* Tue Aug 14 2007 kwizart < kwizart at gmail.com > - 0.8.6c-3.2
- clean-up with svn
- patch smb.c for call_open (from rdieter advice)
- Update license field to GPLv2

* Sun Aug 12 2007 kwizart < kwizart at gmail.com > - 0.8.6c-3.1
- Fix libtool with shared libs when python-vlc is used
  http://bugzilla.livna.org/show_bug.cgi?id=1590
- Fix desktop file to be GNOME HIG compliant
  http://bugzilla.livna.org/show_bug.cgi?id=1591

* Tue Jul 31 2007 kwizart < kwizart at gmail.com > - 0.8.6c-3
- Switch for python-vlc
- Add bugfix patch pre_d
- Fix version field for desktop file.
- Fix ivtv support with updated patch for new videodev2.h
- Clean old Obsoletes/Provides for name 8.1
- Rebuild with firefox-devel 2.0.0.5
- Patch/rebuild with libcdio 0.78.2
- Add mesa's BR
- Add BR libXvMC-devel for svn

* Tue Jun 26 2007 kwizart < kwizart at gmail.com > - 0.8.6c-2
- Update to new libupnp

* Sat Jun 16 2007 kwizart < kwizart at gmail.com > - 0.8.6c-1
- Update to 0.8.6c (final)
- Add patch to uses v4l2 header for new v4l2 encoder API.

* Sat Jun 16 2007 kwizart < kwizart at gmail.com > - 0.8.6c-0.1
- Update to 0.8.6c (bugfix) 20060616
- Drop FLAC, automake110, wxGTK for 2.8, faad2
- Uses shared ffmpeg.

* Thu Jun  7 2007 kwizart < kwizart at gmail.com > - 0.8.6b-6
- Rebuild for F-7 (compat-wxGTK26)

* Mon Jun  4 2007 kwizart < kwizart at gmail.com > - 0.8.6b-5.3
- Uses only -fPIC to prevent Selinux context problems...
- Uses compat-wxGTK26-devel on Fedora 7
- Leave libcorba for now...
  (libquicktime_plugin seems also broken - confirmed by upstream)
- Change static_live555 to internal_live555.
  needed for testing - uses live-devel for livna releases.

* Sat May 19 2007 kwizart < kwizart at gmail.com > - 0.8.6b-5
- Removed no more needed Selinux Context:
  fixed in http://bugzilla.redhat.com/237473

* Sun May 13 2007 kwizart < kwizart at gmail.com > - 0.8.6b-4
- Disabled pth (broken) and...
- Build ffmpeg static (since shared ffmpeg is pth enabled).
- Add post & postun update-desktop-database
- Update static ffmpeg to 20070503 (same as shared version)

* Sun May 13 2007 kwizart < kwizart at gmail.com > - 0.8.6b-3.3
- Test static updated live555

* Sat May 12 2007 kwizart < kwizart at gmail.com > - 0.8.6b-3.2
- Update to the new ffmpeg with pth (testing - wip )

* Fri May  4 2007 kwizart < kwizart at gmail.com > - 0.8.6b-3.1
- Add BR libebml-devel
- Add BR Glide3-devel
- Add BR gnome-vfs2-devel
- Add BR libxml2-devel
- Fix BR faad2-devel < 2.5
- Add rpmfusion BR libopendaap-devel
- Add rpmfusion BR libgoom2-devel
- Add rpmfusion BR libdc1394-devel
- Exclude corba plugin (broken)
- Add relatives %%configure options
- Comment Glide3 (don't work now - wip)

* Thu May  3 2007 kwizart < kwizart at gmail.com > - 0.8.6b-3
- Enable --enable-pth with ffmpeg
  bump release in case testing take much time.

* Thu May  3 2007 kwizart < kwizart at gmail.com > - 0.8.6b-1.3
- Fix Selinux remain quiet with semanage

* Tue May  1 2007 kwizart < kwizart at gmail.com > - 0.8.6b-1.2
- Few improvements for svn version
- Add missing BR ORBit2-devel and pyorbit-devel
- Improved post preun postun section with help from Anvil.

* Mon Apr 30 2007 kwizart < kwizart at gmail.com > - 0.8.6b-1.1
- Add missing BR libtiff-devel
- Fix Selinux buglet when Selinux is not activated
  was https://bugzilla.livna.org/show_bug.cgi?id=1484

* Sat Apr 21 2007 kwizart < kwizart at gmail.com > - 0.8.6b-1
- Update to Final 8.6b
- Enable Dirac codec
- Fix mozilla-vlc libXt.so loading
  (removing mozilla-sdk since using firefox sdk >= 1.5)
- Fix SeLinux context for dmo plugin. Was:
  https://bugzilla.livna.org/show_bug.cgi?id=1404
- Enabled cddax only for x86_64 (broken type).

* Wed Apr 18 2007 kwizart < kwizart at gmail.com > - 0.8.6b-0.3
- Fix BR for libsmbclient-devel for Fedora 7
- Update to 0.8.6-bugfix-20070418
- Add BR libraw1394-devel
- Add BR libavc1394-devel

* Mon Apr 16 2007 kwizart < kwizart at gmail.com > - 0.8.6b-0.2
- Fix svgalib-devel only for x86 x86_64
- Fix firefox-devel headers presence/usability. This remains:
 npapi.h: accepted by the compiler, rejected by the preprocessor!
 npapi.h: proceeding with the compiler's result

* Sat Apr 14 2007 kwizart < kwizart at gmail.com > - 0.8.6b-0.1
- Update to rc 0.8.6b (bugfix)
- Hack configure.ac script (it didn't detect firefox headers)
- Add BR libshout-devel
- Add BR svgalib-devel
- Add BR gtk2-devel
- Add BR directfb-devel (wip)
- Add BR libnotify-devel
- Enabled --enable-speex
- Testing --enable-portaudio not usefull (oss is deprecated)
- Enabled --enable-pda
- Testing --enable-directfb (wip)
- Removed patch5 (was format.c)

* Thu Apr  5 2007 kwizart < kwizart at gmail.com > - 0.8.6a-5
- Use system ffmpeg lib (pth and libtool seems to be incompatible with it)
- Dirac seem to compile fine but testing usability for now.
- Cache isn't usefull for now (and won't be since using system libs)
- Exclude %%{_bindir}/vlcwrapper.py? since this is the guideline about python for now.

* Mon Apr  2 2007 kwizart < kwizart at gmail.com > - 0.8.6a-4.6
- Fix %%{_libdir}/advene directory ownership from: #1458
- Fix .py? presence and perm (644)
- Remove .la after make install
- Add --disable-pth (broken for release and svn)

* Sat Mar 24 2007 kwizart < kwizart at gmail.com > - 0.8.6a-4.5
- Test dirac (disabled mozilla )
- Test Updated static live555 to 2007.02.22
- Clean up svn to release changes

* Thu Mar 22 2007 kwizart < kwizart at gmail.com > - 0.8.6a-4.4
- WIP changes - ld.conf is unusefull...

* Wed Mar 21 2007 kwizart < kwizart at gmail.com > - 0.8.6a-4.3
- Revert back to the static vlc version
 ( will explore this with ld.conf later )

* Wed Mar 21 2007 kwizart < kwizart at gmail.com > - 0.8.6a-4.2
- Fix .desktop file
- Disable broken libtool
- Quick fixes for svn/cache prepare
- Patch format_c
- Fix rpmlint error with python-vlc

* Tue Mar 20 2007 kwizart < kwizart at gmail.com > - 0.8.6a-4.1
- Enable cache for static compilation - wip

* Fri Mar  9 2007 kwizart < kwizart at gmail.com > - 0.8.6a-4
- Enable conditionnal build for
	* mozilla-vlc, java-vlc, dirac
	* ffmpeg and live static
- Enable pth
- Enable gnu_ld

* Thu Mar  8 2007 kwizart < kwizart at gmail.com > - 0.8.6a-3.1
- Fix firefox-devel detection when avaible both i386 and x86_64
  http://bugzilla.livna.org/show_bug.cgi?id=1442

* Thu Mar  8 2007 kwizart < kwizart at gmail.com > - 0.8.6a-3
- Recover patch3 from Ville Skyttä
- Fix FLAC api change see
 http://bugzilla.livna.org/show_bug.cgi?id=1433

* Thu Mar  8 2007 kwizart < kwizart at gmail.com > - 0.8.6a-2
- Update ffmpeg to 20070308
- Enabled static build for internal ffmpeg (x264 vlc modules)
- Fixed: some configure options has changed for ffmpeg

* Sat Mar  3 2007 Thorsten Leemhuis <fedora at leemhuis dot info> - 0.8.6a-1.2
- Rebuild

* Sun Feb  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.8.6a-1.1
- Fix aclocal/automake fix for automake 1.10 without breaking it for earlier.

* Sun Feb  4 2007 Ville Skyttä <ville.skytta at iki.fi> - 0.8.6a-1
- Build internal copy of ffmpeg with $RPM_OPT_FLAGS.
- Don't hardcode path to firefox headers.
- Drop Application and X-Livna categories from desktop entry.
- Clean up some unneeded cruft from specfile.
- Fix aclocal/automake calls during bootstrap.
- Let rpmbuild strip MediaControl.so.

* Sat Feb  3 2007 kwizart < kwizart at gmail.com > - 0.8.6a-0.4.static
- Internal static build of ffmpeg from Matthias version.

* Fri Jan 19 2007 kwizart < kwizart at gmail.com > - 0.8.6a-0.3
- Re-enabled mozilla-vlc
- use ifarch ix86

* Sat Jan 13 2007 kwizart < kwizart at gmail.com > - 0.8.6a-0.2
- Import patches from Matthias version
- try to fix firefox includes for mozilla-vlc -> disabled

* Wed Jan 10 2007 kwizart < kwizart at gmail.com > - 0.8.6a-0.1
- Try to Fix run with libavformat.so.51
- disabled

* Mon Jan  8 2007 kwizart < kwizart at gmail.com > - 0.8.6-5
- Update to BR bugzilla infos.
- Fix perms with python and debug headers.
- Cleaned obsolete-not-provided

* Fri Jan  5 2007 kwizart < kwizart at gmail.com > - 0.8.6-4
- Use BuildConflics with libcdio
- Enabled --enable-cddax
- Enabled --enable-vcdx
-  waiting --enable-quicktime (build fails)

* Fri Jan  5 2007 kwizart < kwizart at gmail.com > - 0.8.6-3
  with help from Rathan
- Update to 0.8.6a (security update!)
  from http://www.videolan.org/sa0701.html - #1342
- Add version to desktop file
- Fix dual shortcuts / Add MimeType

* Wed Jan  3 2007 kwizart < kwizart at gmail.com > - 0.8.6-2
 with help from Rathan
- Enabled --enable-shout
- Enabled --enable-quicktime (x86 only !)
- Enabled --enable-loader (x86 only !)
- Enabled --with-wine-sdk-path (x86 only !)
- Enabled --enable-corba
-  testing --enable-dirac (libdirac-devel reviewing in extra)
   http://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=221405
- Enabled --enable-mediacontrol-python-bindings
- Cosmetic changes in BR

* Mon Dec 11 2006 kwizart < kwizart at gmail.com > - 0.8.6-1.fc6
- Update to 8.6 final
- Change deprecated livdotcom to live555
- build shared librairies is default since 8.6
- Enabled --enable-dvdread
- Enabled --enable-faad
- Enabled --enable-twolame
-   waiting --enable-quicktime (problem finding xqtsdk )
- Enabled --enable-real
- Enabled --enable-realrtsp
- Enabled --enable-tremor
- Enabled --enable-tarkin
-   waiting --enable-dirac (TODO libdirac-devel )
- Enabled --enable-snapshot
- Enabled --enable-portaudio
- Enabled --enable-jack
- Enabled --enable-galaktos
-   waiting --enable-mediacontrol-python-bindings (default install error)
-   waiting --enable-cddax (new version of libcdio 0.78.2)
-   waiting --enable-vcdx (new version of libcdio 0.78.2)

* Mon Dec 04 2006 kwizart < kwizart at gmail.com > - 0.8.6-rc1.1.fc6
- Update to 8.6rc1
- disable components in mozilla-vlc
- disable libvlc_pic.a in devel
- Enable x264-devel for static linking.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.8.5-6
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 Dams <anvil[AT]livna.org> - 0.8.5-5
- BuildReq:libtool

* Sun Sep 24 2006 Dams <anvil[AT]livna.org> - 0.8.5-4
- Fixed the mozilla plugin damn build

* Sat Sep  9 2006 Dams <anvil[AT]livna.org> - 0.8.5-3
- sysfsutils-devel -> libsysfs-devel

* Sat Sep  9 2006 Dams <anvil[AT]livna.org> - 0.8.5-1
- Updated to 0.8.5
- Fixed MOZVER value in case more than one mozilla is installed.
- Dropped patches 1, 2 and 3

* Wed Aug 16 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.4a-2
- Adjust for new live package, enable it on all archs.

* Fri Apr 14 2006 Ville Skyttä <ville.skytta at iki.fi> - 0.8.4a-1
- Apply upstream patch to fix linking with newer ffmpeg/postproc.
- Drop no longer needed build conditionals and build dependencies.
- Enable Avahi, Musepack, SLP and sysfs support, fix SDL and Xv.
- Install icon to %%{_datadir}/icons/hicolor.
- Drop zero Epoch remainders.
- Fix -devel obsoletes.
- Specfile cleanups.

* Fri Mar 24 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.8.4-9.a
- rebuild

* Tue Mar 21 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.8.4-8.a
- fix #775

* Mon Mar 20 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.8.4-7.a
- add -fPIC for all arches

* Mon Mar 20 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.8.4-6.a
- fix build on ppc/i386

* Thu Mar 16 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.8.4-5.a
- fix BR

* Wed Mar 15 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
0.8.4-4.a
- make vlc build again

* Tue Mar 14 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> 0.8.4-3.a
- drop "0.lvn" from release

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jan 09 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0.8.4-0.lvn.3.a
- add all BRs the new ffmpeg needs

* Fri Jan 06 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0.8.4-0.lvn.2.a
- add buildoption "--without mkv" -- ebml in FC3 is to old
- add buildoption "--without svg" -- does not build with svg on FC3-x86-64

* Thu Jan 05 2006 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 0.8.4-0.lvn.1.a
- Update to 0.8.4a [with help from che (Rudolf Kastl)]
- Fix x64
- drop Epoch
- drop vlc-0.8.2-test2-altivec.patch, seems they worked on this
- use " --disable-libcdio" until we update to wxGTK2 2.6
- use "--disable-livedotcom" on x86_64 (does not build)

* Sat Aug  6 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:0.8.2-0.lvn.4
- Fix "--without cddb" build when libcddb-devel is installed.
- BuildRequire live-devel instead of live.

* Wed Aug  3 2005 Dams <anvil[AT]livna.org> - 0:0.8.2-0.lvn.3
- Rebuilt *without* libcddb
- Rebuilt against new libdvbpsi

* Thu Jul 28 2005 Dams <anvil[AT]livna.org> - 0:0.8.2-0.lvn.2
- Rebuilt against new libcddb/libcdio

* Sat Jul  9 2005 Dams <anvil[AT]livna.org> - 0:0.8.2-0.lvn.1
- Updated to final 0.8.2

* Mon Jun  6 2005 Ville Skyttä <ville.skytta at iki.fi> 0:0.8.2-0.lvn.0.1.test2
- Update to 0.8.2-test2, rename to vlc, improve summaries and descriptions.
- Enable many more modules, many small improvements and cleanups here and there
- Use unversioned install dir for the Mozilla plugin, rename to mozilla-vlc.
- Drop < FC3 compatiblity due to unavailability of required lib versions.
- Fold wx and ncurses to the main package (upstream has retired the
  VLC Gnome and KDE UI's, so separate UI packages don't have a purpose
  any more).

* Sat Sep 11 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.2-0.lvn.7
- Remove dependency on libpostproc-devel, it's now in ffmpeg-devel (bug 255).

* Thu Sep  2 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.2-0.lvn.6
- BuildRequire alsa-lib-devel, was lost in previous update (bug 258).
- Add libcdio and libmodplug build dependencies.
- Tweak descriptions, remove unnecessary conditional sections.
- Disable dependency tracking to speed up the build.

* Sun Aug 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:0.7.2-0.lvn.5
- Use system ffmpeg (>= 0.4.9), and make it, ALSA, and fribidi unconditional.
- Build with theora by default.
- Change default font to Vera serif bold.
- Enable pvr support for Hauppauge card users (thanks to Gabriel L. Somlo).

* Mon Jul  5 2004 Dams <anvil[AT]livna.org> 0:0.7.2-0.lvn.4
- Enabled libcddb support

* Wed Jun 30 2004 Dams <anvil[AT]livna.org> 0:0.7.2-0.lvn.3
- speex now conditional and default disabled since vlc requires
  development version.

* Wed Jun 30 2004 Dams <anvil[AT]livna.org> 0:0.7.2-0.lvn.2
- Optional Fribidi and libtheora support (default disabled)

* Tue May 25 2004 Dams <anvil[AT]livna.org> 0:0.7.2-0.lvn.1
- Updated to 0.7.2

* Fri May  7 2004 Dams <anvil[AT]livna.org> 0:0.7.1-0.lvn.1
- BuildConflicts:ffmpeg
- Build against private ffmpeg snapshot

* Tue Mar  9 2004 Dams <anvil[AT]livna.org> 0:0.7.1-0.lvn.1
- Updated to 0.7.1
- Added live.com libraries support
- Added matroska support

* Sun Jan  4 2004 Dams <anvil[AT]livna.org> 0:0.7.0-0.lvn.1
- Updated to 0.7.0
- s/fdr/lvn

* Wed Dec 10 2003 Dams <anvil[AT]livna.org> 0:0.6.2-0.fdr.7
- Conditional ffmpeg build option (default enabled)

* Fri Sep  5 2003 Dams <anvil[AT]livna.org> 0:0.6.2-0.fdr.6
- pth support now default disabled

* Fri Sep  5 2003 Dams <anvil[AT]livna.org> 0:0.6.2-0.fdr.5
- slp support can now be not-build with '--without slp'

* Thu Sep  4 2003 Dams <anvil[AT]livna.org> 0:0.6.2-0.fdr.4
- Added missing defattr for subpackages
- Fixed permissions on mozilla plugin
- fixed build failure due to typos in ncurses changes
- Removed useless explicit 'Requires:' in subpackages declarations

* Tue Sep  2 2003 Dams <anvil[AT]livna.org> 0:0.6.2-0.fdr.3
- Added builddep for libpng-devel and openslp-devel
- Added gnome (default:enabled) and ncurses (default:disabled)
  subpackages
- Removed macros (mkdir/install/perl)
- Modified descriptions
- Removed gtk/gnome2 build deps
- Added conditionnal (default-disabled) build option for alsa
- Added conditionnal builddep for pth-devel

* Fri Aug 22 2003 Dams <anvil[AT]livna.org> 0:0.6.2-0.fdr.2
- Added missing BuildRequires for gtk+-devel

* Thu Aug 14 2003 Dams <anvil[AT]livna.org> 0:0.6.2-0.fdr.1
- Updated to 0.6.2
- Hopefully fixed 'if' conditions for optional buildrequires

* Tue Jul  8 2003 Dams <anvil[AT]livna.org> 0:0.6.0-0.fdr.3
- Providing vlc

* Tue Jul  8 2003 Dams <anvil[AT]livna.org> 0:0.6.0-0.fdr.2
- Moved desktop entry from devel to main package (stupid me)

* Mon Apr 28 2003 Dams <anvil[AT]livna.org>
- Initial build.
