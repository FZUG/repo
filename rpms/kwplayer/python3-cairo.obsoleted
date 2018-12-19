%global debug_package %{nil}
%define cairo_version 1.10.2

### Abstract ###
Name:		python3-cairo
Version:	1.10.0
Release:	12%{?dist}
License:	MPLv1.1 or LGPLv2
Group:		Development/Languages
Summary:	Python 3 bindings for the cairo library
Summary(zh_CN): cairo 库的 Python 3 绑定
URL:		http://cairographics.org/pycairo
Source:		http://cairographics.org/releases/pycairo-%{version}.tar.bz2

# Since Python 3.4, pythonX.Y-config is shell script, not Python script,
#  so prevent waf from trying to invoke it as a Python script
Patch0:		cairo-waf-use-python-config-as-shell-script.patch
Patch1:		pycairo-1.10.0-test-python3.patch
# Add support for cairo_region_t
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=688079
Patch2:		101_pycairo-region.patch

### Build Dependencies ###
BuildRequires:	cairo-devel >= %{cairo_version}
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	python3-pytest
BuildRequires:	lyx-fonts

%description
Python 3 bindings for the cairo library.

%description -l zh_CN
cairo 库的 Python 3 绑定.

%package devel
Summary:	Libraries and headers for python3-cairo
Summary(zh_CN): python3-cairo 库和头文件
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	cairo-devel
Requires:	pkgconfig
Requires:	python3-devel

%description devel
This package contains files required to build wrappers for cairo add-on
libraries so that they interoperate with python3-cairo.

%description devel -l zh_CN
此包包含构建 cairo 插件库封装所必须的文件, 以便使用 python3-cairo 操作.


%prep
%setup -q -n pycairo-%{version}

# Ensure that ./waf has created the cached unpacked version
# of the wafadmin source tree.
# This will be created to a subdirectory like
#    .waf3-1.5.18-a7b91e2a913ce55fa6ecdf310df95752
%{__python3} ./waf --version

%patch0 -p0
%patch1 -p1
%patch2 -p1


%build
# FIXME: we should be using the system version of waf (e.g. %{_bindir}/waf)
export CFLAGS="$RPM_OPT_FLAGS"
export PYTHON=python3
#python3 setup.py install -O1 --skip-build --root %{buildroot}
%{__python3} ./waf --prefix=%{_usr} \
		--libdir=%{_libdir} \
		configure

# do not fail on utf-8 encoded files
LANG=en_US.utf8 %{__python3} ./waf build -v

# remove executable bits from examples
find ./examples/ -type f -print0 | xargs -0 chmod -x

# add executable bit to the _cairo.so library so we strip the debug info:wq


%install
rm -rf $RPM_BUILD_ROOT

DESTDIR=%{buildroot} %{__python3} ./waf install

# add executable bit to the .so libraries so we strip the debug info
find %{buildroot} -name '*.so' | xargs chmod +x
find %{buildroot} -name '*.la' | xargs rm -f


%check
cd test
PYTHONPATH=%{buildroot}%{python3_sitearch} %{_bindir}/py.test-3*


%files
%doc AUTHORS COPYING* NEWS README
%doc examples doc/faq.rst doc/overview.rst doc/README 
%{python3_sitearch}/cairo/

%files devel
%{_includedir}/pycairo/py3cairo.h
%{_libdir}/pkgconfig/py3cairo.pc


%changelog
* Tue Nov 18 2014 mosquito <sensor.wen@gmail.com> - 1.10.0-12
- Fixed https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=688079

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Jakub Čajka <jcajka@redhat.com> - 1.10.0-10
- Fixed tests on ppc(64(le)) by adding missing fonts

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.10.0-8
- Cleanup spec
- Run tests (RHBZ 1045724)

* Mon May 12 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Fixed bundled waf to work correctly with python3.4-config

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 03 2012 David Malcolm <dmalcolm@redhat.com> - 1.10.0-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Aug 18 2011 John (J5) Palmieri <johnp@redhat.com> - 1.10.0-1
- update to upstream 1.10.0

* Thu Feb 10 2011 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-12
- remove cairo_rectangle_int_t patch as it was rejected upstream and is
  no longer needed

* Thu Feb 10 2011 David Malcolm <dmalcolm@redhat.com> - 1.8.10-11
- fix embedded copy of waf so that the package builds against python
3.2 (PEP-3149)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 10 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-9
- add rectangle_int_t wrapper patch which is needed by PyGObject

* Thu Sep 30 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-8
- typo, set CFLAGS to $RPM_OPT_FLAGS not RPM_BUILD_OPTS

* Tue Sep 28 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-7
- add patch to move to using PyCapsule API since PyCObject was removed from 3.2

* Tue Sep 28 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-6
- move defattr above the first file manifest item in the devel sub package 

* Mon Sep 27 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-5
- revert back to using the provided waf script until 
  https://bugzilla.redhat.com/show_bug.cgi?id=637935
  is fixed

* Mon Sep 27 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-4
- add buildreq for waf

* Wed Sep 22 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-3
- Use system waf instead of bundled version (this does not work
  on F13 since the system waf contains syntax which has changed
  in python3)

* Wed Sep 22 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-2
- Fixed up for package review

* Thu Sep 16 2010 John (J5) Palmieri <johnp@redhat.com> - 1.8.10-1
- Initial build.

