%global debug_package %{nil}
%global project go-dbus-generator
%global repo %{project}

# commit
%global _commit 84ee26c38d49a705d6447a80b4c96637c2d59136
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: dbus-generator
Version: 0.0.3
Release: 1.git%{_shortcommit}%{?dist}
Summary: Static dbus binding generator for dlib

Group: Development/Libraries
License: GPLv3
URL: https://github.com/linuxdeepin/go-%{name}
Source0: https://github.com/linuxdeepin/go-%{name}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: golang
BuildRequires: golang-dlib-devel
BuildRequires: golang-gopkg-check-devel
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gobject-2.0)
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtdeclarative-devel

%description
Static dbus binding generator for dlib.

%prep
%setup -q -n %repo-%{_commit}

%build
# qmake path
sed -i 's|qmake|qmake-qt5|' build_test.go template_qml.go
export GOPATH="/usr/share/gocode"
go build -o %{name}

%install
install -Dm 0755 %{name} %{buildroot}%{_bindir}/%{name}

%check
export GOPATH="/usr/share/gocode"
go test -v

%files
%defattr(-,root,root,-)
%doc README.md
%{_bindir}/%{name}

%changelog
* Sun Jul 12 2015 mosquito <sensor.wen@gmail.com> - 0.0.3-1.git84ee26c
- Update to 0.0.3-1.git84ee26c
* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.3git20140924-1
- Initial build
