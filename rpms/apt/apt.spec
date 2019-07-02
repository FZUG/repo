%global debug_package %{nil}
%global gtest_version 1.7.0

# commit
%global _commit 2234ff7c2b143046fd196f544ca4baccc7e2b2ec
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:          apt
Version:       1.8.2
Release:       1%{?dist}
Summary:       Debian's commandline package manager

License:       GPLv2
Url:           https://packages.debian.org/sid/apt
Source0:       http://deb.debian.org/debian/pool/main/a/apt/apt_%{version}.tar.xz
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
BuildRequires: gettext-devel
BuildRequires: gnutls-devel
BuildRequires: lz4-devel
BuildRequires: bzip2-devel
BuildRequires: gcc-c++
BuildRequires: cmake
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
%{cmake} .
_stylesheet=$(ls -d /usr/share/sgml/docbook/xsl-stylesheets-*|xargs basename)
sed -i "s|stylesheet/nwalsh|$_stylesheet|" doc/manpage-style.xsl
find doc/ -name "manpage-style.xsl" | xargs sed -i 's|xml/docbook|sgml/docbook|'
sed -i 's|xml/docbook|sgml/docbook|' doc/docbook-{html,text}-style.xsl
# disable debiandoc, this saves us from sgml problems
sed -i 's|-C doc $@|-C doc manpages|' Makefile
%make_build

%install
%make_install

install -m644 doc/examples/apt.conf %{buildroot}%{_sysconfdir}/apt/

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

mv %{buildroot}/usr/libexec/* %{buildroot}/%{_libdir}

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
%{_datadir}/bash-completion/completions/apt
%{_docdir}/apt-doc/
%{_docdir}/apt-utils/
%{_docdir}/libapt-pkg-doc/
%dir %{_var}/cache/apt/archives/partial
%dir %{_sharedstatedir}/apt/lists/partial
%dir %{_sharedstatedir}/apt/mirrors/partial
%dir %{_sharedstatedir}/apt/periodic
%dir %{_var}/log/apt

%files devel
%defattr(-,root,root,-)
%{_includedir}/apt-pkg
%{_libdir}/libapt-inst.so
%{_libdir}/libapt-pkg.so

%changelog
* Wed Jul 03 2019 Zamir SUN <zsun@fedoraproject.org> - 1.8.2
- Update to 1.8.2

* Thu Dec  1 2016 mosquito <sensor.wen@gmail.com> - 1.2.17-1
- Update to 1.2.17

* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 1.2.14-1
- Update to 1.2.14

* Sat Feb 27 2016 mosquito <sensor.wen@gmail.com> - 1.2.4-1
- Update to 1.2.4

* Fri Feb 12 2016 mosquito <sensor.wen@gmail.com> - 1.2.3-1
- Update to 1.2.3

* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 1.0.10.2-1
- Update to 1.0.10.2

* Thu Jul 30 2015 mosquito <sensor.wen@gmail.com> - 1.0.10.1-1
- Update to 1.0.10.1

* Thu Jul 30 2015 mosquito <sensor.wen@gmail.com> - 1.0.9.10-1
- Initial build
