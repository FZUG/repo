%global debug_package %{nil}
%global project package-query
%global repo %{project}

# commit
%global _commit 3d1115fcc65543f3d73e01c94b7abc3b7bf0c367
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: package-query
Version: 1.6.2
Release: 2.git%{_shortcommit}%{?dist}
Summary: Query ALPM and AUR
Summary(zh_CN): 查询 ALPM 和 AUR

License: GPL
Group: Applications/System
Url: https://github.com/archlinuxfr/package-query
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
make install DESTDIR=%{buildroot}
gzip -9 %{buildroot}%{_mandir}/man8/*

%files
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{name}
%{_mandir}/man8/*.gz

%changelog
* Sun Jul 26 2015 mosquito <sensor.wen@gmail.com> - 1.6.2-2.git3d1115f
- Rebuild for libalpm-4.2.1
* Sun Jul 26 2015 mosquito <sensor.wen@gmail.com> - 1.6.2-1.git3d1115f
- Initial build
