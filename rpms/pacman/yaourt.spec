%global debug_package %{nil}
%global project yaourt
%global repo %{project}

# commit
%global _commit 56818c08c94be17dd5a5319ac15cea4f58b47cf7
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    yaourt
Version: 1.7
Release: 1.git%{_shortcommit}%{?dist}
Summary: A pacman wrapper with extended features and AUR support
Summary(zh_CN): 支持 AUR 的 pacman 前端

License: GPLv2
Group:   Applications/System
Url:     https://archlinux.fr/yaourt-en
Source0: https://github.com/archlinuxfr/yaourt/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source1: https://github.com/FZUG/repo/raw/master/rpms/SOURCES/pacman/yaourt-link

BuildArch: noarch
BuildRequires: gettext gzip
Requires: diffutils
Requires: pacman
Requires: package-query

%description
A pacman wrapper with extended features and AUR support.

%description -l zh_CN
支持 AUR 的 pacman 前端

%prep
%setup -q -n %repo-%{_commit}
find -name 'es_419.po' -exec rm -f '{}' \;

%build
pushd src
make PREFIX=%{_prefix} \
    sysconfdir=%{_sysconfdir} \
    localstatedir=%{_var} \
    libdir=%{_libexecdir}

%install
%make_install -C src \
    PREFIX=%{_prefix} \
    sysconfdir=%{_sysconfdir} \
    localstatedir=%{_var} \
    libdir=%{_libexecdir} \
    DESTDIR=%{buildroot}
gzip -9 %{buildroot}%{_mandir}/man{5,8}/*
install -m 755 %{S:1} %{buildroot}%{_bindir}

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README.pod
%license src/COPYING
%config(noreplace) %{_sysconfdir}/%{name}rc
%{_bindir}/*
%attr(755,-,-) %{_libexecdir}/%{name}/*.sh
%{_mandir}/man*/*.gz
%exclude %{_datadir}/bash-completion/

%changelog
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 1.7-1.git56818c0
- Update to 1.7-1.git56818c0
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 1.6-5.gite75e9b8
- Update to 1.6-5.gite75e9b8
* Sun Aug  2 2015 mosquito <sensor.wen@gmail.com> - 1.6-4.gitd2d8300
- Add yaourt-link's -q, -S option
* Fri Jul 31 2015 mosquito <sensor.wen@gmail.com> - 1.6-3.gitd2d8300
- Add yaourt-link's -L option
* Thu Jul 30 2015 mosquito <sensor.wen@gmail.com> - 1.6-2.gitd2d8300
- Fixed yaourt-link's LINK function
* Sun Jul 26 2015 mosquito <sensor.wen@gmail.com> - 1.6-1.gitd2d8300
- Initial build
