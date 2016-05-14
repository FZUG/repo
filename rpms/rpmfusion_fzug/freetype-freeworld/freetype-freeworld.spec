Summary: A free and portable font rendering engine
Name: freetype-freeworld
Version: 2.6.3
Release: 1%{?dist}
License: (FTL or GPLv2+) and BSD and MIT and Public Domain and zlib with acknowledgement
URL: http://www.freetype.org
Source:  http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2

Patch21:  freetype-2.5.2-enable-spr.patch

# Enable otvalid and gxvalid modules
Patch46:  freetype-2.2.1-enable-valid.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=678397
Patch93:  freetype-2.5.5-thread-safety.patch

## Security fixes:
# none needed yet

Provides: freetype-bytecode
Provides: freetype-subpixel

Requires:      /etc/ld.so.conf.d
BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyphs. FreeType is not a font server or a complete
text-rendering library.

This version is compiled with the patented subpixel rendering enabled.
It transparently overrides the system library using ld.so.conf.d.


%prep
%setup -q -n freetype-%{version}

%patch21 -p1 -b .enable-spr

%patch46 -p1 -b .enable-valid

#patch93 -p1 -b .thread-safety


%build
%configure --disable-static \
           --with-zlib=yes \
           --with-bzip2=yes \
           --with-png=yes \
           --with-harfbuzz=no
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool
make %{?_smp_mflags}

%install
umask 0022

%make_install

# Don't package static a or .la files nor devel files
rm -rf %{buildroot}%{_libdir}/*.{a,la,so} \
       %{buildroot}%{_libdir}/pkgconfig %{buildroot}%{_bindir} \
       %{buildroot}%{_datadir}/aclocal %{buildroot}%{_includedir} \
       %{buildroot}%{_mandir}

# Move library to avoid conflict with official FreeType package
mkdir %{buildroot}%{_libdir}/%{name}
mv -f %{buildroot}%{_libdir}/libfreetype.so.* \
      %{buildroot}%{_libdir}/%{name}

# Register the library directory in /etc/ld.so.conf.d
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d
echo "%{_libdir}/%{name}" \
     >%{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/%{name}
%license docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%doc ChangeLog README
%config(noreplace) %{_sysconfdir}/ld.so.conf.d/%{name}-%{_arch}.conf

%changelog
* Sat May 14 2016 mosquito <sensor.wen@gmail.com> 2.6.3-1
- Update to 2.6.3

* Sun Aug 30 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.5-2
- Add freetype-2.5.5-thread-safety.patch (backport patches for thread-safety)
  from Fedora freetype (backported from upstream 2.5.6) (rh#678397)

* Tue Jun 02 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.5-1
- Update to 2.5.5 (matches Fedora freetype, rh#1178876)
- Pass explicit configure flags to enable/disable required libraries (as Fedora)
- Drop all backported security patches, already fixed in upstream 2.5.5
- Mark license files as %%license instead of %%doc

* Tue Feb 24 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.3-5
- Add freetype-2.5.3-pcf-read-a.patch and freetype-2.5.3-pcf-read-b.patch ("Work
  around behaviour of X11's `pcfWriteFont' and `pcfReadFont' functions") from
  Fedora freetype, fixes regression from CVE-2014-9671 fix (rh#1195652)

* Wed Feb 18 2015 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.3-4
- Add freetype-2.5.3-CVE-2014-9656.patch from Fedora freetype (rh#1191099)
    (Check `p' before `num_glyphs'.)
- Add freetype-2.5.3-CVE-2014-9657.patch from Fedora freetype (rh#1191099)
    (Check minimum size of `record_size'.)
- Add freetype-2.5.3-CVE-2014-9658.patch from Fedora freetype (rh#1191099)
    (Use correct value for minimum table length test.)
- Add freetype-2.5.3-CVE-2014-9675.patch from Fedora freetype (rh#1191193)
    (New macro that checks one character more than `strncmp'.)
- Add freetype-2.5.3-CVE-2014-9660.patch from Fedora freetype (rh#1191099)
    (Check `_BDF_GLYPH_BITS'.)
- Add freetype-2.5.3-CVE-2014-9661a.patch from Fedora freetype (rh#1191099)
    (Initialize `face->ttf_size'. Always set `face->ttf_size' directly.)
- Add freetype-2.5.3-CVE-2014-9661b.patch from Fedora freetype (rh#1191099)
    (Exclusively use the `truetype' font driver for loading the font contained
     in the `sfnts' array.)
- Add freetype-2.5.3-CVE-2014-9662.patch from Fedora freetype (rh#1191099)
    (Handle return values of point allocation routines.)
- Add freetype-2.5.3-CVE-2014-9663.patch from Fedora freetype (rh#1191099)
    (Fix order of validity tests.)
- Add freetype-2.5.3-CVE-2014-9664a.patch from Fedora freetype (rh#1191099)
    (Add another boundary testing.)
- Add freetype-2.5.3-CVE-2014-9664b.patch from Fedora freetype (rh#1191099)
    (Fix boundary testing.)
- Add freetype-2.5.3-CVE-2014-9665.patch from Fedora freetype (rh#1191099)
    (Protect against too large bitmaps.)
- Add freetype-2.5.3-CVE-2014-9666.patch from Fedora freetype (rh#1191099)
    (Protect against addition and multiplication overflow.)
- Add freetype-2.5.3-CVE-2014-9667.patch from Fedora freetype (rh#1191099)
    (Protect against addition overflow.)
- Add freetype-2.5.3-CVE-2014-9668.patch from Fedora freetype (rh#1191099)
    (Protect against addition overflow.)
- Add freetype-2.5.3-CVE-2014-9669.patch from Fedora freetype (rh#1191099)
    (Protect against overflow in additions and multiplications.)
- Add freetype-2.5.3-CVE-2014-9670.patch from Fedora freetype (rh#1191099)
    (Add sanity checks for row and column values.)
- Add freetype-2.5.3-CVE-2014-9671.patch from Fedora freetype (rh#1191099)
    (Check `size' and `offset' values.)
- Add freetype-2.5.3-CVE-2014-9672.patch from Fedora freetype (rh#1191095)
    (Prevent a buffer overrun caused by a font including too many (> 63) strings
     to store names[] table.)
- Add freetype-2.5.3-CVE-2014-9673.patch from Fedora freetype (rh#1191096)
    (Fix integer overflow by a broken POST table in resource-fork.)
- Add freetype-2.5.3-CVE-2014-9674a.patch from Fedora freetype (rh#1191191)
    (Fix integer overflow by a broken POST table in resource-fork.)
- Add freetype-2.5.3-unsigned-long.patch from Fedora freetype (rh#1191191)
    (Use unsigned long variables to read the lengths in POST fragments.)
- Add freetype-2.5.3-CVE-2014-9674b.patch from Fedora freetype (rh#1191191)
    (Additional overflow check in the summation of POST fragment lengths.)

* Fri Dec 12 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.3-3
- Add freetype-2.5.3-hintmask.patch from Fedora freetype (rh#1172634)
    (Don't append to stem arrays after hintmask is constructed.)
- Add freetype-2.5.3-hintmap.patch from Fedora freetype (rh#1172634)
    (Suppress an assert when hintMap.count == 0 in specific situations.)

* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 2.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 11 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.3-1
- Update to 2.5.3 (matches Fedora freetype, rh#1073923)
- Also delete the new manpages (-devel material)
- Specfile cleanups (remove obsolete specfile idioms)
- Enable support for bzip2 compressed fonts

* Fri Jan 17 2014 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.2-1
- Update to 2.5.2 (matches Fedora freetype, rh#1034065)
- Fix incorrect weekdays in the changelog
- Drop upstreamed 0001-Fix-vertical-size-of-emboldened-glyphs.patch
- Rebase enable-spr patch, ftoption.h moved

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.5.0.1-3
- Rebuilt

* Sat Sep 21 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.0.1-2
- Apply 0001-Fix-vertical-size-of-emboldened-glyphs.patch from Fedora

* Sun Sep 15 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.5.0.1-1
- Update to 2.5.0.1 (matches Fedora freetype)
- BuildRequires: libpng-devel
- Drop obsolete backported freetype-2.4.12-enable-adobe-cff-engine.patch

* Thu May 09 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.12-1
- Update to 2.4.12 (matches Fedora freetype)
- Drop freetype-2.4.11-fix-emboldening.patch (fixed upstream)
- Add freetype-2.4.12-enable-adobe-cff-engine.patch from Fedora (rh#959771)

* Tue Mar 19 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.11-2
- Add freetype-2.4.11-fix-emboldening.patch from Fedora freetype (rh#891457)
- Fix License tag

* Thu Jan 03 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.11-1
- Update to 2.4.11 (matches Fedora freetype, rh#889177)

* Mon Jul 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.10-1
- Update to 2.4.10 (matches Fedora freetype, rh#832651)
- Drop upstreamed patches (CVE-2012-1139, CVE-2012-1141, backported bugfixes)

* Mon Apr 02 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.9-1
- Update to 2.4.9 (matches Fedora freetype, fixes various CVEs (rh#806270))
- Add additional security and bugfix patches from Fedora freetype-2.4.9-1

* Wed Nov 23 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.8-2
- Rebuild for #2031

* Thu Nov 17 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.8-1
- Update to 2.4.8 (matches Fedora freetype, fixes CVE-2011-3439 (rh#753837))
- Drop CVE-2011-3256 patch, fixed upstream
- Drop CVE-2010-3311 patch, fixed differently upstream for a while, and the
  additional change added by that patch is no longer needed

* Fri Oct 28 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.4.6-3
- Fix for glibc bug rhbz#747377

* Sun Oct 23 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.6-2
- Add freetype-2.4.6-CVE-2011-3256.patch from Fedora freetype (rh#749174)
    (Handle some border cases)

* Thu Aug 04 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.6-1
- Update to 2.4.6 (matches Fedora freetype)
- Drop freetype-2.4.5-CVE-2011-0226.patch (fixed upstream)

* Mon Jul 25 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.5-1
- Update to 2.4.5 (matches Fedora freetype)
- Drop upstreamed auto-autohint patches
- Add freetype-2.4.5-CVE-2011-0226.patch from Fedora freetype (rh#723469)
    (Add better argument check for `callothersubr'.)
    - based on patches by Werner Lemberg,
      Alexei Podtelezhnikov and Matthias Drochner

* Tue Mar 08 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.4-3
- Fix autohinting fallback (rh#547532): Ignore CFF-based OTFs.

* Sun Feb 20 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.4-2
- Update the description to reflect that the bytecode interpreter was reenabled
  in the stock Fedora freetype, hopefully this time for good (see rh#612395).
- Drop conditionals (again), always build the bytecode interpreter (now also in
  Fedora) and subpixel rendering (as that's the only reason to build
  freetype-freeworld at all)
- Fall back to autohinting if a TTF/OTF doesn't contain any bytecode (rh#547532,
  patch backported from upstream git, also in Fedora freetype)

* Thu Dec 02 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.4-1
- Update to 2.4.4 (matches Fedora freetype)
- Drop freetype-2.4.3-CVE-2010-3855.patch (fixed upstream)

* Mon Nov 15 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.3-2
- Add freetype-2.4.3-CVE-2010-3855.patch
    (Protect against invalid `runcnt' values.)
- Resolves: rh#651764

* Tue Oct 26 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.3-1
- Update to 2.4.3 (matches Fedora freetype)

* Wed Oct 06 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.2-2
- Add freetype-2.4.2-CVE-2010-3311.patch
    (Don't seek behind end of stream.)
- Resolves: rh#638522

* Wed Oct 06 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.4.2-1
- Update to 2.4.2 (matches Fedora freetype, fixes several security issues)
- Update the description to reflect that the bytecode interpreter was disabled
  in the stock Fedora freetype again.
- Restore the conditionals (for the above reason).
- Remove unused with_xfree86 conditional.

* Wed Dec 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.11-2
- Drop conditionals, always build the bytecode interpreter (now also in Fedora)
  and subpixel rendering (as that's the only reason to build freetype-freeworld
  at all)
- Drop 99-DejaVu-autohinter-only.conf

* Wed Dec 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.11-1
- Update to 2.3.11 (matches Fedora freetype, fixes aliasing issue rh#513582)
- Drop upstreamed memcpy-fix patch

* Sat Mar 28 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.9-2
- Provides freetype-bytecode and freetype-subpixel (rh#155210)

* Fri Mar 20 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.9-1
- Update to 2.3.9

* Thu Jan 15 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.8-1
- Update to 2.3.8
- Remove freetype-autohinter-ligature.patch (fixed upstream)

* Mon Dec 08 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.7-2
- Add freetype-autohinter-ligature.patch by Behdad Esfahbod (rh#368561)

* Tue Sep 02 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.7-1
- Update to 2.3.7

* Sat Aug 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 2.3.6-2
- rebuild for RPM Fusion

* Thu Jun 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.6-1
- Update to 2.3.6 (also fixes CVE-2008-1806, CVE-2008-1807 and CVE-2008-1808)
- Drop multilib patch (outdated, not needed since we don't ship a -devel)

* Tue Sep 18 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.5-3.lvn8
- Update to 2.3.5
- Fix builds/unix/libtool to not emit rpath into binaries (#225770,
  Adam Jackson)
- Drop unused freetype-doc tarball
- Use full URL for Source tag
- Fix License tag
- Ship license as %%doc

* Thu Apr 12 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> 2.3.4-1.lvn7
- Rename to freetype-freeworld
- Enable bytecode interpreter and subpixel rendering
- Remove demos
- Remove devel subpackage, delete devel files after install
- Remove triggerpostun
- Install library to libdir/freetype-freeworld
- Register in /etc/ld.so.conf.d (trick lifted from ATLAS specfile)
- Set umask before install
- Disable BCI for DejaVu and Vera because it changes the font weight
- Update description

* Thu Apr 05 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.4-1
- Update to 2.3.4.

* Thu Apr 05 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.3-2
- Include new demos ftgrid and ftdiff in freetype-demos. (#235478)

* Thu Apr 05 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.3-1
- Update to 2.3.3.

* Fri Mar 09 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.2-1
- Update to 2.3.2.

* Fri Feb 02 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.1-1
- Update to 2.3.1.

* Wed Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.0-2
- Add without_subpixel_rendering.
- Drop X11_PATH=/usr.  Not needed anymore.

* Wed Jan 17 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.3.0-1
- Update to 2.3.0.
- Drop upstream patches.
- Drop -fno-strict-aliasing, it should just work.
- Fix typo in ftconfig.h generation.

* Tue Jan 09 2007 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-16
- Backport binary-search fixes from HEAD
- Add freetype-2.2.1-ttcmap.patch
- Resolves: #208734

- Fix rendering issue with some Asian fonts.
- Add freetype-2.2.1-fix-get-orientation.patch
- Resolves: #207261

- Copy non-X demos even if not compiling with_xfree86.

- Add freetype-2.2.1-zero-item-size.patch, to fix crasher.
- Resolves #214048

- Add X11_PATH=/usr to "make"s, to find modern X.
- Resolves #212199

* Mon Sep 11 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-10
- Fix crasher https://bugs.freedesktop.org/show_bug.cgi?id=6841
- Add freetype-2.2.1-memcpy-fix.patch

* Thu Sep 07 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-9
- Add BuildRequires: libX11-devel (#205355)

* Tue Aug 29 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-8
- Add freetype-composite.patch and freetype-more-composite.patch
  from upstream. (#131851)

* Mon Aug 28 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.1-7
- Require pkgconfig in the -devel package

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-6
- pass --disable-static to %%configure. (#172628)

* Thu Aug 17 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-5
- don't package static libs

* Sun Aug 13 2006 Matthias Clasen <mclasen@redhat.com> - 2.2.1-4.fc6
- fix a problem with the multilib patch (#202366)

* Thu Jul 27 2006 Matthias Clasen  <mclasen@redhat.com> - 2.2.1-3
- fix multilib issues

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.2.1-2.1
- rebuild

* Fri Jul 07 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-2
- Remove unused BuildRequires

* Fri Jul 07 2006 Behdad Esfahbod <besfahbo@redhat.com> 2.2.1-1
- Update to 2.2.1
- Remove FreeType 1, to move to extras
- Install new demos ftbench, ftchkwd, ftgamma, and ftvalid
- Enable modules gxvalid and otvalid

* Wed May 17 2006 Karsten Hopp <karsten@redhat.de> 2.1.10-6
- add buildrequires libICE-devel, libSM-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.1.10-5.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.1.10-5.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 18 2005 Bill Nottingham  <notting@redhat.com> 2.1.10-5
- Remove references to obsolete /usr/X11R6 paths

* Tue Nov  1 2005 Matthias Clasen  <mclasen@redhat.com> 2.1.10-4
- Switch requires to modular X

* Fri Oct 21 2005 Matthias Clasen  <mclasen@redhat.com> 2.1.10-3
- BuildRequire gettext 

* Wed Oct 12 2005 Jason Vas Dias <jvdias@redhat.com> 2.1.10-2
- fix 'without_bytecode_interpreter 0' build: freetype-2.1.10-enable-ft2-bci.patch

* Fri Oct  7 2005 Matthias Clasen  <mclasen@redhat.com> 2.1.10-1
- Update to 2.1.10
- Add necessary fixes

* Tue Aug 16 2005 Kristian Høgsberg <krh@redhat.com> 2.1.9-4
- Fix freetype-config on 64 bit platforms.

* Thu Jul 07 2005 Karsten Hopp <karsten@redhat.de> 2.1.9-3
- BuildRequires xorg-x11-devel

* Fri Mar  4 2005 David Zeuthen <davidz@redhat.com> - 2.1.9-2
- Rebuild

* Wed Aug  4 2004 Owen Taylor <otaylor@redhat.com> - 2.1.9-1
- Upgrade to 2.1.9
- Since we are just using automake for aclocal, use it unversioned,
  instead of specifying 1.4.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 19 2004 Owen Taylor <otaylor@redhat.com> 2.1.7-4
- Add patch from freetype CVS to fix problem with eexec (#117743)
- Add freetype-devel to buildrequires and -devel requires
  (Maxim Dzumanenko, #111108)

* Wed Mar 10 2004 Mike A. Harris <mharris@redhat.com> 2.1.7-3
- Added -fno-strict-aliasing to CFLAGS and CXXFLAGS to try to fix SEGV and
  SIGILL crashes in mkfontscale which have been traced into freetype and seem
  to be caused by aliasing issues in freetype macros (#118021)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com> 2.1.7-2.1
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com> 2.1.7-2
- rebuilt

* Fri Jan 23 2004 Owen Taylor <otaylor@redhat.com> 2.1.7-1
- Upgrade to 2.1.7

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling without the demos as that requires XFree86
  (this allows bootstrapping XFree86 on new archs)

* Fri Aug  8 2003 Elliot Lee <sopwith@redhat.com> 2.1.4-4.1
- Rebuilt

* Tue Jul  8 2003 Owen Taylor <otaylor@redhat.com> 2.1.4-4.0
- Bump for rebuild

* Wed Jun 25 2003 Owen Taylor <otaylor@redhat.com> 2.1.4-3
- Fix crash with non-format-0 hdmx tables (found by David Woodhouse)

* Mon Jun  9 2003 Owen Taylor <otaylor@redhat.com> 2.1.4-1
- Version 2.1.4
- Relibtoolize to get deplibs right for x86_64
- Use autoconf-2.5x for freetype-1.4 to fix libtool-1.5 compat problem (#91781)
- Relativize absolute symlinks to fix the -debuginfo package 
  (#83521, Mike Harris)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 22 2003 Jeremy Katz <katzj@redhat.com> 2.1.3-9
- fix build with gcc 3.3

* Tue Feb 25 2003 Owen Taylor <otaylor@redhat.com>
- Add a memleak fix for the gzip backend from Federic Crozat

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 2.1.3-7
- Run libtoolize/aclocal/autoconf so that libtool knows to generate shared libraries 
  on ppc64.
- Use _smp_mflags (for freetype 2.x only)

* Tue Feb  4 2003 Owen Taylor <otaylor@redhat.com>
- Switch to using %%configure (should fix #82330)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Jan  6 2003 Owen Taylor <otaylor@redhat.com> 2.1.3-4
- Make FreeType robust against corrupt fonts with recursive composite 
  glyphs (#74782, James Antill)

* Thu Jan  2 2003 Owen Taylor <otaylor@redhat.com> 2.1.3-3
- Add a patch to implement FT_LOAD_TARGET_LIGHT
- Fix up freetype-1.4-libtool.patch 

* Thu Dec 12 2002 Mike A. Harris <mharris@redhat.com> 2.1.3-2
- Update to freetype 2.1.3
- Removed ttmkfdir sources and patches, as they have been moved from the
  freetype packaging to XFree86 packaging, and now to the ttmkfdir package
- Removed patches that are now included in 2.1.3:
  freetype-2.1.1-primaryhints.patch, freetype-2.1.2-slighthint.patch,
  freetype-2.1.2-bluefuzz.patch, freetype-2.1.2-stdw.patch,
  freetype-2.1.2-transform.patch, freetype-2.1.2-autohint.patch,
  freetype-2.1.2-leftright.patch
- Conditionalized inclusion of freetype 1.4 library.

* Wed Dec 04 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- disable perl, it is not used at all

* Tue Dec 03 2002 Elliot Lee <sopwith@redhat.com> 2.1.2-11
- Instead of removing unpackaged file, include it in the package.

* Sat Nov 30 2002 Mike A. Harris <mharris@redhat.com> 2.1.2-10
- Attempted to fix lib64 issue in freetype-demos build with X11_LINKLIBS
- Cleaned up various _foodir macros throughtout specfile
- Removed with_ttmkfdir build option as it is way obsolete

* Fri Nov 29 2002 Tim Powers <timp@redhat.com> 2.1.2-8
- remove unpackaged files from the buildroot

* Wed Aug 28 2002 Owen Taylor <otaylor@redhat.com>
- Fix a bug with PCF metrics

* Fri Aug  9 2002 Owen Taylor <otaylor@redhat.com>
- Backport autohinter improvements from CVS

* Tue Jul 23 2002 Owen Taylor <otaylor@redhat.com>
- Fix from CVS for transformations (#68964)

* Tue Jul  9 2002 Owen Taylor <otaylor@redhat.com>
- Add another bugfix for the postscript hinter

* Mon Jul  8 2002 Owen Taylor <otaylor@redhat.com>
- Add support for BlueFuzz private dict value, fixing rendering 
  glitch for Luxi Mono.

* Wed Jul  3 2002 Owen Taylor <otaylor@redhat.com>
- Add an experimental FT_Set_Hint_Flags() call

* Mon Jul  1 2002 Owen Taylor <otaylor@redhat.com>
- Update to 2.1.2
- Add a patch fixing freetype PS hinter bug

* Fri Jun 21 2002 Mike A. Harris <mharris@redhat.com> 2.1.1-2
- Added ft rpm build time conditionalizations upon user requests

* Tue Jun 11 2002 Owen Taylor <otaylor@redhat.com> 2.1.1-1
- Version 2.1.1

* Mon Jun 10 2002 Owen Taylor <otaylor@redhat.com>
- Add a fix for PCF character maps

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Mike A. Harris <mharris@redhat.com> 2.1.0-2
- Updated freetype to version 2.1.0
- Added libtool fix for freetype 1.4 (#64631)

* Wed Mar 27 2002 Nalin Dahyabhai <nalin@redhat.com> 2.0.9-2
- use "libtool install" instead of "install" to install some binaries (#62005)

* Mon Mar 11 2002 Mike A. Harris <mharris@redhat.com> 2.0.9-1
- Updated to freetype 2.0.9

* Sun Feb 24 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-4
- Added proper docs+demos source for 2.0.8.

* Sat Feb 23 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-3
- Added compat patch so 2.x works more like 1.x
- Rebuilt with new build toolchain

* Fri Feb 22 2002 Mike A. Harris <mharris@redhat.com> 2.0.8-2
- Updated to freetype 2.0.8, however docs and demos are stuck at 2.0.7
  on the freetype website.  Munged specfile to deal with the problem by using
  {oldversion} instead of version where appropriate.  <sigh>

* Sat Feb  2 2002 Tim Powers <timp@redhat.com> 2.0.6-3
- bumping release so that we don't collide with another build of
  freetype, make sure to change the release requirement in the XFree86
  package

* Fri Feb  1 2002 Mike A. Harris <mharris@redhat.com> 2.0.6-2
- Made ttmkfdir inclusion conditional, and set up a define to include
  ttmkfdir in RHL 7.x builds, since ttmkfdir is now moving to the new
  XFree86-font-utils package.

* Wed Jan 16 2002 Mike A. Harris <mharris@redhat.com> 2.0.6-1
- Updated freetype to version 2.0.6

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 2.0.5-4
- automated rebuild

* Fri Nov 30 2001 Elliot Lee <sopwith@redhat.com> 2.0.5-3
- Fix bug #56901 (ttmkfdir needed to list Unicode encoding when generating
  font list). (ttmkfdir-iso10646.patch)
- Use _smp_mflags macro everywhere relevant. (freetype-pre1.4-make.patch)
- Undo fix for #24253, assume compiler was fixed.

* Mon Nov 12 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.5-2
- Fix build with gcc 3.1 (#56079)

* Sun Nov 11 2001 Mike A. Harris <mharris@redhat.com> 2.0.5-1
- Updated freetype to version 2.0.5

* Sat Sep 22 2001 Mike A. Harris <mharris@redhat.com> 2.0.4-2
- Added new subpackage freetype-demos, added demos to build
- Disabled ftdump, ftlint in utils package favoring the newer utils in
  demos package.

* Tue Sep 11 2001 Mike A. Harris <mharris@redhat.com> 2.0.4-1
- Updated source to 2.0.4
- Added freetype demo's back into src.rpm, but not building yet.

* Wed Aug 15 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-7
- Changed package to use {findlang} macro to fix bug (#50676)

* Sun Jul 15 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-6
- Changed freetype-devel to group Development/Libraries (#47625)

* Mon Jul  9 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.3-5
- Fix up FT1 headers to please Qt 3.0.0 beta 2

* Sun Jun 24 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.0.3-4
- Add ft2build.h to -devel package, since it's included by all other
  freetype headers, the package is useless without it

* Thu Jun 21 2001 Nalin Dahyabhai <nalin@redhat.com> 2.0.3-3
- Change "Requires: freetype = name/ver" to "freetype = version/release",
  and move the requirements to the subpackages.

* Mon Jun 18 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-2
- Added "Requires: freetype = name/ver"

* Tue Jun 12 2001 Mike A. Harris <mharris@redhat.com> 2.0.3-1
- Updated to Freetype 2.0.3, minor specfile tweaks.
- Freetype2 docs are is in a separate tarball now. Integrated it.
- Built in new environment.

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Sat Jan 20 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Build ttmkfdir with -O0, workaround for Bug #24253

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- libtool is used to build libttf, so use libtool to link ttmkfdir with it
- fixup a paths for a couple of missing docs

* Thu Jan 11 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Update ttmkfdir

* Wed Dec 27 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Update to 2.0.1 and 1.4
- Mark locale files as such

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- move .la file to devel pkg
- FHS paths

* Thu Feb 17 2000 Preston Brown <pbrown@redhat.com>
- revert spaces patch, fix up some foundry names to match X ones

* Mon Feb 07 2000 Nalin Dahyabhai <nalin@redhat.com>
- add defattr, ftmetric, ftsbit, ftstrtto per bug #9174

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary

* Wed Jan 12 2000 Preston Brown <pbrown@redhat.com>
- make ttmkfdir replace spaces in family names with underscores (#7613)

* Tue Jan 11 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 1.3.1
- handle RPM_OPT_FLAGS

* Wed Nov 10 1999 Preston Brown <pbrown@redhat.com>
- fix a path for ttmkfdir Makefile

* Thu Aug 19 1999 Preston Brown <pbrown@redhat.com>
- newer ttmkfdir that works better, moved ttmkfdir to /usr/bin from /usr/sbin
- freetype utilities moved to subpkg, X dependency removed from main pkg
- libttf.so symlink moved to devel pkg

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 5)

* Thu Mar 18 1999 Cristian Gafton <gafton@redhat.com>
- fixed the %doc file list

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb 15 1999 Preston Brown <pbrown@redhat.com>
- added ttmkfdir

* Tue Feb 02 1999 Preston Brown <pbrown@redhat.com>
- update to 1.2

* Thu Jan 07 1999 Cristian Gafton <gafton@redhat.com>
- call libtoolize to sanitize config.sub and get ARM support
- dispoze of the patch (not necessary anymore)

* Wed Oct 21 1998 Preston Brown <pbrown@redhat.com>
- post/postun sections for ldconfig action.

* Tue Oct 20 1998 Preston Brown <pbrown@redhat.com>
- initial RPM, includes normal and development packages.
