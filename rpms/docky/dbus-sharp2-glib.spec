%global debug_package %{nil}

Name:    dbus-sharp2-glib
Version: 0.6.0
Release: 1%{?dist}
Summary: C# bindings for D-Bus glib main loop integration
Group:   System Environment/Libraries
License: MIT
URL:     https://github.com/mono/dbus-sharp-glib
Source0: %{url}/releases/download/v0.6/dbus-sharp-glib-%{version}.tar.gz
BuildRequires: mono-devel
BuildRequires: dbus-sharp2-devel >= 0.7.0
# Mono only available on these
ExclusiveArch: %{mono_arches}

%description
C# bindings for D-Bus glib main loop integration

%package devel
Summary: Development files for D-Bus Sharp
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
Development files for D-Bus Sharp development.

%prep
%setup -q -n dbus-sharp-glib-%{version}
sed -i "s|gmcs|mcs|g" configure configure.ac

%build
export MONO_SHARED_DIR=%{_builddir}/%{?buildsubdir}
%configure --libdir=%{_prefix}/lib
%make_build

%install
%make_install

%{__mkdir_p} %{buildroot}%{_libdir}/pkgconfig
test "%{_libdir}" = "%{_prefix}/lib" || \
    mv %{buildroot}%{_prefix}/lib/pkgconfig/* %{buildroot}%{_libdir}/pkgconfig

%files
%doc README
%license COPYING
%{_prefix}/lib/mono/dbus-sharp-glib-2.0
%{_prefix}/lib/mono/gac/dbus-sharp-glib

%files devel
%{_libdir}/pkgconfig/dbus-sharp-glib-2.0.pc

%changelog
* Mon May 23 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.6.0-1
- update to latest release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 18 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.5.0-11
- Rebuild (mono4)

* Tue Mar 24 2015 Than Ngo <than@redhat.com> - 0.5.0-10
- use %%mono_arches

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Brent Baude <baude@us.ibm.com> - 0.5.0-7
- Changed ppc64 to power64 macro

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Mar 11 2012 Christian Krause <chkr@fedoraproject.org> - 0.5.0-3
- Change paths for mono assemblies according to updated packaging
  guidelines (http://fedoraproject.org/wiki/Packaging:Mono)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Christian Krause <chkr@fedoraproject.org> - 0.5.0-1
- Initial spec file
