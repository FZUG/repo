%global debug_package %{nil}
%global project XX-Net
%global repo %{project}

# commit
%global _commit 262bc7343f2ee8533df66316e8c5d1c1b00ec796
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global systemd_user_post() \
if [ $1 -eq 1 ] ; then\
     # Initial installation\
     systemctl preset --user --global %* >/dev/null 2>&1 || :\
fi\
%{nil}

Name:    xx-net
Version: 2.9.1
Release: 1.git%{_shortcommit}%{?dist}
Summary: A stable, easy to use and fast proxy based on GAE
Summary(zh_CN): 基于 GAE 的代理工具

Group:   Applications/Internet
License: BSD
URL:     https://github.com/XX-net/XX-Net
Source0: https://github.com/XX-net/XX-Net/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Patch0:  use-home-config.path

BuildArch: noarch
BuildRequires: systemd
Requires: nss-tools
Requires: libffi-devel
Requires: pyOpenSSL
Requires: pygtk2
Requires: python-appindicator

%description
A stable, easy to use and fast proxy based on GAE.

More https://github.com/XX-net/XX-Net/wiki

%description -l zh_CN
一款稳定易用的基于 GAE 的代理工具. 通过 WebUI 配置管理十分方便.

更多信息 https://github.com/XX-net/XX-Net/wiki

%prep
%setup -q -n %repo-%{_commit}
%patch0 -p1
find -type f -regextype posix-extended \( \
    -name '*.py' -exec sed -i '/^#!\/usr\/bin/d' '{}' \; -or \
    -name '.gitignore' -exec rm -f '{}' \; -or \
    -name '*.sh' -exec rm -f '{}' \; -or \
    -regex '.*.(py|js|css)$' -exec chmod 644 '{}' \; \)

%build

%install
install -d %{buildroot}%{_datadir}/%{name}
mv python27/1.0/lib/noarch lib
cp -r README.md launcher gae_proxy php_proxy x_tunnel lib \
    %{buildroot}%{_datadir}/%{name}

# bin script
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/bash
cd %{_datadir}/%{name}
/usr/bin/python2 launcher/start.py
EOF

# systemd unit file
install -d %{buildroot}%{_userunitdir}
cat > %{buildroot}%{_userunitdir}/%{name}.service <<EOF
[Unit]
Description=A stable, fast proxy based on GAE
Documentation=https://github.com/XX-net/XX-Net/wiki
After=network.target remote-fs.target

[Service]
Type=simple
ExecStart=%{_bindir}/python2 %{_datadir}/%{name}/launcher/start.py
# Send SIGINT for graceful stop
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
EOF

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE.txt
%attr(0755,-,-) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
* Mon Feb 29 2016 mosquito <sensor.wen@gmail.com> - 2.9.1-1.git262bc73
- Release 2.9.1
- Use user home to save config file
* Mon Jan 25 2016 mosquito <sensor.wen@gmail.com> - 2.8.10-1.git84585b1
- Initial build
