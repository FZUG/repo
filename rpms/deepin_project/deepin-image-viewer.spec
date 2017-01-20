%global _commit 933325f50aeb99d2c625db25eba9106f6ba4b7d7
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-image-viewer
Version:        1.2.0
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Image Viewer
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-image-viewer
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

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
%setup -q -n %{name}-%{_commit}
sed -i 's|lrelease|lrelease-qt5|g' viewer/generate_translations.sh
sed -i 's|<exif-data.h|<libexif/exif-data.h|' viewer/utils/imageutils_libexif.h

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
%{_bindir}/%{name}
%{_qt5_plugindir}/imageformats/*.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/services/*.service
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/icons/deepin/apps/scalable/%{name}.svg
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.2.0-1.git933325f
- Update to 1.2.0
* Fri Jan 06 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.3-2
- Fixed build dependecies
* Sat Dec 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.3-1
- Initial package build
