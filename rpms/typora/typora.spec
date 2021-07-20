%global debug_package %{nil}
Name:           typora
Version:        0.10.11
Release:        1%{?dist}
Summary:        a minimal Markdown reading & writing app
License:        EULA
Url:            https://typora.io
Source0:        https://typora.io/linux/typora_%{version}_amd64.deb
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
%description
A minimal Markdown reading & writing app.

%prep
ar x %{SOURCE0}
tar -xf data.tar.xz

%build

%install
cp -R usr %{buildroot}
rm -rf %{buildroot}%{_datadir}/lintian

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%files
%license %{_docdir}/typora/copyright
%{_bindir}/typora
%{_datadir}/applications/%{name}.desktop

%dir %{_datadir}/icons/hicolor
%dir %{_datadir}/icons/hicolor/*
%dir %{_datadir}/icons/hicolor/*/apps
%{_datadir}/icons/hicolor/*/apps/*

%dir %{_datadir}/typora
%{_datadir}/typora/*

%changelog
* Sun Jul 18 2021 Liu Sen <liusen@disroot.org> - 0.10.11-1
- First release
