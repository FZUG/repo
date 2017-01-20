%global project pyjavascriptcore
%global repo %{project}

%global _commit 0bdc416e99412b18cfde10258f1cefe2d417b4eb
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           python2-javascriptcore
Version:        0.0003
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Javascript Core for Python

Group:          Development/Libraries
License:        GPLv3
URL:            https://github.com/sumary/pyjavascriptcore
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  Cython
BuildRequires:  webkitgtk-devel
BuildRequires:  python-devel
BuildRequires:  python2-setuptools
Provides:       python-javascriptcore = %{version}-%{release}
Provides:       pyjavascriptcore = %{version}-%{release}
Obsoletes:      pyjavascriptcore < %{version}-%{release}

%description
Javascript Core for Python.

%prep
%setup -q -n %{repo}-%{_commit}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%doc README COPYING
%{python_sitearch}/javascriptcore-%{version}-py%{python_version}.egg-info
%{python_sitearch}/javascriptcore.so

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.0003-1.git0bdc416
- Rebuild for fedora 25
* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 0.0003-1.git0bdc416
- Rebuild for fedora 22
* Sun Sep 21 2014 mosquito <sensor.wen@gmail.com> - 0.0003-1
- Initial build
