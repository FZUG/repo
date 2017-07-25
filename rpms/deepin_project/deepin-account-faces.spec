%global project dde-account-faces
%global repo %{project}

Name:           deepin-account-faces
Version:        1.0.10
Release:        1%{?dist}
Summary:        Account faces for Linux Deepin
License:        GPLv3
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
%{_var}/lib/AccountsService/icons/*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.10-1.git799e6aa
- Update to 1.0.10
* Sun Oct 09 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.10-1
- Initial package build
