# Note: Golang depends on network. Network should be enabled when building this software.

%global debug_package %{nil}

%global forgeurl https://github.com/fatedier/frp
Version: 0.40.0
%forgemeta

Name:    frp
Release: 2%{?dist}
Summary: A fast reverse proxy to help you expose a local server behind a NAT or firewall to the internet
License: ASL 2.0
URL:	 %{forgeurl}
Source:  %{forgesource}

BuildRequires:  git
BuildRequires:  golang
BuildRequires:  systemd

%description
%{summary}.

%package -n frpc
Summary: Client version of frp.
%description -n frpc
This package provides client version of frp.

%package -n frps
Summary: Server version of frp.
%description -n frps
This package provides server version of frp.

%prep
%forgesetup

%build
export GO111MODULE=on
export GOPROXY=https://goproxy.cn,direct
%{make_build}

%install
%{__install} -Dm775 bin/frpc -t %{buildroot}%{_bindir}
%{__install} -Dm775 bin/frps -t %{buildroot}%{_bindir}
%{__install} -d %{buildroot}%{_sysconfdir}/frp
%{__cp} conf/{frpc_full.ini,frpc.ini,frps_full.ini,frps.ini} %{buildroot}%{_sysconfdir}/frp/
%{__install} -d %{buildroot}%{_unitdir}
%{__cp} conf/systemd/{frpc.service,frpc@.service,frps.service,frps@.service} %{buildroot}%{_unitdir}/

%files -n frpc
%license LICENSE
%{_bindir}/frpc
%{_sysconfdir}/frp/{frpc_full.ini,frpc.ini}
%{_unitdir}/{frpc.service,frpc@.service}

%files -n frps
%license LICENSE
%{_bindir}/frps
%{_sysconfdir}/frp/{frps_full.ini,frps.ini}
%{_unitdir}/{frps.service,frps@.service}

%preun -n frpc
%systemd_preun frpc.service

%preun -n frps
%systemd_preun frps.service

%changelog
* Fri Mar 18 2022 zhullyb <zhullyb@outlook.com> - 0.40.0-2
-  Add preun , see https://github.com/FZUG/repo/pull/392#issuecomment-1069201446


* Sun Mar 13 2022 zhullyb <zhullyb@outlook.com> - 0.40.0-1
-  First Build.
