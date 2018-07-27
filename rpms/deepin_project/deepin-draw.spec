Name:           deepin-draw
Version:        1.0.0
Release:        1%{?dist}
Summary:        A lightweight drawing tool for Linux Deepin
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-draw
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  freeimage-devel
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(dtkwm)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(xcb-aux)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  qt5-linguist
Requires:       deepin-notifications
Requires:       deepin-qt5integration

%description
A lightweight drawing tool for Linux Deepin.

%prep
%setup -q
sed -i 's|lrelease|lrelease-qt5|' generate_translations.sh

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop ||:

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/translations/%{name}*.qm
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/com.deepin.Draw.service
%{_datadir}/icons/deepin/apps/scalable/%{name}.svg
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/x-ddf.xml

%changelog
* Fri Jul 20 2018 mosquito <sensor.wen@gmail.com> - 1.0.0-1
- Initial package build
