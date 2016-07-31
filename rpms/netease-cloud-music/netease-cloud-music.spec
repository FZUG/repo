%global debug_package %{nil}
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "amd64" || echo "i386")
%global __requires_exclude lib(cef|crypto|cue)

Name:    netease-cloud-music
Version: 1.0.0
Release: 1%{?dist}
Summary: Netease Cloud Music, converted from .deb package

Group:   Applications/Multimedia
License: EULA
URL:     http://music.163.com/
Source0: http://s1.music.126.net/download/pc/%{name}_%{version}_amd64_ubuntu16.04.deb
Source1: http://s1.music.126.net/download/pc/%{name}_%{version}_i386_ubuntu16.04.deb
Source2: http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.0.0_1.0.2g-1ubuntu4.1_amd64.deb
Source3: http://security.ubuntu.com/ubuntu/pool/main/o/openssl/libssl1.0.0_1.0.2g-1ubuntu4.1_i386.deb
Source4: http://archive.ubuntu.com/ubuntu/pool/universe/libc/libcue/libcue1_1.4.0-1_amd64.deb
Source5: http://archive.ubuntu.com/ubuntu/pool/universe/libc/libcue/libcue1_1.4.0-1_i386.deb

BuildRequires: dpkg
BuildRequires: desktop-file-utils
Requires: desktop-file-utils
Requires: gstreamer1-plugins-ugly

%description
Netease Cloud Music, converted from .deb package

%prep
%ifarch x86_64
dpkg-deb -X %{S:0} .
dpkg-deb -X %{S:2} .
dpkg-deb -X %{S:4} .
%else
dpkg-deb -X %{S:1} .
dpkg-deb -X %{S:3} .
dpkg-deb -X %{S:5} .
%endif

%build

%install
# main program
install -d %{buildroot}{%{_libdir},%{_bindir}}
cp -r usr/lib/%{name} %{buildroot}%{_libdir}/
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# desktop entry
sed -i '12d' usr/share/applications/%{name}.desktop
install -D -m644 usr/share/applications/%{name}.desktop \
   %{buildroot}%{_datadir}/applications/%{name}.desktop

# icon file
install -D -m644 usr/share/icons/hicolor/scalable/apps/%{name}.svg \
   %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

# library files
install -D -m644 lib/%{_arch}-linux-gnu/libcrypto.so.1.0.0 \
   %{buildroot}%{_libdir}/%{name}/libcrypto.so.1.0.0
install -D -m644 lib/%{_arch}-linux-gnu/libssl.so.1.0.0 \
   %{buildroot}%{_libdir}/%{name}/libssl.so.1.0.0
install -D -m644 usr/lib/libcue.so.1.0.4 \
   %{buildroot}%{_libdir}/%{name}/libcue.so.1

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
%doc usr/share/doc/%{name}/*
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Sun Jul 31 2016 mosquito <sensor.wen@gmail.com> - 1.0.0-1
- Update to 1.0.0
* Tue May 31 2016 mosquito <sensor.wen@gmail.com> - 0.9.0-2
- Add Req gstreamer1-plugins-ugly
* Wed May 25 2016 mosquito <sensor.wen@gmail.com> - 0.9.0-1
- Initial build
