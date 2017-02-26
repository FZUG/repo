%global _commit 383423198028b3c31dd719663f6119240c229587
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-mutter
Version:        3.20.11
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Base window manager for deepin, fork of gnome mutter
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-mutter
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  intltool
BuildRequires:  gnome-common
BuildRequires:  gnome-doc-utils
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  gtk3-devel
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  gnome-desktop3-devel
BuildRequires:  clutter-devel
BuildRequires:  upower-devel
BuildRequires:  libxkbfile-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  xkeyboard-config-devel
BuildRequires:  libgudev-devel
BuildRequires:  zenity
BuildRequires:  deepin-cogl-devel
BuildRequires:  desktop-file-utils
Requires:       dconf
Requires:       deepin-desktop-schemas
Requires:       zenity
#libcanberra
#startup-notification

%description
Base window manager for deepin, fork of gnome mutter

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for base window manager for deepin, fork of gnome mutter

%prep
%setup -q -n %{name}-%{_commit}

%build
./autogen.sh
%configure \
    --libexecdir=%{_libexecdir}/%{name} \
    --enable-gtk-doc \
    --enable-wayland \
    --enable-native-backend \
    --disable-static \
    --disable-schemas-compile \
    --enable-compile-warnings=minimum
%make_build

%install
%make_install PREFIX=%{_prefix}

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang %{name}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post -p /sbin/ldconfig

%postun
/sbin/ldconfig
if [ $1 -eq 0 ]; then
    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null ||:
fi

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &> /dev/null ||:

%files -f %{name}.lang
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_libdir}/%{name}/
%{_libexecdir}/%{name}/mutter-restart-helper
%{_datadir}/GConf/gsettings/%{name}-schemas.convert
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/gnome-control-center/keybindings/50-%{name}-*.xml
%{_mandir}/man1/%{name}.1.gz

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/lib%{name}.so

%changelog
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.20.11-1.git3834231
- Update to 3.20.11
* Sat Jan 21 2017 mosquito <sensor.wen@gmail.com> - 3.20.8-1.git3c2a807
- Update to 3.20.8
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.20.7-1.gitc86611b
- Update to 3.20.7
* Fri Dec 16 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.6-1
- Update to version 3.20.6
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.5-1
- Initial package build
