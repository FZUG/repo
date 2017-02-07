Name:          handbrake
Version:       1.0.2
Release:       1%{?dist}
Summary:       Multithreaded Video Transcoder
License:       GPLv2
Group:         Applications/Multimedia
Url:           http://handbrake.fr/
Source0:       http://handbrake.fr/mirror/HandBrake-%{version}.tar.bz2
Source1:       https://download.handbrake.fr/contrib/libav-12.tar.gz
Source2:       https://download.handbrake.fr/contrib/libbluray-0.9.3.tar.bz2
Source3:       https://download.handbrake.fr/contrib/libvpx-1.5.0.tar.bz2
Source4:       https://download.handbrake.fr/contrib/x265_2.1-1.tar.gz

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
BuildRequires: pkgconfig(opus)
BuildRequires: pkgconfig(jansson)
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
mkdir download
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} download
touch download/*
# Use more system libs
# We had ffmpeg here as well but it broke PGS subtitle processing
# https://forum.handbrake.fr/viewtopic.php?f=13&t=27581
sed -i \
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
make %{?_smp_mflags}
popd

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

%files
%doc AUTHORS.markdown NEWS.markdown THANKS.markdown README.markdown

%files cli
%license COPYING LICENSE
%{_bindir}/HandBrakeCLI

%files gui -f ghb.lang
%license COPYING LICENSE
%{_bindir}/ghb
%{_bindir}/HandBrakeGUI
%{_datadir}/applications/ghb.desktop
%{_datadir}/icons/hicolor/scalable/apps/hb-icon.*

%changelog
* Tue Feb  7 2017 Robin Lee <cheeselee@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2
- Include all the sources which are downloaded during building

* Tue May 24 2016 mosquito <sensor.wen@gmail.com> - 0.10.5-2
- Rebuild for fedora 24

* Mon May 2 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.10.5-2
- Added scriptlets

* Thu Apr 28 2016 David Vásquez <davidjeremias82 AT gmail DOT com> - 0.10.5-1
- Initial build
