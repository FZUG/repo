# Last updated for version 3.14.0
%define debug_package %{nil}
%define glib2_version                  2.38.0
%define gobject_introspection_version  1.39.0
%define python2_version                2.3.5

%if 0%{?fedora} > 12 || 0%{?rhel} > 6
%global with_python3 1
%define python3_version                3.1
%endif

%if 1
  # Verbose build
  %global verbosity V=1
%else
  # Quiet build
  %global verbosity %{nil}
%endif

%global with_check 0

### Abstract ###

Name:		pygobject3
%if 0%{?fedora} >= 22
Version:	3.16.1
%else
Version:	3.14.0
%endif
Release:	2%{?dist}
License:	LGPLv2+ and MIT
Group:		Development/Languages
Summary:	Python 2 bindings for GObject Introspection
URL:		https://live.gnome.org/PyGObject
#VCS: git:git://git.gnome.org/pygobject
Source0:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.16/pygobject-3.16.1.tar.xz
Source1:	http://ftp.gnome.org/pub/GNOME/sources/pygobject/3.14/pygobject-3.14.0.tar.xz

# bug: https://bugs.freedesktop.org/show_bug.cgi?id=44336
Patch0:		01_cairo_region.patch

BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: gobject-introspection-devel >= %{gobject_introspection_version}
BuildRequires: python2-devel >= %{python2_version}
%if 0%{?with_python3}
BuildRequires: python3-devel >= %{python3_version}
BuildRequires: python3-cairo-devel
%endif # if with_python3

BuildRequires: cairo-gobject-devel
BuildRequires: pycairo-devel

# Required by the upstream selftest suite:
%if %{with_check}
%if 0%{?fedora}
# Temporarily disabled pyflakes tests to avoid the build failing due to too new
# pyflakes 0.7.2 in F19
# https://bugzilla.gnome.org/show_bug.cgi?id=701009
#BuildRequires: pyflakes
BuildRequires: python-pep8
%endif
## for the Gdk and Gtk typelibs, used during the test suite:
BuildRequires: gtk3
## for xvfb-run:
BuildRequires: xorg-x11-server-Xvfb
BuildRequires: dejavu-sans-fonts
BuildRequires: dejavu-sans-mono-fonts
BuildRequires: dejavu-serif-fonts
## for dbus-launch, used by test_gdbus:
BuildRequires: dbus-x11
%endif # with_check

Requires: %{name}-base%{?_isa} = %{version}-%{release}

# The cairo override module depends on this
Requires: pycairo%{?_isa}

%description
The %{name} package provides a convenient wrapper for the GObject library
for use in Python programs.

%package base
Summary:	Python 2 bindings for GObject Introspection base package
Group:		Development/Languages
Requires:	gobject-introspection%{?_isa} >= %{gobject_introspection_version}

%description base
This package provides the non-cairo specific bits of the GObject Introspection
library.

%package devel
Summary:	Development files for embedding PyGObject introspection support
Group:		Development/Languages
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	gobject-introspection-devel%{?_isa}

%description devel
This package contains files required to embed PyGObject

%if 0%{?with_python3}
%package -n python3-gobject
Summary:	Python 3 bindings for GObject Introspection
Group:		Development/Languages

# The cairo override module depends on this
Requires:	python3-cairo%{?_isa}
Requires:	gobject-introspection%{?_isa} >= %{gobject_introspection_version}

%description -n python3-gobject
The python3-gobject package provides a convenient wrapper for the GObject 
library and and other libraries that are compatible with GObject Introspection, 
for use in Python 3 programs.

%endif # with_python3

%prep
%if 0%{?fedora} >= 22
%setup -q -b 0 -n pygobject-%{version}
%else
%setup -q -b 1 -n pygobject-%{version}
%endif
%patch0 -p1

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
find %{py3dir} -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'
%endif # with_python3

find -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python}|'

%build
PYTHON=%{__python} 
export PYTHON
%configure
make %{?_smp_mflags} %{verbosity}

%if 0%{?with_python3}
pushd %{py3dir}
PYTHON=%{__python3}
export PYTHON
%configure
make %{_smp_mflags} %{verbosity}
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
PYTHON=%{__python3}
export PYTHON
make DESTDIR=$RPM_BUILD_ROOT install %{verbosity}
popd
%endif # with_python3

make DESTDIR=$RPM_BUILD_ROOT install %{verbosity}
find $RPM_BUILD_ROOT -name '*.la' -delete
find $RPM_BUILD_ROOT -name '*.a' -delete

# Don't include makefiles in the installed docs, in order to avoid creating
# multilib conflicts
rm -rf _docs
mkdir _docs
cp -a examples _docs
rm _docs/examples/Makefile*

%check
%if %{with_check}
# Run the selftests under a temporary xvfb X server (so that they can
# initialize Gdk etc):

# FIXME: disabled for python3
# Currently this fails with python3 with:
#  File "/builddir/build/BUILD/python3-pygobject3-3.3.4-4.fc19/gi/__init__.py", line 23, in <module>
#    from ._gi import _API, Repository
#ValueError: level must be >= 0
# Reported upstream as http://bugs.python.org/issue15610
%if 0
pushd %{py3dir}
PYTHON=%{__python3}
export PYTHON
xvfb-run make DESTDIR=$RPM_BUILD_ROOT check %{verbosity}
popd
%endif # with_python3

xvfb-run make DESTDIR=$RPM_BUILD_ROOT check %{verbosity}

%endif # with_check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(644, root, root, 755)
%{python_sitearch}/gi/_gi_cairo.so

%files base
%defattr(644, root, root, 755)
%doc AUTHORS NEWS README COPYING
%dir %{python_sitearch}/gi
%{python_sitearch}/gi/*
%exclude %{python_sitearch}/gi/_gi_cairo.so
%{python_sitearch}/pygobject-*.egg-info
%{python_sitearch}/pygtkcompat/

%files devel
%defattr(644, root, root, 755)
%doc _docs/*
%dir %{_includedir}/pygobject-3.0/
%{_includedir}/pygobject-3.0/pygobject.h
%{_libdir}/pkgconfig/pygobject-3.0.pc

%if 0%{?with_python3}
%files -n python3-gobject
%defattr(644, root, root, 755)
%doc AUTHORS NEWS README COPYING
%dir %{python3_sitearch}/gi
%{python3_sitearch}/gi/*
%{python3_sitearch}/pygobject-*.egg-info
%{python3_sitearch}/pygtkcompat/

%endif # with_python3

%changelog
* Thu May 07 2015 mosquito <sensor.wen@gmail.com> - 3.16.1-2
- Fixed bug: https://bugs.freedesktop.org/show_bug.cgi?id=44336
- Rebuilt for 3.16.1

* Tue Apr 14 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.1-1
- Update to 3.16.1

* Tue Mar 24 2015 Kalev Lember <kalevlember@gmail.com> - 3.16.0-1
- Update to 3.16.0

* Thu Mar 05 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.91-1
- Update to 3.15.91

* Sat Feb 21 2015 Kalev Lember <kalevlember@gmail.com> - 3.15.0-1
- Update to 3.15.0

* Thu Nov 20 2014 mosquito <sensor.wen@gmail.com> - 3.14.0-2
- Fixed bug: https://bugs.freedesktop.org/show_bug.cgi?id=44336

* Mon Sep 22 2014 Kalev Lember <kalevlember@gmail.com> - 3.14.0-1
- Update to 3.14.0

* Tue Sep 16 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.92-1
- Update to 3.13.92

* Tue Sep 02 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.91-1
- Update to 3.13.91

* Thu Aug 21 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-2
- Backport a fix for virt-manager crash (#1130758)

* Tue Aug 19 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.90-1
- Update to 3.13.90

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.4-1
- Update to 3.13.4

* Tue Jun 24 2014 Richard Hughes <rhughes@redhat.com> - 3.13.3-1
- Update to 3.13.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 26 2014 Kalev Lember <kalevlember@gmail.com> - 3.13.2-1
- Update to 3.13.2
- Drop old testsuite patches

* Mon May 12 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Apr 29 2014 Richard Hughes <rhughes@redhat.com> - 3.13.1-1
- Update to 3.13.1

* Tue Apr 15 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.1-1
- Update to 3.12.1

* Sat Apr 05 2014 Kalev Lember <kalevlember@gmail.com> - 3.12.0-2
- Update dep versions
- Tighten deps with %%_isa

* Mon Mar 24 2014 Richard Hughes <rhughes@redhat.com> - 3.12.0-1
- Update to 3.12.0

* Tue Mar 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.92-1
- Update to 3.11.92

* Tue Mar 04 2014 Richard Hughes <rhughes@redhat.com> - 3.11.91-1
- Update to 3.11.91

* Tue Feb 18 2014 Richard Hughes <rhughes@redhat.com> - 3.11.90-1
- Update to 3.11.90

* Wed Feb 05 2014 Richard Hughes <rhughes@redhat.com> - 3.11.5-1
- Update to 3.11.5

* Tue Jan 14 2014 Richard Hughes <rhughes@redhat.com> - 3.11.4-1
- Update to 3.11.4

* Tue Dec 17 2013 Richard Hughes <rhughes@redhat.com> - 3.11.3-1
- Update to 3.11.3

* Mon Nov 18 2013 Richard Hughes <rhughes@redhat.com> - 3.11.2-1
- Update to 3.11.2

* Tue Oct 29 2013 Richard Hughes <rhughes@redhat.com> - 3.11.1-1
- Update to 3.11.1

* Wed Sep 25 2013 Kalev Lember <kalevlember@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Wed Sep 18 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.92-1
- Update to 3.9.92

* Tue Sep 03 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.91-1
- Update to 3.9.91

* Thu Aug 22 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.90-1
- Update to 3.9.90

* Fri Aug  9 2013 Daniel Drake <dsd@laptop.org> - 3.9.5-1
- Update to 3.9.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.2-1
- Update to 3.9.2

* Sun Jun 02 2013 Kalev Lember <kalevlember@gmail.com> - 3.9.1-2
- Disable pyflakes tests to avoid failures with too new pyflakes 0.7.2

* Fri May 10 2013 Richard Hughes <rhughes@redhat.com> - 3.9.1-1
- Update to 3.9.1

* Thu Apr 25 2013 Peter Robinson <pbrobinson@fedoraproject.org> 3.8.1-2
- Add upstream patch to fix Sugar (RHBZ 947538)

* Mon Apr 15 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Tue Apr  2 2013 David Malcolm <dmalcolm@redhat.com> - 3.8.0-2
- add workarounds for ppc64 (rhbz#924425)

* Tue Mar 26 2013 Kalev Lember <kalevlember@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Wed Mar 20 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.92-1
- Update to 3.7.92

* Thu Mar  7 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.91-1
- Update to 3.7.91

* Thu Feb 21 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.90-1
- Update to 3.7.90

* Wed Feb 06 2013 Kalev Lember <kalevlember@gmail.com> - 3.7.5.1-1
- Update to 3.7.5.1
- Re-enable tests

* Wed Jan 16 2013 Matthias Clasen <mclasen@redhat.com> - 3.7.4-1
- Update to 3.7.4

* Fri Dec 28 2012 Dan Horák <dan[at]danny.cz> - 3.7.3-2
- Fix GBytes test (gnome#690837)

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.3-1
- Update to 3.7.3
- Drop upstreamed patches; rebase the ignore-more-pep8-errors patch

* Thu Dec 13 2012 Ray Strode <rstrode@redhat.com> 3.7.1-3
- Split non-cairo parts into a subpackage

* Mon Nov 12 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-2
- Remove lib64 rpaths (#817701)
- Move code examples to the -devel subpackage and fix the multilib
  conflict (#831434)

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 3.7.1-1
- Update to 3.7.1

* Tue Nov  6 2012 Daniel Drake <dsd@laptop.org> - 3.4.1.1-2
- Upstream fix for property lookup; needed for basic Sugar operation.

* Wed Oct 17 2012 Kalev Lember <kalevlember@gmail.com> - 3.4.1.1-1
- Update to 3.4.1.1

* Thu Sep 13 2012 Daniel Drake <dsd@laptop.org> - 3.3.91-1
- Latest version; upstreamed patches dropped

* Wed Aug 15 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-9
- avoid dragging pyflakes and python-pep8 into RHEL (patch 7)

* Fri Aug 10 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-8
- add endianness patch (rhbz#841596; attachment 603634)

* Fri Aug 10 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-7
- update endianness patch for rhbz#841596 (to attachment 603367)

* Thu Aug  9 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-6
- fix issues on big-endian 64-bit machines (rhbz#841596, rhbz#842880)

* Thu Aug  9 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-5
- use xvfb-run in selftests; update known failures

* Wed Aug  8 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-4
- add a %%check check; add V=1 to all make invocations

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.4-2
- remove rhel logic from with_python3 conditional

* Tue Jul 17 2012 Richard Hughes <hughsient@gmail.com> - 3.3.4-1
- Update to 3.3.4

* Tue Jun 26 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.3.1-2
- fix a segfault when dealing with mismatched .so/typelib files

* Mon Jun 25 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 3.3.3.1-1
- Update to 3.3.3.1

* Tue Jun 19 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.2-1
- Update to 3.3.2

* Sat May 05 2012 Kalev Lember <kalevlember@gmail.com> - 3.3.1-1
- Update to 3.3.1
- Dropped the now unneeded -lm patch

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Thu Mar 22 2012 Matthias Clasen <mclasen@redhat.com> - 3.1.93-1
- Update to 3.1.93

* Wed Mar 21 2012 Kalev Lember <kalevlember@gmail.com> - 3.1.92-1
- Update to 3.1.92

* Sun Feb 26 2012 Matthias Clasen <mclasen@redhat.com> - 3.1.1-1
- Update to 3.1.1

* Tue Feb  7 2012 Matthias Clasen <mclasen@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.0.3-1
- udpate to 3.0.3

* Sat Oct 22 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.0.2-1
- udpate to 3.0.2

* Fri Sep 30 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 3.0.1-1
- udpate to 3.0.1

* Tue Sep 20 2011 Matthias Clasen <mclasen@redhat.com> - 3.0.0-1
- Update to 3.0.0

* Thu Sep 15 2011 John (J5) Palmieri <johnp@gnome.org> - 2.90.4-1
- update to 2.90.4
- get rid of packaging cruft that is taken care of by upstream now

* Wed Aug 31 2011 Ignacio Casal Quinteiro <icq@gnome.org> - 2.90.3-1
- udpate to 2.90.3

* Mon Aug 22 2011 John (J5) Palmieri <johnp@redhat.com> - 2.90.2-3
- remove some old requires

* Fri Aug 19 2011 John (J5) Palmieri <johnp@redhat.com> - 2.90.2-2
- fix up issues uncovered during package review
- disable docs because they still reference the static bindings 
  and upstream is working on new documentation

* Thu Aug 18 2011 John (J5) Palmieri <johnp@redhat.com> - 2.90.2-1
- Initial package
