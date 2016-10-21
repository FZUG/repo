# http://pkgs.fedoraproject.org/cgit/rpms/docky.git
%global         majorver 2.2
%global         minorver 1.1
%global         debug_package %{nil}

%if 0%{?el6}
%define mono_arches %ix86 x86_64 ia64 %{arm} sparcv9 alpha s390x ppc ppc64
%endif

Name:           docky
Version:        %{majorver}.%{minorver}
Release:        1%{?dist}
Summary:        Advanced dock application written in Mono
License:        GPLv3+
URL:            http://wiki.go-docky.com
Source0:        https://launchpad.net/docky/%{majorver}/%{version}/+download/%{name}-%{version}.tar.xz
# The "Icon Magnification" was removed from "Docky" due
# to a potential violation of US Patent 7434177
Patch0:         docky-startscript-path.patch

BuildRequires:  mono-devel
BuildRequires:  pkgconfig(gapi-2.0)
BuildRequires:  pkgconfig(gconf-2.0)
BuildRequires:  pkgconfig(gconf-sharp-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(glib-sharp-2.0)
# Docky does not use gio-sharp library yet (it has its own for now)
BuildRequires:  pkgconfig(gio-sharp-2.0)
BuildRequires:  pkgconfig(gkeyfile-sharp)
BuildRequires:  pkgconfig(gnome-keyring-sharp-1.0)
BuildRequires:  pkgconfig(gtk+-2.0) >= 2.14.3
BuildRequires:  pkgconfig(gtk-sharp-2.0)
BuildRequires:  pkgconfig(mono-addins)
BuildRequires:  pkgconfig(mono-addins-gui)
BuildRequires:  pkgconfig(mono-addins-setup)
BuildRequires:  pkgconfig(mono-cairo)
BuildRequires:  pkgconfig(dbus-sharp-2.0) >= 0.7
BuildRequires:  pkgconfig(dbus-sharp-glib-2.0) >= 0.5
BuildRequires:  pkgconfig(notify-sharp)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0) >= 2.14.3
BuildRequires:  pkgconfig(libwnck-1.0) >= 2.20
BuildRequires:  gettext
BuildRequires:  perl-XML-Parser
BuildRequires:  automake, libtool, intltool
BuildRequires:  desktop-file-utils
BuildRequires:  gtk-update-icon-cache
Requires:       gtk-sharp2-gapi
# Mono only available on these
ExclusiveArch:  %{mono_arches}

%description
Docky is an advanced shortcut bar that sits at the bottom, top, and/or sides
of your screen. It provides easy access to some of the files, folders,
and applications on your computer, displays which applications are
currently running, holds windows in their minimized state, and more.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
This package contains libraries and header files
for developing applications that use %{name}.

%prep
%setup -q
%patch0 -p1

sed -i -e 's|gmcs|mcs|g' configure configure.ac m4/shamrock/mono.m4

%build
autoreconf -vif
%configure --disable-schemas-install \
           --with-gconf-schema-file-dir=%{_sysconfdir}/gconf/schemas
make %{?_smp_mflags}

%install
%make_install

#gapi_codegen.exe is not distributed (licence is GNU GPL v2)
rm -f %{buildroot}%{_libdir}/%{name}/gapi_codegen*

desktop-file-install \
    --dir %{buildroot}%{_sysconfdir}/xdg/autostart \
    --add-only-show-in=GNOME \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --delete-original \
    --dir %{buildroot}%{_datadir}/applications \
    --remove-category Application \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

# autostart is disabled by default
echo "X-GNOME-Autostart-enabled=false" >> \
    %{buildroot}%{_sysconfdir}/xdg/autostart/%{name}.desktop

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

%files -f %{name}.lang
%doc AUTHORS NEWS
%license COPYING COPYRIGHT
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.*
%{_datadir}/icons/hicolor/*/apps/gmail.png
%{_datadir}/icons/hicolor/*/mimetypes/*
%{_datadir}/applications/*.desktop
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%config(noreplace) %{_sysconfdir}/xdg/autostart/%{name}.desktop
%{_mandir}/man1/%{name}.1*

%files devel
%{_libdir}/pkgconfig/%{name}.*.pc

%changelog
* Tue May 24 2016 Leigh Scott <leigh123linux@googlemail.com> - 2.2.1.1-1
- Update to 2.2.1.1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Claudio Rodrigo Pereyra Diaz <elsupergomez@fedoraproject.org> 2.2.0-5
- Build for Mono 4
- Use mono macros

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 2.2.0-2
- Replace ppc64 with power64 macro

* Thu Sep 19 2013 Christopher Meng <rpm@cicku.me> - 2.2.0-1
- Update to 2.2.0(BZ#958779)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Lukas Zapletal <lzap+rpm[@]redhat.com> - 2.1.4-1
- version bump - new 2.1 stable branch

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul  5 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0.12-3
- Bump build

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Mar 10 2011 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.12-1
- version bump

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.11-1
- version bump

* Mon Jan 10 2011 Dan Horák <dan[at]danny.cz> - 2.0.10-2
- updated the supported arch list

* Mon Jan 10 2011 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.10-1
- Version bump
- Man page added
- Patch for shebang not needed anymore (fixed in mainstream)

* Mon Oct 25 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.7-3
- Fixing many things reported in the bug 635450
- Licence change
- Zooming code completly removed

* Mon Oct 25 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.7-2
- Fixed requirement on mono-core

* Mon Oct 18 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.7-1
- Version bump

* Mon Sep 06 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.6-1
- Initial package
- Many fixes in spec (thank to Christian Krause)

* Mon Sep 06 2010 Lukas Zapletal <lzap+rpm@redhat.com> - 2.0.6-1
- Initial package
