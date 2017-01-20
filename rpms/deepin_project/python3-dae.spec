%global project dae
%global repo %{project}

%global _commit 350848717ee19b439ac51efd6d9dc2c88769ec3b
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           python3-%{repo}
Version:        1.0.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin desktop application engine
License:        GPLv3
URL:            https://github.com/linuxdeepin/dae
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-qt5-devel
Requires:       python3-xlib
Requires:       python3-qt5
Requires:       python3-qt5-webkit

%description
Deepin desktop application engine

%prep
%setup -q -n %{repo}-%{_commit}

%build
%{__python3} setup.py build

%install
%{__python3} setup.py install --root="%{buildroot}" --optimize=1

%files
%{python3_sitelib}/*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.2-1.git3508487
- Update to 1.0.2
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.2-1
- Update to version 1.0.2
* Thu Dec 29 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.1-3
- Major rewrite of SPEC file
* Thu Dec 22 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.1-2
- Fixed dependency for xlib
* Wed Dec 21 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.1-1
- Initial package build
