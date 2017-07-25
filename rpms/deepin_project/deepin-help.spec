%global project dde-help
%global repo %{project}

%global commit 84f3f549e6bcc509c6aaf5758bdf39a59f0dc77b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-help
Version:        15.4.8
Release:        1%{?dist}
Summary:        Help files for DDE
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-help
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
BuildArch:      noarch
Requires:       deepin-manual

%description
%{summary}

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
%make_install

%files
%defattr(-,root,root,-)
%license LICENSE
%{_datadir}/dman/dde/

%changelog
* Thu Jul 20 2017 mosquito <sensor.wen@gmail.com> - 15.4.8-1.git84f3f54
- Update to 15.4.8
* Sat Jul 15 2017 mosquito <sensor.wen@gmail.com> - 15.4.7-1.gitad0be94
- Initial build
