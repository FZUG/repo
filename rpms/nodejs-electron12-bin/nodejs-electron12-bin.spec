Name:           nodejs-electron12-bin
Version:        12.2.3
Release:        1%{?dist}
Summary:        Build cross-platform desktop apps with JavaScript, HTML, and CSS
License:        MIT
Url:            https://github.com/electron/electron
Source0:        %{url}/releases/download/v%{version}/electron-v%{version}-linux-x64.zip
Source1:        electron12-launcher.sh
Source2:        https://raw.githubusercontent.com/electron/electron/main/LICENSE

BuildRequires:  bsdtar

Provides:       nodejs-electron12 = %{version}
Provides:       electron12 = %{version}
AutoReqProv: no

%description
Build cross-platform desktop apps with JavaScript, HTML, and CSS

%prep
install -Dm644 %{S:2} %{_builddir}/

%build

%install
install -dm755 "%{buildroot}%{_prefix}/lib/electron12"
bsdtar -xf %{S:0} -C "%{buildroot}%{_prefix}/lib/electron12"
chmod u+s "%{buildroot}%{_prefix}/lib/electron12/chrome-sandbox"
install -Dm755 %{S:1} "%{buildroot}%{_bindir}/electron12"

%files
%license LICENSE
%{_bindir}/electron12
%{_prefix}/lib/electron12/

%changelog
* Sat Mar 05 2022 zhullyb <zhullyb@outlook.com> - 12.2.3-1
- First Build


