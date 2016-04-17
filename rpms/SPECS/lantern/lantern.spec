# https://aur.archlinux.org/packages/lantern-headless-git
# https://github.com/getlantern/lantern/blob/valencia/Makefile
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "amd64" || echo "386")
%global debug_package %{nil}
%global project lantern
%global repo %{project}

# commit, git rev-parse --short HEAD
%global _commit 65615be886ed283b67e6681fbf049de548aff1af
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})
# git show -s --format=%ci "%%{_shortcommit}"
%global _revision_date 2016-04-15 16:28:36 -0700
%global _build_date %(date -u '+%Y%m%d.%H%M%%S')
%global go_arch %(go env GOHOSTARCH)
%global go_root %(go env GOROOT)

%global systemd_user_post() \
if [ $1 -eq 1 ] ; then\
    # Initial installation\
    systemctl preset --user --global %* >/dev/null 2>&1 || :\
fi\
%{nil}

# headless mode: it doesn't depend on the systray support libraries,
# and will not show systray or UI.
%global with_headless 0

Name:    golang-github-getlantern-lantern
Version: 2.2.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: fast, reliable and secure access to the open Internet
Summary(zh_CN): 快速, 可靠, 安全的访问互联网的代理软件

Group:   Applications/Internet
License: Apache 2.0
URL:     https://getlantern.org
Source0: https://github.com/getlantern/lantern/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

Provides: %{repo} = %{version}-%{release}
Obsoletes: %{repo} < %{version}-%{release}
BuildRequires: npm
BuildRequires: systemd
BuildRequires: golang-bin
BuildRequires: gtk3-devel
BuildRequires: libappindicator-gtk3-devel
%if 0%{?fedora}
BuildRequires: golang-github-hashicorp-golang-lru-devel
BuildRequires: golang-github-skratchdot-open-golang-devel
BuildRequires: golang-github-davecgh-go-spew-devel
BuildRequires: golang-bitbucket-kardianos-osext-devel
BuildRequires: golang-googlecode-uuid-devel
BuildRequires: golang-github-gorilla-websocket-devel
BuildRequires: golang-gopkg-check-devel
%endif
%{systemd_requires}

%description
Lantern is a free desktop application that delivers fast,
reliable and secure access to the open Internet.

Proxy: tcp://127.0.0.1:8787
WebUI: http://127.0.0.1:16823

%description -l zh_CN
Lantern 是一个免费的代理程序, 可以快速、可靠、安全地访问互联网.
它采用多种技术来保持畅通, 包括 P2P 和 domain fronting.

Proxy: tcp://127.0.0.1:8787
WebUI: http://127.0.0.1:16823

%prep
%setup -q -n %repo-%{_commit}
%if 0%{?fedora}
rm -rf src/github.com/getlantern/pac-cmd/binaries \
    src/gopkg.in/check.v1 \
    src/github.com/hashicorp/golang-lru \
    src/github.com/skratchdot/open-golang/open \
    src/github.com/davecgh/go-spew/spew \
    src/github.com/kardianos/osext \
    src/code.google.com/p/go-uuid/uuid \
    src/github.com/gorilla/websocket
sed -i '/kardianos/s|github.com|bitbucket.org|g' \
    src/github.com/getlantern/go-update/update.go \
    src/github.com/getlantern/go-update/check/check.go \
    src/github.com/getlantern/launcher/launcher_darwin.go \
    src/github.com/getlantern/launcher/launcher_windows.go \
    src/github.com/mitchellh/panicwrap/panicwrap.go
%endif

%build
export GOPATH=`pwd`:%{gopath}

# Build lantern-ui
LANTERN_UI="src/github.com/getlantern/lantern-ui"
APP="$LANTERN_UI/app"
DIST="$LANTERN_UI/dist"
DEST="src/github.com/getlantern/flashlight/ui/resources.go"
echo 'var LANTERN_BUILD_REVISION = "%{_shortcommit}";' > $APP/js/revision.js
pushd $LANTERN_UI
npm install
node_modules/gulp/bin/gulp.js build
popd
go build -a -v -o tarfs github.com/getlantern/tarfs/tarfs
echo -e "// +build !stub\n" > $DEST
./tarfs -pkg ui $DIST >> $DEST

# Build lantern
build_tags='prod'
%if 0%{?with_headless}
build_tags+=' headless'
%endif
loggly_token=$(sed -n '/^LOGGLY_TOKEN /s|.*=[[:space:]]\(.*\)$|\1|p' Makefile)
ldflags="-s -w \
    -X \"github.com/getlantern/flashlight.Version=%{_shortcommit}\" \
    -X \"github.com/getlantern/flashlight.RevisionDate=%{_revision_date}\" \
    -X \"github.com/getlantern/flashlight.BuildDate=%{_build_date}\" \
    -X \"github.com/getlantern/flashlight/logging.logglyToken=${loggly_token}\" \
    -X \"github.com/getlantern/flashlight.compileTimePackageVersion=%{version}\""

CGO_ENABLED=1 GOOS=linux GOARCH=%{arch} \
go build -a -v -o %{repo}_linux_%{arch} -tags="$build_tags" \
    -ldflags="${ldflags} -linkmode internal -extldflags \"-static\"" \
    github.com/getlantern/flashlight/main

%install
installer_resources='./installer-resources/linux'
packaged_yaml='.packaged-lantern.yaml'
packaged_settings='startupurl:'

install -Dm755 %{repo}_linux_%{arch} %{buildroot}%{_libdir}/%{repo}/%{repo}-binary
install -Dm755 ${installer_resources}/%{repo}.sh %{buildroot}%{_libdir}/%{repo}
echo "$packaged_settings" > %{buildroot}%{_libdir}/%{repo}/${packaged_yaml}
touch %{buildroot}%{_libdir}/%{repo}/%{repo}.yaml

install -d %{buildroot}%{_bindir}
ln -sfv %{_libdir}/%{repo}/%{repo}.sh %{buildroot}%{_bindir}/%{repo}
ln -sfv %{_libdir}/%{repo}/%{repo}-binary %{buildroot}%{_bindir}/%{repo}-bin

# systemd service file
install -d %{buildroot}%{_userunitdir}
cat > %{buildroot}%{_userunitdir}/%{repo}.service <<EOF
[Unit]
Description=%{summary}
Documentation=https://github.com/getlantern/lantern
After=network.target

[Service]
Type=simple
ExecStart=%{_bindir}/%{repo} -headless -addr 127.0.0.1:8787
KillSignal=SIGINT

[Install]
WantedBy=multi-user.target
EOF

# desktop and icon files
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{repo}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=%{repo}
Exec=%{repo}
Icon=%{repo}
EOF

install -Dm644 ${installer_resources}/icon*.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{repo}.png

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:
%systemd_user_post %{repo}.service

%preun
%systemd_user_preun %{repo}.service

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
%{_bindir}/%{repo}*
%{_libdir}/%{repo}/
%{_datadir}/applications/%{repo}.desktop
%{_datadir}/icons/hicolor/*/apps/%{repo}.png
%{_userunitdir}/%{repo}.service

%changelog
* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 2.2.0-1.git65615be
- Release 2.2.0
* Tue Mar 22 2016 mosquito <sensor.wen@gmail.com> - 2.1.1-1.gitfd97e0e
- Release 2.1.1
- Remove devel package
* Wed Mar  2 2016 mosquito <sensor.wen@gmail.com> - 2.1.0-3.git273a629
- Do not need to build twice, due to links lantern-ui.
- Remove lantern-ui package
* Mon Feb 29 2016 mosquito <sensor.wen@gmail.com> - 2.1.0-2.git273a629
- Update to 2.1.0-2.git273a629
* Sun Feb 28 2016 mosquito <sensor.wen@gmail.com> - 2.1.0-1.git8166903
- Release 2.1.0
- Do not require lantern-ui, due to static links.
* Fri Feb  5 2016 mosquito <sensor.wen@gmail.com> - 2.0.11-2.gitfdff338
- Add source code subpackage
* Thu Feb  4 2016 mosquito <sensor.wen@gmail.com> - 2.0.11-1.gitfdff338
- Initial build
