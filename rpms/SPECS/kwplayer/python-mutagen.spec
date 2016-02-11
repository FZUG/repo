%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global realname mutagen
%global debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global with_python3 1
%endif

Name:           python-%{realname}
Version:        1.31
Release:        2%{?dist}
Summary:        Mutagen is a Python module to handle audio metadata
Summary(zh_CN): 一个处理音频元数据的Python模块

Group:          Development/Languages
License:        GPLv2
URL:            https://bitbucket.org/lazka/mutagen/overview
Source0:        https://bitbucket.org/lazka/mutagen/downloads/%{realname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel

%description
Mutagen is a Python module to handle audio metadata. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bitstreams.

%if 0%{?with_python3}
%package -n python3-%{realname}
Summary:        Read and write audio tags for many formats in Python 3
Summary(zh_CN): 一个处理音频元数据的Python3模块
BuildRequires:  python3-devel

%description -n python3-%{realname}
Mutagen is a Python module to handle audio meta-data. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bit-streams.
%endif # with_python3

%prep
%setup -q -n %{realname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
%{__python} setup.py build

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with_python3

%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -p -m 0644 man/*.1 %{buildroot}%{_mandir}/man1

%check
# Without this the testsuite fails with
# RuntimeError: This test suite needs a unicode locale encoding. Try setting LANG=C.UTF-8
# Hopefully all builders have this locale installed/configured
export LANG=en_US.utf-8
%{__python} setup.py test

%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py test
%endif # with_python3

%files
%defattr(-,root,root,-)
%doc NEWS README.rst docs/tutorial.rst docs/api_notes.rst docs/bugs.rst
%license COPYING
%if ! 0%{?with_python3}
%{_bindir}/m*
%{_mandir}/man1/m*.1*
%endif
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-*.egg-info

%if 0%{?with_python3}
%files -n python3-mutagen
%defattr(-,root,root,-)
%doc NEWS README.rst docs/tutorial.rst docs/api_notes.rst docs/bugs.rst
%license COPYING
%{_bindir}/m*
%{_mandir}/man1/m*.1*
%{python3_sitelib}/%{realname}
%{python3_sitelib}/%{realname}-%{version}-*.egg-info
%endif # with_python3

%changelog
* Thu Feb 11 2016 mosquito <sensor.wen@gmail.com> - 1.31-2
- Move the scripts to the python3 package

* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 1.31-1
- Update to 1.31

* Mon Aug 31 2015 mosquito <sensor.wen@gmail.com> - 1.30-1
- Update to 1.30

* Tue May 19 2015 mosquito <sensor.wen@gmail.com> - 1.29-1
- Update to 1.29

* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 1.28-1
- Update to 1.28

* Sat Nov 29 2014 mosquito <sensor.wen@gmail.com> - 1.27-1
- Update to 1.27

* Mon Nov 17 2014 mosquito <sensor.wen@gmail.com> - 1.26-1
- Update to 1.26
- add python3 support

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 19 2010 Silas Sewell <silas@sewell.ch> - 1.20-1
- Update to 1.20

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.19-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 06 2010 Silas Sewell <silas@sewell.ch> - 1.19-1
- Update to 1.19
- Add tests

* Thu Feb 18 2010 Silas Sewell <silas@sewell.ch> - 1.18-1
- Update to 1.18

* Thu Oct 22 2009 Silas Sewell <silas@sewell.ch> - 1.17-1
- Update to 1.17

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 02 2009 Silas Sewell <silas@sewell.ch> - 1.16-1
- Update to 1.16
- New project URLs

* Sun Apr 12 2009 Silas Sewell <silas@sewell.ch> - 1.15-3
- Normalize spec

* Fri Apr 10 2009 Silas Sewell <silas@sewell.ch> - 1.15-2
- Make sed safer
- Add back in removed changelogs

* Sun Mar 29 2009 Silas Sewell <silas@sewell.ch> - 1.15-1
- Update to 1.15

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.13-3
- Rebuild for Python 2.6

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-2
- Add egg-info to package

* Mon Dec 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.13-1
- 1.13

* Sat Aug 25 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.12-1
- Update to 1.12
- License tag fix

* Sat Apr 28 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.11-1
- Update to 1.11

* Wed Jan 31 2007 Michał Bentkowski <mr.ecik at gmail.com> - 1.10.1-1
- Update to 1.10.1

* Wed Dec 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.9-1
- Bump to 1.9

* Tue Dec 12 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-2
- Python 2.5 rebuild

* Sun Oct 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.8-1
- Bump to 1.8

* Fri Sep 29 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-2
- .pyo files no longer ghosted

* Fri Aug 11 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.6-1
- Update upstream to 1.6

* Fri Jul 21 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-5
- Some fixes in preamble.
- Change name from mutagen to python-mutagen.
- Delete CFLAGS declaration.

* Thu Jul 20 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-4
- Add BuildArch: noarch to preamble.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-3
- Remove python-abi dependency.
- Prep section deletes first two lines in __init__.py file due to rpmlint error.

* Sat Jul 15 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-2
- Clean at files section.
- Fix charset in TUTORIAL file.

* Fri Jul 14 2006 Michał Bentkowski <mr.ecik at gmail.com> - 1.5.1-1
- First build.
