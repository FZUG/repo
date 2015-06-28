%global debug_package %{nil}
%global project freshplayerplugin
%global repo %{project}

# commit
%global _commit ca0281d60da3dc81205c4e71f866a9450030f8bb
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: freshplayerplugin
Version: 0.2.4
Release: 1.git%{_shortcommit}%{?dist}
Summary: PPAPI-host NPAPI-plugin adapter
Summary(zh_CN): PPAPI-host NPAPI-plugin adapter

Group: System Environment/Libraries
# https://github.com/i-rinat/freshplayerplugin/raw/master/LICENSE
License: MIT
URL: https://github.com/i-rinat/freshplayerplugin
Source0: https://github.com/i-rinat/freshplayerplugin/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: cmake >= 2.8.8
BuildRequires: pkgconfig
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
BuildRequires: chrpath

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
mkdir build
pushd build
%{cmake} -DCMAKE_BUILD_TYPE=Release ..
make %{?_smp_mflags}

%install
# library file
chrpath -d build/libfreshwrapper-pepperflash.so
install -d %{buildroot}%{_libdir}/mozilla/plugins/
install -m 755 build/libfreshwrapper-pepperflash.so \
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
%doc LICENSE README.md data/freshwrapper.conf.example doc/*.md
%{_sysconfdir}/freshwrapper.conf
%{_libdir}/mozilla/plugins/*.so

%changelog
* Mon Jun  1 2015 mosquito <sensor.wen@gmail.com> - 0.2.4-1.gitca0281d
- Initial build
