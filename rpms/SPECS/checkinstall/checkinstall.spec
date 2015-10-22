%global debug_package %{nil}
%global fversion 1.6.2

Name:      checkinstall
Version:   1.6.3
Release:   1%dist
Summary:   CheckInstall installations tracker
License:   GPLv2+
Group:     Development/Tools
Url:       http://asic-linux.com.mx/~izto/checkinstall
Source:    http://checkinstall.izto.org/files/source/%{name}-%{fversion}.tar.gz
# git patch
# git diff 49b8ebd65c62313daaafb063717c7aeb9546829a
Patch0:    checkinstall-latest.patch
Requires:  rpm-build dpkg

%description
CheckInstall keeps track of all the files created or modified by your
installation script ("make install" "make install_modules", "setup", etc),
builds a standard binary package and installs it in your system giving
you the ability to uninstall it with your distribution's standard
package management utilities.

%prep
%setup -q -n %{name}-%{fversion}
%patch0 -p1

%build
make PREFIX=%{_prefix}

%install
# remove space
sed -i 's|[[:space:]]*$||' %{name} %{name}rc-dist installwatch/installwatch makepak

# change files path
sed -i 's|${INSTALLDIR}/lib/checkinstall|/etc|' %{name}
sed -i 's|#PREFIX#|%{_prefix}|' installwatch/installwatch
sed -i 's|/local||' %{name}rc-dist

install -D -m 755 checkinstall %{buildroot}%{_bindir}/checkinstall
install -m 755 installwatch/installwatch %{buildroot}%{_bindir}
install -D -m 755 makepak %{buildroot}%{_sbindir}/makepak
install -D -m 755 installwatch/installwatch.so %{buildroot}%{_libdir}/checkinstall/installwatch.so
install -D -m 644 checkinstallrc-dist %{buildroot}%{_sysconfdir}/checkinstallrc

# locale files
pushd locale
for i in *.mo
do
    LANG=${i/%{name}-/}
    install -D -m 644 $i %{buildroot}%{_datadir}/locale/${LANG%.*}/LC_MESSAGES/%{name}.mo
done
popd

%find_lang %{name}

%files -f %{name}.lang
%doc README RELNOTES FAQ BUGS TODO CREDITS
%license COPYING
%{_bindir}/installwatch
%{_bindir}/checkinstall
%{_sbindir}/makepak
%{_sysconfdir}/checkinstallrc
%dir %{_libdir}/checkinstall/
%{_libdir}/checkinstall/installwatch.so

%changelog
* Thu Oct 22 2015 mosquito <sensor.wen@gmail.com> - 1.6.3-1
- Update to 1.6.3

* Wed Feb 18 2015 luigiwalser <luigiwalser> 1.6.2.16-13.mga5
+ Revision: 815593
- fix patch5 in the patch, not by using a symlink

* Wed Oct 15 2014 umeabot <umeabot> 1.6.2.16-12.mga5
+ Revision: 747332
- Second Mageia 5 Mass Rebuild

* Thu Sep 18 2014 umeabot <umeabot> 1.6.2.16-11.mga5
+ Revision: 693591
- Rebuild to fix library dependencies

* Tue Sep 16 2014 umeabot <umeabot> 1.6.2.16-10.mga5
+ Revision: 678363
- Mageia 5 Mass Rebuild

* Fri Oct 18 2013 umeabot <umeabot> 1.6.2.16-9.mga4
+ Revision: 521392
- Mageia 4 Mass Rebuild

* Tue Jan 22 2013 fwang <fwang> 1.6.2.16-8.mga3
+ Revision: 390731
- update rpm group

* Fri Jan 11 2013 umeabot <umeabot> 1.6.2.16-7.mga3
+ Revision: 347651
- Mass Rebuild - https://wiki.mageia.org/en/Feature:Mageia3MassRebuild

* Mon Jan 07 2013 pterjan <pterjan> 1.6.2.16-6.mga3
+ Revision: 340566
- Replace the patch about glibc minor with one from opensus not needing to be updated for each new glibc

* Fri Jul 13 2012 solbu <solbu> 1.6.2.16-5.mga3
+ Revision: 270553
- imported package checkinstall
- Renamed patches, according to policy.
- Spec cleanup
- Don't ship COPYING and INSTALL

* Tue Dec 06 2011 Götz Waschk <waschk@mandriva.org> 1.6.2.16-4mdv2012.0
+ Revision: 738144
- rebuild
- update patch 3
- yearly rebuild

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.6.2.16-2mdv2011.0
+ Revision: 610134
- rebuild

* Fri Jan 29 2010 Götz Waschk <waschk@mandriva.org> 1.6.2.16-1mdv2010.1
+ Revision: 498052
- new version 1.6.2
- update patch 3 for the new glibc
- add Debian patch to make installwatch build

  + Thierry Vignaud <tvignaud@mandriva.com>
    - rebuild

* Wed Jan 28 2009 Götz Waschk <waschk@mandriva.org> 1.6.2.16-0.3mdv2009.1
+ Revision: 334790
- patch for rpm's new way to set the build root
- update paths, arch and man page compression in patch 0

* Mon Jan 26 2009 Götz Waschk <waschk@mandriva.org> 1.6.2.16-0.2mdv2009.1
+ Revision: 333703
- fix glibc detection
- new git snapshot
- update patch 0
- drop patch 1

* Mon Jan 26 2009 Götz Waschk <waschk@mandriva.org> 1.6.1-7mdv2009.1
+ Revision: 333662
- remove some broken rpm version tests
- update license

* Wed Jul 23 2008 Thierry Vignaud <tvignaud@mandriva.com> 1.6.1-6mdv2009.0
+ Revision: 243862
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Tue Oct 16 2007 Götz Waschk <waschk@mandriva.org> 1.6.1-4mdv2008.1
+ Revision: 99075
- fix path to installwatch.so

* Mon Oct 15 2007 Götz Waschk <waschk@mandriva.org> 1.6.1-3mdv2008.1
+ Revision: 98371
- replace remaining /usr/lib on 64 bit, fixing bug #34775

* Wed Apr 18 2007 Götz Waschk <waschk@mandriva.org> 1.6.1-3mdv2008.0
+ Revision: 14740
- fix for x86_64

* Mon Nov 27 2006 Götz Waschk <waschk@mandriva.org> 1.6.1-2mdv2007.0
+ Revision: 87354
- fix build on 64 bit
- Import checkinstall

* Fri Nov 24 2006 Götz Waschk <waschk@mandriva.org> 1.6.1-1mdv2007.1
- drop patch 1
- New version 1.6.1

* Fri Jul 21 2006 Götz Waschk <waschk@mandriva.org> 1.6.0-1mdv2007.0
- Rebuild

* Mon Feb 13 2006 Götz Waschk <waschk@mandriva.org> 1.6.0-2mdk
- fix bug #21100 (switched options), thanks to danxuliu)

* Fri Aug 12 2005 Götz Waschk <waschk@mandriva.org> 1.6.0-1mdk
- rediff patch, it was partitially merged
- new version

* Tue Aug 09 2005 Götz Waschk <waschk@mandriva.org> 1.6.0-0.beta4.3mdk
- update patch to fix bug 16848 (thanks to sieczka)

* Tue May 24 2005 Götz Waschk <waschk@mandriva.org> 1.6.0-0.beta4.2mdk
- update patch 0 to fix bug 16110 (thanks to Jan Ciger)

* Thu Dec 02 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.0-0.beta4.1mdk
- update patch 0
- new version

* Mon Jun 21 2004 Buchan Milne <bgmilne@linux-mandrake.com> 1.6.0-0.beta3.2mdk
- require rpm-build

* Tue May 04 2004 Götz Waschk <waschk@linux-mandrake.com> 1.6.0-0.beta3.1mdk
- rediff patch
- new version
