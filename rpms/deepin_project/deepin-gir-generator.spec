%global project go-gir-generator
%global repo %{project}

Name:           deepin-gir-generator
Version:        1.0.1
Release:        2%{?dist}
Summary:        Generate static golang bindings for GObject
License:        GPLv3
URL:            https://github.com/linuxdeepin/go-gir-generator
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
Patch0:         SettingsBackendLike.patch

BuildRequires:  gcc-go
BuildRequires:  gobject-introspection-devel
BuildRequires:  libgudev-devel

%description
Generate static golang bindings for GObject

%prep
%setup -q -n %{repo}-%{version}

GIO_VER=$(v=$(rpm -q --qf %{RPMTAG_VERSION} gobject-introspection); echo ${v//./})
if [ $GIO_VER -ge 1521 ]; then
# Our gobject-introspection is too new
# https://cr.deepin.io/#/c/16880/
%patch0 -p1
fi

%build
export GOPATH="%{gopath}"
%make_build

%install
%make_install

%files
%doc README.md
%license LICENSE
%{_bindir}/gir-generator
%{gopath}/src/gir/

%changelog
* Thu Aug  3 2017 mosquito <sensor.wen@gmail.com> - 1.0.1-2
- Fix undefined type SettingsBackendLike

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.0.1-1.git9ee7058
- Update to 1.0.1

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.9.6-1.gitfe260d3
- Update to 0.9.6

* Wed Jan 04 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 0.9.6-3
- Renamed package to deepin-go-gir-generator

* Sun Dec 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.9.6-2
- Changed lib path

* Fri Oct 28 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.9.6-1
- Compilation rework

* Thu Sep 29 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.9.5-2
- Compilation rework

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.9.5-1
- Initial package build
