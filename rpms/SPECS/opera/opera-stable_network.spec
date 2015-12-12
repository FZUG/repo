%global debug_package %{nil}
%global tmproot /tmp/%{name}-%{version}
%global appname opera
%global appurl  http://ftp.opera.com/pub/%{appname}/desktop/%{version}/linux/%{name}_%{version}_amd64.deb

# Due to changes in Chromium, Opera is no longer able to use the system
# FFmpeg library for H264 video playback on Linux, so H264-encoded videos
# fail to play by default (but HTML5 video encoded using different formats,
# like webm, work). For legal reasons, Opera may not be distributed with H264
# compatible FFmpeg library included into package.
%global __requires_exclude (libffmpeg)

Name:    opera-stable
Version: 34.0.2036.25
Release: 1
Summary: Fast and secure web browser
Summary(ru): Быстрый и безопасный Веб-браузер
Summary(zh_CN): 快速安全的欧朋浏览器

Group:   Applications/Internet
License: Proprietary
URL:     http://www.opera.com/browser

ExclusiveArch: x86_64
BuildRequires: axel dpkg
BuildRequires: desktop-file-utils
Requires: axel dpkg
Requires: desktop-file-utils
Requires: /usr/bin/gtk-update-icon-cache
Requires: /usr/bin/update-mime-database

%description
 Opera is a fast, secure, and user-friendly web browser.
 It includes web developer tools, news aggregation, and the ability
 to compress data via Opera Turbo on congested networks.

%description -l ru
 Opera — это быстрый, безопасный и дружественный к пользователю
 веб-браузер. Он включает средства веб-разработки и сбора новостей,
 а также возможность сжимать трафик в перегруженных сетях
 посредством технологии Opera Turbo.

%description -l zh_CN
 Opera 是一款快速, 安全, 友好的 web 浏览器.
 它包含 web 开发工具, 新闻聚合, 通过 Opera Turbo 技术
 在低速网络中传输经过压缩的数据.

%prep
%build

%install
# Download opera
test -f %{name}_%{version}_amd64.deb || axel -a %appurl

# Extract DEB package
dpkg-deb -X %{name}_%{version}_amd64.deb %{buildroot}

# Move /usr/lib/x86_64-linux-gnu/#{name} to #{_libdir}
mv %{buildroot}/usr/lib/*-linux-gnu/%{appname} %{buildroot}/usr/lib/%{name}
rm -rf %{buildroot}/usr/lib/*-linux-gnu
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

# Modify desktop file
mv %{buildroot}%{_datadir}/applications/%{appname}.desktop \
   %{buildroot}%{_datadir}/applications/%{name}.desktop

# Rename icon files
for i in 256x256 128x128 48x48 32x32 16x16; do
mv %{buildroot}%{_datadir}/icons/hicolor/${i}/apps/%{appname}.png \
   %{buildroot}%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done
mv %{buildroot}%{_datadir}/pixmaps/%{appname}.xpm \
   %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# Fix symlink
rm -f %{buildroot}%{_bindir}/*
ln -sfv %{_libdir}/%{name}/%{appname} %{buildroot}%{_bindir}/%{name}
ln -sfv %{_libdir}/%{name}/lib/libffmpeg.so.34 %{buildroot}%{_libdir}

# Clean files
rm -rf %{buildroot}%{_datadir}/{menu,lintian}

%pre
if [ $1 -ge 1 ]; then
# Download opera
cd /tmp
test -f %{name}_%{version}_amd64.deb || axel -a %appurl

# Extract DEB package
mkdir %{tmproot} &>/dev/null ||:
dpkg-deb -x %{name}_%{version}_amd64.deb %{tmproot}

# Move /usr/lib/x86_64-linux-gnu/#{name} to #{_libdir}
mv %{tmproot}/usr/lib/*-linux-gnu/%{appname} %{tmproot}/usr/lib/%{name}
rm -rf %{tmproot}/usr/lib/*-linux-gnu
mv %{tmproot}/usr/lib %{tmproot}%{_libdir}

# Modify desktop file
mv %{tmproot}%{_datadir}/applications/%{appname}.desktop \
   %{tmproot}%{_datadir}/applications/%{name}.desktop
sed -i -e '
    s|^TryExec=%{appname}|TryExec=%{name}|
    s|^Exec=%{appname}|Exec=%{name}|
    s|^Icon=%{appname}|Icon=%{name}|
    /Unity/s|^|#|' \
  %{tmproot}%{_datadir}/applications/%{name}.desktop

# Rename icon files
for i in 256x256 128x128 48x48 32x32 16x16; do
mv %{tmproot}%{_datadir}/icons/hicolor/${i}/apps/%{appname}.png \
   %{tmproot}%{_datadir}/icons/hicolor/${i}/apps/%{name}.png
done
mv %{tmproot}%{_datadir}/pixmaps/%{appname}.xpm \
   %{tmproot}%{_datadir}/pixmaps/%{name}.xpm

# Install *.desktop file:
desktop-file-install \
  --dir %{tmproot}%{_datadir}/applications \
  --add-category Network \
  --add-category WebBrowser \
  --delete-original \
  %{tmproot}%{_datadir}/applications/%{name}.desktop

# Fix symlink
rm -f %{tmproot}%{_bindir}/*

# Clean files
rm -rf %{tmproot}%{_datadir}/{menu,lintian}
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/usr/* /usr/; rm -rf %{tmproot}
    ln -sf %{_libdir}/%{name}/%{appname} %{_bindir}/%{name}
    ln -sf %{_libdir}/%{name}/lib/libffmpeg.so.34 %{_libdir}

    chown root:root "%{_libdir}/%{name}/opera_sandbox"
    chmod 4755 "%{_libdir}/%{name}/opera_sandbox"
    chmod 0755 "%{_libdir}/%{name}/lib/libffmpeg.so.34"
fi

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
    /usr/bin/update-mime-database %{_datadir}/mime &>/dev/null ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
/usr/bin/update-mime-database /usr/share/mime &>/dev/null ||:

%files
%defattr(-,root,root,-)
%ghost %{_bindir}/%{name}
%ghost %{_libdir}/%{name}
%ghost %{_libdir}/libffmpeg.so.*
%ghost %{_datadir}/pixmaps/%{name}.xpm
%ghost %{_datadir}/mime/packages/%{name}.xml
%ghost %{_datadir}/applications/%{name}.desktop
%ghost %{_datadir}/icons/hicolor/*/apps/%{name}.png
%ghost %{_defaultdocdir}/%{name}

%changelog
* Sun Dec 13 2015 mosquito <sensor.wen@gmail.com> -34.0.2036.25-1
- Update to 34.0.2036.25
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> -32.0.1948.25-1
- Update to 32.0.1948.25
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> -31.0.1889.99-1
- Update to 31.0.1889.99
* Mon Jun 29 2015 mosquito <sensor.wen@gmail.com> -30.0.1835.88-1
- Update to 30.0.1835.88
* Tue May 26 2015 mosquito <sensor.wen@gmail.com> -29.0.1795.60-1
- Update to 29.0.1795.60
* Wed Dec 17 2014 mosquito <sensor.wen@gmail.com> -26.0.1656.60-1
- Update to 26.0.1656.60
* Wed Dec 10 2014 mosquito <sensor.wen@gmail.com> -26.0.1656.32-2
- Rebuild
* Wed Dec 10 2014 mosquito <sensor.wen@gmail.com> -26.0.1656.32-1
- Initial built
