%global debug_package %{nil}
%global project freshplayerplugin
%global repo %{project}

# commit
%global _commit 3c6567a8c32a69bfeb20b280b9dcf060b5859954
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: freshplayerplugin
Version: 0.3.3
Release: 1.git%{_shortcommit}%{?dist}
Summary: PPAPI-host NPAPI-plugin adapter
Summary(zh_CN): PPAPI-host NPAPI-plugin adapter

Group: System Environment/Libraries
# https://github.com/i-rinat/freshplayerplugin/raw/master/LICENSE
License: MIT
URL: https://github.com/i-rinat/freshplayerplugin
Source0: https://github.com/i-rinat/freshplayerplugin/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: cmake >= 2.8.8
BuildRequires: pkgconfig chrpath
BuildRequires: ragel
BuildRequires: alsa-lib-devel
BuildRequires: openssl-devel
BuildRequires: glib2-devel
BuildRequires: libconfig-devel
BuildRequires: pango-devel
BuildRequires: libevent-devel
BuildRequires: gtk2-devel
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
%setup -q -n %repo-%{_commit}

%build
mkdir build && pushd build
%{cmake} -DCMAKE_BUILD_TYPE=Release ..
make %{?_smp_mflags}

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
%defattr(-,root,root,-)
%doc README.md data/freshwrapper.conf.example doc/*.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/freshwrapper.conf
%{_libdir}/mozilla/plugins/*.so

%changelog
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
