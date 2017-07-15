%global project dde-help
%global repo %{project}

%global _commit ad0be943ffeab911ac32efbfb0669a08dd14b753
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-help
Version:        15.4.7
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Help files for DDE
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-help
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
BuildArch:      noarch
Requires:       deepin-manual

%description
%{summary}

%prep
%setup -q -n %{repo}-%{_commit}

%build

%install
%make_install

%files
%defattr(-,root,root,-)
%license LICENSE
%{_datadir}/dman/dde/

%changelog
* Sat Jul 15 2017 mosquito <sensor.wen@gmail.com> - 15.4.7-1.gitad0be94
- Initial build
