%global __strip_shared %(test $(rpm -E%?fedora) -eq 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "amd64" || echo "386")
%global debug_package %{nil}
%global project lantern
%global repo %{project}

# commit
%global _commit fdff338235569a69d2120717247439ecc7f774c3
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})
# git show -s --format=%ci "%%{_shortcommit}"
%global _revision_date 2016-01-29 12:04:37 -0800
%global _build_date %(date -u '+%Y%m%d.%H%M%%S')

%global systemd_user_post() \
if [ $1 -eq 1 ] ; then\
    # Initial installation\
    systemctl preset --user --global %* >/dev/null 2>&1 || :\
fi\
%{nil}

# headless mode: it doesn't depend on the systray support libraries,
# and will not show systray or UI.
%global with_headless 0

Name:    lantern
Version: 2.0.11
Release: 1.git%{_shortcommit}%{?dist}
Summary: fast, reliable and secure access to the open Internet
Summary(zh_CN): 快速, 可靠, 安全的访问互联网的代理软件

Group:   Applications/Internet
License: Apache 2.0
URL:     https://getlantern.org
Source0: https://github.com/getlantern/lantern/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: systemd
BuildRequires: golang-bin
BuildRequires: gtk3-devel
BuildRequires: libappindicator-gtk3-devel
%{systemd_requires}

%description
Lantern is a free desktop application that delivers fast,
reliable and secure access to the open Internet. (Headless Version)

%description -l zh_CN
Lantern 是一个免费的代理程序, 可以快速、可靠、安全地访问互联网.
它采用多种技术来保持畅通, 包括 P2P 和 domain fronting.

%prep
%setup -q -n %repo-%{_commit}

%build
source ./setenv.bash

build_tags='prod'
%if 0%{?with_headless}
build_tags+=' headless'
%endif
sed -e '/packageVersion/s|=.*|= "%{version}"|' -e 's|!prod|prod|' \
    src/github.com/getlantern/flashlight/autoupdate.go > \
    src/github.com/getlantern/flashlight/autoupdate-prod.go

logger_token=$(sed -n '/^LOGGLY_TOKEN /s|.*=[[:space:]]\(.*\)$|\1|p' Makefile)
ldflags="-w -X \"main.version=%{_shortcommit}\" \
    -X \"main.revisionDate=%{_revision_date}\" \
    -X \"main.buildDate=%{_build_date}\" \
    -X \"github.com/getlantern/flashlight/logging.logglyToken=${logger_token}\""

CGO_ENABLED=1 GOOS=linux GOARCH=%{arch} \
go build -o %{name}_linux_%{arch} -tags="$build_tags" \
    -ldflags="${ldflags} -linkmode internal -extldflags \"-static\"" \
    github.com/getlantern/flashlight

%install
# These comments come from deb.
installer_resources='./installer-resources/linux'
#packaged_yaml='.packaged-lantern.yaml'
#packaged_settings='startupurl:'

#install -Dm644 %{name}_linux_%{arch} %{buildroot}%{_libdir}/%{name}/%{name}-binary
#install -Dm755 ${installer_resources}/%{name}.sh %{buildroot}%{_libdir}/%{name}
#echo "$packaged_settings" > %{buildroot}%{_libdir}/%{name}/${packaged_yaml}
#touch %{buildroot}%{_libdir}/%{name}/%{name}.yaml
#ln -sfv %{_libdir}/%{name}/%{name}.sh %{buildroot}%{_bindir}/%{name}
install -Dm755 %{name}_linux_%{arch} %{buildroot}%{_bindir}/%{name}

# systemd service file
install -d %{buildroot}%{_userunitdir}
cat > %{buildroot}%{_userunitdir}/%{name}.service <<EOF
[Unit]
Description=Lantern
After=network.target

[Service]
ExecStart=%{_bindir}/%{name}

[Install]
WantedBy=default.target
EOF

# desktop and icon files
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=%{name}
Exec=%{name}
Icon=%{name}
EOF

install -Dm644 ${installer_resources}/icon*.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# stripe shared files
%{__strip_shared}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc README.md
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_userunitdir}/%{name}.service

%changelog
* Thu Feb  4 2016 mosquito <sensor.wen@gmail.com> - 2.0.11-1.gitfdff338
- Initial build
