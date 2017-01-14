%global _mozc_commit 280e38fe3d9db4df52f0713acf2ca65898cd697a
%global _mozc_shortcommit %(c=%{_mozc_commit}; echo ${c:0:7})
%global _jud_commit e5b3425575734c323e1d947009dd74709437b684
%global _jud_shortcommit %(c=%{_jud_commit}; echo ${c:0:7})
%global _protobuf_commit c44ca26fe89ed8a81d3ee475a2ccc1797141dbce
%global _protobuf_shortcommit %(c=%{_protobuf_commit}; echo ${c:0:7})
%global _gtest_commit 82b11b8cfcca464c2ac74b623d04e74452e74f32
%global _gtest_shortcommit %(c=%{_gtest_commit}; echo ${c:0:7})
%global _jsoncpp_commit 11086dd6a7eba04289944367ca82cea71299ed70
%global _jsoncpp_shortcommit %(c=%{_gtest_commit}; echo ${c:0:7})
%global _fcitx_patchver 2.18.2612.102.1
%global _build_type Release

%global fcitx_icon_dir %{_datadir}/fcitx/mozc/icon/
%global fcitx_addon_dir %{_datadir}/fcitx/addon/
%global fcitx_inputmethod_dir %{_datadir}/fcitx/inputmethod/
%global fcitx_lib_dir %{_libdir}/fcitx/

%global		pkg	mozc

Name:		mozc
Version:	2.20.2673.102
Release:	1%{?dist}
Summary:	A Japanese Input Method Editor (IME) designed for multi-platform

Group:		System Environment/Libraries
License:	BSD and ASL 2.0 and UCD and Public Domain and mecab-ipadic
URL:		https://github.com/google/mozc
# src/data/unicode/: UCD
#  Copyright (c) 1991-2008 Unicode, Inc.
# src/data/test/stress_test/sentences.txt: Public Domain
# src/data/dictionary/: mecab-ipadic and BSD
#   See http://code.google.com/p/mozc/issues/detail?id=20
#   also data/installer/credits_en.html
Source0:	https://github.com/google/%{name}/archive/%{_mozc_commit}.tar.gz#/%{name}-%{_mozc_shortcommit}.tar.gz
Source1:	mozc-init.el
# Public Domain
Source2:	http://www.post.japanpost.jp/zipcode/dl/kogaki/zip/ken_all.zip
Source3:	http://www.post.japanpost.jp/zipcode/dl/jigyosyo/zip/jigyosyo.zip
Source4:	ibus-setup-mozc-jp.desktop
# BSD
Source5:	https://github.com/hiroyuki-komatsu/japanese-usage-dictionary/archive/%{_jud_commit}/%{_jud_commit}.tar.gz#/japanese-usage-dictionary-%{_jud_shortcommit}.tar.gz
# BSD
Source6:	https://github.com/google/protobuf/archive/%{_protobuf_commit}/%{_protobuf_commit}.tar.gz#/protobuf-%{_protobuf_shortcommit}.tar.gz
# BSD
# only for tests
Source7:	https://github.com/google/googletest/archive/%{_gtest_commit}/%{_gtest_commit}.tar.gz#/gtest-%{_gtest_shortcommit}.tar.gz
# Public Domain or MIT
# only for tests
Source8:	https://github.com/open-source-parsers/jsoncpp/archive/%{_jsoncpp_commit}/%{_jsoncpp_commit}.tar.gz#/jsoncpp-%{_jsoncpp_shortcommit}.tar.gz
Patch0:		mozc-build-ninja.patch
## to avoid undefined symbols with clang.
Patch1:		mozc-build-gcc.patch
Patch2:		mozc-build-verbosely.patch
Patch3:		http://download.fcitx-im.org/fcitx-mozc/fcitx-mozc-%{_fcitx_patchver}.patch

BuildRequires:	python gettext
BuildRequires:	libstdc++-devel zlib-devel libxcb-devel glib2-devel qt5-qtbase-devel zinnia-devel gtk2-devel
BuildRequires:	clang ninja-build
BuildRequires:	gyp >= 0.1-0.4.840svn
BuildRequires:	ibus-devel >= 1.5.4
BuildRequires:	emacs
BuildRequires:	xemacs xemacs-packages-extra
BuildRequires:	fcitx-devel

Requires:	zinnia-tomoe-ja
Requires:	emacs-filesystem >= %{_emacs_version}
Requires:	xemacs-filesystem >= %{_xemacs_version}
Provides:	bundled(protobuf) = 3.0.2-1.git%{_protobuf_shortcommit}
Provides:	emacs-mozc = %{version}-%{release}, emacs-mozc-el = %{version}-%{release}
Obsoletes:	emacs-mozc <= 2.17.2077.102-4, emacs-mozc-el <= 2.17.2077.102-4
Provides:	xemacs-mozc = %{version}-%{release}, xemacs-mozc-el = %{version}-%{release}
Obsoletes:	xemacs-mozc <= 2.17.2077.102-4, xemacs-mozc-el <= 2.17.2077.102-4
Provides:	emacs-common-mozc = %{version}-%{release}
Obsoletes:	emacs-common-mozc <= 2.17.2077.102-4

%description
Mozc is a Japanese Input Method Editor (IME) designed for
multi-platform such as Chromium OS, Windows, Mac and Linux.

%package	-n ibus-mozc
Summary:	The mozc engine for IBus input platform
Group:		System Environment/Libraries
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	ibus%{?_isa} >= 1.5.4

%description	-n ibus-mozc
Mozc is a Japanese Input Method Editor (IME) designed for
multi-platform such as Chromium OS, Windows, Mac and Linux.

This package contains the Input Method Engine for IBus.

%package	-n fcitx-%{name}
Summary:	The Mozc backend for Fcitx
Group:		System Environment/Libraries
Requires:	fcitx%{?_isa}
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description	-n fcitx-%{name}
The Mozc backend for Fcitx provides a Japanese input method.


%prep
%setup -q -n %{name}-%{_mozc_commit} -a 2 -a 3 -a 5 -a 6 -a 7 -a 8
%patch0 -p1 -b .0-ninja
%patch1 -p1 -b .1-gcc
%patch2 -p1 -b .2-verbose
%patch3 -p1 -b .3-fcitx
pushd src
PYTHONPATH="$PWD:$PYTHONPATH" \
python2 dictionary/gen_zip_code_seed.py \
    --zip_code="../KEN_ALL.CSV" \
    --jigyosyo="../JIGYOSYO.CSV" \
    >> data/dictionary_oss/dictionary09.txt
popd
rmdir src/third_party/{japanese_usage_dictionary,protobuf,gtest,jsoncpp}
mv japanese-usage-dictionary-%{_jud_commit} src/third_party/japanese_usage_dictionary
mv protobuf-%{_protobuf_commit} src/third_party/protobuf
mv googletest-%{_gtest_commit} src/third_party/gtest
mv jsoncpp-%{_jsoncpp_commit} src/third_party/jsoncpp

%build
pushd src
# replace compiler flags to build with the proper debugging information
t=`mktemp /tmp/mozc.gyp-XXXXXXXX`
opts=$(for i in $RPM_OPT_FLAGS; do
	echo "i \\"
	echo "\"$i\","
done)
sed -ne "/'linux_cflags':/{p;n;p;:a;/[[:space:]]*\],/{\
$opts
p;b b};n;b a;};{p};:b" gyp/common.gypi > $t && mv $t gyp/common.gypi || exit 1

# -Wall from RPM_OPT_FLAGS overrides -Wno-* options from gyp.
# gyp inserts -Wall to the head of release_extra_flags.
flags=${RPM_OPT_FLAGS/-Wall/}

_gyp_opts='
    use_libzinnia=1
    zinnia_model_file=%{_datadir}/zinnia/model/tomoe/handwriting-ja.model
    ibus_mozc_path=%{ibus_mozc_path}
    ibus_mozc_icon_path=%{ibus_mozc_icon_path}
    document_dir=%{_datadir}/doc/ibus-mozc
    release_extra_cflags="'$flags'"'

QTDIR=%{_prefix} GYP_DEFINES="${_gyp_opts}" \
python2 build_mozc.py gyp --gypdir=%{_bindir} --server_dir=%{_libexecdir}/%{name}
python2 build_mozc.py build -c %{_build_type} \
    unix/ibus/ibus.gyp:ibus_mozc \
    unix/fcitx/fcitx.gyp:fcitx-mozc \
    unix/emacs/emacs.gyp:mozc_emacs_helper \
    server/server.gyp:mozc_server \
    gui/gui.gyp:mozc_tool \
    renderer/renderer.gyp:mozc_renderer
popd


%install
pushd src
install -d $RPM_BUILD_ROOT%{_libexecdir}/mozc/documents
install -p -m0755 out_linux/Release/mozc_server $RPM_BUILD_ROOT%{_libexecdir}/mozc
install -p -m0755 out_linux/Release/mozc_tool $RPM_BUILD_ROOT%{_libexecdir}/mozc
install -p -m0755 out_linux/Release/mozc_renderer $RPM_BUILD_ROOT%{_libexecdir}/mozc
install -p -m0644 data/installer/credits_en.html $RPM_BUILD_ROOT%{_libexecdir}/mozc/documents

# ibus-mozc
install -d $RPM_BUILD_ROOT%{_datadir}/ibus/component
install -d $RPM_BUILD_ROOT%{_datadir}/ibus-mozc
install -p -m0755 out_linux/Release/ibus_mozc $RPM_BUILD_ROOT%{_libexecdir}/ibus-engine-mozc
install -p -m0644 out_linux/Release/gen/unix/ibus/mozc.xml $RPM_BUILD_ROOT%{_datadir}/ibus/component/
(cd data/images/unix;
install -p -m0644 ime_product_icon_opensource-32.png $RPM_BUILD_ROOT%{_datadir}/ibus-mozc/product_icon.png
for i in ui-*.png; do
	install -p -m0644 $i $RPM_BUILD_ROOT%{_datadir}/ibus-mozc/${i//ui-/}
done)
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications  %{SOURCE4}

# fcitx-mozc
for mofile in out_linux/%{_build_type}/gen/unix/fcitx/po/*.mo; do
    filename=`basename $mofile`
    lang=${filename/.mo/}
    install -Dm0644 $mofile ${RPM_BUILD_ROOT}%{_datadir}/locale/$lang/LC_MESSAGES/fcitx-%{name}.mo
done
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_addon_dir}
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_inputmethod_dir}
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_icon_dir}
install -m755 -d ${RPM_BUILD_ROOT}%{fcitx_lib_dir}
install -m755 out_linux/%{_build_type}/fcitx-mozc.so ${RPM_BUILD_ROOT}%{fcitx_lib_dir}
install -m644 unix/fcitx/fcitx-mozc.conf ${RPM_BUILD_ROOT}%{fcitx_addon_dir}
install -m644 unix/fcitx/mozc.conf ${RPM_BUILD_ROOT}%{fcitx_inputmethod_dir}
install -m644 data/images/product_icon_32bpp-128.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc.png
install -m644 data/images/unix/ui-alpha_full.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-alpha_full.png
install -m644 data/images/unix/ui-alpha_half.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-alpha_half.png
install -m644 data/images/unix/ui-direct.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-direct.png
install -m644 data/images/unix/ui-hiragana.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-hiragana.png
install -m644 data/images/unix/ui-katakana_full.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-katakana_full.png
install -m644 data/images/unix/ui-katakana_half.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-katakana_half.png
install -m644 data/images/unix/ui-dictionary.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-dictionary.png
install -m644 data/images/unix/ui-properties.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-properties.png
install -m644 data/images/unix/ui-tool.png ${RPM_BUILD_ROOT}%{fcitx_icon_dir}/mozc-tool.png

# emacs-common-mozc
install -d $RPM_BUILD_ROOT%{_bindir}
install -p -m0755 out_linux/Release/mozc_emacs_helper $RPM_BUILD_ROOT%{_bindir}

# emacs-mozc*
install -d $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{pkg}
install -d $RPM_BUILD_ROOT%{_emacs_sitestartdir}
install -p -m0644 unix/emacs/mozc.el $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{pkg}
install -p -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_emacs_sitestartdir}

emacs -batch -f batch-byte-compile $RPM_BUILD_ROOT%{_emacs_sitelispdir}/%{pkg}/mozc.el

# xemacs-mozc*
install -d $RPM_BUILD_ROOT%{_xemacs_sitelispdir}/%{pkg}
install -d $RPM_BUILD_ROOT%{_xemacs_sitestartdir}
install -p -m0644 unix/emacs/mozc.el $RPM_BUILD_ROOT%{_xemacs_sitelispdir}/%{pkg}
install -p -m0644 %{SOURCE1} $RPM_BUILD_ROOT%{_xemacs_sitestartdir}

xemacs -batch -f batch-byte-compile $RPM_BUILD_ROOT%{_xemacs_sitelispdir}/%{pkg}/mozc.el
popd

# Register as an AppStream component to be visible in the software center
#
# NOTE: It would be *awesome* if this file was maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/mozc.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="inputmethod">
  <id>mozc.xml</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>Mozc</name>
  <summary>Japanese input method</summary>
  <description>
    <p>
      The Mozc input method is designed for entering Japanese text.
      It is multi-platform and is available on Chromium OS, Windows, Mac and Linux.
    </p>
    <p>
      Input methods are typing systems allowing users to input complex languages.
      They are necessary because these contain too many characters to simply be laid
      out on a traditional keyboard.
    </p>
  </description>
  <url type="homepage">https://code.google.com/p/ibus/</url>
  <url type="bugtracker">https://code.google.com/p/ibus/issues/list</url>
  <url type="help">https://code.google.com/p/ibus/wiki/FAQ</url>
  <languages>
    <lang percentage="100">ja</lang>
  </languages>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

%find_lang fcitx-mozc

%check
pushd src
python2 build_mozc.py runtests -c %{_build_type}
popd

%post -n ibus-mozc
[ -x %{_bindir}/ibus ] && %{_bindir}/ibus write-cache --system >& /dev/null || :

%postun -n ibus-mozc
[ -x %{_bindir}/ibus ] && %{_bindir}/ibus write-cache --system >& /dev/null || :

%files
%doc AUTHORS CONTRIBUTING.md CONTRIBUTORS docs README.md docs/about_branding.md
%doc docs/design_doc docs/release_history.md
%license LICENSE
%dir %{_libexecdir}/mozc
%{_bindir}/mozc_emacs_helper
%{_libexecdir}/mozc/mozc_server
%{_libexecdir}/mozc/mozc_tool
%{_libexecdir}/mozc/documents
%dir %{_emacs_sitelispdir}/%{pkg}
%{_emacs_sitelispdir}/%{pkg}/*.elc
%{_emacs_sitestartdir}/*.el
%{_emacs_sitelispdir}/%{pkg}/*.el
%dir %{_xemacs_sitelispdir}/%{pkg}
%{_xemacs_sitelispdir}/%{pkg}/*.elc
%{_xemacs_sitestartdir}/*.el
%{_xemacs_sitelispdir}/%{pkg}/*.el

%files	-n ibus-mozc
%dir %{_datadir}/ibus-mozc
%{_libexecdir}/ibus-engine-mozc
%{_libexecdir}/mozc/mozc_renderer
%{_datadir}/appdata/*.appdata.xml
%{_datadir}/applications/ibus-setup-mozc-jp.desktop
%{_datadir}/ibus/component/mozc.xml
%{_datadir}/ibus-mozc/*.png

%files -n fcitx-mozc -f fcitx-mozc.lang
%defattr(-,root,root,-)
%{fcitx_lib_dir}/fcitx-%{name}.so
%{fcitx_addon_dir}/fcitx-%{name}.conf
%dir %{fcitx_inputmethod_dir}
%{fcitx_inputmethod_dir}/%{name}.conf
%dir %{_datadir}/fcitx/%{name}
%dir %{fcitx_icon_dir}
%{fcitx_icon_dir}/%{name}.png
%{fcitx_icon_dir}/%{name}-alpha_full.png
%{fcitx_icon_dir}/%{name}-alpha_half.png
%{fcitx_icon_dir}/%{name}-direct.png
%{fcitx_icon_dir}/%{name}-hiragana.png
%{fcitx_icon_dir}/%{name}-katakana_full.png
%{fcitx_icon_dir}/%{name}-katakana_half.png
%{fcitx_icon_dir}/%{name}-dictionary.png
%{fcitx_icon_dir}/%{name}-properties.png
%{fcitx_icon_dir}/%{name}-tool.png

%changelog
* Thu Jan 12 2017 Robin Lee <cheeselee@fedoraproject.org> - 2.20.2673.102-1
- Update to 2.20.2673.102
- URL changed to github
- Bundled japanese-usage-dictionary and protobuf
- Enable tests, and bundled googletest and jsoncpp for tests
- BR removed: protobuf-devel protobuf-c
- BR qt5 instead of qt4, since upstream no longer supports qt4
- Fix Provides for elisp packages
- Don't undefine _hardened_build
- Include some documents
- Add fcitx input module

* Sun Dec  4 2016 mosquito <sensor.wen@gmail.com> - 2.18.2612.102-1
- Update to 2.18.2612.102

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 2.17.2322.102-2
- Rebuild for protobuf 3.1.0

* Fri Jun  3 2016 Akira TAGOH <tagoh@redhat.com> - 2.17.2322.102-1
- Update to 2.17.2322.102.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.2077.102-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan  4 2016 Akira TAGOH <tagoh@redhat.com>
- Use %%global instead of %%define.

* Wed Sep 16 2015 Richard Hughes <rhughes@redhat.com> - 2.17.2077.102-6
- Increase AppStream search result weighting when using the 'ja' locale.

* Tue Jun 23 2015 Akira TAGOH <tagoh@redhat.com> - 2.17.2077.102-5
- Merge emacs sub-packages into main (#1234578)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.2077.102-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Akira TAGOH <tagoh@redhat.com> - 2.17.2077.102-3
- Build with the proper compiler options to get the debugging information. (#1219594)

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 2.17.2077.102-2
- Rebuilt for protobuf soname bump

* Tue Apr 28 2015 Akira TAGOH <tagoh@redhat.com> - 2.17.2077.102-1
- rebase to 2.17.2077.102.

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.15.1814.102-4
- Register as an AppStream component.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15.1814.102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug  6 2014 Akira TAGOH <tagoh@redhat.com> - 1.15.1814.102-2
- Drop BR: openssl-devel (#1126245)
- Fix the broken deps for the recent changes in zinnia.

* Thu Jun 26 2014 Akira TAGOH <tagoh@redhat.com> - 1.15.1814.102-1
- New upstream release.
- Update zipcode.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13.1651.102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jan  8 2014 Akira TAGOH <tagoh@redhat.com> - 1.13.1651.102-1
- New upstream release (#1048793)

* Tue Nov  5 2013 Akira TAGOH <tagoh@redhat.com> - 1.12.1599.102-1
- New upstream release (#1026004)
- Update zipcode.

* Tue Oct  1 2013 Akira TAGOH <tagoh@redhat.com> - 1.11.1522.102-3
- Disable ibus-mozc on the password box in gtk. (#1013789)
- Update zipcode.

* Fri Sep 27 2013 Akira TAGOH <tagoh@redhat.com> - 1.11.1522.102-2
- Update ibus cache at %%post/%%postun.

* Tue Sep  3 2013 Akira TAGOH <tagoh@redhat.com> - 1.11.1522.102-1
- New upstream release (#1003331)

* Fri Aug 16 2013 Akira TAGOH <tagoh@redhat.com> - 1.11.1502.102-3
- Fix no setup icon at gnome-control-center.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.11.1502.102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 19 2013 Akira TAGOH <tagoh@redhat.com> - 1.11.1502.102-1
- New upstream release. (#985318)
- Update zipcode dictionaries.

* Mon Apr 15 2013 Akira TAGOH <tagoh@redhat.com> - 1.10.1390.102-1
- New upstream release. (#328711)
- Move credit text since it was referenced by the program at runtime.

* Thu Mar 28 2013 Akira TAGOH <tagoh@redhat.com> - 1.10.1389.102-1
- New upstream release. (#928711)
- Improve the spec file (#891078)

* Wed Mar 13 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.1187.102-4
- Apply an upstream patch to fix a text property for menus (#920122)
- Update zipcode dictionaries.

* Tue Mar 12 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.1187.102-3
- Rebuild against latest protobuf.

* Mon Jan 28 2013 Akira TAGOH <tagoh@redhat.com> - 1.6.1187.102-2
- Add ibus-setup-mozc-jp.desktop to make the configuration tool accessible
  from the input source configuration on control-center. (#904625)
- Updated License, BR, and Summary. partially fixes of #891078

* Fri Aug 31 2012 Akira TAGOH <tagoh@redhat.com> - 1.6.1187.102-1
- New upstream release. (#853362)
  - no SCIM support anymore.
- Update zipcode dictionaries.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1090.102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun  7 2012 Akira TAGOH <tagoh@redhat.com> - 1.5.1090.102-2
- Enable mozc_renderer.

* Tue Jun  5 2012 Akira TAGOH <tagoh@redhat.com> - 1.5.1090.102-1
- New upstream release. (#828202)
- Update zipcode dictionaries.
- set "default" to the layout in mozc.xml to avoid adding jp keyboard layout
  unexpectedly.

* Thu Apr 26 2012 Akira TAGOH <tagoh@redhat.com> - 1.5.1053.102-1
- New upstream release. (#816526)
- Update zipcode dictionaries.

* Mon Mar 26 2012 Akira TAGOH <tagoh@redhat.com> - 1.4.1033.102-1
- New upstream release.

* Fri Mar  9 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.4.1003.102-2
- Rebuild for ibus 1.4.99.20120304

* Thu Mar  8 2012 Akira TAGOH <tagoh@redhat.com> - 1.4.1003.102-1
- New upstream release.
- Update zipcode dictionaries.

* Wed Mar  7 2012 Takao Fujiwara <tfujiwar@redhat.com> - 1.3.975.102-3
- Rebuild for ibus 1.4.99.20120304

* Mon Feb 27 2012 Akira TAGOH <tagoh@redhat.com> - 1.3.975.102-2
- Fix docdir.

* Mon Feb 13 2012 Akira TAGOH <tagoh@redhat.com> - 1.3.975.102-1
- New upstream release.
- Update zipcode dictionaries.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.930.102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Akira TAGOH <tagoh@redhat.com> - 1.3.930.102-1
- New upstream release.

* Thu Dec  1 2011 Akira TAGOH <tagoh@redhat.com> - 1.3.911.102-1
- New upstream release.

* Tue Nov 29 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.855.102-2
- Add zipcode dictionary.

* Tue Nov 15 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.855.102-1
- New upstream release.

* Fri Sep 30 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.831.102-1
- New upstream release.

* Wed Aug 17 2011 Akira TAGOH <tagoh@redhat.com> - 1.2.809.102-1
- New upstream release.

* Thu Aug 11 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.773.102-3
- Re-enable hotkeys support and add a symbol. (#727022)

* Thu Jul 21 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.773.102-1
- New upstream release.

* Mon Jul 11 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.758.102-2
- Revert hotkeys patch.

* Mon Jul  4 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.758.102-1
- New upstream release.

* Mon Jun 13 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.717.102-3
- Rebuild against new protobuf.

* Wed Jun  1 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.717.102-2
- Fix broken emacs-mozc package.

* Mon May 23 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.717.102-1
- New upstream release.

* Wed Apr 20 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.690.102-0.2.20110419svn
- Fix a wrong path to the model file for handwriting.
- add dep to zinnia-tomoe.

* Tue Apr 19 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.690.102-0.1.20110419svn
- Update to 1.1.690.102.

* Tue Mar  8 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.626.102-0.2.20110301svn
- Fix mozc.el not working when byte-compiled.

* Wed Mar  2 2011 Akira TAGOH <tagoh@redhat.com> - 1.1.626.102-0.1.20110301svn
- Update to 1.1.626.102.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.558.102-0.2.20101216svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 16 2010 Akira TAGOH <tagoh@redhat.com> - 1.0.558.102-0.1.20101216svn
- Update to 1.0.558.102.

* Mon Nov  8 2010 Akira TAGOH <tagoh@redhat.com> - 0.13.523.102-0.2.20101104svn
- Rebuilt against ibus-1.3.99.

* Thu Nov  4 2010 Akira TAGOH <tagoh@redhat.com> - 0.13.523.102-0.1.20101104svn
- Update to 0.13.523.102.

* Fri Oct  8 2010 Akira TAGOH <tagoh@redhat.com> - 0.13.499.102-0.1.20101008svn
- Update to 0.13.499.102.

* Mon Sep 27 2010 Akira TAGOH <tagoh@redhat.com> - 0.13.481.102-0.1.20100927svn
- Update to 0.13.481.102.
- Add emacs-common-mozc, emacs-mozc, emacs-mozc-el, xemacs-mozc and xemacs-mozc-el subpackage.

* Fri Sep 10 2010 Akira TAGOH <tagoh@redhat.com> - 0.13.464.102-0.1.20100910svn
- Update to 0.13.464.102.

* Mon Aug 23 2010 Akira TAGOH <tagoh@redhat.com> - 0.12.434.102-0.2.20100823svn
- Drop the unnecessary Obsoletes tag.
- Output more build messages. (Mamoru Tasaka)
- Own %%{_datadir}/ibus-mozc
- add credits_*.html
- rebase to drop more exec bits.

* Fri Aug 20 2010 Akira TAGOH <tagoh@redhat.com> - 0.12.434.102-0.1.20100820svn
- drop exec bits for source code.
- clean up spec file.
- add mecab-ipadic to License tag.

* Tue Aug 17 2010 Akira TAGOH <tagoh@redhat.com> - 0.12.434.102-0.1.20100817svn
- Update to 0.12.434.102.

* Thu Jul 29 2010 Akira TAGOH <tagoh@redhat.com> - 0.12.422.102-0.1.20100729svn
- Update to 0.12.422.102.

* Mon Jul 12 2010 Akira TAGOH <tagoh@redhat.com> - 0.12.410.102-0.1.20100712svn
- Update to 0.12.410.102.

* Tue Jun 22 2010 Akira TAGOH <tagoh@redhat.com> - 0.11.383.102-0.1.20100621svn
- Update to 0.11.383.102.
- Add a subpackage for scim.

* Thu May 27 2010 Akira TAGOH <tagoh@redhat.com> - 0.11.365.102-0.1.20100527svn
- Update to 0.11.365.102.
- Update mozc-config.
- correct the server directory.

* Thu May 20 2010 Akira TAGOH <tagoh@redhat.com> - 0.11.354.100-0.1.20100520svn
- Updates from svn.
- Add mozc-config from git.

* Tue May 11 2010 Akira TAGOH <tagoh@redhat.com> - 0.10.288.102-0.1.20100511svn
- Initial build.
