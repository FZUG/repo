Name:          handbrake
Version:       0.10.5
Release:       2%{dist}
Summary:       Multithreaded Video Transcoder
License:       GPLv2
Group:         Applications/Multimedia
Url:           http://handbrake.fr/
Source0:       http://handbrake.fr/mirror/HandBrake-%{version}.tar.bz2

BuildRequires: curl wget
BuildRequires: cmake
BuildRequires: intltool
BuildRequires: libtool
BuildRequires: nasm yasm
BuildRequires: lame-devel
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(bzip2)
BuildRequires: pkgconfig(dbus-glib-1)
BuildRequires: pkgconfig(dvdnav)
BuildRequires: pkgconfig(dvdread)
BuildRequires: pkgconfig(gstreamer-1.0)
BuildRequires: pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires: pkgconfig(gtk+-3.0) >= 3.10
BuildRequires: pkgconfig(webkitgtk-3.0)
BuildRequires: pkgconfig(gudev-1.0)
BuildRequires: pkgconfig(libass)
BuildRequires: pkgconfig(libavcodec) >= 57
BuildRequires: pkgconfig(libavformat) >= 57
BuildRequires: pkgconfig(libavresample) >= 3
BuildRequires: pkgconfig(libavutil) >= 55
BuildRequires: pkgconfig(libswscale) >= 4
BuildRequires: pkgconfig(libbluray)
BuildRequires: pkgconfig(libnotify)
BuildRequires: pkgconfig(samplerate)
BuildRequires: pkgconfig(theora)
BuildRequires: pkgconfig(vorbis)
BuildRequires: pkgconfig(vpx)
BuildRequires: pkgconfig(x265)
BuildRequires: x264-devel
Requires:      %{name}-cli = %{version}-%{release}
Requires:      %{name}-gui = %{version}-%{release}

%description
HandBrake is an open-source, GPL-licensed, multiplatform, multithreaded video
transcoder.

%package cli
Summary:       Multithreaded Video Transcoder
Group:         Applications/Multimedia

%description cli
HandBrake is an open-source, GPL-licensed, multiplatform, multithreaded video
transcoder.

This package contains a command-line interface for Handbrake.

%package gui
Summary:       Multithreaded Video Transcoder
Group:         Applications/Multimedia

%description gui
HandBrake is an open-source, GPL-licensed, multiplatform, multithreaded video
transcoder.

This package contains a GTK+ graphical user interface for Handbrake.

%prep
%setup -q -n HandBrake-%{version}

# Use more system libs
# We had ffmpeg here as well but it broke PGS subtitle processing
# https://forum.handbrake.fr/viewtopic.php?f=13&t=27581
sed -i \
    -e '/MODULES += contrib\/libbluray/d' \
    -e '/MODULES += contrib\/libdvdnav/d' \
    -e '/MODULES += contrib\/libdvdread/d' \
    make/include/main.defs

%build
export CFLAGS="%{optflags} -fno-strict-aliasing -Wno-unused -I%{_includedir}/ffmpeg"
export CXXFLAGS="$CFLAGS -Wno-reorder"

./configure \
    --force \
    --prefix=%{_prefix} \
    --strip="/bin/true" \
    --optimize=speed \
    --disable-gtk-update-checks

pushd build
%make_build

%install
%make_install -C build
%__ln_s ghb %{buildroot}%{_bindir}/HandBrakeGUI

%find_lang ghb

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/ghb.desktop

%post gui
/usr/bin/update-desktop-database &> /dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gui
/usr/bin/update-desktop-database &> /dev/null || :
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans gui
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f ghb.lang
%doc AUTHORS CREDITS NEWS THANKS
%license COPYING

%files cli
%defattr(-,root,root,-)
%{_bindir}/HandBrakeCLI

%files gui
%defattr(-,root,root,-)
%{_bindir}/ghb
%{_bindir}/HandBrakeGUI
%{_datadir}/applications/ghb.desktop
%{_datadir}/icons/hicolor/scalable/apps/hb-icon.*

%changelog
* Tue May 24 2016 mosquito <sensor.wen@gmail.com> - 0.10.5-2
- Rebuild for fedora 24

* Mon May 2 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.10.5-2
- Added scriptlets

* Thu Apr 28 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.10.5-1
- Initial build
