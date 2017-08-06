Name:           deepin-metacity
Version:        3.22.10
Release:        1%{?dist}
Summary:        2D window manager for Deepin
License:        GPLv2+
URL:            https://github.com/linuxdeepin/deepin-metacity
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  libtool
BuildRequires:  yelp-tools
BuildRequires:  autoconf-archive
BuildRequires:  bamf-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  json-glib-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libgtop2-devel
BuildRequires:  startup-notification-devel
BuildRequires:  zenity
Requires:       dconf
Requires:       deepin-desktop-schemas
Requires:       control-center-filesystem

%description
2D window manager for Deepin.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q

%build
./autogen.sh
%configure \
    --disable-static \
    --disable-schemas-compile
%make_build

%install
%make_install PREFIX=%{_prefix}
# Remove libtool archives
find %{buildroot} -name '*.la' -delete

%find_lang %{name}

%check
desktop-file-validate %{_datadir}/gnome/applications/%{name}.desktop \
  %{_datadir}/gnome/wm-properties/%{name}-wm.desktop

%post
/sbin/ldconfig
/usr/bin/update-desktop-database -q ||:

%postun
/sbin/ldconfig
/usr/bin/update-desktop-database -q ||:
if [ $1 -eq 0 ]; then
    /usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas &>/dev/null ||:
fi

%posttrans
/usr/bin/glib-compile-schemas /usr/share/glib-2.0/schemas &>/dev/null ||:

%files -f %{name}.lang
%doc README
%license COPYING
%{_bindir}/%{name}*
%{_libdir}/lib%{name}*.so.*
%dir %{_datadir}/GConf/
%dir %{_datadir}/GConf/gsettings/
%{_datadir}/GConf/gsettings/%{name}-schemas.convert
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/glib-2.0/schemas/com.deepin.*.xml
%{_datadir}/gnome-control-center/keybindings/50-%{name}-*.xml
%{_datadir}/gnome/wm-properties/%{name}-wm.desktop
%{_datadir}/help/
%{_datadir}/themes/
%{_mandir}/man1/%{name}*

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/lib%{name}*.pc
%{_libdir}/lib%{name}*.so

%changelog
* Sat Aug  5 2017 mosquito <sensor.wen@gmail.com> - 3.22.10-1
- Fix license

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.22.10-1.gite9af397
- Update to 3.22.10

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.22.8-1.gitcb3e4c5
- Update to 3.22.8

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.22.3-1.git4a90335
- Update to 3.22.3

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.22.0-1.gitb633b85
- Update to 3.22.0

* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 3.22.0-1
- Update to version 3.22.0

* Thu Jan 05 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.6-2
- Split the package to main and devel

* Fri Dec 16 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.6-1
- Update to version 3.20.6

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.5-1
- Initial package build
