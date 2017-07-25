%global project go-lib
%global repo %{project}

%global commit 3c9791f1a391d7de7d50ee4e308da669143e2060
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-%{repo}
Version:        1.0.5
Release:        1%{?dist}
Summary:        Go bindings for Deepin Desktop Environment development

Group:          Development/Libraries
License:        GPLv3
URL:            https://github.com/linuxdeepin/go-lib
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  golang

%description
DLib is a set of Go bindings/libraries for DDE development.
Containing dbus (forking from guelfey), glib, gdkpixbuf, pulse and more.

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
install -d %{buildroot}%{gopath}/src/pkg.deepin.io/lib/
cp -r * %{buildroot}%{gopath}/src/pkg.deepin.io/lib/
rm -rf %{buildroot}%{gopath}/src/pkg.deepin.io/lib/debian

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{gopath}/src/pkg.deepin.io/lib/

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.0.5-1.git3c9791f
- Update to 1.0.5
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.0.3-1.gitb084e27
- Update to 1.0.3
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 0.5.5-1.git01150d5
- Update to 0.5.5
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.5.3-1.git44767e8
- Update to 0.5.3
* Sun Jul 12 2015 mosquito <sensor.wen@gmail.com> - 0.3.0-1.git98ac007
- Update to 0.3.0-1.git98ac007
* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.4git20140928-1
- Initial build
