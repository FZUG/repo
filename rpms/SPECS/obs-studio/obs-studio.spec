%global debug_package %{nil}
%global project obs-studio
%global repo %{project}

# commit
%global _commit 725a36bc0f7c12dcfece44cf5c431e46acc55a74
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:       obs-studio
Version:    0.12.3
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
make %{?_smp_mflags}

%install
%make_install -C build

%post
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
/sbin/ldconfig

%postun
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
/sbin/ldconfig

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
