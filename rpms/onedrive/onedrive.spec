%global debug_package %{nil}
# commit
%global project onedrive
%global repo %{project}
%global _commit eb8d0fe039290da1b536654995d02a7e272bb9d7
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           onedrive
Version:        1.1
Release:        2.git%{_shortcommit}%{?dist}
Summary:        OneDrive Free Client written in D
Group:          Applications/Internet
License:        GPLv3
URL:            https://github.com/skilion/onedrive
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Patch1:         0001-ldc2-makefile.patch
Patch2:         0002-create-default-config.patch
BuildRequires:  ldc
BuildRequires:  libcurl-devel
BuildRequires:  sqlite-devel
BuildRequires:  systemd
Requires(post): systemd
Requires(preun): systemd 

%description
Free CLI client for Microsoft OneDrive written in D.
This do not support OneDrive for business.

%prep
%setup -q -n %repo-%{_commit}
%patch1 -p1
%patch2 -p1

%build
%make_build DC="ldc2"

%install
%make_install \
    PREFIX="%{_prefix}" \
    CONFDIR="%{buildroot}%{_sysconfdir}"

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%files
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_bindir}/%{name}
%{_userunitdir}/%{name}.service

%changelog
* Tue Oct 25 2016 mosquito <sensor.wen@gmail.com> 1.1-2.giteb8d0fe
- add BReq systemd
* Thu Oct 20 2016 Ziqian SUN <sztsian@gmail.com> 1.1-1.giteb8d0fe
- initial package
