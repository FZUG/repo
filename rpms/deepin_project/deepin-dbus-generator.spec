%global repo go-dbus-generator

Name:           deepin-dbus-generator
Version:        0.6.6
Release:        3%{?dist}
Summary:        Convert dbus interfaces to go-lang or qml wrapper code
License:        GPLv3+
URL:            https://github.com/linuxdeepin/go-dbus-generator
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
BuildRequires:  golang
BuildRequires:  golang(gopkg.in/check.v1)
BuildRequires:  golang(pkg.deepin.io/lib)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5Qml)

%description
Static dbus binding generator for dlib.

%prep
%setup -q -n %{repo}-%{version}
# qmake path
sed -i 's|qmake|qmake-qt5|' build_test.go template_qml.go

%build
export GOPATH="%{gopath}"
BUILD_ID="0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
function gobuild { go build -a -ldflags "-B $BUILD_ID" -v -x "$@"; }
gobuild -o dbus-generator

%install
install -Dm755 dbus-generator %{buildroot}%{_bindir}/dbus-generator

%files
%doc README.md
%license LICENSE
%{_bindir}/dbus-generator

%changelog
* Tue Mar 13 2018 mosquito <sensor.wen@gmail.com> - 0.6.6-3
- Fix build failure

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 0.6.6-1
- Update to 0.6.6

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.6.5-1.git9f8b51d
- Update to 0.6.5

* Sun Jul 12 2015 mosquito <sensor.wen@gmail.com> - 0.0.3-1.git84ee26c
- Update to 0.0.3-1.git84ee26c

* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.3git20140924-1
- Initial build
