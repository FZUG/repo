%global debug_package %{nil}

# Due to changes in Chromium, Opera is no longer able to use the system
# FFmpeg library for H264 video playback on Linux, so H264-encoded videos
# fail to play by default (but HTML5 video encoded using different formats,
# like webm, work). For legal reasons, Opera may not be distributed with H264
# compatible FFmpeg library included into package.
%global __requires_exclude (libffmpeg)

Name:    opera-developer
Version: 37.0.2171.0
Release: 1%{?dist}
Summary: Fast and secure web browser
Summary(ru): Быстрый и безопасный Веб-браузер
Summary(zh_CN): 快速安全的欧朋浏览器

Group:   Applications/Internet
License: Proprietary
URL:     http://www.opera.com/browser
Source0: http://ftp.opera.com/pub/%{name}/%{version}/linux/%{name}_%{version}_amd64.deb
Source1: http://ftp.opera.com/pub/%{name}/%{version}/linux/%{name}_%{version}_i386.deb

BuildRequires: dpkg
BuildRequires: desktop-file-utils
Requires: chrpath
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
# Extract DEB package
%ifarch x86_64
dpkg-deb -X %{SOURCE0} %{buildroot}
%else
dpkg-deb -X %{SOURCE1} %{buildroot}
%endif

# Move /usr/lib/x86_64-linux-gnu/#{name} to #{_libdir}
mv %{buildroot}/usr/lib/*-linux-gnu/%{name} %{buildroot}/usr/lib/
rm -rf %{buildroot}/usr/lib/*-linux-gnu
%ifarch x86_64
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}
%endif

# Modify desktop file:
sed -i '/Unity/s|^|#|' %{buildroot}%{_datadir}/applications/%{name}.desktop

# Install *.desktop file:
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category Network \
  --add-category WebBrowser \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Fix symlink
rm -f %{buildroot}%{_bindir}/*
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}

# Clean files
rm -rf %{buildroot}%{_datadir}/{menu,lintian}

%post
chrpath -r %{_libdir}/%{name}/lib %{_libdir}/%{name}/%{name} &>/dev/null ||:
chown root:root "%{_libdir}/%{name}/opera_sandbox"
chmod 4755 "%{_libdir}/%{name}/opera_sandbox"

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
%{_bindir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/pixmaps/%{name}.xpm
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_defaultdocdir}/%{name}

%changelog
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> -37.0.2171.0-1
- Update version 37.0.2171.0
* Sun Feb 28 2016 mosquito <sensor.wen@gmail.com> -37.0.2142.0-1
- Update version 37.0.2142.0
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> -36.0.2129.0-1
- Update version 36.0.2129.0
* Thu Jan 28 2016 mosquito <sensor.wen@gmail.com> -36.0.2120.0-1
- Update version 36.0.2120.0
* Sun Jan 17 2016 mosquito <sensor.wen@gmail.com> -36.0.2106.0-1
- Update version 36.0.2106.0
* Sun Dec 13 2015 mosquito <sensor.wen@gmail.com> -36.0.2072.0-1
- Update version 36.0.2072.0
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> -34.0.1996.0-1
- Update version 34.0.1996.0
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> -32.0.1933.0-1
- Update version 32.0.1933.0
* Mon Jun 29 2015 mosquito <sensor.wen@gmail.com> -32.0.1899.0-1
- Update version 32.0.1899.0
* Tue May 26 2015 mosquito <sensor.wen@gmail.com> -31.0.1857.0-1
- Update version 31.0.1857.0
* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> -28.0.1719.0-1
- Initial built
