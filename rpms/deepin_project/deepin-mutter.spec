Name:           deepin-mutter
Version:        3.20.21
Release:        1%{?dist}
Summary:        Base window manager for deepin, fork of gnome mutter
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-mutter
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  intltool
BuildRequires:  desktop-file-utils
BuildRequires:  gnome-common
%if 0%{?fedora} > 26
BuildRequires:  cogl-devel >= 1.22.2-7
%else
BuildRequires:  deepin-cogl-devel
%endif
BuildRequires:  pkgconfig(clutter-1.0)
BuildRequires:  pkgconfig(clutter-wayland-1.0)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gsettings-desktop-schemas)
BuildRequires:  pkgconfig(gnome-doc-utils)
BuildRequires:  pkgconfig(gnome-desktop-3.0)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(libcanberra-gtk)
BuildRequires:  pkgconfig(libstartup-notification-1.0)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(upower-glib)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xkeyboard-config)
BuildRequires:  zenity
Requires:       dconf
Requires:       deepin-desktop-schemas
Requires:       zenity

%description
Base window manager for deepin, fork of gnome mutter.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for base window manager for deepin,
fork of gnome mutter.

%prep
%setup -q

# Starting from GLib 2.49, the gdbus-codegen tool automatically generates
# the auto cleanup symbols for the GDBus proxy and skeleton interfaces.
# https://github.com/GNOME/mutter/commit/aeda556
%if 0%{?fedora} > 26
sed -i '/G_DEFINE_AUTOPTR_CLEANUP_FUNC.*GUdev/d' src/backends/native/meta-launcher.c
%endif

# Fix fsf address
find -type f -print0 | xargs -0 sed -i \
  's|59 Temple Place - Suite 330|51 Franklin Street, Fifth Floor|; s|02111-1307|02110-1301|'

%build
# https://github.com/linuxdeepin/deepin-mutter/issues/1
export CFLAGS="%optflags -std=gnu99"
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

# Remove libtool archives
find %{buildroot} -name '*.la' -delete

%find_lang %{name}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/lib%{name}.so.*
%{_libdir}/%{name}/
%exclude %{_libdir}/%{name}/Meta-3.0.gir
%{_libexecdir}/%{name}/mutter-restart-helper
%{_datadir}/GConf/gsettings/%{name}-schemas.convert
%{_datadir}/applications/%{name}.desktop
%{_datadir}/glib-2.0/schemas/*.xml
%{_datadir}/gnome-control-center/keybindings/50-%{name}-*.xml
%{_mandir}/man1/%{name}.1.gz

%files devel
%{_includedir}/%{name}/
%{_libdir}/%{name}/Meta-3.0.gir
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/lib%{name}.so

%changelog
* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 3.20.21-1
- Update to 3.20.21

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.20.20-1.git0b40582
- Update to 3.20.20

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.20.17-1.git6b2b181
- Update to 3.20.17

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
