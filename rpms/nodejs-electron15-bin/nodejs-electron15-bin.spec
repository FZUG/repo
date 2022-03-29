Name:           nodejs-electron15-bin
Version:        15.5.0
Release:        1%{?dist}
Summary:        Build cross-platform desktop apps with JavaScript, HTML, and CSS
License:        MIT
Url:            https://github.com/electron/electron
Source0:        %{url}/releases/download/v%{version}/electron-v%{version}-linux-x64.zip
Source1:        electron15-launcher.sh
Source2:        https://raw.githubusercontent.com/electron/electron/main/LICENSE

BuildRequires:  bsdtar

Provides:       nodejs-electron15 = %{version}
Provides:       electron15 = %{version}
AutoReqProv: no

%description
Build cross-platform desktop apps with JavaScript, HTML, and CSS

%prep
install -Dm644 %{S:2} %{_builddir}/

%build

%install
install -dm755 "%{buildroot}%{_prefix}/lib/electron15"
bsdtar -xf %{S:0} -C "%{buildroot}%{_prefix}/lib/electron15"
chmod u+s "%{buildroot}%{_prefix}/lib/electron15/chrome-sandbox"
install -Dm755 %{S:1} "%{buildroot}%{_bindir}/electron15"

%files
%license LICENSE
%{_bindir}/electron15
%{_prefix}/lib/electron15/

%changelog
* Tue Mar 29 2022 zhullyb <zhullyb@outlook.com> - 15.5.0-1
- new version

* Wed Mar 23 2022 zhullyb <zhullyb@outlook.com> - 15.4.2-1
- new version

* Tue Mar 22 2022 zhullyb <zhullyb@outlook.com> - 15.4.0-1
- First Build


