%global debug_package %{nil}
%global appname opera

# Due to changes in Chromium, Opera is no longer able to use the system
# FFmpeg library for H264 video playback on Linux, so H264-encoded videos
# fail to play by default (but HTML5 video encoded using different formats,
# like webm, work). For legal reasons, Opera may not be distributed with H264
# compatible FFmpeg library included into package.
%global __requires_exclude (libffmpeg)

Name: opera-stable
Version: 32.0.1948.25
Release: 1%{?dist}
Summary: Fast and secure web browser
Summary(ru): Быстрый и безопасный Веб-браузер
Summary(zh_CN): 快速安全的欧朋浏览器

Group: Applications/Internet
License: Proprietary
URL: http://www.opera.com/browser
Source0: http://ftp.opera.com/pub/%{appname}/desktop/%{version}/linux/%{name}_%{version}_amd64.deb

ExclusiveArch: x86_64
BuildRequires: desktop-file-utils
BuildRequires: dpkg

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
dpkg-deb -X %{SOURCE0} %{buildroot}

# Move /usr/lib/x86_64-linux-gnu/#{name} to #{_libdir}
mv %{buildroot}/usr/lib/*-linux-gnu/%{appname} %{buildroot}/usr/lib/%{name}
rm -rf %{buildroot}/usr/lib/*-linux-gnu
mv %{buildroot}/usr/lib %{buildroot}%{_libdir}

# Modify desktop file
mv %{buildroot}%{_datadir}/applications/%{appname}.desktop \
   %{buildroot}%{_datadir}/applications/%{name}.desktop
sed  -i -e 's|TryExec=%{appname}|TryExec=%{name}|' \
	-e 's|Exec=%{appname}|Exec=%{name}|' \
	-e 's|Icon=%{appname}|Icon=%{name}|' \
	-e '/Unity/s|^|#|' \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Rename icon files
mv %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{appname}.png \
   %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
mv %{buildroot}%{_datadir}/pixmaps/%{appname}.xpm \
   %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

# Install *.desktop file:
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  --add-category Network \
  --add-category WebBrowser \
  --delete-original \
  %{buildroot}%{_datadir}/applications/%{name}.desktop

# Fix symlink
rm -f %{buildroot}%{_bindir}/*
ln -sfv %{_libdir}/%{name}/%{appname} %{buildroot}%{_bindir}/%{name}

# Clean files
rm -rf %{buildroot}%{_datadir}/menu
rm -rf %{buildroot}%{_datadir}/lintian

%post
chown root:root "%{_libdir}/%{name}/opera_sandbox"
chmod 4755 "%{_libdir}/%{name}/opera_sandbox"

update-desktop-database &>/dev/null ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
if [ -x %{_bindir}/gtk-update-icon-cache ]; then
    %{_bindir}/gtk-update-icon-cache --quiet %{_datadir}/icons/hicolor ||:
fi

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
update-desktop-database &>/dev/null ||:

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/pixmaps/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*
%{_defaultdocdir}/%{name}

%changelog
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
