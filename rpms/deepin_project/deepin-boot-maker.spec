Name:           deepin-boot-maker
Version:        2.0.3.1
Release:        1%{?dist}
Summary:        Tool to create a bootable usb stick quick and easy
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-boot-maker
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python3
BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(dtkwidget) = 2.0
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme
Requires:       p7zip-plugins
Requires:       syslinux-nonlinux
Provides:       bundled(libxsys)

%description
Deepin Boot Maker is help for user to create a boot usb stick
quick and easy, it designed to support only deepin install iso,
but it can can work for all ubuntu live install iso too.

%prep
%setup -q
sed -i 's|lrelease|lrelease-qt5|' src/tools/translate_generation.py
sed -i 's|lib|libexec|' src/service/data/com.deepin.bootmaker.service src/service/service.pro
sed -i '/paths;/apaths.push_back("%{_datadir}/syslinux/"); //fedora' \
  src/vendor/src/libxsys/DiskUtil/Syslinux.cpp

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop ||:

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libexecdir}/deepin-daemon/%{name}-service
%{_datadir}/dman/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/dbus-1/system-services/com.deepin.bootmaker.service
%{_datadir}/dbus-1/system.d/com.deepin.bootmaker.conf

%changelog
* Thu Aug 31 2017 mosquito <sensor.wen@gmail.com> - 2.0.3.1-1
- Update to 2.0.3.1

* Thu Aug 31 2017 mosquito <sensor.wen@gmail.com> - 2.0.3-1
- Initial package build
