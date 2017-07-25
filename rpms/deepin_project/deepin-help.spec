%global project dde-help
%global repo %{project}

Name:           deepin-help
Version:        15.4.8
Release:        1%{?dist}
Summary:        Help files for DDE
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-help
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
BuildArch:      noarch
Requires:       deepin-manual

%description
%{summary}

%prep
%setup -q -n %{repo}-%{version}

%build

%install
%make_install

%files
%license LICENSE
%{_datadir}/dman/dde/

%changelog
* Thu Jul 20 2017 mosquito <sensor.wen@gmail.com> - 15.4.8-1.git84f3f54
- Update to 15.4.8

* Sat Jul 15 2017 mosquito <sensor.wen@gmail.com> - 15.4.7-1.gitad0be94
- Initial build
