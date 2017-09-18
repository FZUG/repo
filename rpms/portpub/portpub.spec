%global reponame popub
%global commit 25cf44ee922c0b91a42c071ec0a9b21d2014eb24
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
URL:     https://github.com/1dot75cm/popub
Source0: %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

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
BUILD_ID="0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
%make_build PREFIX=%{_prefix} GOBUILD="go build -compiler gc -ldflags \"${LDFLAGS} -B $BUILD_ID\" -a -v -x"

%install
%make_install PREFIX=%{_prefix}

%files local
%doc README.md
%license COPYING
%{_bindir}/%{name}-local
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/local.d
%{_unitdir}/%{name}-local@.service
%{_userunitdir}/%{name}-local@.service

%files relay
%doc README.md
%license COPYING
%{_bindir}/%{name}-relay
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/relay.d
%{_unitdir}/%{name}-relay@.service
%{_userunitdir}/%{name}-relay@.service

%changelog
* Mon Sep 18 2017 mosquito <sensor.wen@gmail.com> - 0-0.1.20170406git25cf44e
- Improve makefile

* Sat Sep 09 2017 Zamir SUN <zsun@fedoraproject.org> - 0-0.1.20170406gitccd226a
- Initial with git version ccd226a.
