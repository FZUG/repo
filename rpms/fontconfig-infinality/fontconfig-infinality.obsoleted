# https://github.com/bohoomil/fontconfig-ultimate/pull/176
# https://github.com/drenninghoff/infinality-ultimate-fedora
# https://github.com/archfan/infinality_bundle/tree/master/02_fontconfig-iu
# http://pkgs.fedoraproject.org/cgit/rpms/fontconfig.git
# https://aur.archlinux.org/packages/fontconfig-infinality

%global freetype_version 2.1.4
%global _commit c0e90598b4a50a92432268ccc442c2e067a54924
%global _fontconfdir %{_fontconfig_templatedir}.infinality

Name:           fontconfig-infinality
Version:        2.12.1
Release:        1%{?dist}
Summary:        Font configuration and customization library
# src/ftglue.[ch] is in Public Domain
# src/fccache.c contains Public Domain code
# fc-case/CaseFolding.txt is in the UCD
# otherwise MIT
License:        MIT and Public Domain and UCD
Group:          System Environment/Libraries
URL:            http://fontconfig.org
Source0:        http://fontconfig.org/release/fontconfig-%{version}.tar.bz2
Source1:        http://pkgs.fedoraproject.org/cgit/rpms/fontconfig.git/plain/25-no-bitmap-fedora.conf
Source2:        https://github.com/bohoomil/fontconfig-ultimate/archive/%{_commit}/fontconfig-ultimate-%{_commit}.tar.gz

# https://bugzilla.redhat.com/show_bug.cgi?id=140335
Patch0:         http://pkgs.fedoraproject.org/cgit/rpms/fontconfig.git/plain/fontconfig-sleep-less.patch
Patch11:        https://github.com/julroy67/fontconfig-ultimate/raw/master/fontconfig_patches/01-configure.patch
Patch12:        https://github.com/julroy67/fontconfig-ultimate/raw/master/fontconfig_patches/02-configure.ac.patch
Patch13:        https://github.com/bohoomil/fontconfig-ultimate/raw/master/fontconfig_patches/03-Makefile.in.patch
Patch14:        https://github.com/julroy67/fontconfig-ultimate/raw/master/fontconfig_patches/04-Makefile.conf.d.patch
Patch15:        https://github.com/julroy67/fontconfig-ultimate/raw/master/fontconfig_patches/05-Makefile.am.in.patch

BuildRequires:  expat-devel
BuildRequires:  freetype-devel >= %{freetype_version}
# rpm macros with font
BuildRequires:  fontpackages-devel
BuildRequires:  autoconf automake libtool

Requires:       fontpackages-filesystem freetype
Requires(pre):  freetype
Requires(post): grep coreutils
Requires:       font(:lang=en)
Provides:       fontconfig = %{version}-%{release}
Provides:       fontconfig%{?_isa} = %{version}-%{release}
Conflicts:      fontconfig%{?_isa}

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by 
applications.

%package devel
Summary:        Font configuration and customization library
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       freetype-devel >= %{freetype_version}
Requires:       pkgconfig
Provides:       fontconfig-devel = %{version}-%{release}
Provides:       fontconfig-devel%{?_isa} = %{version}-%{release}
Conflicts:      fontconfig-devel%{?_isa}

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which 
will use fontconfig.

%package devel-doc
Summary:        Development Documentation files for fontconfig library
Group:          Documentation
BuildArch:      noarch
Requires:       %{name}-devel = %{version}-%{release}
Provides:       fontconfig-doc = %{version}-%{release}
Conflicts:      fontconfig-doc

%description devel-doc
The fontconfig-devel-doc package contains the documentation files
which is useful for developing applications that uses fontconfig.

%prep
%setup -q -n fontconfig-%{version} -a2
%patch0 -p1 -b .sleep-less
%patch11 -p1 -b .configure
%patch12 -p1 -b .configure.ac
%patch13 -p1 -b .Makefile.in
%patch14 -p1 -b .Makefile.conf.d
%patch15 -p1 -b .Makefile.am.in

ln -s fontconfig-ultimate-%{_commit}/conf.d.infinality conf.d.infinality

aclocal
libtoolize -f
automake -afi

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

%configure \
    --with-add-fonts=/usr/share/X11/fonts/Type1,/usr/share/X11/fonts/TTF,/usr/local/share/fonts \
    --disable-static
%make_build

%install
%make_install INSTALL="install -p"

find %{buildroot} -name '*.la' -exec rm -f {} ';'

install -m644 %{SOURCE1} %{buildroot}%{_fontconfig_confdir}
ln -s %{_fontconfig_templatedir}/25-unhint-nonlatin.conf %{buildroot}%{_fontconfig_confdir}

pushd fontconfig-ultimate-%{_commit}/fontconfig_patches/
for i in combi free ms; do
  install -dm755 %{buildroot}%{_fontconfdir}/${i}
  install -Dm644 ${i}/*.conf %{buildroot}%{_fontconfdir}/${i}/
done
install -Dm755 fc-presets %{buildroot}%{_bindir}/fc-presets
ln -sf %{_fontconfdir}/free/30-metric-aliases-free.conf %{buildroot}%{_fontconfig_confdir}
ln -sf %{_fontconfdir}/free/37-repl-global-free.conf %{buildroot}%{_fontconfig_confdir}
ln -sf %{_fontconfdir}/free/60-latin-free.conf %{buildroot}%{_fontconfig_confdir}
ln -sf %{_fontconfdir}/free/65-non-latin-free.conf %{buildroot}%{_fontconfig_confdir}
ln -sf %{_fontconfdir}/free/66-aliases-wine-free.conf %{buildroot}%{_fontconfig_confdir}

# move installed doc files back to build directory to package themm
# in the right place
mv %{buildroot}%{_docdir}/fontconfig/* .
rmdir %{buildroot}%{_docdir}/fontconfig/

%check
make check

%post
/sbin/ldconfig

umask 0022

mkdir -p %{_localstatedir}/cache/fontconfig

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
  HOME=/root /usr/bin/fc-cache -f
fi

%postun -p /sbin/ldconfig

%transfiletriggerin -- /usr/share/fonts /usr/share/X11/fonts/Type1 /usr/share/X11/fonts/TTF /usr/local/share/fonts
HOME=/root /usr/bin/fc-cache -s

%transfiletriggerpostun -- /usr/share/fonts /usr/share/X11/fonts/Type1 /usr/share/X11/fonts/TTF /usr/local/share/fonts
HOME=/root /usr/bin/fc-cache -s

%files
%doc README AUTHORS
%doc doc/fontconfig-user.txt doc/fontconfig-user.html
%doc %{_fontconfig_confdir}/README
%license COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-cache
%{_bindir}/fc-cat
%{_bindir}/fc-list
%{_bindir}/fc-match
%{_bindir}/fc-pattern
%{_bindir}/fc-query
%{_bindir}/fc-scan
%{_bindir}/fc-validate
%{_bindir}/fc-presets
%{_fontconfig_templatedir}/*.conf
%{_datadir}/fontconfig/conf.avail.infinality/*.conf
%{_datadir}/fontconfig/conf.avail.infinality/{combi,free,ms}/*.conf
%{_datadir}/xml/fontconfig
# fonts.conf is not supposed to be modified.
# If you want to do so, you should use local.conf instead.
%config %{_fontconfig_masterdir}/fonts.conf
%config(noreplace) %{_fontconfig_confdir}/*.conf
%dir %{_localstatedir}/cache/fontconfig
%{_mandir}/man1/*
%{_mandir}/man5/*

%files devel
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig
%{_mandir}/man3/*

%files devel-doc
%doc doc/fontconfig-devel.txt doc/fontconfig-devel

%changelog
* Sat Dec 10 2016 mosquito <sensor.wen@gmail.com> - 2.12.1-1
- Initial build, based on fontconfig-2.12.1-1 package
