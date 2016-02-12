%global debug_package %{nil}
%global project package-query
%global repo %{project}

# commit
%global _commit a2e8235e4fa37506dd0c4f00a859c2fba44b619d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    package-query
Version: 1.7
Release: 1.git%{_shortcommit}%{?dist}
Summary: Query ALPM and AUR
Summary(zh_CN): 查询 ALPM 和 AUR

License: GPL
Group:   Applications/System
Url:     https://github.com/archlinuxfr/package-query
Source0: https://github.com/archlinuxfr/package-query/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: libalpm-devel
BuildRequires: libarchive-devel
BuildRequires: yajl-devel
BuildRequires: libcurl-devel
BuildRequires: gettext-devel
BuildRequires: libtool
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gzip
Requires: pacman
Requires: yajl

%description
Query ALPM and AUR.

%description -l zh_CN
查询 ALPM 和 AUR.

%prep
%setup -q -n %repo-%{_commit}

%build
libtoolize
aclocal -I m4 --install
autoheader
automake --foreign --add-missing
autoconf
%configure --with-aur-url=https://aur.archlinux.org
make %{?_smp_mflags}

%install
%make_install DESTDIR=%{buildroot}
gzip -9 %{buildroot}%{_mandir}/man8/*

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{name}
%{_mandir}/man8/*.gz

%changelog
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 1.7-1.gita2e8235
- Update to 1.7-1.gita2e8235
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 1.6.2-3.git9305778
- Update to 1.6.2-3.git9305778
* Sun Jul 26 2015 mosquito <sensor.wen@gmail.com> - 1.6.2-2.git3d1115f
- Rebuild for libalpm-4.2.1
* Sun Jul 26 2015 mosquito <sensor.wen@gmail.com> - 1.6.2-1.git3d1115f
- Initial build
