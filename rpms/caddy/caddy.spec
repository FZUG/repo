%global debug_package %{nil}
%global _commit       94e382ef0a88f610a3962eefdde355b591f3eac9
%global _shortcommit  %(c=%{_commit}; echo ${c:0:7})
%global gopkgname     github.com/mholt/caddy
%global with_systemd  1

%global caddy_user    caddy
%global caddy_group   %{caddy_user}
%global caddy_home    %{_localstatedir}/lib/caddy
%global caddy_logdir  %{_localstatedir}/log/caddy
%global caddy_confdir %{_sysconfdir}/caddy
%global caddy_datadir %{_datadir}/caddy
%global caddy_webroot %{caddy_datadir}/html

Name:           caddy
Version:        0.9.5
Release:        1.git%{_shortcommit}%{?dist}
Summary:        A configurable, general-purpose HTTP/2 web server for any platform
License:        Apache 2.0
URL:            https://github.com/mholt/caddy
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz
Source1:        Caddyfile.conf
Patch0:         systemd-unit-file.patch
Patch1:         build-script.patch

BuildRequires:  git
BuildRequires:  golang
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

%description
Caddy is a general-purpose web server for Windows, Mac, Linux, BSD, and
Android. It is a capable but easier alternative to other popular web servers.

Please see https://caddyserver.com/docs for more information.

%prep
%setup -q -n %{name}-%{_commit}
%patch0 -p1
%patch1 -p1

export GOPATH="$(pwd)/build"
mkdir -p ${GOPATH}/src/%{gopkgname}
cp -r * ${GOPATH}/src/%{gopkgname} || :

# Download dependencies
go get -d %{gopkgname}/...

%build
export GOPATH="$(pwd)/build"
pushd ${GOPATH}/src/%{gopkgname}/caddy
sed -i 's|<gitTag>|v%{version}|;s|<gitCommit>|%{_shortcommit}|' build.bash
bash build.bash

%install
builddir="build/src/%{gopkgname}"
install -Dm755 ${builddir}/caddy/caddy %{buildroot}%{_bindir}/caddy
install -Dm644 %{S:1} %{buildroot}%{caddy_confdir}/Caddyfile
install -Dm644 dist/init/linux-systemd/caddy.service %{buildroot}%{_unitdir}/caddy.service

install -dm770 %{buildroot}/etc/ssl/%{name}
install -dm755 %{buildroot}%{caddy_logdir}
install -dm755 %{buildroot}%{caddy_home}

install -dm755 %{buildroot}%{caddy_webroot}
cat > %{buildroot}%{caddy_webroot}/index.html <<EOF
Hello, Caddy.
EOF

%pre
getent group %{caddy_group} &>/dev/null || groupadd -r -g 33 %{caddy_group}
getent passwd %{caddy_user} &>/dev/null || useradd --system --uid 33 \
    --gid %{caddy_group} --no-user-group \
    --home-dir %{caddy_home} --no-create-home \
    --shell /sbin/nologin \
    --comment "Caddy web server" %{caddy_user}

%post
%if 0%{?with_systemd}
%systemd_post %{name}.service
%endif
if [ $1 -ge 1 ]; then
  chown %{name}:root /etc/ssl/%{name}
  chown %{name}:root %{caddy_logdir}
  chown %{name}:root %{caddy_home}
fi

%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun_with_restart %{name}.service
%endif

%files
%doc README.md
%license LICENSE.txt
# bind to privileged ports (e.g. 80, 443) as a non-root user
%caps(cap_net_bind_service=+ep) %{_bindir}/%{name}
%{_sysconfdir}/%{name}/
%{_sysconfdir}/ssl/%{name}/
%{_localstatedir}/lib/%{name}/
%{_localstatedir}/log/%{name}/
%{_datadir}/%{name}/
%{_unitdir}/%{name}.service

%changelog
* Tue Feb 21 2017 mosquito <sensor.wen@gmail.com> - 0.9.5-1.git94e382e
- Initial build
