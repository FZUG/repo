Name:           nodejs-electron17-bin
Version:        17.2.0
Release:        1%{?dist}
Summary:        Build cross-platform desktop apps with JavaScript, HTML, and CSS
License:        MIT
Url:            https://github.com/electron/electron
Source0:        https://npmmirror.com/mirrors/electron/v%{version}/electron-v%{version}-linux-x64.zip
# You can find original source here: https://github.com/electron/electron/releases
Source1:        electron17-launcher.sh
Source2:        https://raw.githubusercontent.com/electron/electron/main/LICENSE

BuildRequires:  bsdtar

Provides:       nodejs-electron17 = %{version}
Provides:       electron17 = %{version}
AutoReqProv: no

%description
Build cross-platform desktop apps with JavaScript, HTML, and CSS

%prep
install -Dm644 %{S:2} %{_builddir}/

%build

%install
install -dm755 "%{buildroot}%{_prefix}/lib/electron17"
bsdtar -xf %{S:0} -C "%{buildroot}%{_prefix}/lib/electron17"
chmod u+s "%{buildroot}%{_prefix}/lib/electron17/chrome-sandbox"
install -Dm755 %{S:1} "%{buildroot}%{_bindir}/electron17"

%files
%license LICENSE
%{_bindir}/electron17
%{_prefix}/lib/electron17/

%changelog
* Wed Mar 23 2022 zhullyb <zhullyb@outlook.com> - 17.2.0-1
- new version

* Fri Mar 18 2022 zhullyb <zhullyb@outlook.com> - 17.1.1-1
- First Build


