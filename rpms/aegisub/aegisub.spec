%bcond_with ffms2

Name:           aegisub
Version:        3.2.2
Release:        1%{?dist}
Summary:        A general-purpose subtitle editor with ASS/SSA support
License:        BSD-3-Clause
Url:            http://www.aegisub.org/
Source0:        http://ftp.aegisub.org/pub/releases/%{name}-%{version}.tar.xz

BuildRequires:  automake
BuildRequires:  boost-devel
BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  wxWidgets-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(zlib)
%if %{with ffms2}
BuildRequires:  pkgconfig(ffms2)
%endif

%description
Aegisub is an advanced subtitle editor for Windows, and UNIX-like systems, such
as Linux, Mac OS X and BSD. It is open source software and free for any use.

Aegisub natively works with the Advanced SubStation Alpha format (aptly
abbreviated ASS) which allows for many advanced effects in the subtitles, apart
from just basic timed text. Aegisub's goal is to support using these advanced
functions with ease.

%prep
%setup -q

FAKE_BUILDDATE=$(LC_ALL=C date -u '+%%b %%e %%Y')
FAKE_BUILDTIME=$(LC_ALL=C date -u '+%%H:%%M:%%S')
sed -i "s|__DATE__|\"$FAKE_BUILDDATE\"|
        s|__TIME__|\"$FAKE_BUILDTIME\"|" src/version.cpp
sed -i "/^LDFLAGS/s|$| -pthread|" Makefile.inc.in

%build
autoreconf -fi
%configure \
    --with-player-audio=PulseAudio \
    --without-oss \
    --disable-update-checker
%make_build

%install
%make_install
%find_lang %{name}-32

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

%files -f %{name}-32.lang
%defattr(-,root,root,-)
%doc LICENCE
%{_bindir}/%{name}-3.2
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Sat Dec  3 2016 mosquito <sensor.wen@gmail.com> - 3.2.2-1
- Initial build
