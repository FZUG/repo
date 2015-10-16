%global  debug_package %{nil}

# provides filter
%if 0%{?rhel} > 6 || 0%{?fedora}
%global  __provides_exclude  (libtool)
%else
%{?filter_setup:
%filter_from_provides /libtool/d;
%filter_setup}
%endif

%if 0%{?fedora} >= 16 || 0%{?rhel} >= 7
%global  with_systemd  1
%endif

# ircd-hybrid-selinux conditional
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%global  with_selinux  1
%endif

%if 0%{?with_selinux}
%global  selinuxtype   targeted
%global  moduletype    services
%global  modulename    %{name}

# Usage: _format var format
# Expand 'modulename' into various formats as needed
# Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulename}; do %1+=%2; %1+=" "; done;

# Relabel files
%global relabel_files() %{_sbindir}/restorecon -R %{_sbindir}/%{name} %{_var}/run/%{name} %{_sharedstatedir}/%{name} %{_sysconfdir}/%{name} %{_var}/log/%{name} %{_unitdir}/%{name}.service &>/dev/null ||:

# Version of SELinux we were using
%if 0%{?fedora} >= 21
%global  selinux_policyver 3.13.1-105
%else
%global  selinux_policyver 3.13.1-39
%endif
%endif # with_selinux

Name:     ircd-hybrid
Version:  8.2.9
Release:  1%{?dist}
Summary:  Internet Relay Chat Server

Group:    System Environment/Daemons
License:  GPLv2+
URL:      http://www.ircd-hybrid.org
Source0:  https://github.com/ircd-hybrid/ircd-hybrid/archive/%{version}/%{name}-%{version}.tar.gz
Source1:  %{name}.init
Source2:  %{name}.sysconfig
Source3:  %{name}.service
Source4:  %{name}.logrotate
Source5:  %{name}-tmpfiles.conf
Source6:  ircd.conf
Source7:  ircd.motd
Source21: %{name}.te
Source22: %{name}.fc
Source23: %{name}.if
Source24: Makefile
Patch0:   fhs_comply.patch

BuildRequires: libtool, libtool-ltdl-devel
BuildRequires: autoconf, automake, m4
BuildRequires: openssl-devel
BuildRequires: GeoIP-devel
%if 0%{?with_systemd}
BuildRequires: systemd-devel
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%else
Requires(pre): shadow-utils
Requires(post): chkconfig
Requires(preun): chkconfig, initscripts
Requires(postun): initscripts
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%endif

# RE: rhbz#1195804 - ensure min NVR for selinux-policy
%if 0%{?with_selinux}
Requires: selinux-policy >= %{selinux_policyver}
Requires(pre): %{name}-selinux >= %{version}-%{release}
%endif # with_selinux

%description
Ircd-hybrid is an advanced IRC server which is most commonly used on the
EFNet IRC network.

%if 0%{?with_selinux}
%package  selinux
Summary:  SELinux policies for %{name}
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): selinux-policy-targeted >= %{selinux_policyver}
Requires(post): policycoreutils
%if 0%{?fedora} > 22
Requires(post): policycoreutils-python-utils
%else
Requires(post): policycoreutils-python
%endif
Requires(post): libselinux-utils

%description selinux
SELinux policy modules for use with %{name}.
%endif # with_selinux


%prep
%setup -q
%patch0 -p1

%if 0%{?with_selinux}
mkdir selinux
cp %{S:21} %{S:22} %{S:23} %{S:24} selinux/
%endif # with_selinux

%build
autoreconf -vi
%configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}/%{name} \
    --program-suffix=-hybrid \
    --enable-openssl \
    --disable-assert
%{__make} %{?_smp_mflags}

%if 0%{?with_selinux}
pushd selinux
make
popd
%endif # with_selinux

%install
%{__rm} -rf %{buildroot}

%makeinstall \
    prefix=%{buildroot}%{_libdir}/%{name} \
    sysconfdir=%{buildroot}%{_sysconfdir}/%{name}

%if 0%{?with_systemd}
%{__install} -m 0755 -D %{SOURCE3} %{buildroot}%{_unitdir}/%{name}.service
%{__install} -m 0644 -D %{SOURCE5} %{buildroot}%{_tmpfilesdir}/%{name}.conf
%{__mkdir_p} %{buildroot}%{_rundir}/%{name}
%else
%{__install} -m 0755 -D %{SOURCE1} %{buildroot}%{_initrddir}/%{name}
%{__install} -m 0640 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__mkdir_p} %{buildroot}%{_var}/run/%{name}
%endif
%{__install} -m 0640 -D %{SOURCE6} %{buildroot}%{_sysconfdir}/%{name}/ircd.conf
%ifarch %{ix86}
sed -i 's|lib64|lib|g' %{buildroot}%{_sysconfdir}/%{name}/ircd.conf
%endif
%{__install} -m 0640 -D %{SOURCE7} %{buildroot}%{_sysconfdir}/%{name}/ircd.motd
%{__install} -m 0644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%{__mkdir_p} %{buildroot}%{_var}/{log,lib}/%{name}/

chmod 755 %{buildroot}%{_libdir}/%{name}/modules/{,autoload/}*.so

# remove tools
rm -rf %{buildroot}%{_bindir}

%if 0%{?with_selinux}
# install SELinux interfaces
%_format INTERFACES $x.if
install -d %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 selinux/$INTERFACES \
    %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}

# install policy modules
%_format MODULES $x.pp.bz2
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 selinux/$MODULES %{buildroot}%{_datadir}/selinux/packages
%endif # with_selinux

%clean
%{__rm} -rf %{buildroot}

%pre
getent group %{name} >/dev/null || groupadd -r %{name}
getent passwd %{name} >/dev/null || \
  useradd -r -g %{name} -d %{_var}/lib/%{name} \
    -s /sbin/nologin -c "IRC service account" %{name}
exit 0

%post
%if 0%{?with_systemd}
%systemd_post %{name}.service
%else
if [ $1 -eq 1 ]; then
    /sbin/chkconfig --add %{name}
fi
%endif

%if 0%{?with_selinux}
%post selinux
# Install all modules in a single transaction
if [ $1 -eq 1 ]; then
    %{_sbindir}/setsebool -P -N global_ssp=1
fi
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
%{_sbindir}/semodule -n -s %{selinuxtype} -i $MODULES
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %relabel_files
fi
%endif # with_selinux

%preun
%if 0%{?with_systemd}
%systemd_preun %{name}.service
%else
if [ $1 -eq 0 ]; then
    /sbin/service %{name} stop &>/dev/null ||:
    /sbin/chkconfig --del %{name}
fi
%endif

%postun
%if 0%{?with_systemd}
%systemd_postun_with_restart %{name}.service
%else
if [ $1 -ge 1 ]; then
    /sbin/service %{name} condrestart &>/dev/null ||:
fi
%endif

%if 0%{?with_selinux}
%postun selinux
if [ $1 -eq 0 ]; then
    %{_sbindir}/semodule -n -r %{modulename} &>/dev/null ||:
    if %{_sbindir}/selinuxenabled ; then
        %{_sbindir}/load_policy
        %relabel_files
    fi
fi
%endif # with_selinux


%files
%defattr(-,root,root,-)
%doc AUTHORS NEWS README doc/{*.txt,technical/}
%{!?_licensedir:%global license %doc}
%license COPYING
%dir %{_sysconfdir}/%{name}/
%exclude %{_sysconfdir}/%{name}/reference.conf
%attr(640,root,%{name}) %config(noreplace) %{_sysconfdir}/%{name}/ircd*
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%if 0%{?with_systemd}
%{_unitdir}/%{name}.service
%{_tmpfilesdir}/%{name}.conf
%attr(750,%{name},root) %dir %{_rundir}/%{name}/
%else
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(750,%{name},root) %dir %{_var}/run/%{name}/
%endif
%attr(750,%{name},root) %dir %{_var}/log/%{name}/
%attr(750,%{name},root) %dir %{_var}/lib/%{name}/
%{_sbindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/%{name}
%{_mandir}/man8/%{name}.8*

%if 0%{?with_selinux}
%files selinux
%defattr(-,root,root,-)
%{_datadir}/selinux/*
%endif # with_selinux

%changelog
* Wed Oct 14 2015 mosquito <sensor.wen@gmail.com> - 8.2.9-1
- Update to 8.2.9
- Add SELinux module (ircd-hybrid 1.0.0)

* Mon Aug 20 2012 Lubomir Rintel (GoodData) <lubo.rintel@gooddata.com> - 7.3.1-2
- Fix lib directory path
- Fix logging

* Fri Aug 21 2009 Keiran "Affix" Smith <fedora@affix.me> - 7.3.1-1
- Update to 7.3.1

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 7.2.3-10
- rebuilt with new openssl

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 7.2.3-7
- rebuild with new openssl

* Thu Jul 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 7.2.3-6
- fix license tag

* Mon Mar 24 2008 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.3-5
- Handle user creation like in guideline

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 7.2.3-4
- Autorebuild for GCC 4.3

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 7.2.3-3
 - Rebuild for deps

* Sat May 05 2007 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.3-2
- Rebuild

* Mon Aug 28 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.3-1
- Update de 7.2.3

* Mon Aug 28 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.2-3
- Rebuild for Fedora Extras 6

* Mon Aug 28 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.2-2
- Rebuild for Fedora Extras 6

* Mon Jul 17 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.2-1
- Update de 7.2.2

* Tue Feb 14 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.1-1
- Update de 7.2.1

* Tue Feb 14 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.0-6
- Rebuild for FC5

* Fri Feb 10 2006 Eric Tanguy <eric.tanguy@univ-nantes.fr> - 7.2.0-5
- Rebuild for FC5

* Fri Dec 09 2005 Eric Tanguy 7.2.0-4
- Modify spec file to help files

* Fri Dec 09 2005 Eric Tanguy 7.2.0-3
- Modify spec file to use configure correctly

* Fri Dec 09 2005 Eric Tanguy 7.2.0-2
- Modify spec file to take into account the 7.2.0 update

* Fri Dec 09 2005 Eric Tanguy 7.2.0-1
- Update to 7.2.0

* Fri Nov 18 2005 Eric Tanguy 7.1.3-11
- modify changelog
- modify abslolute path to relative one for doc/Tao-of-IRC.940110

* Fri Nov 18 2005 Eric Tanguy 7.1.3-10
- modify %%{__mkdir_p} for devel

* Wed Nov 16 2005 Eric Tanguy 7.1.3-9
- Patch to support openssl >= 0.9.6
- Use of sed in place of dos2unix

* Wed Nov 16 2005 Eric Tanguy 7.1.3-8
- Modify source for x86_64 support

* Wed Nov 09 2005 Eric Tanguy 7.1.3-7
- Change ircd's home to %%{_libdir}/ircd

* Mon Nov 07 2005 Eric Tanguy 7.1.3-6
- Modify chkconfig in ircd-hybrid.init
- Modify premission %%{_sysconfdir}/ircd/

* Fri Nov 04 2005 Eric Tanguy 7.1.3-5
- Modify chkconfig in ircd-hybrid.init

* Tue Nov 01 2005 Eric Tanguy 7.1.3-4
- Use fedora-useradd instead of useradd
- Create %%{_var}/lib/ircd/

* Mon Oct 31 2005 Eric Tanguy 7.1.3-3
- Comment obsoletes
- Modify exe permissions for modules/*.so and modules/autoload/*.so

* Sat Oct 22 2005 Eric Tanguy 7.1.3-2
- Improved spec file

* Sun Oct 16 2005 Eric Tanguy 7.1.3-1
- Update to 7.1.3.

* Wed Sep 14 2005 Matthias Saou <http://freshrpms.net/> 7.1.2-1
- Update to 7.1.2.

* Wed Aug 17 2005 Matthias Saou <http://freshrpms.net/> 7.1.1-1
- Update to 7.1.1.

* Mon Feb 16 2004 Matthias Saou <http://freshrpms.net/> 7.0-5
- Adapt the great spec file from PLD.
- Rewrite the init script for Fedora / YDL.

