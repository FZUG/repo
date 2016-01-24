%global debug_package %{nil}
%global project XX-Net
%global repo %{project}

# commit
%global _commit 84585b1399a83307660a4be913de9fc363d0804a
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    xx-net
Version: 2.8.10
Release: 1.git%{_shortcommit}%{?dist}
Summary: A stable, easy to use and fast proxy based on GAE
Summary(zh_CN): 基于 GAE 的代理工具

Group:   Applications/Internet
License: BSD
URL:     https://github.com/XX-net/XX-Net
Source0: https://github.com/XX-net/XX-Net/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: systemd
Requires: nss-tools
Requires: libffi-devel
Requires: pyOpenSSL
Requires: pygtk2
Requires: python-appindicator
%{systemd_requires}

%description
A stable, easy to use and fast proxy based on GAE.

More https://github.com/XX-net/XX-Net/wiki

%description -l zh_CN
一款稳定易用的基于 GAE 的代理工具. 通过 WebUI 配置管理十分方便.

更多信息 https://github.com/XX-net/XX-Net/wiki

%prep
%setup -q -n %repo-%{_commit}

sed -i "/^noarch_lib/s|join(.[a-z,_ ']*)|join(root_path,'lib')|" \
  php_proxy/local/{cert_util,web_control,proxy}.py \
  gae_proxy/local/{check_local_network,cert_util,check_ip,proxy}.py \
  launcher/{update_from_github,start,gtk_tray,setup,web_control}.py

%build

%install
install -d %{buildroot}%{_datadir}/%{name}
mv python27/1.0/lib/noarch lib
cp -r README.md gae_proxy launcher php_proxy lib %{buildroot}%{_datadir}/%{name}

# bin script
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/bash
cd %{_datadir}/%{name}
if hash python2 2>/dev/null; then
    python2 launcher/start.py
else
    python launcher/start.py
fi
EOF

# systemd unit file
install -d %{buildroot}%{_unitdir}
cat > %{buildroot}%{_unitdir}/%{name}.service <<EOF
[Unit]
Description=A stable, fast proxy based on GAE
Documentation=https://github.com/XX-net/XX-Net/wiki
After=network.target remote-fs.target

[Service]
Type=simple
ExecStart=/usr/bin/python %{_datadir}/%{name}/launcher/start.py
# Send SIGINT for graceful stop
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
EOF

# dont check update
install -d %{buildroot}%{_datadir}/%{name}/data/launcher
cat > %{buildroot}%{_datadir}/%{name}/data/launcher/config.yaml <<EOF
modules:
  gae_proxy: {auto_start: 1, show_detail: 1}
  launcher: {allow_remote_connect: 0, control_port: 8085, proxy: pac}
  php_proxy: {control_port: 8083}
update: {check_update: dont-check, last_path: /usr/share/xx-net/launcher, uuid: `uuidgen`}
EOF

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE.txt
%attr(0755,-,-) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_unitdir}/%{name}.service

%changelog
* Mon Jan 25 2016 mosquito <sensor.wen@gmail.com> - 2.8.10-1.git84585b1
- Initial build
