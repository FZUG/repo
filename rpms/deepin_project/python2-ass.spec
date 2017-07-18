%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global project python-ass
%global repo %{project}

%global commit c8ffa0b1008c2b2262a2ee7c0f8881f0201a4c8d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           python2-ass
Version:        0.4.2
Release:        1.git%{shortcommit}%{?dist}
Summary:        Advanced SubStation Alpha subtitle files

License:        MIT
URL:            https://github.com/rfw/python-ass
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Provides:       %{repo} = %{version}-%{release}

%description
Advanced SubStation Alpha subtitle files

%prep
%setup -q -n %{repo}-%{commit}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --root="%{buildroot}"

%files
%{python2_sitelib}/ass*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.4.2-1.gitc8ffa0b
- Rewrite
* Thu Dec 22 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.4.2-1
- Initial package build
