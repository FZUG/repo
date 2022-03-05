# Note: Npm depends on network. Network should be enabled when building this software.

%global debug_package %{nil}

Name:           motrix
Version:        1.6.11
Release:        1%{?dist}
Summary:        A full-featured download manager.
License:        MIT
Url:            https://github.com/agalwood/Motrix
Source0:        https://github.com/agalwood/Motrix/archive/refs/tags/v%{version}.tar.gz
Source1:        motrix-launcher.sh
Source2:        motrix.desktop
Source3:        motrix.xml
Patch0:         motrix-1.16.11-npm-deps-fix.patch
# Motrix 1.6.11 can't be built normally, fixed in future version but not tagged yet.
# https://github.com/agalwood/Motrix/commit/7868a4870b9bc485c66174f7bf4b92ed324f5458

BuildRequires:  nodejs
BuildRequires:  npm
BuildRequires:  yarnpkg
Requires:       electron11

%description
A full-featured download manager.

%prep
%autosetup -n Motrix-%{version}

%build
yarn
yarn run build:dir

%install
install -Dm644 release/linux-unpacked/resources/app.asar -t "%{buildroot}%{_prefix}/lib/motrix/"
cp -r release/linux-unpacked/resources/engine "%{buildroot}%{_prefix}/lib/motrix/"
install -Dm644 static/512x512.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/motrix.png
install -Dm755 %{SOURCE1} %{buildroot}%{_bindir}/motrix
install -Dm644 %{SOURCE2} %{buildroot}%{_datadir}/applications/motrix.desktop
install -Dm644 %{SOURCE3} %{buildroot}%{_datadir}/mime/packages/motrix.xml

%files
%{_bindir}/motrix
%{_prefix}/lib/motrix
%{_datadir}/applications/motrix.desktop
%{_datadir}/icons/hicolor/512x512/apps/motrix.png
%{_datadir}/mime/packages/motrix.xml

%changelog
* Sat Mar 05 2022 zhullyb <zhullyb@outlook.com> - 1.6.11-1
- First build.


