%global project freshplayerplugin
%global repo %{project}

%global commit 8debda7f3a03bedfface616fe459d70e6f58e37a
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:    freshplayerplugin
Version: 0.3.7
Release: 1.git%{shortcommit}%{?dist}
Summary: PPAPI-host NPAPI-plugin adapter
Summary(zh_CN): PPAPI-host NPAPI-plugin adapter

Group:   System Environment/Libraries
License: MIT
URL:     https://github.com/i-rinat/freshplayerplugin
Source0: %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires: cmake >= 2.8.8
BuildRequires: pkgconfig chrpath
BuildRequires: ragel
BuildRequires: alsa-lib-devel
BuildRequires: openssl-devel
BuildRequires: glib2-devel
BuildRequires: libconfig-devel
BuildRequires: pango-devel
BuildRequires: libevent-devel
BuildRequires: libXrandr-devel
BuildRequires: libXrender-devel
BuildRequires: libXcursor-devel
BuildRequires: libv4l-devel
BuildRequires: mesa-libGLES-devel
BuildRequires: mesa-libGL-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: jack-audio-connection-kit-devel
BuildRequires: soxr-devel
BuildRequires: ffmpeg-devel
BuildRequires: libva-devel
BuildRequires: libvdpau-devel
BuildRequires: libicu-devel

%description
 The main goal of this project is to get PPAPI (Pepper)
 Flash player working in Firefox by implementing a
 wrapper, some kind of adapter which will look like
 browser to PPAPI  plugin and look like NPAPI plugin
 for browser.

%description -l zh_CN
该项目的主要目标是让 PPAPI (Pepper) Flash player
通过封装, 以 PPAPI/NPAPI 插件的形式工作在 Firefox.

%prep
%setup -q -n %{repo}-%{commit}

%build
mkdir build && pushd build
%cmake -DCMAKE_BUILD_TYPE=Release ..
%make_build

%install
# library file
chrpath -d build/libfreshwrapper-flashplayer.so
install -d %{buildroot}%{_libdir}/mozilla/plugins/
install -m 755 build/libfreshwrapper-flashplayer.so \
    %{buildroot}%{_libdir}/mozilla/plugins/

# config file
install -d %{buildroot}%{_sysconfdir}
install -m 644 data/freshwrapper.conf.example \
    %{buildroot}%{_sysconfdir}/freshwrapper.conf
sed -i '/enable_xembed/s|1$|0|' %{buildroot}%{_sysconfdir}/freshwrapper.conf

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc README.md data/freshwrapper.conf.example doc/*.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/freshwrapper.conf
%{_libdir}/mozilla/plugins/*.so

%changelog
* Mon Sep 11 2017 mosquito <sensor.wen@gmail.com> - 0.3.7-1.git8debda7
- Update to 0.3.7
* Thu Oct  6 2016 mosquito <sensor.wen@gmail.com> - 0.3.6-1.git333df0b
- Update to 0.3.6
* Fri Jul 15 2016 mosquito <sensor.wen@gmail.com> - 0.3.5-2.git51946f8
- Rebuild for ffmpeg 3.0.2
* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 0.3.5-1.git51946f8
- Update version to 0.3.5-1.git51946f8
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 0.3.4-1.git2b06d00
- Update version to 0.3.4-1.git2b06d00
* Sun Dec  6 2015 mosquito <sensor.wen@gmail.com> - 0.3.3-1.git3c6567a
- Update version to 0.3.3-1.git3c6567a
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 0.3.2-1.git8cc1005
- Update version to 0.3.2-1.git8cc1005
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 0.3.1-1.gitacb0ee4
- Update version to 0.3.1-1.gitacb0ee4
* Wed Jul  1 2015 mosquito <sensor.wen@gmail.com> - 0.3.0-1.gite77cb63
- Update version to 0.3.0-1.gite77cb63
* Mon Jun  1 2015 mosquito <sensor.wen@gmail.com> - 0.2.4-1.gitca0281d
- Initial build
