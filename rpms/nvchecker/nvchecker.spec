%global srcname nvchecker

Name:           python-%{srcname}
Version:        1.1
Release:        1%{?dist}
Summary:        New version checker for software releases.

License:        MIT
URL:            https://pypi.python.org/pypi/%{srcname}
Source0:        %pypi_source

BuildArch:      noarch 
BuildRequires:  python3-devel python3-pytest-xdist python3-structlog python3-pytest-asyncio python3-pycurl python3-tornado python3-aiohttp

%description
nvchecker (short for new version checker) is for checking if a new version of some software has been released.

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
New version checker for software releases.


%prep
%autosetup -n %{srcname}-%{version}

%build
%py3_build

%install
%py3_install


%files -n python3-%{srcname}
%doc README.rst
%{python3_sitelib}/*
%{_bindir}/nvchecker
%{_bindir}/nvcmp
%{_bindir}/nvtake

%changelog
* Wed Aug 22 2018 Bangjie Deng <dengbangjie@foxmail.com> 1.1-1
- Initial RPM release
