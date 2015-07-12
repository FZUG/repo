%global debug_package %{nil}
%global project go-lib
%global repo %{project}

# commit
%global _commit 98ac0073b3d4e310e6570676fa74e4372b7dac7d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})
%global goleader pkg.linuxdeepin.com

Name: golang-dlib
Version: 0.3.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: Go bindings for Deepin Desktop Environment development

Group: Development/Libraries
License: GPLv3
URL: https://github.com/linuxdeepin/go-lib
Source0: https://github.com/linuxdeepin/go-lib/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: golang
BuildRequires: pulseaudio-libs-devel
BuildRequires: gtk3-devel
Requires: glib2

%description
DLib is a set of Go bindings/libraries for DDE development.
Containing dbus (forking from guelfey), glib, gdkpixbuf, pulse and more.

%package devel
Summary: Go bindings for Deepin Desktop Environment development
BuildArch: noarch

%description devel
DLib is a set of Go bindings/libraries for DDE development.
Containing dbus (forking from guelfey), glib, gdkpixbuf, pulse and more.

%prep
%setup -q -n %repo-%{_commit}

%build

%install
install -d %{buildroot}%{gopath}/src/%{goleader}/lib/
cp -r * %{buildroot}%{gopath}/src/%{goleader}/lib/
rm -rf %{buildroot}%{gopath}/src/%{goleader}/lib/dabian

%files devel
%defattr(-,root,root,-)
%doc debian/copyright
%{gopath}/src/%{goleader}/lib

%changelog
* Sun Jul 12 2015 mosquito <sensor.wen@gmail.com> - 0.3.0-1.git98ac007
- Update to 0.3.0-1.git98ac007
* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.4git20140928-1
- Initial build
