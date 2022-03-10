Name:           nodejs-electron16-bin
Version:        16.1.0
Release:        1%{?dist}
Summary:        Build cross-platform desktop apps with JavaScript, HTML, and CSS
License:        MIT
Url:            https://github.com/electron/electron
Source0:        %{url}/releases/download/v%{version}/electron-v%{version}-linux-x64.zip
Source1:        electron16-launcher.sh
Source2:        https://raw.githubusercontent.com/electron/electron/main/LICENSE

BuildRequires:  bsdtar

Provides:       nodejs-electron16 = %{version}
Provides:       electron16 = %{version}
AutoReqProv: no

%description
Build cross-platform desktop apps with JavaScript, HTML, and CSS

%prep
install -Dm644 %{S:2} %{_builddir}/

%build

%install
install -dm755 "%{buildroot}%{_prefix}/lib/electron16"
bsdtar -xf %{S:0} -C "%{buildroot}%{_prefix}/lib/electron16"
chmod u+s "%{buildroot}%{_prefix}/lib/electron16/chrome-sandbox"
install -Dm755 %{S:1} "%{buildroot}%{_bindir}/electron16"

%files
%license LICENSE
%{_bindir}/electron16
%{_prefix}/lib/electron16/

%changelog
* Wed Mar 09 2022 zhullyb <zhullyb@outlook.com> - 16.1.0-1
- First Build


