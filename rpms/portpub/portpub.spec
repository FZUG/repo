%global reponame portpub
%global commit ccd226a3fc7e59d89c77391be3c556e34d7c23a8
%global commitdate 20170406
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%if 0%{!?_unitdir:1}
%global _unitdir /usr/lib/systemd/system
%endif

Name:    %{reponame}
Version: 0
Release: 0.1.%{commitdate}git%{shortcommit}%{?dist}
Summary: Publish a service from localhost onto your server
License: GPLv3+

URL:     https://github.com/m13253/portpub
Source0: %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1: %{name}-conf
Source2: %{name}-relay@.service
Source3: %{name}-local@.service

ExclusiveArch: %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
%{systemd_requires}

%description
%{summary}.

%package local
Summary: Publish a service from localhost onto your server - client side

%description local
%{summary}.
Local side package.

%package relay
Summary: Publish a service from localhost onto your server - server side

%description relay
%{summary}.
Server side package.

%prep
%setup -q -n %{name}-%{commit}

%build
pushd %{name}-local
%gobuild -o %{name}-local

pushd ../%{name}-relay
%gobuild -o %{name}-relay

%install
install -Dm0755 %{name}-local/%{name}-local %{buildroot}%{_bindir}/%{name}-local
install -Dm0755 %{name}-relay/%{name}-relay %{buildroot}%{_bindir}/%{name}-relay
install -Dm0644 %{S:1} %{buildroot}%{_sysconfdir}/%{name}.d/local
install -Dm0644 %{S:1} %{buildroot}%{_sysconfdir}/%{name}.d/relay

install -d %{buildroot}{%{_unitdir},%{_userunitdir}}
install -m 0644 %{S:2} %{S:3} %{buildroot}%{_unitdir}/
install -m 0644 %{S:2} %{S:3} %{buildroot}%{_userunitdir}/

%post local
%systemd_post %{name}-local@local.service

%preun local
%systemd_preun %{name}-local@local.service

%postun local
%systemd_postun %{name}-local@local.service

%post relay
%systemd_post %{name}-relay@relay.service

%preun relay
%systemd_preun %{name}-relay@relay.service

%postun relay
%systemd_postun %{name}-relay@relay.service

%files local
%doc README.md
%license COPYING
%{_bindir}/%{name}-local
%dir %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}.d/local
%{_unitdir}/%{name}-local@.service
%{_userunitdir}/%{name}-local@.service

%files relay
%doc README.md
%license COPYING
%{_bindir}/%{name}-relay
%dir %{_sysconfdir}/%{name}.d
%config(noreplace) %{_sysconfdir}/%{name}.d/relay
%{_unitdir}/%{name}-relay@.service
%{_userunitdir}/%{name}-relay@.service

%changelog
* Sat Sep 09 2017 Zamir SUN <zsun@fedoraproject.org> - 0-0.1.20170406gitccd226a
- Initial with git version ccd226a.
