%global project go-dbus-generator
%global repo %{project}

Name:           deepin-dbus-generator
Version:        0.6.6
Release:        1%{?dist}
Summary:        Convert dbus interfaces to go-lang or qml wrapper code
Group:          Development/Libraries
License:        GPLv3
URL:            https://github.com/linuxdeepin/go-dbus-generator
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-go
BuildRequires:  golang(gopkg.in/check.v1)
BuildRequires:  golang(pkg.deepin.io/lib)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Quick)

%description
Static dbus binding generator for dlib.

%prep
%setup -q -n %{repo}-%{version}
# qmake path
sed -i 's|qmake|qmake-qt5|' build_test.go template_qml.go

%build
export GOPATH="%{gopath}"
%make_build

%install
%make_install GOPATH="%{gopath}"

%files
%doc README.md
%license LICENSE
%{_bindir}/dbus-generator

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 0.6.6-1.gitace6ac0
- Update to 0.6.6

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.6.5-1.git9f8b51d
- Update to 0.6.5

* Sun Jul 12 2015 mosquito <sensor.wen@gmail.com> - 0.0.3-1.git84ee26c
- Update to 0.0.3-1.git84ee26c

* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.3git20140924-1
- Initial build
