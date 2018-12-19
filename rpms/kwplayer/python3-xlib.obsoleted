%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global debug_package %{nil}
%global project python3-xlib
%global repo %{project}

# commit
%global _commit e68a323cc8e2441c488344cc2225fef0baa17526
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		python3-xlib
Version:	0.15
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Python3 X Library

License:	GPLv2
URL:		https://github.com/LiuLang/python3-xlib
# https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Source0:	https://github.com/LiuLang/python3-xlib/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel

%description
python3-xlib is python3 version of python-xlib.

%prep
%setup -q -n %repo-%{_commit}

%build
%{__python3} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT
 
%files
%doc README.md LICENSE doc examples
%{python3_sitelib}/Xlib/*
%{python3_sitelib}/python3_xlib-0.15-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/Xlib/__pycache__

%changelog
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 0.15-1
- Rename version name
* Wed Nov 19 2014 mosquito <sensor.wen@gmail.com> - 0.15git20141113-1
- Update version to 0.15git20141113
* Mon Nov 17 2014 mosquito <sensor.wen@gmail.com> - 0.15-1
- Initial build
