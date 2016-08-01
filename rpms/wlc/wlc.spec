%global _with_latest 1
%global _commit 4cbd5b71a598603231786161af7ae5a75aa49fa4
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           wlc
Version:        0.0.4
Release:        1%{?dist}
Summary:        Wayland compositor library
Group:          User Interface/X
License:        MIT
URL:            https://github.com/Cloudef/wlc
%if 0%{?_with_latest}
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz
%else
Source0:        %{url}/archive/v%{version}.tar.gz
%endif

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
%if 0%{?_with_latest}
%autosetup -n %{name}-%{_commit}
%else
%autosetup -n %{name}-%{version}
%endif

%build
%cmake .
%make_build

%install
%make_install

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
* Mon Aug  1 2016 mosquito <sensor.wen@gmail.com> - 0.0.4-1
- Update to 0.0.4

* Mon May 23 2016 nrechn <neil@gyz.io> - 0.0.3-1
- Update to 0.0.3

* Mon May 09 2016 nrechn <neil@gyz.io> - 0.0.2-1
- Initial packaging
