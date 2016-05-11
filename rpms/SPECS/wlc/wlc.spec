Name:           wlc
Version:        0.0.2
Release:        1%{?dist}
Summary:        Wayland compositor library
Group:          User Interface/X
License:        MIT
URL:            https://github.com/Cloudef/wlc
Source0:        https://github.com/Cloudef/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(x11-xcb)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-xkb)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(chck)
BuildRequires:  pkgconfig(wayland-protocols)

%description
Wlc is a library for creating Wayland compositors.

%package devel
Summary:        Wayland compositor library development files
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains files useful for software development with wlc,
a Wayland compositor library.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%check
ctest -V %{?_smp_mflags}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%doc README.rst
%{_libdir}/libwlc.so.*

%files devel
%doc CONTRIBUTING.rst
%{_includedir}/wlc/*.h
%{_libdir}/libwlc.so
%{_libdir}/pkgconfig/wlc.pc

%changelog
* Thu May 09 2016 nrechn <neil@gyz.io> - 0.0.2-1
- Initial packaging
