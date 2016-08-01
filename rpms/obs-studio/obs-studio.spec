%global debug_package %{nil}
%global project obs-studio
%global repo %{project}

# commit
%global _commit cf983b7ccf8a8493289170385c78cb05596eb29e
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:       obs-studio
Version:    0.15.2
Release:    1.git%{_shortcommit}%{?dist}
Summary:    A recording/broadcasting program
Summary(zh_CN): 跨平台屏幕录制软件

Group:      Applications/Multimedia
License:    GPLv2
URL:        https://obsproject.com
Source:     https://github.com/jp9000/obs-studio/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  hicolor-icon-theme
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  jansson-devel
BuildRequires:  x264-devel
BuildRequires:  libv4l-devel
BuildRequires:  freetype-devel
BuildRequires:  fontconfig-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libX11-devel
BuildRequires:  libGL-devel
BuildRequires:  systemd-devel
BuildRequires:  ImageMagick-devel
BuildRequires:  libcurl-devel
BuildRequires:  zlib-devel

%description
Open Broadcaster Software is free and open source software
for video recording and live streaming.

%description -l zh_CN
Open Broadcaster Software 是一款免费开源的视频录制/直播软件.
- 使用 H264/AAC 编码视频, 支持封装格式为 MP4/FLV
- 支持 RTMP 流媒体直播

%package devel
Summary:    Header files and library for %{name}
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description devel
Open Broadcaster Software is free and open source software
for video recording and live streaming.

%description devel -l zh_CN
Open Broadcaster Software 是一款免费开源的视频录制/直播软件.

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir build && pushd build
%{cmake} .. \
    -DUNIX_STRUCTURE=ON \
%ifarch x86_64
    -DOBS_MULTIARCH_SUFFIX=64 \
%endif
    -DOBS_VERSION_OVERRIDE=%{version} \
    -DCMAKE_BUILD_TYPE=Release
%make_build

%install
%make_install -C build

%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:
/sbin/ldconfig

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:
/sbin/ldconfig

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc CONTRIBUTING README
%license COPYING
%{_bindir}/obs
%{_libdir}/obs-plugins
%{_libdir}/libobs*.so.*
%{_datadir}/applications/obs.desktop
%{_datadir}/icons/hicolor/*/apps/obs*
%{_datadir}/obs/

%files devel
%defattr(-,root,root,-)
%{_libdir}/cmake/LibObs
%{_libdir}/libobs*.so
%{_includedir}/obs

%changelog
* Mon Aug  1 2016 mosquito <sensor.wen@gmail.com> - 0.15.2-1.gitcf983b7
- Update to 0.15.2-1.gitcf983b7
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 0.15.1-1.git2732375
- Update to 0.15.1-1.git2732375
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 0.14.2-1.git48185cc
- Update to 0.14.2-1.git48185cc
* Tue Mar 22 2016 mosquito <sensor.wen@gmail.com> - 0.13.4-1.gitbcdb3dc
- Update to 0.13.4-1.gitbcdb3dc
* Sat Feb 27 2016 mosquito <sensor.wen@gmail.com> - 0.13.2-1.git4ce6df0
- Update to 0.13.2-1.git4ce6df0
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 0.13.1-1.gita6c8a92
- Update to 0.13.1-1.gita6c8a92
* Thu Jan 28 2016 mosquito <sensor.wen@gmail.com> - 0.13.0-1.git514b59c
- Update to 0.13.0-1.git514b59c
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 0.12.4-1.git2c8887b
- Update to 0.12.4-1.git2c8887b
* Sun Dec  6 2015 mosquito <sensor.wen@gmail.com> - 0.12.3-1.git725a36b
- Update to 0.12.3-1.git725a36b
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 0.12.0-1.git80b20ab
- Update to 0.12.0-1.git80b20ab
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 0.11.3-1.git4aef24a
- Update to 0.11.3-1.git4aef24a
* Wed Jul  1 2015 mosquito <sensor.wen@gmail.com> - 0.10.1-1.git82471d7
- Update to 0.10.1-1.git82471d7
* Sun May 10 2015 mosquito <sensor.wen@gmail.com> - 0.9.1-1.git8fb2929
- Rebuild for fedora
* Fri Mar 27 2015 jimmy@boombatower.com
- Update to 0.9.1 release.
  https://github.com/jp9000/obs-studio/releases/tag/0.9.1
* Thu Mar 26 2015 jimmy@boombatower.com
- Update to 0.9.0 release.
  https://github.com/jp9000/obs-studio/releases/tag/0.9.0
* Sat Feb 21 2015 jimmy@boombatower.com
- Update to 0.8.3 release.
  https://github.com/jp9000/obs-studio/releases/tag/0.8.3
* Thu Feb 12 2015 jimmy@boombatower.com
- Update to 0.8.2 release.
  https://github.com/jp9000/obs-studio/releases/tag/0.8.2
  https://github.com/jp9000/obs-studio/releases/tag/0.8.1
  https://github.com/jp9000/obs-studio/releases/tag/0.8.0
* Thu Jan 15 2015 jimmy@boombatower.com
- Update to 0.7.3 release.
  Details at https://github.com/jp9000/obs-studio/releases/tag/0.7.3
* Wed Jan  7 2015 jimmy@boombatower.com
- Update to 0.7.2 release.
  Details at https://github.com/jp9000/obs-studio/releases/tag/0.7.2 and
    https://github.com/jp9000/obs-studio/releases/tag/0.7.1
* Thu Nov 13 2014 jimmy@boombatower.com
- Initial 0.6.4 release.
