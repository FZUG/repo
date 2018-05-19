# https://github.com/bohoomil/fontconfig-ultimate/pull/176
# https://github.com/drenninghoff/infinality-ultimate-fedora
# https://github.com/archfan/infinality_bundle/tree/master/01_freetype2-iu
# http://pkgs.fedoraproject.org/cgit/rpms/freetype.git
# https://aur.archlinux.org/packages/freetype2-infinality

# Patented subpixel rendering disabled by default.
%bcond_without subpixel_rendering
%bcond_without xfree86

Name:    freetype-infinality
Version: 2.7
Release: 1%{?dist}
Summary: A free and portable font rendering engine
License: (FTL or GPLv2+) and BSD and MIT and Public Domain and zlib with acknowledgement
Group:   System Environment/Libraries
URL:     http://www.freetype.org

Source0: http://download.savannah.gnu.org/releases/freetype/freetype-%{version}.tar.bz2
Source1: http://download.savannah.gnu.org/releases/freetype/freetype-doc-%{version}.tar.bz2
Source2: http://download.savannah.gnu.org/releases/freetype/ft2demos-%{version}.tar.bz2
Source3: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/ftconfig.h
Source4: https://github.com/drenninghoff/infinality-ultimate-fedora/raw/master/freetype-infinality-ultimate/infinality-settings.sh
Source5: https://github.com/drenninghoff/infinality-ultimate-fedora/raw/master/freetype-infinality-ultimate/infinality-settings-generic
Source6: https://github.com/drenninghoff/infinality-ultimate-fedora/raw/master/freetype-infinality-ultimate/xft-settings.sh
Source7: https://github.com/bohoomil/fontconfig-ultimate/raw/b910d2ffe4f4346773c494f43329069c628dfe9a/01_freetype2-iu/freetype2.sh

Patch1:  https://github.com/archfan/infinality_bundle/raw/master/01_freetype2-iu/0002-infinality-2.7-2016.09.09.patch

# Enable subpixel rendering
#Patch21: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/freetype-2.3.0-enable-spr.patch

# Enable infinality subpixel hinting
#Patch22: https://github.com/julroy67/fontconfig-ultimate/raw/pkgbuild/01_freetype2-iu/0003-Enable-infinality-subpixel-hinting.patch

# Enable otvalid and gxvalid modules
#Patch46: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/freetype-2.2.1-enable-valid.patch

# Enable additional demos
Patch47: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/freetype-2.5.2-more-demos.patch

# Fix multilib conflicts
Patch88: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/freetype-multilib.patch

# https://bugzilla.redhat.com/show_bug.cgi?id=1161963
Patch92: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/freetype-2.5.3-freetype-config-prefix.patch

Patch93: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/freetype-2.6.5-libtool.patch

Patch94: http://pkgs.fedoraproject.org/cgit/rpms/freetype.git/plain/freetype-2.7-valgrind.patch

BuildRequires: libX11-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel

Provides: freetype-bytecode = %{version}-%{release}
%if %{with subpixel_rendering}
Provides: freetype-subpixel = %{version}-%{release}
%endif
Provides: freetype = %{version}-%{release}
Provides: freetype%{?_isa} = %{version}-%{release}
Provides: freetype-freeworld%{?_isa} = %{version}-%{release}
Provides: freetype-freeworld = %{version}-%{release}
Conflicts: freetype%{?_isa}

%description
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments. FreeType is a library which can open and
manages font files as well as efficiently load, hint and render
individual glyph. FreeType is not a font server or a complete
text-rendering library.


%package demos
Summary:  A collection of FreeType demos
Group:    System Environment/Libraries
Requires: %{name} = %{version}-%{release}
Provides: freetype-demos = %{version}-%{release}
Provides: freetype-demos%{?_isa} = %{version}-%{release}
Conflicts: freetype-demos%{?_isa}

%description demos
The FreeType engine is a free and portable font rendering
engine, developed to provide advanced font support for a variety of
platforms and environments.  The demos package includes a set of useful
small utilities showing various capabilities of the FreeType library.


%package devel
Summary:  FreeType development libraries and header files
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}
Provides: freetype-devel = %{version}-%{release}
Provides: freetype-devel%{?_isa} = %{version}-%{release}
Conflicts: freetype-devel%{?_isa}

%description devel
The freetype-devel package includes the static libraries and header files
for the FreeType font rendering engine.

Install freetype-devel if you want to develop programs which will use
FreeType.


%prep
%setup -q -b1 -a2 -n freetype-%{version}

%patch1 -p1 -b .infinality
sed -i '/#define TT_CONFIG_OPTION_SUBPIXEL_HINTING  1/d' include/freetype/config/ftoption.h

%if %{with subpixel_rendering}
#patch21 -p1 -b .enable-spr
#patch22 -p1 -b .enable-infinality-spr
%endif

#patch46 -p1 -b .enable-valid

pushd ft2demos-%{version}
%patch47 -p1 -b .more-demos
popd

%patch88 -p1 -b .multilib

%patch92 -p1 -b .freetype-config-prefix

%patch93 -p1 -b .libtool

%patch94 -p1 -b .valgrind

cp %{SOURCE4} %{SOURCE5} .


%build
%configure \
    --disable-static \
    --with-zlib=yes \
    --with-bzip2=yes \
    --with-png=yes \
    --with-harfbuzz=no
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' builds/unix/libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' builds/unix/libtool
%make_build

%if %{with xfree86}
# Build demos
pushd ft2demos-%{version}
make TOP_DIR=".."
popd
%endif

# Convert FTL.txt and example3.cpp to UTF-8
pushd docs
iconv -f latin1 -t utf-8 < FTL.TXT > FTL.TXT.tmp && \
touch -r FTL.TXT FTL.TXT.tmp && \
mv FTL.TXT.tmp FTL.TXT

iconv -f iso-8859-1 -t utf-8 < "tutorial/example3.cpp" > "tutorial/example3.cpp.utf8"
touch -r tutorial/example3.cpp tutorial/example3.cpp.utf8 && \
mv tutorial/example3.cpp.utf8 tutorial/example3.cpp
popd


%install
%make_install gnulocaledir=%{buildroot}%{_datadir}/locale

# Package demos
for _i in ftbench ftchkwd ftdump ftlint ftmemchk ftpatchk fttimer ftvalid; do
    builds/unix/libtool --mode=install \
        install -m755 ft2demos-%{version}/bin/$_i %{buildroot}%{_bindir}
done
%if %{with xfree86}
for _i in ftdiff ftgamma ftgrid ftmulti ftstring ftview; do
    builds/unix/libtool --mode=install \
        install -m755 ft2demos-%{version}/bin/$_i %{buildroot}%{_bindir}
done
%endif

# fix multilib issues
mv %{buildroot}%{_includedir}/freetype2/freetype/config/ftconfig.h \
   %{buildroot}%{_includedir}/freetype2/freetype/config/ftconfig-%{__isa_bits}.h
install -Dm644 %{SOURCE3} %{buildroot}%{_includedir}/freetype2/freetype/config/ftconfig.h

# install infinality-settings.sh
install -Dm755 %{SOURCE6} %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/xft-settings.sh

# install freetype2.sh
install -Dm644 %{SOURCE7} %{buildroot}%{_sysconfdir}/profile.d/freetype2.sh

# Don't package static a or .la files
rm -f %{buildroot}%{_libdir}/*.{a,la}


%triggerpostun -- freetype < 2.0.5-3
{
  # ttmkfdir updated - as of 2.0.5-3, on upgrades we need xfs to regenerate
  # things to get the iso10646-1 encoding listed.
  for I in %{_datadir}/fonts/*/TrueType /usr/share/X11/fonts/TTF; do
      [ -d $I ] && [ -f $I/fonts.scale ] && [ -f $I/fonts.dir ] && touch $I/fonts.scale
  done
  exit 0
}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{!?_licensedir:%global license %%doc}
%license docs/LICENSE.TXT docs/FTL.TXT docs/GPLv2.TXT
%doc README
%doc infinality-settings-generic infinality-settings.sh
%{_libdir}/libfreetype.so.*
%config(noreplace) %{_sysconfdir}/profile.d/freetype2.sh
%{_sysconfdir}/X11/xinit/xinitrc.d/xft-settings.sh

%files demos
%doc ChangeLog README
%{_bindir}/ftbench
%{_bindir}/ftchkwd
%{_bindir}/ftdump
%{_bindir}/ftlint
%{_bindir}/ftmemchk
%{_bindir}/ftpatchk
%{_bindir}/fttimer
%{_bindir}/ftvalid
%if %{with xfree86}
%{_bindir}/ftdiff
%{_bindir}/ftgamma
%{_bindir}/ftgrid
%{_bindir}/ftmulti
%{_bindir}/ftstring
%{_bindir}/ftview
%endif

%files devel
%doc docs/CHANGES docs/formats.txt docs/ft2faq.html
%doc docs/design
%doc docs/glyphs
%doc docs/reference
%doc docs/tutorial
%dir %{_includedir}/freetype2
%{_includedir}/freetype2/*
%{_bindir}/freetype-config
%{_libdir}/libfreetype.so
%{_libdir}/pkgconfig/freetype2.pc
%{_datadir}/aclocal/freetype2.m4
%{_mandir}/man1/*

%changelog
* Sat Dec 10 2016 mosquito <sensor.wen@gmail.com> - 2.7-1
- Initial build, based on freetype-2.7-2 package
