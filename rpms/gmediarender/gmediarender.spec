%global debug_package %{nil}
%global project gmrender-resurrect
%global repo %{project}

# commit
%global _commit 400361649f3d540c08001c0ad68222388e65be67
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    gmediarender
Version: 0.0.7
Release: 1.git%{_shortcommit}%{?dist}
Summary: Resource efficient UPnP/DLNA renderer

License: LGPLv2+
URL:     http://github.com/hzeller/gmrender-resurrect
Source0: http://github.com/hzeller/gmrender-resurrect/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: systemd
BuildRequires: automake
BuildRequires: libupnp-devel
BuildRequires: gstreamer1-devel

Requires: gstreamer1-plugins-ugly
Requires: gstreamer1-plugins-bad-free
Requires: gstreamer1-plugins-base
Requires: gstreamer1-plugins-good
Requires(pre): shadow-utils

%description
GMediaRender is a resource efficient UPnP/DLNA renderer.

%prep
%setup -q -n %repo-%{_commit}
autoreconf -vfi

%build
%configure
make %{?_smp_mflags}

%install
install -d %{buildroot}%{_bindir}
install -m 0755 src/%{name} %{buildroot}%{_bindir}

install -d %{buildroot}%{_datadir}/%{name}
install -m 0644 data/grender-*.png %{buildroot}%{_datadir}/%{name}

install -d %{buildroot}%{_unitdir}
install -m 0644 dist-scripts/fedora/%{name}.service %{buildroot}%{_unitdir}

install -d %{buildroot}/usr/lib/firewalld/services
install -m 0644 dist-scripts/fedora/*.xml %{buildroot}/usr/lib/firewalld/services

%pre
getent group %{name} &>/dev/null || groupadd -r %{name}
getent passwd %{name} &>/dev/null || \
    useradd -r -g %{name} -G audio -M -d %{_datadir}/%{name} -s /sbin/nologin \
    -c "GMediaRender DLNA/UPnP Renderer" %{name}

%post
%systemd_post %{name}.service
%firewalld_reload

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
if [ $1 -eq 0 ]; then
    getent passwd %{name} &>/dev/null && userdel %{name}
    getent group %{name} &>/dev/null && groupdel %{name}
fi

%files
%defattr(-,root,root,-)
%doc README.md
%license COPYING
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/grender-*.png
%config(noreplace) %{_unitdir}/%{name}.service
/usr/lib/firewalld/services/%{name}.xml
/usr/lib/firewalld/services/ssdp.xml

%changelog
* Thu Jan 28 2016 mosquito <sensor.wen@gmail.com> - 0.0.7-1.git4003616
- Build for Fedora23
* Sun Mar 29 2015 <admin@vortexbox.org>
- Updated for systemd snippets, added automatic system user/group add
  and removal upon installation, added FirewallD support
* Mon Sep 16 2013 <admin@vortexbox.org>
- Initial release
