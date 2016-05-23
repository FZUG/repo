Name:           gstreamer1-libav
Version:        1.8.1
Release:        2%{?dist}
Summary:        GStreamer 1.0 libav-based plug-ins
Group:          Applications/Multimedia
License:        LGPLv2+
URL:            http://gstreamer.freedesktop.org/
Source0:        http://gstreamer.freedesktop.org/src/gst-libav/gst-libav-%{version}.tar.xz
Patch0:         gst-ffmpeg-0.10.12-ChangeLog-UTF-8.patch
BuildRequires:  gstreamer1-devel >= 1.8.0
BuildRequires:  gstreamer1-plugins-base-devel >= 1.8.0
BuildRequires:  orc-devel bzip2-devel zlib-devel ffmpeg-devel
%ifarch %{ix86} x86_64
BuildRequires:  yasm
%endif

%description
GStreamer is a streaming media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

This package provides libav-based GStreamer plug-ins.


%package devel-docs
Summary: Development documentation for the libav GStreamer plug-in
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description devel-docs
GStreamer is a streaming media framework, based on graphs of elements which
operate on media data.

This package contains the development documentation for the libav GStreamer
plug-in.


%prep
%setup -q -n gst-libav-%{version}
%patch0 -p1
# hack to allow building against 1.8.0 as 1.8.1 is not yet in the buildroot
sed -i 's/GST_REQ=1.8.1/GST_REQ=1.8.0/' configure
sed -i 's/GST_PBREQ=1.8.1/GST_PBREQ=1.8.0/' configure


%build
export CFLAGS="$RPM_OPT_FLAGS -Wno-deprecated-declarations"
%configure --disable-dependency-tracking --disable-static \
  --with-package-name="gst-libav 1.0 rpmfusion rpm" \
  --with-package-origin="http://rpmfusion.org/" \
  --with-system-libav
make %{?_smp_mflags} V=1


%install
%make_install V=1
rm $RPM_BUILD_ROOT%{_libdir}/gstreamer-1.0/libgst*.la


%files
%doc AUTHORS COPYING.LIB ChangeLog NEWS README TODO
%{_libdir}/gstreamer-1.0/libgstlibav.so

%files devel-docs
# Take the dir and everything below it for proper dir ownership
%doc %{_datadir}/gtk-doc


%changelog
* Fri May 20 2016 mosquito <sensor.wen@gmail.com> - 1.8.1-2
- Rebuild for ffmpeg-3.0

* Sat May 14 2016 mosquito <sensor.wen@gmail.com> - 1.8.1-1
- Update to 1.8.1

* Sat Jan 23 2016 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.3-1
- Update to 1.6.3

* Thu Dec 24 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.2-1
- Update to 1.6.2

* Sat Oct 31 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.6.1-1
- Update to 1.6.1
- Upstream is using ffmpeg instead of libav now, switch to system ffmpeg-libs

* Sat May 16 2015 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.5-1
- Update to 1.4.5
- Update libav to 10.6

* Wed Oct  1 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.3-1
- Update to 1.4.3
- Includes libav 10.5

* Fri Aug 29 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.4.1-1
- Update to 1.4.1 (rf#3343)
- Includes libav 10.4

* Sun Jun 15 2014 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.4-1
- Update to 1.2.4 (rf#3269)
- Update libav to 9.13

* Sat Feb 15 2014 Michael Kuhn <suraia@ikkoku.de> - 1.2.3-1
- Update to 1.2.3.
- Update libav to 9.11.

* Sat Jan 04 2014 Michael Kuhn <suraia@ikkoku.de> - 1.2.2-1
- Update to 1.2.2.

* Sat Nov 16 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.1-1
- Rebase to 1.2.1

* Sun Oct 13 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.2.0-1
- Rebase to 1.2.0
- Upgrade the buildin libav to 9.10 to get all the security fixes from
  upstream libav
- Switch back to included libav copy again, libav and ffmpeg have
  deviated to much to use a system ffmpeg lib as libav replacement,
  this fixes a bad memory-leak (rpmfusion#2976)

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 1.1.3-4
- Rebuilt

* Tue Aug 27 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-3
- Rebuild now devel properly points to f20

* Mon Aug 26 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-2
- Rebuild for ffmpeg-2.0

* Thu Aug  8 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.1.3-1
- Rebase to 1.1.3
- Switch back to using system ffmpeg

* Tue Aug  6 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.9-1
- Rebase to 1.0.9
- This includes an upgrade of the buildin libav to 0.8.8 which includes a
  bunch of security fixes from
- No longer overwrite the included libav, as the bundled one is the latest

* Mon Mar 25 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.6-1
- Rebase to 1.0.6
- Upgrade the buildin libav to 0.8.6 to get all the security fixes from
  upstream libav

* Sun Mar 10 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-2
- Add a patch from upstream git to fix h264 decoding artifacts (rf#2710)
- Add a patch from upstream libav to fix miscompilation with gcc-4.8
  (rf#2710, gnome#695166, libav#388)

* Sat Mar  2 2013 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.5-1
- Rebase to 1.0.5 (rf#2688)
- Upgrade the buildin libav to 0.8.5 to get all the security fixes from
  upstream libav

* Sat Nov  3 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-2
- Build included libav with the default RPM_OPT_FLAGS (rf#2560, rf#2472)

* Sun Oct 28 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 1.0.2-1
- Rebase to 1.0.2
- Included libav copy updated to 0.8.4
- Change the license to LGPLv2+, as the GPL only postproc plugin is no longer
  included
- Replace references to ffmpeg with libav (rf#2472)
- Add COPYING.LIB to %%doc (rf#2472)
- Run make with V=1 (rf#2472)

* Sun Sep 23 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.99-1
- New upstream release 0.11.99

* Sun Sep  9 2012 Hans de Goede <j.w.r.degoede@gmail.com> - 0.11.93-1
- First version of gstreamer1-libav for rpmfusion
