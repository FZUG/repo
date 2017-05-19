%global _commit 1e1e1b8a97ecfc07de37e3f2646290d5c38be34f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-cogl
Version:        1.22.5
Release:        1.git%{_shortcommit}%{?dist}
Summary:        An object oriented GL/GLES Abstraction/Utility Layer for Deepin
License:        GPLv2
URL:            https://github.com/linuxdeepin/deepin-cogl
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  intltool libtool
BuildRequires:  glib2-devel gtk-doc
BuildRequires:  mesa-libGLES-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libgbm-devel
BuildRequires:  mesa-libwayland-egl-devel
BuildRequires:  libwayland-client-devel
BuildRequires:  libwayland-server-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXfixes-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  cairo-devel
BuildRequires:  pango-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  gobject-introspection-devel

Provides:       cogl%{?_isa} = %{version}-%{release}
Obsoletes:      cogl%{?_isa} < %{version}-%{release}
Conflicts:      cogl%{?_isa} < %{version}-%{release}

%description
An object oriented GL/GLES Abstraction/Utility Layer for Deepin

%package devel
Summary:        Header and development files
Requires:       %{name} = %{version}-%{release}
Provides:       cogl-devel = %{version}-%{release}
Obsoletes:      cogl-devel < %{version}-%{release}

%description devel
Header files and libraries for building and developing apps with %{name}.

%prep
%setup -q -n %{name}-%{_commit}
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
%defattr(-,root,root)
%doc COPYING NEWS README ChangeLog
%{_libdir}/*.so.*
%{_libdir}/girepository-1.0/Cogl*.typelib

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/cogl/
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gir-1.0/Cogl*.gir
%{_datadir}/cogl/
%{_datadir}/locale/

%changelog
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.22.5-1.git1e1e1b8
- Update to 1.22.5
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.22.3-1.git9ee8ef2
- Update to 1.22.3
* Sat Dec 17 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.22.3-3
- Redone package in a newer format
* Sat Dec 17 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.22.3-2
- Added conflict and obsolete for cogl library
* Fri Dec 16 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.22.3-1
- Initial package build
