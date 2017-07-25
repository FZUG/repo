Name:           deepin-image-viewer
Version:        1.2.14
Release:        1%{?dist}
Summary:        Deepin Image Viewer
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-image-viewer
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  deepin-tool-kit-devel
BuildRequires:  freeimage-devel
BuildRequires:  LibRaw-devel
BuildRequires:  libexif-devel
BuildRequires:  startup-notification-devel
BuildRequires:  xcb-util-devel

%description
Deepin Image Viewer

%prep
%setup -q
sed -i 's|lrelease|lrelease-qt5|g' viewer/generate_translations.sh

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

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
%{_qt5_plugindir}/imageformats/*.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/icons/deepin/apps/scalable/%{name}.svg
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.2.14-1.gite77fde5
- Update to 1.2.14

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.2.13-1.gita6ac784
- Update to 1.2.13

* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 1.2.4-1.gitfad9c98
- Update to 1.2.4

* Sat Jan 21 2017 mosquito <sensor.wen@gmail.com> - 1.2.1-1.git8378500
- Update to 1.2.1

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.2.0-1.git933325f
- Update to 1.2.0

* Fri Jan 06 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.3-2
- Fixed build dependecies

* Sat Dec 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.3-1
- Initial package build
