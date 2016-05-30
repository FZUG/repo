%undefine _hardened_build

Name:           moc
Epoch:          1
Version:        2.6
Release:        0.3.alpha2%{?dist}
Summary:        Music on Console - Console audio player for Linux/UNIX
Group:          Applications/Multimedia
License:        GPLv2+
URL:            http://moc.daper.net/
Source0:        http://ftp.daper.net/pub/soft/%{name}/unstable/%{name}-%{version}-alpha2.tar.xz

# Fix rpmlint E: incorrect-fsf-address
Patch0:         trivial-update-FSF-address.patch

BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(ao)
BuildRequires:  faad2-devel
BuildRequires:  file-devel
BuildRequires:  pkgconfig(flac)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(id3tag)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libcurl)
BuildRequires:  libdb-devel
BuildRequires:  libmpcdec-devel
BuildRequires:  pkgconfig(libmodplug)
BuildRequires:  pkgconfig(librcc)
BuildRequires:  pkgconfig(libtimidity)
BuildRequires:  pkgconfig(mad)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(ogg)
BuildRequires:  libtool
BuildRequires:  libtool-ltdl-devel
BuildRequires:  pkgconfig(popt)
BuildRequires:  pkgconfig(samplerate)
BuildRequires:  pkgconfig(sndfile)
BuildRequires:  pkgconfig(speex)
BuildRequires:  pkgconfig(taglib)
BuildRequires:  pkgconfig(vorbis)
BuildRequires:  pkgconfig(wavpack)
BuildRequires:  pkgconfig(zlib)

%description
MOC (music on console) is a console audio player for LINUX/UNIX designed to be
powerful and easy to use. You just need to select a file from some directory
using the menu similar to Midnight Commander, and MOC will start playing all
files in this directory beginning from the chosen file.

%prep
%autosetup -n %{name}-%{version}-alpha2 -p1

%build
%configure \
       --disable-rpath \
       --disable-cache \
       --disable-debug \
       --with-pic \
       --with-aac \
       --with-alsa \
       --with-curl  \
       --with-ffmpeg \
       --with-flac \
       --with-jack \
       --with-modplug \
       --with-mp3 \
       --with-musepack \
       --with-ncurses \
       --with-oss \
       --with-rcc \
       --with-samplerate \
       --with-sndfile \
       --with-speex \
       --with-vorbis \
       --with-wavpack

%make_build V=1

%install
%make_install

%{__rm} -r %{buildroot}%{_docdir}/%{name}
%{__rm} -r %{buildroot}%{_libdir}/%{name}/decoder_plugins/lib*.la

%files
%doc AUTHORS README* config.example.in keymap.example
%license COPYING
%{_bindir}/%{name}p
%{_datadir}/%{name}
%{_libdir}/%{name}/decoder_plugins/lib*.so
%{_mandir}/man1/%{name}p.1.*

%changelog
* Mon May 30 2016 mosquito <sensor.wen@gmail.com> - 1:2.6-0.3.alpha2
- Use pkgconfig for BReq
- Add --with-pic, --with-ncurses, --with-rcc flags

* Fri May 27 2016 nrechn <neil@gyz.io> - 1:2.6-0.2.alpha2
- Fix filename display issue
- rebuild for FZUG

* Mon May 09 2016 Maxim Orlov <murmansksity@gmail.com> - 1:2.6-0.1.alpha2.R
- Update to 2.6-alpha2

* Thu Nov  4 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.5.0-0.2.20101030svn2252
- update to last snapshot

* Mon Apr 26 2010 Arkady L. Shane <ashejn@yandex-team.ru> - 2.5.0-0.1.alpha4
- update to 2.5.0-alpha4

* Wed May 13 2009 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.4-1
- update to 2.4.4

* Wed Nov 21 2007 Arkady L. Shane <ashejn@yandex-team.ru> - 2.4.3-1
- initial build for Fedora
