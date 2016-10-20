%global debug_package %{nil}
# commit
%global project onedrive
%global repo %{project}
%global _commit eb8d0fe039290da1b536654995d02a7e272bb9d7
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           onedrive
Version:        1.1
Release:        1.git%{_shortcommit}%{?dist}
Summary:        OneDrive Free Client written in D
Group:          Applications/Internet
License:        GPLv3
URL:            https://github.com/skilion/onedrive
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Patch1:         0001-ldc2-makefile.patch
Patch2:         0002-create-default-config.patch
BuildRequires:  ldc
BuildRequires:  libcurl-devel
BuildRequires:	sqlite-devel


%description
Free CLI client for Microsoft OneDrive written in D.
This do not support OneDrive for business.

%prep
%setup -q -n %repo-%{_commit}
%patch1 -p1
%patch2 -p1

%build
export DFLAGS="%{_d_optflags}"
make %{?_smp_mflags}

%install
%{__mkdir_p} %{buildroot}%{_bindir}
install -Dm 0755 %{name} %{buildroot}%{_bindir}/%{name}

%clean
rm -rf %{buildroot}

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog
* Thu Oct 20 2016 Ziqian SUN <sztsian@gmail.com> 1.1-1.giteb8d0fe
- initial package
