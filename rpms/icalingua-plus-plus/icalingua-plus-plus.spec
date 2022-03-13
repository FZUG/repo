# Note: Npm depends on network. Network should be enabled when building this software.

%global debug_package %{nil}

Name:           icalingua-plus-plus
Version:        2.5.5
Release:        1%{?dist}
Summary:        A Linux client for QQ and more
License:        AGPL 3.0
Url:            https://github.com/Icalingua-plus-plus/Icalingua-plus-plus
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz
Source1:        icalingua-launcher.sh
Source2:        icalingua-plus-plus.desktop
Patch0:         icalingua-build-production.patch

Requires:       electron13
BuildRequires:  nodejs
BuildRequires:  clang
BuildRequires:  yarnpkg
BuildRequires:  python

%description
%{summary}.

%prep
%setup -q -n Icalingua-plus-plus-%{version}
%patch0

%build
yarn config set registry https://registry.npmmirror.com
export SASS_BINARY_SITE=https://npmmirror.com/mirrors/node-sass/
export ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
cd icalingua
yarn
yarn build:ci
yarn build:electron --dir -c.extraMetadata.version=%{version}

%install
install -Dm755 %{S:1} %{buildroot}%{_bindir}/icalingua++
install -Dm644 icalingua/build/linux-unpacked/resources/app.asar -t %{buildroot}%{_prefix}/lib/icalingua-plus-plus/
cd pkgres
install -Dm644 512x512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/icalingua-plus-plus.png
install -Dm644 %{S:2} %{buildroot}%{_datadir}/applications/icalingua-plus-plus.desktop

%files
%{_bindir}/icalingua++
%{_prefix}/lib/icalingua-plus-plus/
%{_datadir}/applications/icalingua-plus-plus.desktop
%{_datadir}/icons/hicolor/512x512/apps/icalingua-plus-plus.png

%changelog
* Wed Mar 09 2022 zhullyb <zhullyb@outlook.com> - 2.5.5-1
- First build.


