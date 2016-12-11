# https://github.com/RussianFedora/aegisub
# https://build.opensuse.org/package/show/openSUSE:Factory/aegisub
# https://www.archlinux.org/packages/community/x86_64/aegisub

Name:           aegisub
Version:        3.2.2
Release:        2%{?dist}
Summary:        A general-purpose subtitle editor with ASS/SSA support
License:        BSD-3-Clause
Url:            http://www.aegisub.org/
Source0:        http://ftp.aegisub.org/pub/releases/%{name}-%{version}.tar.xz

BuildRequires:  intltool
BuildRequires:  boost-devel
BuildRequires:  wxWidgets-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fftw3)
BuildRequires:  pkgconfig(ffms2)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(hunspell)
BuildRequires:  pkgconfig(icu-i18n)
BuildRequires:  pkgconfig(libass)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(portaudio-2.0)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(lua)
BuildRequires:  desktop-file-utils

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

#remove version postfix
sed -e 's|aegisub-[0-9.]*|aegisub|' -i configure.ac

%build
autoreconf -fi
%configure \
    --without-oss \
    --without-openal \
    --with-player-audio=PulseAudio \
    --with-wx-config=wx-config-3.0 \
    --disable-update-checker
%make_build

%install
%make_install
%find_lang %{name}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

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

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc automation/demos/ automation/v4-docs/
%license LICENCE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%changelog
* Sun Dec 11 2016 mosquito <sensor.wen@gmail.com> - 3.2.2-2
- Add BReq ffms2, freetype2, icu-i18n, portaudio-2.0, libavcodec
- Rename execution file
* Sat Dec  3 2016 mosquito <sensor.wen@gmail.com> - 3.2.2-1
- Initial build
