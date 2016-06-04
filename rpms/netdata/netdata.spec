%global debug_package %{nil}
# Conditional build
%bcond_without nfacct
%if 0%{?fedora} || 0%{?rhel} >= 7
%bcond_without systemd
%endif

Name:    netdata
Version: 1.2.0
Release: 2%{?dist}
Summary: Real-time performance monitoring, done right
License: GPLv3+
Group:   Applications/System
URL:     http://github.com/firehol/netdata/
Source0: http://github.com/firehol/netdata/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires: libtool
BuildRequires: pkgconfig(uuid)
BuildRequires: pkgconfig(zlib)
%if %{with nfacct}
BuildRequires: pkgconfig(libmnl)
BuildRequires: pkgconfig(libnetfilter_acct)
%endif
%if %{with systemd}
BuildRequires: systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

%description
netdata is the fastest way to visualize metrics. It is a resource
efficient, highly optimized system for collecting and visualizing any
type of realtime timeseries data, from CPU usage, disk activity, SQL
queries, API calls, web site visitors, etc.

netdata tries to visualize the truth of now, in its greatest detail,
so that you can get insights of what is happening now and what just
happened, on your systems and applications.

%prep
%setup -q

%build
autoreconf -ivf
%configure \
    --with-zlib \
    --with-math \
    %{?with_nfacct:--enable-plugin-nfacct} \
    --with-user=%{name}
%{make_build}

%install
%{__make} install DESTDIR=%{buildroot}
install -m 644 -p system/%{name}.conf %{buildroot}%{_sysconfdir}/%{name}/
find %{buildroot} -name .keep | xargs rm

%if %{with systemd}
install -Dm 644 -p system/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
%endif

%pre
getent group %{name} > /dev/null || groupadd -r %{name}
getent passwd %{name} > /dev/null || useradd -r -g %{name} \
    -c %{name} -s /sbin/nologin -d %{_datadir}/%{name} %{name}

%if %{with systemd}
%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service
%endif

%files
%defattr(-,root,root,-)
%doc README.md
%license COPYING
%{_sbindir}/%{name}
%dir %{_datadir}/%{name}
%{_libexecdir}/%{name}
%{?with_systemd:%{_unitdir}/%{name}.service}
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.conf
%attr(-,%{name},%{name}) %dir %{_localstatedir}/cache/%{name}
%attr(-,%{name},%{name}) %dir %{_localstatedir}/log/%{name}

# override defattr for web files
%defattr(644,root,%{name},755)
%{_datadir}/%{name}/web

%changelog
* Fri Jun  3 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-2
- Add autoreconf
* Fri Jun  3 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-1
- Initial build
