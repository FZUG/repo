%global debug_package %{nil}
%global gtest_version 1.7.0

Name:          apt
Version:       1.2.3
Release:       1%{?dist}
Summary:       Debian's commandline package manager

License:       GPLv2
Url:           https://packages.debian.org/sid/apt
Source0:       https://ftp.debian.org/debian/pool/main/a/%{name}/%{name}_%{version}.tar.xz
Source1:       https://github.com/google/googletest/archive/release-%{gtest_version}/googletest-release-%{gtest_version}.tar.gz

BuildRequires: libdb-devel
BuildRequires: curl-devel
BuildRequires: gtest-devel
BuildRequires: zlib-devel
BuildRequires: xz-devel
BuildRequires: dpkg-dev
BuildRequires: docbook-style-xsl
BuildRequires: doxygen
BuildRequires: libxslt
BuildRequires: w3m
BuildRequires: po4a
BuildRequires: graphviz
BuildRequires: gettext
BuildRequires: dash
Requires: gnupg
#Provides: libapt-inst apt-utils
#Prevides: libapt-pkg libapt-pkg-dev

%description
This package provides commandline tools for searching and managing as well
as querying information about packages as a low-level access to all features
of the libapt-pkg library.

These include:
* apt-get for retrieval of packages and information about them
  from authenticated sources and for installation, upgrade and
  removal of packages together with their dependencies
* apt-cache for querying available information about installed
  as well as installable packages
* apt-cdrom to use removable media as a source for packages
* apt-config as an interface to the configuration settings
* apt-key as an interface to manage authentication keys

%package devel
Summary: Development headers for APT's libapt-pkg
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains development files for developing with APT's
libapt-pkg package manipulation library.

%prep
%setup -q -a1

%build
# gtest source
mkdir src; cp googletest-release-%{gtest_version}/src/* src/
sed -i '/#include/s|src/||' src/gtest-all.cc
sed -i -r '/(GTEST_SRCS|CXX)/s|\$\(GTEST_DIR\)|../..|g' test/libapt/makefile
# this only copies config.{guess,sub} and displays errors
automake --add-missing --force -W none ||:
_stylesheet=$(ls -d /usr/share/sgml/docbook/xsl-stylesheets-*|xargs basename)
sed -i "s|stylesheet/nwalsh|$_stylesheet|" doc/manpage-style.xsl
find doc/ -name "manpage-style.xsl" | xargs sed -i 's|xml/docbook|sgml/docbook|'
sed -i 's|xml/docbook|sgml/docbook|' doc/docbook-{html,text}-style.xsl
# disable debiandoc, this saves us from sgml problems
sed -i 's|-C doc $@|-C doc manpages|' Makefile
# bash 4.3.33 seems to have problems, use dash instead (sh symlink in Debian)
sed -i 's|#!/bin/sh|#!/bin/dash|' configure
%configure
make %{?_smp_mflags} GTEST_DIR=%{_includedir}/gtest

%install
# apt
install -Dm755 bin/apt %{buildroot}%{_bindir}/apt
for file in {cache,cdrom,config,get,key,mark}; do
  install -m755 bin/apt-$file %{buildroot}%{_bindir}/
done
# apt-utils
for file in {extracttemplates,ftparchive,sortpkgs}; do
  install -m755 bin/apt-$file %{buildroot}%{_bindir}/
done

install -d %{buildroot}%{_libdir}
# libapt-inst
install -m755 bin/libapt-inst.so.2.0.0 %{buildroot}%{_libdir}
ln -sfv %{_libdir}/libapt-inst.so.2.0.0 %{buildroot}%{_libdir}/libapt-inst.so.2.0
ln -sfv %{_libdir}/libapt-inst.so.2.0.0 %{buildroot}%{_libdir}/libapt-inst.so
# libapt-pkg
install -m755 bin/libapt-pkg.so.5.0.0 %{buildroot}%{_libdir}
ln -sfv %{_libdir}/libapt-pkg.so.5.0.0 %{buildroot}%{_libdir}/libapt-pkg.so.5.0
ln -sfv %{_libdir}/libapt-pkg.so.5.0.0 %{buildroot}%{_libdir}/libapt-pkg.so
# libapt-private
install -m755 bin/libapt-private.so.0.0.0 %{buildroot}%{_libdir}
ln -sfv %{_libdir}/libapt-private.so.0.0.0 %{buildroot}%{_libdir}/libapt-private.so.0.0
ln -sfv %{_libdir}/libapt-private.so.0.0.0 %{buildroot}%{_libdir}/libapt-private.so
# apt-utils
install -Dm755 bin/apt-internal-solver %{buildroot}%{_libdir}/apt/solvers/apt
install -Dm755 bin/apt-dump-solver %{buildroot}%{_libdir}/apt/solvers/dump
# apt
install -d %{buildroot}%{_libdir}/apt/methods
install -m755 bin/apt-helper %{buildroot}%{_libdir}/apt/
install -m755 bin/methods/* %{buildroot}%{_libdir}/apt/methods/
rm -f %{buildroot}%{_libdir}/apt/methods/{bzip2,gzip,lzma,ssh,xz}
ln -sfv %{_libdir}/apt/methods/rsh %{buildroot}%{_libdir}/apt/methods/ssh
for i in bzip2 gzip lzma xz; do
ln -sfv %{_libdir}/apt/methods/store %{buildroot}%{_libdir}/apt/methods/${i}
done
install -d %{buildroot}%{_libdir}/dpkg/methods/apt
install -m755 dselect/{install,setup,update} %{buildroot}%{_libdir}/dpkg/methods/apt/
install -m644 dselect/{desc.apt,names} %{buildroot}%{_libdir}/dpkg/methods/apt/

# ALL manpages
install -d %{buildroot}%{_mandir}/man{1,5,8}
for part in {1,5,8}; do
  for lang in {de,en,es,fr,it,ja,nl,pl,pt}; do
    install -d %{buildroot}%{_mandir}/$lang/man$part
    gzip -f doc/$lang/*.$part ||:
    install -m644 doc/$lang/*.$part.gz %{buildroot}%{_mandir}/$lang/man$part/ ||:
  done
  install -m644 %{buildroot}%{_mandir}/en/man$part/* %{buildroot}%{_mandir}/man$part/
done

# ALL example configs
install -d %{buildroot}%{_defaultdocdir}/apt/examples
install -m644 doc/examples/* %{buildroot}%{_defaultdocdir}/apt/examples

# ALL locales
for lang in locale/*; do
  install -d %{buildroot}%{_datadir}/$lang/LC_MESSAGES
  install -m644 $lang/LC_MESSAGES/* %{buildroot}%{_datadir}/$lang/LC_MESSAGES/
done

# libapt-pkg-dev
install -d %{buildroot}%{_includedir}/apt-pkg
install -m644 include/apt-pkg/* %{buildroot}%{_includedir}/apt-pkg/
# libapt-private-dev
install -d %{buildroot}%{_includedir}/apt-private
install -m644 include/apt-private/* %{buildroot}%{_includedir}/apt-private/

# Configuration
install -d %{buildroot}%{_sysconfdir}/apt/{apt.conf,preferences,sources.list,trusted.gpg}.d
install -m644 doc/examples/apt.conf %{buildroot}%{_sysconfdir}/apt/
cat > %{buildroot}%{_sysconfdir}/apt/sources.list <<EOF
deb http://cn.archive.ubuntu.com/ubuntu/ vivid main restricted
deb-src http://cn.archive.ubuntu.com/ubuntu/ vivid main restricted
deb http://cn.archive.ubuntu.com/ubuntu/ vivid-updates main restricted
deb-src http://cn.archive.ubuntu.com/ubuntu/ vivid-updates main restricted

deb http://cn.archive.ubuntu.com/ubuntu/ vivid universe
deb-src http://cn.archive.ubuntu.com/ubuntu/ vivid universe
deb http://cn.archive.ubuntu.com/ubuntu/ vivid-updates universe
deb-src http://cn.archive.ubuntu.com/ubuntu/ vivid-updates universe

deb http://cn.archive.ubuntu.com/ubuntu/ vivid multiverse
deb-src http://cn.archive.ubuntu.com/ubuntu/ vivid multiverse
deb http://cn.archive.ubuntu.com/ubuntu/ vivid-updates multiverse
deb-src http://cn.archive.ubuntu.com/ubuntu/ vivid-updates multiverse

deb http://cn.archive.ubuntu.com/ubuntu/ vivid-backports main restricted universe multiverse
deb-src http://cn.archive.ubuntu.com/ubuntu/ vivid-backports main restricted universe multiverse

deb http://security.ubuntu.com/ubuntu/ vivid-security main restricted
deb-src http://security.ubuntu.com/ubuntu/ vivid-security main restricted
deb http://security.ubuntu.com/ubuntu/ vivid-security universe
deb-src http://security.ubuntu.com/ubuntu/ vivid-security universe
deb http://security.ubuntu.com/ubuntu/ vivid-security multiverse
deb-src http://security.ubuntu.com/ubuntu/ vivid-security multiverse
EOF
install -d %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/apt <<EOF
/var/log/apt/term.log {
  rotate 12
  monthly
  compress
  missingok
  notifempty
}
/var/log/apt/history.log {
  rotate 12
  monthly
  compress
  missingok
  notifempty
}
EOF

# var directory
install -d %{buildroot}%{_var}/cache/apt/archives/partial
install -d %{buildroot}%{_sharedstatedir}/apt/{lists,mirrors}/partial
install -d %{buildroot}%{_sharedstatedir}/apt/periodic
install -d %{buildroot}%{_var}/log/apt

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%post devel -p /sbin/ldconfig
%postun devel -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license COPYING COPYING.GPL
%doc README.md AUTHORS
%dir %{_sysconfdir}/apt/apt.conf.d
%dir %{_sysconfdir}/apt/preferences.d
%dir %{_sysconfdir}/apt/sources.list.d
%dir %{_sysconfdir}/apt/trusted.gpg.d
%config(noreplace) %{_sysconfdir}/apt/apt.conf
%config(noreplace) %{_sysconfdir}/apt/sources.list
%config(noreplace) %{_sysconfdir}/logrotate.d/apt
%{_bindir}/apt*
%{_libdir}/libapt-inst.so.*
%{_libdir}/libapt-pkg.so.*
%{_libdir}/libapt-private.so.*
%{_libdir}/apt/
%{_libdir}/dpkg/
%{_mandir}/*/man[158]/*.[158].gz
%{_mandir}/man[158]/*.[158].gz
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_defaultdocdir}/apt/examples/
%dir %{_var}/cache/apt/archives/partial
%dir %{_sharedstatedir}/apt/lists/partial
%dir %{_sharedstatedir}/apt/mirrors/partial
%dir %{_sharedstatedir}/apt/periodic
%dir %{_var}/log/apt

%files devel
%defattr(-,root,root,-)
%{_includedir}/apt-pkg
%{_includedir}/apt-private
%{_libdir}/libapt-inst.so
%{_libdir}/libapt-pkg.so
%{_libdir}/libapt-private.so

%changelog
* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 1.2.3-1
- Update to 1.2.3
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 1.0.10.2-1
- Update to 1.0.10.2
* Thu Jul 30 2015 mosquito <sensor.wen@gmail.com> - 1.0.10.1-1
- Update to 1.0.10.1
* Thu Jul 30 2015 mosquito <sensor.wen@gmail.com> - 1.0.9.10-1
- Initial build
