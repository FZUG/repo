Name:           deepin-picker
Version:        1.6.1
Release:        1%{?dist}
Summary:        Color picker tool for deepin
License:        GPLv3
Url:            https://github.com/linuxdeepin/deepin-picker
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(dtkwidget) >= 2.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
Requires:       hicolor-icon-theme

%description
Simplest color picker.

%prep
%setup -q
sed -i 's|=lupdate|=lupdate-qt5|;s|=lrelease|=lrelease-qt5|' %{name}.pro
sed -i 's|Picker;||' %{name}.desktop

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/dbus-1/services/com.deepin.Picker.service

%changelog
* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 1.6.1-1
- Update to 1.6.1

* Mon Oct 23 2017 mosquito <sensor.wen@gmail.com> - 1.1-1
- Update to 1.1

* Tue Oct 17 2017 mosquito <sensor.wen@gmail.com> - 1.0-1
- Update to 1.0

* Fri Oct 13 2017 mosquito <sensor.wen@gmail.com> - 0.4-1
- Initial package
