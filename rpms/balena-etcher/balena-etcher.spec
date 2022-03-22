# Note: Npm depends on network. Network should be enabled when building this software.

%global debug_package %{nil}

Name:           balena-etcher
Version:        1.7.8
Release:        1%{?dist}
Summary:        Flash OS images to SD cards & USB drives, safely and easily.
License:        ASL 2.0
Url:            https://github.com/balena-io/etcher
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        balena-etcher-electron.sh
Source2:        balena-etcher-electron.desktop
BuildRequires:  clang
BuildRequires:  nodejs
BuildRequires:  npm

Requires:       electron12
Requires:       libusb

AutoReqProv: no

%description
%{summary}.

%prep
%autosetup -n etcher-%{version}

%build
npm ci
npm run webpack
npm prune --production

%install
%define _appdir %{buildroot}%{_prefix}/lib/balena-etcher

install -d "%{_appdir}"

install package.json "%{_appdir}"
cp -a {lib,generated,node_modules} "%{_appdir}"
install -D assets/icon.png "%{_appdir}/assets/icon.png"
install -D lib/gui/app/index.html "%{_appdir}/lib/gui/app/index.html"

install -Dm755 %{S:1} "%{buildroot}%{_bindir}/balena-etcher-electron"
install -Dm644 %{S:2} "%{buildroot}%{_datadir}/applications/balena-etcher-electron.desktop"

for size in 16x16 32x32 48x48 128x128 256x256 512x512; do
  install -Dm644 "assets/iconset/${size}.png" "%{buildroot}%{_datadir}/icons/hicolor/${size}/apps/balena-etcher-electron.png"
done

%files
%{_bindir}/balena-etcher-electron
%{_prefix}/lib/balena-etcher
%{_datadir}/applications/balena-etcher-electron.desktop
%{_datadir}/icons/hicolor/*/apps/balena-etcher-electron.png

%changelog
* Fri Mar 18 2022 zhullyb <zhullyb@outlook.com> - 1.7.8-1
- new version

* Tue Feb 22 2022 zhullyb <zhullyb@outlook.com> - 1.7.7-1
- new version

* Mon Feb 21 2022 zhullyb <zhullyb@outlook.com> - 1.7.6-1
- new version

* Mon Feb 21 2022 zhullyb <zhullyb@outlook.com> - 1.7.5-1
- First build


