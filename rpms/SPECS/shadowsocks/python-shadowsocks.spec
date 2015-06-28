%global debug_package %{nil}
%global project shadowsocks
%global repo %{project}

# commit
%global _commit 16db66675bb1160b4104140a7927036c5552333c
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%if 0%{?fedora} > 12
%global with_python3 1
%else
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:           python-shadowsocks
Version:        2.6.10
Release:        1.git%{_shortcommit}%{?dist}
Summary:        A fast tunnel proxy that help you get through firewalls

License:        Apache
URL:            http://shadowsocks.org
# https://pypi.python.org/packages/source/s/%%{repo}/%%{repo}-%%{version}.tar.gz
Source0:        https://github.com/shadowsocks/shadowsocks/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  m2crypto
Requires:       m2crypto
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# m2crypto is not available for python3
#BuildRequires:  python3-m2crypto
%endif

%description
Shadowsocks is a socks5 tunnel proxy, designed to secure your Internet
traffic.

This package contains the client and server implementation for Shadowsocks in
Python 2.

%if 0%{?with_python3}
%package -n python3-%{repo}
Summary:        A fast tunnel proxy that help you get through firewalls (Python 3)

%description -n python3-%{repo}
Shadowsocks is a socks5 tunnel proxy, designed to secure your Internet
traffic.

This package contains the client and server implementation for Shadowsocks in
Python 3.
%endif

%prep
%setup -q -n %{repo}-%{_commit}
# remove shebangs in the module files
sed -i -e '/^#!\//, 1d' %{repo}/*.py %{repo}/crypto/*.py
# explicitly remove the included egg
rm -rf %{repo}*.egg-info

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python2} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
mv %{buildroot}%{_bindir}/{,python3-}sslocal
mv %{buildroot}%{_bindir}/{,python3-}ssserver
%endif # with_python3
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

%check
%{__python2} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif # with_python3

%files
%doc README.rst LICENSE
%{_bindir}/sslocal
%{_bindir}/ssserver
%{python2_sitelib}/%{repo}*

%if 0%{?with_python3}
%files -n python3-%{repo}
%doc README.rst LICENSE
%{_bindir}/python3-sslocal
%{_bindir}/python3-ssserver
%{python3_sitelib}/%{repo}*
%endif

%changelog
* Tue Jun  2 2015 mosquito <sensor.wen@gmail.com> - 2.6.10-1.git16db666
- Update to 2.6.10

* Sun Nov 16 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.4.3-2
- Build a subpackage for python3

* Sun Nov 16 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Sat Sep 13 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue Jul 15 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.11-1
- Update to 2.0.11, LICENSE included
- Explicitly remove the included egg

* Sat Jul 12 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.10-2
- BuildRequires python2-setuptools

* Sat Jul 12 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.10-1
- Update to 2.0.10
- Requries and BuildRequires m2crypto

* Sun Jul  6 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.8-2
- Explicitly use python2 macros

* Sat Jun 28 2014 Robin Lee <cheeselee@fedoraproject.org> - 2.0.8-1
- Initial package for Fedora
