%global _icondir %{_datadir}/icons/hicolor

Name:		nitrokey-app
Version:	0.5.1
Release:	1%{?dist}
Summary:	Nitrokey Configuration tool

Group:		Applications/System
License:	GPLv3
URL:		https://github.com/Nitrokey/nitrokey-app
#Source0:	%{url}/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source0:	%{url}/archive/v%{version}.tar.gz

BuildRequires:	qt5-qtbase-devel
BuildRequires:	libnotify-devel
BuildRequires:	libappindicator-devel
BuildRequires:	libusb-devel
BuildRequires:	gtk2-devel
BuildRequires:  desktop-file-utils
BuildRequires:	gtk-update-icon-cache

%description
Nitrokey app, the application to configure Nitrokey Pro and Nitrokey Storage.

%prep
%setup -q -n %{name}-%{version}

%build
%{qmake_qt5} %{name}-qt5.pro
%make_build

%install
# install 
install -Dm 0755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dm0644 data/40-nitrokey.rules %{buildroot}%{_udevrulesdir}/40-nitrokey.rules
install -Dm0644 data/bash-autocomplete/%{name} %{buildroot}%{_datadir}/bash-completion/completions/%{name}

# icon files
install -Dm0644 data/%{name}-small.xpm    %{buildroot}%{_datadir}/pixmaps/%{name}-small.xpm
pushd data/icons/hicolor
install -Dm0644 48x48/apps/%{name}.png    %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -Dm0644 scalable/apps/%{name}.svg %{buildroot}%{_icondir}/scalable/apps/%{name}.svg
for size in 128x128 48x48 32x32; do
install -Dm0644 ${size}/apps/%{name}.png  %{buildroot}%{_icondir}/${size}/apps/%{name}.png
done
popd

# desktop file
install -d %{buildroot}%{_datadir}/applications
desktop-file-install --delete-original --dir=%{buildroot}%{_datadir}/applications data/nitrokey-app.desktop
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/pixmaps/%{name}*
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/bash-completion/completions/%{name}
%{_udevrulesdir}/40-nitrokey.rules

%changelog
* Thu Oct 13 2016 Zamir SUN <zsun@fedoraproject.org> - 0.5.1-1
- Initial nitrokey-app
