%global project go-gir-generator
%global repo %{project}

%global _commit 9ee7058956d8debee0198f2b8b37bb9e361f3451
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-gir-generator
Version:        1.0.1
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Generate static golang bindings for GObject
License:        GPLv3
URL:            https://github.com/linuxdeepin/go-gir-generator
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  gcc-go
BuildRequires:  gobject-introspection-devel
BuildRequires:  libgudev-devel
Provides:       %{repo}%{?_isa} = %{version}-%{release}

%description
Generate static golang bindings for GObject

%prep
%setup -q -n %{repo}-%{_commit}

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
