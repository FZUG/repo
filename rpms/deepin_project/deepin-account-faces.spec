%global repo dde-account-faces

Name:           deepin-account-faces
Version:        1.0.10
Release:        2%{?dist}
Summary:        Account faces for Linux Deepin
License:        GPLv2+
URL:            https://github.com/linuxdeepin/dde-account-faces
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
BuildArch:      noarch

%description
Account faces for Linux Deepin

%prep
%setup -q -n %{repo}-%{version}

%build

%install
%make_install

%files
%{_sharedstatedir}/AccountsService/icons/*

%changelog
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.10-1
- Update to 1.0.10

* Sun Oct 09 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.10-1
- Initial package build
