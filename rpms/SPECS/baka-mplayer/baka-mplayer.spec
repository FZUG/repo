%global debug_package %{nil}
%global project Baka-MPlayer
%global repo %{project}

# commit
%global _commit 554ec3818ed4a4a3fa287756e0589779ca7d33f9
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: baka-mplayer
Version: 2.0.3
Release: 1.git%{_shortcommit}%{?dist}
Summary: The mpv based media player
Summary(zh_CN): 基于 mpv 的媒体播放器

License: GPLv2
Group: Applications/Multimedia
Url: http://bakamplayer.u8sand.net
Source0: https://github.com/u8sand/Baka-MPlayer/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: qt5-qttools-devel
BuildRequires: pkgconfig(Qt5Core) >= 5.2.0
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: pkgconfig(Qt5X11Extras)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(mpv)
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
%if 0%{?fedora} > 21
Requires(post): gtk-update-icon-cache
Requires(postun): gtk-update-icon-cache
%endif

%description
Baka MPlayer is a free and open source, cross-platform, libmpv based multimedia
player. Its simple design reflects the idea for an uncluttered, simple, and
enjoyable environment for watching tv shows.

%description -l zh_CN
Baka MPlayer 是一款开源, 跨平台, 基于 libmpv 的多媒体播放器.
其遵循简洁的设计理念, 使用户在简单, 愉快的环境中观看视频.

%prep
%setup -q -n %repo-%{_commit}

%build
%{_qt5_qmake} src/Baka-MPlayer.pro CONFIG+="release install_translations man.extra" \
lupdate=lupdate-qt5 lrelease=lrelease-qt5 \
DOCDIR=%{_docdir} LICENSEDIR=%{_docdir} \
QMAKE_CFLAGS+="%{optflags}" QMAKE_CXXFLAGS+="%{optflags}"
make %{?_smp_mflags}

%install
%make_install INSTALL_ROOT=%{buildroot}

%post
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%postun
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc DOCS/%{name}.md LICENSE
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man1/%{name}.1.gz
%{_datadir}/pixmaps/%{name}.svg
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/applications/%{name}.desktop

%changelog
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 2.0.3-1.git554ec38
- Update to 2.0.3-1.git554ec38
* Thu Jul 23 2015 mosquito <sensor.wen@gmail.com> - 2.0.3-1.git8b02c84
- Initial build
