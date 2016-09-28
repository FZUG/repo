AutoReqProv: no

%global currenf 52.0a1
%global _optdir /opt
%ifarch x86_64
%global arch x86_64
%else
%global arch i686
%endif

Summary:  Standalone web browser from mozilla.org, nightly build
Name: firefox-nightly
Version: 52.0a1
Release: 1.prebuilt%{?dist}
License: MPLv1.1 or GPLv2+ or LGPLv2+
Group: Applications/Internet
URL: http://www.mozilla.org/projects/firefox
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: wget
BuildRequires: tar
Requires: alsa-lib
Requires: libX11
Requires: libXcomposite
Requires: libXdamage
Requires: libnotify
Requires: libXt
Requires: libXext
Requires: glib2
Requires: dbus-glib
Requires: libjpeg-turbo
Requires: cairo-gobject
Requires: libffi
Requires: fontconfig
Requires: freetype
Requires: libgcc
Requires: gtk3
Requires: gtk2
Requires: hunspell
Requires: zlib
Requires: nspr >= 4.10.8
Requires: nss >= 3.19.2
Requires: sqlite >= 3.8.10.2

%description
Mozilla Firefox is an open-source web browser, designed for standards 
compliance, performance and portability.

%prep


%build
wget -c --no-check-certificate -P %{_builddir} https://archive.mozilla.org/pub/firefox/nightly/latest-mozilla-central/firefox-%{currenf}.en-US.linux-%{arch}.tar.bz2
tar -jxvf firefox-%{currenf}.en-US.linux-*.tar.bz2  -C %{_builddir}

%install

install -dm 755 %{buildroot}/{usr/{bin,share/{applications,pixmaps}},opt}
install -dm 755 %{buildroot}/%{_optdir}/firefox-%{version}/browser/defaults/preferences/

install -m644 %{_builddir}/firefox/browser/icons/mozicon128.png %{buildroot}/usr/share/pixmaps/%{name}-icon.png
cp -rf %{_builddir}/firefox/* %{buildroot}/opt/firefox-%{version}/
ln -s /opt/firefox-%{version}/firefox %{buildroot}/usr/bin/firefox-nightly

cat > %{buildroot}/%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Name=Firefox Nightly
GenericName=Web Browser
Icon=/usr/share/pixmaps/firefox-nightly-icon.png
Type=Application
Categories=Application;Network;
MimeType=text/html
Encoding=UTF-8
Exec=firefox-nightly %u
Terminal=false
MultipleArgs=false
StartupNotify=false
EOF

cat > %{buildroot}/%{_datadir}/applications/%{name}-safe.desktop << EOF
[Desktop Entry]
Name=Firefox Nightly - Safe Mode
GenericName=Web Browser - Safe Mode
Icon=/usr/share/pixmaps/firefox-nightly-icon.png
Type=Application
Categories=Application;Network;
MimeType=text/html
Encoding=UTF-8
Exec=firefox-nightly -safe-mode %u
Terminal=false
MultipleArgs=false
StartupNotify=false
EOF

# disable update check
echo '// Disable update check
pref("app.update.enabled", false);' > %{buildroot}/opt/firefox-%{version}/browser/defaults/preferences/vendor.js

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/%{name}
%{_datadir}/applications/%{name}*.desktop
%{_datadir}/pixmaps/%{name}-icon.png
%{_optdir}/firefox-%{version}/

%changelog
* Wed Sep 28 2016 nrechn <nrechn@gmail.com> - 52.0a1-1
- Updated to 52.0a1

* Sun Sep 4 2016 nrechn <nrechn@gmail.com> - 51.0a1-2
- Rebuild 51.0a1
- Fix "Release" version number

* Sat Aug 6 2016 nrechn <nrechn@gmail.com> - 51.0a1-1
- Updated to 51.0a1

* Fri Jul 15 2016 nrechn <nrechn@gmail.com> - 50.0a1-1
- Updated to 50.0a1

* Tue Mar 29 2016 nrechn <nrechn@gmail.com> - 49.0a1-1
- Updated to 49.0a1

* Tue Mar 29 2016 David Vásquez <davidjeremias82@gmail.com> - 48.0a1-1
- Updated to 48.0a1

* Mon Aug 10 2015 David Vásquez <davidjeremias82@gmail.com> - 43-0a1
- Initial build
