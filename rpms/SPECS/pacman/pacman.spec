# We ship a .pc file but don't want to have a dep on pkg-config. We
# strip the automatically generated dep here and instead co-own the
# directory.
%global __requires_exclude pkg-config

%global libmajor 10
%global libminor 0

# Use the same directory of the main package for subpackage licence and docs
%global _docdir_fmt %{name}

# commit
%global debug_package %{nil}
%global _commit fea9abc8db3b8161ab32774a0ddd7c405cfbe44f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           pacman
Version:        5.0.0
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Package manager for the Arch distribution
License:        GPLv2+
Url:            https://www.archlinux.org/pacman
Source0:        https://projects.archlinux.org/%{name}.git/snapshot/%{name}-%{_shortcommit}.tar.gz
# mirrorlist retrieved from https://www.archlinux.org/mirrorlist/all
# with mirrors.kernel.org uncommented
# wget https://www.archlinux.org/mirrorlist/all && sed -r 's+^#(Server = https://mirrors.kernel.org/)+\1+' <all >mirrorlist)'
Source1:        mirrorlist

BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  gettext-devel
BuildRequires:  asciidoc
BuildRequires:  doxygen
BuildRequires:  libarchive-devel
BuildRequires:  gpgme-devel
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
Requires:       %{name}-filesystem = %{version}-%{release}
Requires:       bsdtar
Requires:       fakeroot
Recommends:     arch-install-scripts

%description
Pacman is the package manager used by the Arch distribution. It is a
frontend for the ALPM (Arch Linux Package Management) library.

Pacman does not strive to "do everything." It will add, remove and
upgrade packages in the system, and it will allow you to query the
package database for installed packages, files and owners. It also
attempts to handle dependencies automatically and can download
packages from a remote server. Arch packages are simple archives, with
.pkg.tar.gz extension for binary packages and .src.tar.gz for source
packages.


%package -n libalpm
Summary: Arch Linux Package Management library

%description -n libalpm
This library is the backend behind Pacman — the package manager used
by the Arch distribution. It uses simple compressed files as a package
format, and maintains a text-based package database.


%package -n libalpm-devel
Summary: Development headers for libalpm
Requires: libalpm%{_isa} = %{version}-%{release}

%description -n libalpm-devel
This package contains the public headers necessary to use libalpm.


%package filesystem
Summary: Pacman filesystem layout
License: Public Domain
BuildArch: noarch

%description filesystem
This package provides some directories used by pacman and related
packages.


%prep
%setup -q -n %{name}-%{_shortcommit}

%build
autoreconf -i
patch -d build-aux -Np0 -i ltmain-asneeded.patch
%configure --enable-debug --enable-doxygen CFLAGS="$CFLAGS -Wno-error"
make %{?_smp_mflags}

%install
%make_install
%find_lang pacman
%find_lang pacman-scripts
%find_lang libalpm
cat pacman-scripts.lang >> pacman.lang

# work around --disable-static not working
find %{buildroot} \( -name '*.a' -o -name '*.la' \) -print -delete
# work around some garbage files being installed
find %{buildroot} -name '*_BUILD_*' -print -delete

install -Dm0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pacman.d/mirrorlist

cat >>%{buildroot}%{_sysconfdir}/pacman.conf <<EOF

# The testing repositories are disabled by default. To enable, uncomment the
# repo name header and Include lines. You can add preferred servers immediately
# after the header, and they will be used before the default mirrors.

#[testing]
#SigLevel = Never
#Include = /etc/pacman.d/mirrorlist

[core]
SigLevel = Required DatabaseOptional
Include = /etc/pacman.d/mirrorlist

[extra]
SigLevel = Never
Include = /etc/pacman.d/mirrorlist

#[community-testing]
#SigLevel = Never
#Include = /etc/pacman.d/mirrorlist

[community]
SigLevel = Never
Include = /etc/pacman.d/mirrorlist

# If you want to run 32 bit applications on your x86_64 system,
# enable the multilib repositories as required here.

#[multilib-testing]
#SigLevel = Never
#Include = /etc/pacman.d/mirrorlist

#[multilib]
#SigLevel = Never
#Include = /etc/pacman.d/mirrorlist

#[archlinuxfr]
#SigLevel = Never
#Server = http://repo.archlinux.fr/\$arch

#[archlinuxcn]
#SigLevel = Never
#Server = http://repo.archlinuxcn.org/\$arch
EOF


%post -n libalpm -p /sbin/ldconfig
%postun -n libalpm -p /sbin/ldconfig


%files -f pacman.lang
%{_bindir}/vercmp
%{_bindir}/testpkg
%{_bindir}/cleanupdelta
%{_bindir}/pacsort
%{_bindir}/pactree
%{_bindir}/pacman
%{_bindir}/makepkg
%{_bindir}/pacman-db-upgrade
%{_bindir}/pacman-key
%{_bindir}/pacman-optimize
%{_bindir}/pkgdelta
%{_bindir}/repo-add
%{_bindir}/makepkg-template
%{_bindir}/repo-elephant
%{_bindir}/repo-remove
%config(noreplace) %{_sysconfdir}/makepkg.conf
%config(noreplace) %{_sysconfdir}/pacman.conf
%config(noreplace) %{_sysconfdir}/pacman.d/mirrorlist
%dir %{_sharedstatedir}/pacman
%dir %{_localstatedir}/cache/pacman
%dir %{_localstatedir}/cache/pacman/pkg
%{_datadir}/pacman/*
%{_datadir}/makepkg/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%license COPYING
%doc NEWS

%files -n libalpm -f libalpm.lang
%{_libdir}/libalpm.so.%{libmajor}.%{libminor}.*
%{_libdir}/libalpm.so.%{libmajor}
%license COPYING

%files -n libalpm-devel
%{_includedir}/alpm_list.h
%{_includedir}/alpm.h
%{_libdir}/pkgconfig/libalpm.pc
%{_libdir}/libalpm.so
%{_mandir}/man3/*
%license COPYING
%doc HACKING

%files filesystem
%dir %{_sysconfdir}/pacman.d
%dir %{_datadir}/pacman
%dir %{_datadir}/makepkg


%changelog
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 5.0.0-1.gitfea9abc
- Update to version 5.0.0-1.gitfea9abc

* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 4.2.1-3.git5780350
- Update to version 4.2.1-3.git5780350

* Thu Aug  6 2015 mosquito <sensor.wen@gmail.com> - 4.2.1-2.gitdeac973
- Add depend fakeroot

* Wed Jul 29 2015 mosquito <sensor.wen@gmail.com> - 4.2.1-1.gitdeac973
- Update to version 4.2.1-1.gitdeac973
- Add other repository

* Sat Jun 20 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.2.1-1
- Update to version 4.2.1
- libalpm is bumped to version 9.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-5.20130626git28cb22e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jan 07 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1.2-4.20130626git28cb22e
- Require bsdtar (#1176244)
- Use %%license and a single directory for documentation

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-3.20130626git28cb22e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.2-2.20130626git28cb22e
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 22 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1.2-1.20130626git28cb22e
- Build from git snapshot.
- Include /etc/pacman.d/mirrorlist.
- Add pacman-filesystem package.
- Add missing build dependencies and fix other packaging issues.
- Package accepted (#998127).

* Fri Aug 16 2013 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.1.2-1
- Initial packaging.
