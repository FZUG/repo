Name:           nodejs-electron13-bin
Version:        13.6.9
Release:        1%{?dist}
Summary:        Build cross-platform desktop apps with JavaScript, HTML, and CSS
License:        MIT
Url:            https://github.com/electron/electron
Source0:        %{url}/releases/download/v%{version}/electron-v%{version}-linux-x64.zip
Source1:        electron13-launcher.sh
Source2:        https://raw.githubusercontent.com/electron/electron/main/LICENSE

BuildRequires:  bsdtar

Provides:       nodejs-electron13 = %{version}
Provides:       electron13 = %{version}
AutoReqProv: no

%description
Build cross-platform desktop apps with JavaScript, HTML, and CSS

%prep
install -Dm644 %{S:2} %{_builddir}/

%build

%install
install -dm755 "%{buildroot}%{_prefix}/lib/electron13"
bsdtar -xf %{S:0} -C "%{buildroot}%{_prefix}/lib/electron13"
chmod u+s "%{buildroot}%{_prefix}/lib/electron13/chrome-sandbox"
install -Dm755 %{S:1} "%{buildroot}%{_bindir}/electron13"

%files
%license LICENSE
%{_bindir}/electron13
%{_prefix}/lib/electron13/

%changelog
* Wed Mar 09 2022 zhullyb <zhullyb@outlook.com> - 13.6.9-1
- First Build


