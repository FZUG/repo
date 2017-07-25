%global project go-gir-generator
%global repo %{project}

Name:           deepin-gir-generator
Version:        1.0.1
Release:        1%{?dist}
Summary:        Generate static golang bindings for GObject
License:        GPLv3
URL:            https://github.com/linuxdeepin/go-gir-generator
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  gcc-go
BuildRequires:  gobject-introspection-devel
BuildRequires:  libgudev-devel

%description
Generate static golang bindings for GObject

%prep
%setup -q -n %{repo}-%{version}

%build
export GOPATH="%{gopath}"
%make_build

%install
%make_install

%files
%{_bindir}/gir-generator
%{gopath}/src/gir/

%changelog
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
