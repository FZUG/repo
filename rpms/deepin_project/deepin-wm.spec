Name:           deepin-wm
Version:        1.9.30
Release:        1%{?dist}
Summary:        Deepin Window Manager
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-wm
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  intltool
BuildRequires:  gnome-common
BuildRequires:  pkgconfig(clutter-gtk-1.0)
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(granite)
BuildRequires:  pkgconfig(gee-0.8)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(libbamf3)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libcanberra-gtk3)
BuildRequires:  pkgconfig(libdeepin-mutter)
BuildRequires:  pkgconfig(libwnck-3.0)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(vapigen)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xkbfile)
Requires:       deepin-desktop-schemas
Requires:       gnome-desktop
Requires:       libcanberra-gtk3
Requires:       hicolor-icon-theme

%description
Deepin Window Manager

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}

%prep
%setup -q

# fix background path
sed -i 's|default_background.jpg|default.png|' \
    src/Background/BackgroundSource.vala

%build
export CXXFLAGS="$CXXFLAGS -DWNCK_I_KNOW_THIS_IS_UNSTABLE"
./autogen.sh
%configure --disable-schemas-compile
%make_build

%install
%make_install PREFIX="%{_prefix}"

# Remove libtool archives
find %{buildroot} -name '*.la' -delete

%find_lang %{name}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop ||:

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/lib*.so.*
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/vala/vapi/%{name}*

%files devel
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%changelog
* Thu Aug  2 2018 mosquito <sensor.wen@gmail.com> - 1.9.30-1
- Update to 1.9.30

* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 1.9.29-1
- Update to 1.9.29

* Sat Mar 24 2018 mosquito <sensor.wen@gmail.com> - 1.9.24-1
- Update to 1.9.24

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.21-2
- Remove obsolete scriptlets

* Wed Nov 15 2017 mosquito <sensor.wen@gmail.com> - 1.9.21-1
- Update to 1.9.21

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 1.9.17-1
- Update to 1.9.17

* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 1.9.16-1
- Update to 1.9.16

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 1.9.15-1
- Update to 1.9.15

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.9.14-1.git90453e3
- Update to 1.9.14

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.9.12-1.git42cd230
- Update to 1.9.12

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 1.9.5-1.git3d3e077
- Update to 1.9.5

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.9.2-1.git4cb2f7e
- Update to 1.9.2

* Wed Jan 04 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.0-2
- Split the package to main and devel

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.0-1
- Update to version 1.2.0

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.2-1
- Initial package build
