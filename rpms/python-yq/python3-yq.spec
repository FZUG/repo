%global debug_package %{nil}

Name:           python3-yq
Version:        2.14.0
Release:        1%{?dist}
Summary:        Command-line YAML, XML, TOML processor - jq wrapper for YAML/XML/TOML documents

License:        APL 2.0
URL:            https://kislyuk.github.io/yq/
Source0:        https://files.pythonhosted.org/packages/source/y/yq/yq-%{version}.tar.gz

BuildRequires:  python3-setuptools_scm
BuildRequires:  python3-devel
Requires:       jq
Requires:       python3-argcomplete
Requires:       python3-toml
Requires:       python3-xmltodict
Requires:       python3-yaml

%description
%{summary}.

%prep
%autosetup -n yq-%{version}


%build
%py3_build


%install
%py3_install


%files
%license LICENSE
%{_bindir}/{tomlq,xq,yq}
%{python3_sitelib}/{yq,yq-%{version}-py3.*.egg-info}

%changelog
* Tue Mar 01 2022 zhullyb <zhullyb@outlook.com>
- First build.
