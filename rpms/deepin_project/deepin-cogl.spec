Name:           deepin-cogl
Version:        1.22.5
Release:        2%{?dist}
Summary:        An object oriented GL/GLES Abstraction/Utility Layer for Deepin
License:        GPLv2
URL:            https://github.com/linuxdeepin/deepin-cogl
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  intltool libtool
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(xrandr)
BuildRequires:  pkgconfig(xcomposite)
BuildRequires:  pkgconfig(xdamage)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
Provides:       cogl%{?_isa} = %{version}-%{release}

%description
An object oriented GL/GLES Abstraction/Utility Layer for Deepin.

%package devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Provides:       cogl-devel = %{version}-%{release}

%description devel
Header files and libraries for building and developing apps with %{name}.

%prep
%setup -q
NOCONFIGURE=1 ./autogen.sh

%build
%configure --prefix=%{_prefix} \
    --enable-gles2 \
    --enable-{kms,wayland}-egl-platform \
    --enable-wayland-egl-server

# https://bugzilla.gnome.org/show_bug.cgi?id=655517
sed -i -e 's| -shared | -Wl,-O1,--as-needed\0|g' libtool
make -j1

%install
%make_install

#Remove libtool archives
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc NEWS README ChangeLog
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/Cogl*.typelib

%files devel
%{_libdir}/*.so
%{_includedir}/cogl/
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Cogl*.gir
%{_datadir}/cogl/
%{_datadir}/locale/

%changelog
* Thu Aug 31 2017 mosquito <sensor.wen@gmail.com> - 1.22.5-2
- Rewrite dependencies

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.22.5-1
- Update to 1.22.5

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.22.3-1.git9ee8ef2
- Update to 1.22.3

* Sat Dec 17 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.22.3-3
- Redone package in a newer format

* Sat Dec 17 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.22.3-2
- Added conflict and obsolete for cogl library

* Fri Dec 16 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.22.3-1
- Initial package build
