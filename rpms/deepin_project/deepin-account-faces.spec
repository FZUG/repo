%global project dde-account-faces
%global repo %{project}

%global _commit 799e6aa0605167bab6b283aa1114c8aee555a45f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-account-faces
Version:        1.0.10
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Account faces for Linux Deepin
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-account-faces
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
BuildArch:      noarch
Provides:       %{repo} = %{version}-%{release}

%description
Account faces for Linux Deepin

%prep
%setup -q -n %{repo}-%{_commit}

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
