%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global debug_package %{nil}

Name:           nvchecker
Version:        2.7
Release:        2%{?dist}
Summary:        New version checker for software releases

License:        MIT
URL:            https://github.com/lilydjwg/nvchecker
Source0:        https://github.com/lilydjwg/nvchecker/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	make
BuildRequires:  python3-devel
BuildRequires:  python3-docutils
BuildRequires:  python3-setuptools
BuildRequires:  python3-pygments
Requires:       python3
Requires:       python3-tomli
Requires:       python3-structlog
Requires:       python3-appdirs
Requires:       python3-tornado
Requires:       python3-pycurl

Provides:       python3-%{name} = %{version}
Obsoletes:      python3-%{name} <= %{version}

%description
%{summary}

%package bash-completion
Summary:        bash completion files for %{name}
Requires:       %{name} = %{version}-%{release}
Requires:       bash

%description bash-completion
This package installs %{summary}.

%prep
%autosetup

%build
%{__python3} setup.py build
make -C docs man

%install
%{__python3} setup.py install --root="%{buildroot}" --optimize=1 --skip-build
%{__install} -Dm644 docs/_build/man/nvchecker.1 -t %{buildroot}%{_datadir}/man/man1/
%{__install} -Dm644 scripts/nvtake.bash_completion %{buildroot}%{_datadir}/bash-completion/completions/nvtake

%files
%license LICENSE
%doc docs/usage.rst
%doc sample_config.toml
%{_bindir}/{nvchecker,nvchecker-ini2toml,nvchecker-notify,nvcmp,nvtake}
%{python3_sitelib}/*
%{_datadir}/man/man1/nvchecker.1.gz

%files bash-completion
%{_datadir}/bash-completion/completions/nvtake

%changelog
* Sun Feb 27 2022 zhullyb <zhullyb@outlook.com> - 2.7-2
- Add make into buildrequires
- Specify the version of provided python3-nvchecker

* Sat Feb 26 2022 zhullyb <zhullyb@outlook.com> - 2.7-1
- new version

* Wed Aug 22 2018 Bangjie Deng <dengbangjie@foxmail.com> 1.1-1
- Initial RPM release
