Name:           nodejs-electron11-bin
Version:        11.5.0
Release:        1%{?dist}
Summary:        Build cross-platform desktop apps with JavaScript, HTML, and CSS
License:        MIT
Url:            https://github.com/electron/electron
Source0:        https://npmmirror.com/mirrors/electron/v%{version}/electron-v%{version}-linux-x64.zip
# You can find original source here: https://github.com/electron/electron/releases
Source1:        electron11-launcher.sh
Source2:        https://raw.githubusercontent.com/electron/electron/main/LICENSE

BuildRequires:  bsdtar

Provides:       nodejs-electron11 = %{version}
Provides:       electron11 = %{version}
AutoReqProv: no

%description
Build cross-platform desktop apps with JavaScript, HTML, and CSS

%prep
install -Dm644 %{S:2} %{_builddir}/

%build

%install
install -dm755 "%{buildroot}%{_prefix}/lib/electron11"
bsdtar -xf %{S:0} -C "%{buildroot}%{_prefix}/lib/electron11"
chmod u+s "%{buildroot}%{_prefix}/lib/electron11/chrome-sandbox"
install -Dm755 %{S:1} "%{buildroot}%{_bindir}/electron11"

%files
%license LICENSE
%{_bindir}/electron11
%{_prefix}/lib/electron11/

%changelog
* Sun Mar 06 2022 zhullyb <zhullyb@outlook.com> - 11.5.0-1
- First Build


