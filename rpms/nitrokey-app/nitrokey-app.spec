Name:		nitrokey-app
Version:	0.5.1
Release:	1%{?dist}
Summary:	Nitrokey Configuration tool

Group:		Applications/System
License:	GPLv3
URL:		https://github.com/Nitrokey/nitrokey-app
#Source0:	https://github.com/Nitrokey/nitrokey-app/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source0:	https://github.com/Nitrokey/nitrokey-app/archive/v%{version}.tar.gz
Source1:	https://www.nitrokey.com/sites/default/files/40-nitrokey.rules

BuildRequires:	qt5-qtbase-devel
BuildRequires:	libnotify-devel
BuildRequires:	libappindicator-devel
BuildRequires:	libusb-devel
BuildRequires:	gtk2-devel
BuildRequires:  desktop-file-utils
Requires:	libnotify
Requires:	libusb
Requires:	libappindicator

%description
Nitrokey app, the application to configure Nitrokey.

%prep
%setup -q -n %{name}-%{version}
cp -p %SOURCE1 .

%build
mkdir build
pushd build
%{_qt5_qmake} ../%{name}-qt5.pro
make %{?_smp_mflags}

%install
# install 
install -Dm 0755 build/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 0644 images/CS_icon-red.png %{buildroot}%{_datadir}/icons/%{name}.png
install -D -p -m 644 40-nitrokey.rules %{buildroot}%_udevrulesdir/40-nitrokey.rules

# desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Version=%{version}
Type=Application
Encoding=UTF-8
Name=Nitrokey App
GenericName=Nitrokey App
Comment=A Nitrokey configuration tool written in QT5
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Utility;
EOF

%post
%postun

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/icons/%{name}.png
%{_datadir}/applications/%{name}.desktop
%_udevrulesdir/40-nitrokey.rules

%changelog
* Thu Oct 13 2016 Zamir SUN <zsun@fedoraproject.org> - 0.5.1-1
- Initial nitrokey-app
