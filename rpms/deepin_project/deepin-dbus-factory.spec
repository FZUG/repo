%global   debug_package   %{nil}
%global   repo            dbus-factory
%global   import_path     dbus

Name:           golang-deepin-%{repo}
Version:        3.1.9
Release:        1%{?dist}
Summary:        Golang DBus factory for Deepin Desktop Environment
License:        GPLv3+
URL:            https://github.com/linuxdeepin/dbus-factory
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

BuildRequires:  golang(pkg.deepin.io/lib)
BuildRequires:  deepin-dbus-generator
BuildRequires:  jq
BuildRequires:  libxml2
Provides:       deepin-go-%{repo} = %{version}-%{release}
Obsoletes:      deepin-go-%{repo} < %{version}-%{release}

%description
Golang DBus factory for Deepin Desktop Environment.

%package devel
Summary:        %{summary}
BuildArch:      noarch

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%setup -q -n %{repo}-%{version}

%build
%make_build

%install
%make_install GOPATH=%{gopath}

%files devel
%doc README.md
%license LICENSE
%{gopath}/src/dbus/

%changelog
* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 3.1.9-1
- Update to 3.1.9

* Tue Oct 17 2017 mosquito <sensor.wen@gmail.com> - 3.1.8-2
- BR: libxml2

* Sat Oct 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.8-1
- Update to 3.1.8

* Thu Aug 24 2017 mosquito <sensor.wen@gmail.com> - 3.1.7-2
- Obsolete deepin-qml-dbus-factory package

* Thu Aug  3 2017 mosquito <sensor.wen@gmail.com> - 3.1.7-1
- Update to 3.1.7

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.6-1.git0ef9267
- Update to 3.1.6

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.1.4-1.git2308ee3
- Update to 3.1.4

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.0-1.git1fb380c
- Update to 3.1.0

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.9-1.git247464a
- Update to 3.0.9

* Sun Jul  5 2015 mosquito <sensor.wen@gmail.com> - 2.90.0-1.git402c0f2
- Update version to 2.90.0-1.git402c0f2

* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20140928-1
- Initial build
