Note: Golang depends on network. Network should be enabled when building this software.

%global debug_package %{nil}

%global forgeurl https://github.com/fatedier/frp
Version: 0.40.0
%forgemeta

Name:    frp
Release: 1%{?dist}
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
export GOPROXY=https://mirrors.aliyun.com/goproxy/
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

%changelog
* Sun Mar 13 2022 zhullyb <zhullyb@outlook.com>
-  First Build.
