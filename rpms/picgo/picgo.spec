# Note: Npm depends on network. Network should be enabled when building this software.

%global debug_package %{nil}

%global forgeurl https://github.com/Molunerfinn/PicGo

Version: 2.3.0
%forgemeta

Name:    picgo
Release: 1%{?dist}
Summary: A simple & beautiful tool for pictures uploading built by vue-cli-electron-builder.
License: MIT
URL:	 https://molunerfinn.com/PicGo/
Source0: %{forgesource}
Source1: picgo.desktop
Source2: picgo-launcher.sh

Patch0:  picgo-2.3.0-use-electron16.patch
# https://github.com/Molunerfinn/PicGo/commit/ea20d3b9712db21a7aa368833f25b55f12e0acfc
Patch1:  picgo-build-dir.patch

BuildRequires:  clang
BuildRequires:  npm
BuildRequires:  yarnpkg
BuildRequires:  python2

Requires:       electron16

%description
%{summary}.

%prep
%forgeautosetup -p1

%build
yarn
npm run electron:build

%install
install -Dm644 dist_electron/linux-unpacked/resources/app.asar -t %{buildroot}%{_prefix}/lib/picgo/
install -Dm644 build/icons/256x256.png %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/picgo.png
install -Dm644 %{S:1} -t %{buildroot}%{_datadir}/applications/
install -Dm755 %{S:2} %{buildroot}%{_bindir}/picgo

%files
%license    LICENSE
%{_bindir}/picgo
%{_prefix}/lib/picgo/
%{_datadir}/applications/picgo.desktop
%{_datadir}/icons/hicolor/256x256/apps/picgo.png

%changelog
* Thu Mar 10 2022 zhullyb <zhullyb@outlook.com> - 2.3.0-1
- First build.

