# rpmlint calls the following error:
#   E: non-executable-script /usr/lib/python3.3/site-packages/keybinder/keybinder_gtk.py 0644L /usr/bin/env
#   This text file contains a shebang or is located in a path dedicated for
#   executables, but lacks the executable bits and cannot thus be executed.  If
#   the file is meant to be an executable script, add the executable bits,
#   otherwise remove the shebang or move the file elsewhere.

%{!?python3_sitelib: %global python_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global debug_package %{nil}
%global project python3-keybinder
%global repo %{project}

# commit
%global _commit 1f633d0f8cf3d84ec83b6338a7965840b6d1940f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		python3-keybinder
Version:	1.1.2
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Python3 Keybinding Library for X

License:	GPLv3
URL:		https://github.com/LiuLang/python3-keybinder
# https://pypi.python.org/packages/source/p/%{name}/%{name}-%{version}.tar.gz
Source0:	https://github.com/LiuLang/python3-keybinder/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:	noarch
BuildRequires:	python3-devel
# not in repos now:
# include this line will call rpmlint to error explicit-lib-dependency
Requires:	python3-xlib

%description
python3-keybinder uses python3-Xlib to bind global keyboard shortcuts.
It runs on almost all desktop environments and window managers on Linux Desktop.

%prep
%setup -q -n %repo-%{_commit}

%build
%{__python3} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}

%files
%doc examples LICENSE README.md
%{python3_sitelib}/keybinder/*
%{python3_sitelib}/python3_keybinder-%{version}-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/keybinder/__pycache__

%changelog
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 1.1.2-1
- Rename version name
* Thu Nov 27 2014 mosquito <sensor.wen@gmail.com> - 1.1.2git20141120-1
- Update version to 1.1.2git20141120
* Wed Nov 19 2014 mosquito <sensor.wen@gmail.com> - 1.1.2git20141113-1
- Update version to 1.1.2git20141113
* Mon Nov 17 2014 mosquito <sensor.wen@gmail.com> - 1.1.2-1
- Initial build
