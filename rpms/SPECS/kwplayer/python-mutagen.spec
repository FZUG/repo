%{!?python3_sitelib: %global python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global realname mutagen
%global debug_package %{nil}

%if 0%{?fedora} || 0%{?rhel} >= 7
%global with_python3 1
%endif
%global with_python2 1

Name:		python-%{realname}
Version:	1.28
Release:	1%{?dist}
Summary:	Mutagen is a Python module to handle audio metadata

Group:		Development/Languages
License:	GPLv2
URL:		https://bitbucket.org/lazka/mutagen/overview
Source0:	https://bitbucket.org/lazka/mutagen/downloads/%{realname}-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	python2-devel

%description
Mutagen is a Python module to handle audio metadata. It supports
reading ID3 (all versions), APEv2, FLAC, and Ogg Vorbis/FLAC/Theora.
It can write ID3v1.1, ID3v2.4, APEv2, FLAC, and Ogg Vorbis/FLAC/Theora
comments. It can also read MPEG audio and Xing headers, FLAC stream
info blocks, and Ogg Vorbis/FLAC/Theora stream headers. Finally, it
includes a module to handle generic Ogg bitstreams.

%if 0%{?with_python3}
%package -n python3-%{realname}
Summary:	Read and write audio tags for many formats in Python 3
BuildRequires:	python3-devel

%description -n python3-%{realname}
A fork of the mutagen package, modified to support Python 3.3+.
I take no credit for the original mutagen - the copyright for that 
is owned by the original developers.
This package isn't compatible with Python 2.x, and will never be.
The intention is to improve the existing code over time, 
making it more Pythonic and better documented, 
and possibly adding new features such as id3v2.3 support.
%endif # with_python3

%prep
%setup -q -n %{realname}-%{version}

%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # with_python3

%build
# Python 2 build:
%{__python} setup.py build

# Python 3 build:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf $RPM_BUILD_ROOT

# Install mutagen for Python 3:
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install -O1 --skip-build --root %{buildroot}
popd
%endif # with_python3

# Install mutagen for Python 2:
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%{__install} -d %{buildroot}%{_mandir}/man1
%{__install} -p -m 0644 man/*.1 %{buildroot}%{_mandir}/man1

%check
%{__python} setup.py test

%if 0%{?with_python3}
%{__python3} setup.py test
%endif # with_python3

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README.rst docs/tutorial.rst docs/api_notes.rst docs/bugs.rst
%{_bindir}/*
%{_mandir}/man1/m*.1*
%{python_sitelib}/%{realname}
%{python_sitelib}/%{realname}-%{version}-py%{python_version}.egg-info

%if 0%{?with_python3}
%files -n python3-mutagen
%defattr(-,root,root,-)
%doc COPYING NEWS README.rst docs/tutorial.rst docs/api_notes.rst docs/bugs.rst
%{python3_sitelib}/%{realname}
%{python3_sitelib}/%{realname}-%{version}-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/mutagen/__pycache__
%endif # with_python3

%changelog
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
