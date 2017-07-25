%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global project pysrt
%global repo %{project}

%global commit e7c644fd0eac94985d25185a0e473c4802a52e0c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

%if 0%{?fedora}
%global with_python3 1
%endif

Name:           python2-%{repo}
Version:        1.1.1
Release:        1%{?dist}
Summary:        pysrt is a Python library used to edit or create SubRip files.
License:        GPLv3
URL:            https://github.com/byroot/pysrt
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  python-setuptools
Provides:       python-%{repo} = %{version}-%{release}

%description
pysrt is a Python library used to edit or create SubRip files.

%if 0%{?with_python3}
%package -n python3-%{repo}
Summary:        pysrt is a Python library used to edit or create SubRip files.
BuildRequires:  python3-devel

%description -n python3-%{repo}
pysrt is a Python library used to edit or create SubRip files.
%endif # with_python3

%prep
%setup -q -n %{repo}-%{commit}

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
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
popd
%endif # with_python3

%{__python2} setup.py install -O1 --skip-build --root=%{buildroot}

%files
%doc README.rst
%license LICENCE.txt
%{_bindir}/srt
%{python2_sitelib}/%{repo}*

%if 0%{?with_python3}
%files -n python3-%{repo}
%doc README.rst
%license LICENCE.txt
%{python3_sitelib}/%{repo}*
%endif # with_python3

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.1.1-1.gite7c644f
- Update to 1.1.1
* Thu Dec 22 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.1-1
- Initial package build
