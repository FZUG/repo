%global debug_package %{nil}
%global arch x86_64
%global __requires_exclude lib(qcef|cef|cue|evdevgamepad|qt*|Qt*)

Name:    netease-cloud-music
Version: 1.1.0
Release: 1%{?dist}
Summary: Netease Cloud Music, converted from .deb package

Group:   Applications/Multimedia
License: EULA
URL:     https://music.163.com/
Source0: https://d1.music.126.net/dmusic/%{name}_%{version}_amd64_ubuntu.deb
Source1: %{name}.appdata.xml

ExclusiveArch:  %{ix86} x86_64 %{arm} aarch64 ppc64le
BuildRequires: dpkg
BuildRequires: desktop-file-utils
Requires: desktop-file-utils
Requires: gstreamer1-plugins-ugly

%description
Netease Cloud Music, converted from .deb package

%prep
dpkg-deb -X %{S:0} .

%build

%install
# main program
install -d %{buildroot}{%{_libdir},%{_bindir}}
cp usr/bin/%{name} %{buildroot}%{_bindir}/%{name}
cp -r usr/lib/%{name} %{buildroot}%{_libdir}/
sed -i 's/libjasper.so.1/libjasper.so.4/g' %{buildroot}/%{_libdir}/netease-cloud-music/plugins/imageformats/libqjp2.so
mkdir -p %{buildroot}/usr/lib
ln -s %{_libdir}/%{name}/ %{buildroot}/usr/lib/%{name}

install -d %{buildroot}%{_datadir}/appdata
cp %{SOURCE1} %{buildroot}%{_datadir}/appdata/

# desktop entry
install -D -m644 usr/share/applications/%{name}.desktop \
   %{buildroot}%{_datadir}/applications/%{name}.desktop

# icon file
install -D -m644 usr/share/icons/hicolor/scalable/apps/%{name}.svg \
   %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg


%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
     /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
     /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}/
/usr/lib/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%dir %{_datadir}/appdata
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Sun Mar 25 2018 robberphex <robberphex@gmail.com> - 1.1.0-1
- Update to 1.1.0
- Add appdata.xml
* Mon Oct 03 2016 nrechn <nrechn@gmail.com> - 1.0.0-2
- Fix source libssl not found
- Update source libssl package
* Sun Jul 31 2016 mosquito <sensor.wen@gmail.com> - 1.0.0-1
- Update to 1.0.0
* Tue May 31 2016 mosquito <sensor.wen@gmail.com> - 0.9.0-2
- Add Req gstreamer1-plugins-ugly
* Wed May 25 2016 mosquito <sensor.wen@gmail.com> - 0.9.0-1
- Initial build
