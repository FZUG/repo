%global debug_package %{nil}
%global tmproot /tmp/%{name}-%{version}
%global appurl  http://ftp.opera.com/pub/%{name}/%{version}/linux/%{name}_%{version}_amd64.deb

# Due to changes in Chromium, Opera is no longer able to use the system
# FFmpeg library for H264 video playback on Linux, so H264-encoded videos
# fail to play by default (but HTML5 video encoded using different formats,
# like webm, work). For legal reasons, Opera may not be distributed with H264
# compatible FFmpeg library included into package.
%global __requires_exclude (libffmpeg)

Name:    opera-beta
Version: 34.0.2036.24
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
mv %{buildroot}/usr/lib/*-linux-gnu/%{name} %{buildroot}/usr/lib/
rm -rf %{buildroot}/usr/lib/*-linux-gnu
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

# Fix symlink
rm -f %{buildroot}%{_bindir}/*
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}
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
mv %{tmproot}/usr/lib/*-linux-gnu/%{name} %{tmproot}/usr/lib/
rm -rf %{tmproot}/usr/lib/*-linux-gnu
mv %{tmproot}/usr/lib %{tmproot}%{_libdir}

# Modify desktop file:
sed -i '/Unity/s|^|#|' %{tmproot}%{_datadir}/applications/%{name}.desktop

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
    ln -sf %{_libdir}/%{name}/%{name} %{_bindir}
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
* Sun Dec 13 2015 mosquito <sensor.wen@gmail.com> -34.0.2036.24-1
- Update to 34.0.2036.24
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> -32.0.1948.19-1
- Update version 32.0.1948.19
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> -32.0.1948.4-1
- Update version 32.0.1948.4
* Mon Jun 29 2015 mosquito <sensor.wen@gmail.com> -31.0.1889.16-1
- Update version 31.0.1889.16
* Tue May 26 2015 mosquito <sensor.wen@gmail.com> -30.0.1835.26-1
- Update version 30.0.1835.26
* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> -27.0.1689.33-1
- Initial built
