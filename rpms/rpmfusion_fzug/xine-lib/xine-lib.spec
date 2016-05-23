%global         plugin_abi  2.5
%global         codecdir    %{_libdir}/codecs

%ifarch %{ix86}
    %global     have_vidix  1
%else
    %global     have_vidix  0
%endif # ix86

Summary:        A multimedia engine
Name:           xine-lib
Version:        1.2.6
Release:        9%{?dist}
License:        GPLv2+
URL:            http://www.xine-project.org/
Source0:        http://downloads.sourceforge.net/xine/xine-lib-%{version}.tar.xz

# http://bugzilla.redhat.com/477226
Patch1:         xine-lib-1.1.16.2-multilib.patch
Patch2:         ffmpeg_2.9.patch

Provides:         xine-lib(plugin-abi) = %{plugin_abi}
%{?_isa:Provides: xine-lib(plugin-abi)%{?_isa} = %{plugin_abi}}

Obsoletes:      xine-lib-extras-freeworld < 1.1.21-10
Provides:       xine-lib-extras-freeworld = %{version}-%{release}

BuildRequires:  gawk
BuildRequires:  sed
BuildRequires:  gettext-devel
# X11
BuildRequires:  libX11-devel
BuildRequires:  libXv-devel
BuildRequires:  libXt-devel
BuildRequires:  libXext-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXvMC-devel
BuildRequires:  libGLU-devel
BuildRequires:  libv4l-devel
BuildRequires:  libxcb-devel
BuildRequires:  libva-devel
BuildRequires:  libvdpau-devel
# Video
BuildRequires:  SDL-devel
BuildRequires:  libtheora-devel
BuildRequires:  libmng-devel
BuildRequires:  aalib-devel >= 1.4
BuildRequires:  libcaca-devel >= 0.99-0.5.beta14
BuildRequires:  ImageMagick-devel >= 6.2.4.6-1
BuildRequires:  libvpx-devel
%if 0%{?_with_freetype:1}
BuildRequires:  fontconfig-devel
%endif # freetype
# Audio
BuildRequires:  ffmpeg-devel >= 0.4.9-0.22.20060804
BuildRequires:  a52dec-devel
BuildRequires:  alsa-lib-devel >= 0.9.0
BuildRequires:  faad2-devel
BuildRequires:  flac-devel
BuildRequires:  jack-audio-connection-kit-devel
BuildRequires:  libdca-devel
BuildRequires:  libmad-devel
BuildRequires:  libmodplug-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  libvorbis-devel
BuildRequires:  speex-devel
BuildRequires:  wavpack-devel
# CDs / DVDs
BuildRequires:  libcdio-devel
BuildRequires:  vcdimager-devel >= 0.7.23
BuildRequires:  libdvdnav-devel
BuildRequires:  libdvdread-devel
BuildRequires:  libbluray-devel
# Other
BuildRequires:  pkgconfig
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  gtk2-devel
BuildRequires:  libsmbclient-devel


%description
This package contains the Xine library.  It can be used to play back
various media, decode multimedia files from local disk drives, and display
multimedia streamed over the Internet. It interprets many of the most
common multimedia formats available - and some uncommon formats, too. 

%package        devel
Summary:        Xine library development files
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       zlib-devel
%description    devel
This package contains development files for %{name}.

%package        extras
Summary:        Additional plugins for %{name} 
Requires:       %{name}%{?_isa} = %{version}-%{release}
%description    extras
This package contains extra plugins for %{name}:
  - JACK
  - GDK-Pixbuf
  - SMB
  - SDL
  - AA-lib
  - Libcaca
  - Image decoding


%prep
%setup -q
%patch1 -p1 -b .multilib
%patch2 -p1 -b .ffmpeg_2.9


%build
export SDL_CFLAGS="$(sdl-config --cflags)" SDL_LIBS="$(sdl-config --libs)"
# Keep list of options in mostly the same order as ./configure --help.
%configure \
    --disable-dependency-tracking \
    --enable-ipv6 \
    --enable-v4l2 \
    --enable-libv4l \
    --enable-xvmc \
    --disable-gnomevfs \
%if 0%{?_with_freetype:1}
%if 0%{?_with_antialiasing:1}
    --enable-antialiasing \
%endif # antialiasing
    --with-freetype \
    --with-fontconfig \
%endif # freetype
    --with-caca \
    --with-external-dvdnav \
    --with-xv-path=%{_libdir} \
    --with-libflac \
    --without-esound \
    --with-wavpack \
    --with-real-codecs-path=%{codecdir} \
    --with-w32-path=%{codecdir}

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} V=1


%install
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang libxine2
cp -pR $RPM_BUILD_ROOT%{_docdir}/xine-lib __docs
rm -rf $RPM_BUILD_ROOT%{_docdir}/xine-lib

# Removing useless files
rm -Rf $RPM_BUILD_ROOT%{_libdir}/libxine*.la __docs/README \
       __docs/README.{freebsd,irix,solaris,MINGWCROSS,WIN32}

# Directory for binary codecs
mkdir -p $RPM_BUILD_ROOT%{codecdir}


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files -f libxine2.lang
%doc AUTHORS COPYING COPYING.LIB CREDITS ChangeLog* README TODO
%doc __docs/README.* __docs/faq.*
%doc doc/README.dxr3 doc/README.network_dvd
%dir %{codecdir}/
%{_datadir}/xine-lib/
%{_libdir}/libxine.so.*
%{_mandir}/man5/xine.5*
%dir %{_libdir}/xine/
%dir %{_libdir}/xine/plugins/
%dir %{_libdir}/xine/plugins/%{plugin_abi}/
%{_libdir}/xine/plugins/%{plugin_abi}/mime.types
# Listing every plugin separately for better control over binary packages
# containing exactly the plugins we want, nothing accidentally snuck in
# nor dropped.
%dir %{_libdir}/xine/plugins/%{plugin_abi}/post/
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_audio_filters.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_goom.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_mosaico.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_planar.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_switch.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_tvtime.so
%{_libdir}/xine/plugins/%{plugin_abi}/post/xineplug_post_visualizations.so
%if %{have_vidix}
%dir %{_libdir}/xine/plugins/%{plugin_abi}/vidix/
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/cyberblade_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/mach64_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/mga_crtc2_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/mga_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/nvidia_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/pm2_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/pm3_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/radeon_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/rage128_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/savage_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/sis_vid.so
%{_libdir}/xine/plugins/%{plugin_abi}/vidix/unichrome_vid.so
%endif # vidix
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_alsa.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_file.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_none.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_oss.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_pulseaudio.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_a52.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_bitplane.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dts.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dvaudio.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dxr3_spu.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_dxr3_video.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_faad.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_ff.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_gsm610.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_libjpeg.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_libvpx.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_lpcm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_mad.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_mpeg2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_mpc.so
%ifarch %{ix86}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_qt.so
%endif # ix86
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_real.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_rgb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spu.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spucc.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spucmml.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spudvb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_spuhdmv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_h264.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_h264_alter.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_mpeg12.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_mpeg4.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_vdpau_vc1.so
%ifarch %{ix86}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_w32dll.so
%endif # ix86
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_yuv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_audio.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_asf.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_avi.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_fli.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_flv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_games.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_iff.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_image.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_matroska.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mng.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_modplug.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_block.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_elem.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_pes.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_mpeg_ts.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_nsv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_playlist.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_pva.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_qt.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_rawdv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_real.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_slave.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_vc1_es.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_yuv_frames.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_dmx_yuv4mpeg2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_flac.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_bluray.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_cdda.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_dvb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_dvd.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_file.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_http.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_mms.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_net.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_pnm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_pvr.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_rtp.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_rtsp.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_stdin_fifo.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_v4l2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_vcd.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_vcdo.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_nsf.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_sputext.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vdr.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_dxr3.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_fb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_none.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_opengl.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_opengl2.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_raw.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_vaapi.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_vdpau.so
%if %{have_vidix}
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_vidix.so
%endif # vidix
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xcbshm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xcbxv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xshm.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xv.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xvmc.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_xxmc.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_wavpack.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_xiph.so

%files extras
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_ao_out_jack.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_gdk_pixbuf.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_decode_image.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_smb.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_inp_test.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_aa.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_caca.so
%{_libdir}/xine/plugins/%{plugin_abi}/xineplug_vo_out_sdl.so

%files devel
%doc __docs/hackersguide/*
%{_bindir}/xine-config
%{_bindir}/xine-list*
%{_datadir}/aclocal/xine.m4
%{_includedir}/xine.h
%{_includedir}/xine/
%{_libdir}/libxine.so
%{_libdir}/pkgconfig/libxine.pc
%{_mandir}/man1/xine-config.1*
%{_mandir}/man1/xine-list*.1*


%changelog
* Sun May 01 2016 Sérgio Basto <sergio@serjux.com> - 1.2.6-9
- Add patch to build with ffmpeg3

* Tue Nov 04 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.6-8
- Rebuilt for vaapi 0.36

* Mon Oct 20 2014 Sérgio Basto <sergio@serjux.com> - 1.2.6-7
- Rebuilt for FFmpeg 2.4.3

* Wed Oct 01 2014 Sérgio Basto <sergio@serjux.com> - 1.2.6-6
- Rebuilt again for FFmpeg 2.3.x (with FFmpeg 2.3.x in build root)

* Wed Oct 01 2014 Sérgio Basto <sergio@serjux.com> - 1.2.6-5
- Rebuilt for FFmpeg 2.3.x (with FFmpeg 2.3.x in build root)

* Sat Sep 27 2014 kwizart <kwizart@gmail.com> - 1.2.6-4
- Rebuilt for FFmpeg 2.3x

* Thu Sep 25 2014 Xavier Bachelot <xavier@bachelot.org> 1.2.6-3
- Rebuild for ffmpeg 2.4.

* Thu Aug 07 2014 Sérgio Basto <sergio@serjux.com> - 1.2.6-2
- Rebuilt for ffmpeg-2.3

* Sun Jul 06 2014 Xavier Bachelot <xavier@bachelot.org> 1.2.6-1
- Update to 1.2.6.

* Tue Apr 08 2014 Xavier Bachelot <xavier@bachelot.org> 1.2.5-1
- Update to 1.2.5.
- Drop upstream'ed patch.
- Enable VP8/9 decoder through libvpx.

* Tue Mar 25 2014 Xavier Bachelot <xavier@bachelot.org> 1.2.4-5
- Rebuild for ffmpeg 2.2.

* Wed Feb 26 2014 Nicolas Chauvet <kwizart@gmail.com> - 1.2.4-4
- Rebuilt for libcdio

* Tue Nov 05 2013 Xavier Bachelot <xavier@bachelot.org> 1.2.4-3
- Rebuild for ffmpeg 2.1.

* Sat Oct 12 2013 Xavier Bachelot <xavier@bachelot.org> 1.2.4-2
- Make the build more verbose.
- Don't run autogen.sh gratuitously and drop BR: autoconf automake libtool.
  Consequently, add a code snippet to remove rpath.
- Drop obsolete no autopoint patch and Requires: gettext-devel instead.
- Drop obsolete Requires: pkgconfig for -devel subpackage.
- Drop obsolete Group: tags.
- Bump xine-lib-extras-freeworld Obsoletes:.

* Tue Sep 24 2013 Xavier Bachelot <xavier@bachelot.org> 1.2.4-1
- Update to 1.2.4.
- Drop upstream'ed patches and hacks.
- More spec file cleanup.

* Fri Sep 20 2013 Xavier Bachelot <xavier@bachelot.org> 1.2.3-2
- Update to 1.2.3.
- Merge xine-lib and xine-lib-extras-freeworld.
- Use pristine source.
- Clean up old Obsoletes/Provides.
- Clean up old conditional building.
- Clean up spec.
- Enable VDPAU support.
- Enable VAAPI support.
- Add a patch to fix a lock up when vaapi plugin init fails.
- Move test input plugin to -extras.

* Fri Sep 20 2013 Xavier Bachelot <xavier@bachelot.org> 1.1.21-10
- Rebuild for libbluray-0.4.0.

* Sat Aug 31 2013 Till Maas <opensource@till.name> - 1.1.21-9
- Disable directfb support for Fedora 20 and newer, because it was retired

* Tue Aug 27 2013 Jon Ciesla <limburgher@gmail.com> - 1.1.21-8
- libmng rebuild.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.21-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 30 2013 Kevin Fenzi <kevin@scrye.com> - 1.1.21-6
- Rebuild for broken deps in rawhide

* Tue Feb 12 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.21-5
- find the Samba 4 libsmbclient.h using pkg-config, fixes FTBFS (#909825)

* Mon Sep 17 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.21-4
- rebuild for new directfb

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.21-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jul 21 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.21-2.1
- disable libbluray support on F16, libbluray too old

* Mon Jul 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.21-2
- do not remove DVD plugin, not encumbered (only uses libdvdread/libdvdnav)

* Tue Jun 12 2012 Xavier Bachelot <xavier@bachelot.org> 1.1.21-1
- Update to 1.1.21.
- Enable libbluray support.

* Sat Mar 10 2012 Rex Dieter <rdieter@fedoraproject.org> 1.1.20.1-3
- rebuild (ImageMagick)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 03 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.20.1-1
- update to 1.1.20.1 (bugfix release)
- drop upstreamed link-libdvdread patch

* Sun Nov 20 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.20-1
- update to 1.1.20 (#753758)
- use .xz tarball
- drop old conditionals
- drop ESD (esound) support on F17+ (native PulseAudio just works)
- drop autotools patch, run autogen.sh in %%prep instead
- drop unused deepbind patch
- drop xvmclib_header patch, fixed upstream
- use the system libdvdnav (and libdvdread) instead of the bundled one
- fix system libdvdnav support to also link libdvdread
- plugin ABI is now 1.30

* Fri Jul 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 1.1.19-7
- rebuild for new DirectFB (1.5.0)

* Mon Feb 14 2011 Rex Dieter <rdieter@fedoraproject.org> 1.1.19-6
- split v4l, libv4l handling
- omit v4l(1) bits (f15+)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.19-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 24 2011 Rex Dieter <rdieter@fedoraproject.org> - 1.1.19-4
- xvmclib header changes, fixes ftbfs (#635653,#661071)

* Sun Nov 28 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.19-3
- rebuild for new directfb (1.4.11)

* Wed Sep 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.19-2
- rebuild (ImageMagick)

* Sun Jul 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.19-1
- 1.1.19

* Mon Jul 19 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.18.1-3
- no directfb on arm (yet)

* Tue Jun  1 2010 Ville Skyttä <ville.skytta@iki.fi> - 1.1.18.1-2
- Rebuild.

* Sun Mar 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.18.1-1
- xine-lib-1.1.18.1

* Sun Mar 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.18-2
- rebuild (ImageMagick)

* Wed Feb 24 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.1.18-1
- xine-lib-1.1.18, plugin-abi 1.28 (#567913)

* Sat Dec 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.17-3
- bump flac_decoder priority (rh#301861,xine#225)

* Mon Dec 07 2009 Bastien Nocera <bnocera@redhat.com> 1.1.17-2
- Remove gnome-vfs2 plugin, it's mostly useless

* Wed Dec 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.17-1
- xine-lib-1.1.17, plugin-abi 1.27

* Sun Nov 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.3-5
- move -pulseaudio into main pkg (f12+)
- update URL

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.16.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.3-3
- rebuild (DirectFB)

* Fri Apr 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.3-2.1
- drop old_caca hacks/patches (F-9)

* Fri Apr 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.3-2
- fix modtracker mimetypes

* Fri Apr 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.3-1
- xine-lib-1.1.16.3, plugin-abi 1.26

* Thu Mar 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.2-6
- add-mime-for-mod.patch 

* Tue Mar 10 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.16.2-5
- rebuild for new ImageMagick

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.16.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.2-3
- xine-lib-devel muiltilib conflict (#477226)

* Tue Feb 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.2-2
- xine-lib-safe-audio-pause3 patch (#486255, kdebug#180339)

* Tue Feb 10 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.16.2-1.1
- also patch the caca version check in configure(.ac)

* Tue Feb 10 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.2-1
- xine-lib-1.1.16.2

* Mon Feb 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.1-4
- gapless-race-fix patch (kdebug#180339)

* Sat Feb 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.1-3
- safe-audio-pause patch (kdebug#180339)

* Mon Jan 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.1-2
- Provides: xine-lib(plugin-abi)%%{?_isa} = %%{plugin_abi}
- touchup Summary/Description

* Fri Jan 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16.1-1
- xine-lib-1.1.16.1
- include avsync patch (#470568)

* Sun Jan 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16-2
- drop deepbind patch (#480504)
- caca support (EPEL)

* Wed Jan 07 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.16-1.1
- patch for old libcaca in F9-

* Wed Jan 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.1.16-1
- xine-lib-1.1.16, plugin ABI 1.25
- --with-external-libdvdnav, include mpeg demuxers (#213597)

* Fri Dec 12 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1.15-4
- rebuild for pkgconfig deps

* Tue Oct 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.15-3
- rebuild for new libcaca

* Thu Oct 23 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1.15-2
- respin

* Wed Aug 20 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1.15-1
- xine-lib-1.1.15, plugin ABI 1.24 (rh#455752, CVE-2008-3231)
- Obsoletes: -arts (f9+)

* Sun Apr 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.1.12-3
- rebuild for new ImageMagick (6.4.0.10)

* Thu Apr 24 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1.12-2
- CVE-2008-1878

* Wed Apr 16 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.12-1
- 1.1.12 (plugin ABI 1.21); qt, mkv, and pulseaudio patches applied upstream.

* Wed Apr  9 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.11.1-3
- Apply upstream fixes for Quicktime (#441705) and Matroska regressions
  introduced in 1.1.11.1.

* Mon Apr 07 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1.11.1-2
- pulse-rework2 patch (#439731)
- -pulseaudio subpkg (#439731)

* Sun Mar 30 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.11.1-1
- 1.1.11.1 (security update, #438663, CVE-2008-1482).
- Provide versioned xine-lib(plugin-abi) so 3rd party packages installing
  plugins can use it instead of requiring a version of xine-lib.

* Wed Mar 19 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.11-1
- 1.1.11 (security update, #438182, CVE-2008-0073).
- Drop jack and wavpack build conditionals.
- Specfile cleanups.

* Fri Mar  7 2008 Rex Dieter <rdieter@fedoraproject.org> - 1.1.10.1-1.1
- xcb support for f7+ (#373411)

* Fri Feb  8 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.10.1-1
- 1.1.10.1 (security update, #431541).

* Sun Jan 27 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.10-2
- Include spu, spucc, and spucmml decoders (#213597).

* Sun Jan 27 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.10-1
- 1.1.10 (security update).

* Mon Jan 21 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.9.1-3
- Fix version number in libxine.pc (#429487).

* Sun Jan 20 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.9.1-2
- Disable upstream "discard buffers on ao close" 1.1.9 changeset (#429182).

* Sat Jan 12 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.9.1-1
- 1.1.9.1 (security update).

* Sun Jan  6 2008 Ville Skyttä <ville.skytta@iki.fi> - 1.1.9-1
- 1.1.9.

* Thu Sep 27 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.8-6
- Enable wavpack support by default for all distros.

* Sun Sep 23 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.8-5
- Enable JACK support by default for all distros.

* Wed Sep 19 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.8-4
- Fix "--without wavpack" build.

* Sat Sep 15 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.8-3
- Move XCB plugins to the main package.
- Make aalib, caca, pulseaudio, jack, and wavpack support optional at build
  time in preparation for the first EPEL build.

* Sun Sep 09 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.1.8-2
- remove the dependency from -extras to -arts, and use Obsoletes to
  provide an upgrade path

* Thu Aug 30 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.8-1
- 1.1.8, "open" patch applied upstream.
- Build XCB plugins by default for Fedora 8+ only.

* Sat Aug 25 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.1.7-3
- Split the aRts plugin into its own subpackage

* Tue Aug 14 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.7-2
- Include XCB output plugins (in -extras at least for now).
- Protect "open" with glibc 2.6.90 and -D_FORTIFY_SOURCE=2.
- Clean up %%configure options.
- License: GPLv2+

* Thu Jun  7 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.7-1
- 1.1.7.

* Wed Jun 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 1.1.6-3
- respin (for libmpcdec)

* Wed Apr 25 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.6-2
- Make Real codec search path /usr/lib(64)/codecs again (#237743).

* Wed Apr 18 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.6-1
- 1.1.6.

* Wed Apr 11 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.5-1
- 1.1.5.
- Include GSM 06.10 decoder (#228186).
- Re-enable CACA support.

* Sun Apr  8 2007 Ville Skyttä <ville.skytta@iki.fi>
- Exclude vidix dir on systems that don't have vidix.
- Specfile cleanups.

* Mon Mar 26 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.4-4
- Add PulseAudio support (in -extras, #234035/Jost Diederichs).
- Adjust Samba build dependencies to work for both <= and > FC6.
- Add --with freetype and --with antialiasing build time options,
  default disabled, and an upstream patch for FreeType memory leak (#233194).

* Sat Mar 10 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.4-3
- Apply upstream fix for CVE-2007-1246.

* Wed Feb 14 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.4-2
- Rebuild.

* Wed Jan 31 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.4-1
- 1.1.4, with wavpack and system libmpcdec support.

* Thu Jan 18 2007 Aurelien Bompard <abompard@fedoraproject.org> 1.1.3-4
- rebuild

* Wed Jan  3 2007 Ville Skyttä <ville.skytta@iki.fi> - 1.1.3-3
- Fix libflac decoder with FLAC < 1.1.3 (#220961).
- Apply upstream patch for FLAC >= 1.1.3.

* Sun Dec 17 2006 Ville Skyttä <ville.skytta@iki.fi> - 1.1.3-2
- Don't run autotools during build.

* Mon Dec 04 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.3-1
- version 1.1.3
- patch2 applied upstream
- Disable CACA support by default, needs newer than what's in FE ATM.
- Split extras plugins in a separate package
- Enable JACK support (in extras subpackage)
- Enable DirectFB support (in extras subpackage)

* Sat Nov 11 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.2-18
- Make shn files available to amarok. References:
  http://xine.cvs.sourceforge.net/xine/xine-lib/src/demuxers/demux_shn.c?r1=1.1.2.2&r2=1.2
  https://launchpad.net/distros/ubuntu/+source/xine-lib/+bug/63130

* Wed Oct 18 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.2-17
- cleanup docs
- remove mms
- delete more source files in the cleanup script
- drop patch3 (affecting mms)

* Tue Oct 17 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.2-16
- fix files list
- add BR gtk2-devel
- remove xineplug_decode_gdk_pixbuf.so from x86-only

* Mon Oct 16 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.2-15
- removed libdts
- drop dxr patch (it's removed from tarball)
- list xineplug_decode_gdk_pixbuf.so and xineplug_vo_out_vidix.so only on x86

* Sun Oct 15 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.2-14
- update SOURCE1 to remove liba52 from tarball (patented)

* Tue Sep 12 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.2-13
- drop patches 2 and 4

* Fri Sep 08 2006 Aurelien Bompard <abompard@fedoraproject.org> 1.1.2-12
- initial Fedora Extras package
