%global debug_package %{nil}
%global project dbus-factory
%global repo %{project}

# commit
%global _commit 402c0f2e5de07f03a6f65845ae7e0854cdd3bc08
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: dbus-factory
Version: 2.90.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: Go-lang dbus gen for dlib

Group: Development/Libraries
License: GPLv3
URL: https://github.com/linuxdeepin/%{name}
Source0: https://github.com/linuxdeepin/%{name}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: golang
BuildRequires: golang-dlib-devel
BuildRequires: dbus-generator
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: qt5-qtwebkit-devel

%description
Go-lang dbus gen for dlib.

%package -n dde-go-%{name}
Summary: Go-lang dbus gen for dlib
%description -n dde-go-%{name}
Go-lang dbus gen for dlib.

%package -n dde-qml-%{name}
Summary: Go-lang dbus gen QML for dlib
%description -n dde-qml-%{name}
Go-lang dbus gen QML for dlib.

%prep
%setup -q -n %repo-%{_commit}

%build
make all

%install
make install DESTDIR=%{buildroot} GOPATH=%{gopath} QT5_LIBDIR=%{_qt5_prefix}

%files -n dde-go-%{name}
%defattr(-,root,root,-)
%doc README.md
%{gopath}/src/dbus/

%files -n dde-qml-%{name}
%defattr(-,root,root,-)
%doc README.md
%{_qt5_prefix}/qml/DBus/

%changelog
* Sun Jul  5 2015 mosquito <sensor.wen@gmail.com> - 2.90.0-1.git402c0f2
- Update version to 2.90.0-1.git402c0f2
* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20140928-1
- Initial build
