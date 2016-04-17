%global debug_package %{nil}
%global project html2text
%global repo %{project}

# commit
%global _commit cff6d96389521c3d117895e694e881e5bc9b1672
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%if 0%{?fedora} || 0%{?rhel} >= 7
%global with_python3 1
%{!?python3_sitelib: %define python3_sitelib %(%{__python3} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%global with_python2 1
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:    python-html2text
Version: 2016.4.2
Release: 1.git%{_shortcommit}%{?dist}
Summary: Converts a page of HTML into plain ASCII text
Summary(zh_CN): 转换页面中的 HTML 为 ASCII 字符

Group:   Development/Languages
License: GPLv3
URL:     http://alir3z4.github.io/html2text
Source0: https://github.com/Alir3z4/html2text/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-setuptools
BuildRequires: python-coverage

%description
html2text is a Python script that converts a page of HTML into clean,
easy-to-read plain ASCII text. Better yet, that ASCII also happens to
be valid Markdown (a text-to-HTML format).

Also known as: THE ASCIINATOR, html to text, htm to txt, htm2txt, ...

%description -l zh_CN
html2text 使用 Python 语言编写, 用于转换页面中的 HTML 为整洁、易读的
ASCII 文本. 更好的是, ASCII 文本还可以有效的以 Markdown 格式编写.

html2text 还被称为: THE ASCIINATOR, html to text, htm to txt, htm2txt, ...


%if 0%{?with_python3}
%package -n python3-html2text
Summary: Converts a page of HTML into plain ASCII text
Summary(zh_CN): 转换页面中的 HTML 为 ASCII 字符
BuildArch: noarch
BuildRequires: python3-devel
BuildRequires: python3-setuptools

%description -n python3-html2text
html2text is a Python script that converts a page of HTML into clean,
easy-to-read plain ASCII text. Better yet, that ASCII also happens to
be valid Markdown (a text-to-HTML format).

Also known as: THE ASCIINATOR, html to text, htm to txt, htm2txt, ...

%description -n python3-html2text -l zh_CN
html2text 使用 Python 语言编写, 用于转换页面中的 HTML 为整洁、易读的
ASCII 文本. 更好的是, ASCII 文本还可以有效的以 Markdown 格式编写.

html2text 还被称为: THE ASCIINATOR, html to text, htm to txt, htm2txt, ...
%endif # with_python3


%prep
%setup -q -n %repo-%{_commit}

%build
%{__python} setup.py build --build-base=python2
%if 0%{?with_python3}
%{__python3} setup.py build --build-base=python3
%endif # with_python3


%install
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install -O1 --skip-build --root=%{buildroot}
install -Dm 0644 python2/lib/html2text/__init__.py %{buildroot}%{python_sitelib}/html2text/__init__.py
install -Dm 0644 python2/lib/html2text/config.py %{buildroot}%{python_sitelib}/html2text/config.py
install -Dm 0644 python2/lib/html2text/compat.py %{buildroot}%{python_sitelib}/html2text/compat.py
install -Dm 0644 python2/lib/html2text/utils.py %{buildroot}%{python_sitelib}/html2text/utils.py
install -Dm 0644 python2/lib/html2text/cli.py %{buildroot}%{python_sitelib}/html2text/cli.py
mv %{buildroot}%{_bindir}/{html2text,%{name}}

%if 0%{?with_python3}
%{__python3} setup.py install -O1 --skip-build --root=%{buildroot}
install -Dm 0644 python3/lib/html2text/__init__.py %{buildroot}%{python3_sitelib}/html2text/__init__.py
install -Dm 0644 python3/lib/html2text/config.py %{buildroot}%{python3_sitelib}/html2text/config.py
install -Dm 0644 python3/lib/html2text/compat.py %{buildroot}%{python3_sitelib}/html2text/compat.py
install -Dm 0644 python3/lib/html2text/utils.py %{buildroot}%{python3_sitelib}/html2text/utils.py
install -Dm 0644 python3/lib/html2text/cli.py %{buildroot}%{python3_sitelib}/html2text/cli.py
mv %{buildroot}%{_bindir}/{,python3-}html2text
%endif # with_python3


%check
# Unit test
PYTHONPATH=%{buildroot}%{python_sitelib} coverage run --source=html2text setup.py test -v
%if 0%{?with_python3}
PYTHONPATH=%{buildroot}%{python3_sitelib} coverage run --source=html2text setup.py test -v
%endif # with_python3


%files
%defattr(-,root,root,-)
%doc AUTHORS.rst ChangeLog.rst README.md
%license COPYING
%{_bindir}/%{name}
%{python_sitelib}/html2text
%{python_sitelib}/html2text-%{version}-py%{python_version}.egg-info

%if 0%{?with_python3}
%files -n python3-html2text
%defattr(-,root,root,-)
%doc AUTHORS.rst ChangeLog.rst README.md
%license COPYING
%{_bindir}/python3-html2text
%{python3_sitelib}/html2text
%{python3_sitelib}/html2text-%{version}-py%{python3_version}.egg-info
%endif # with_python3


%changelog
* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 2016.4.2-1.gitcff6d96
- Update version to 2016.4.2

* Sun Jan 17 2016 mosquito <sensor.wen@gmail.com> - 2016.1.8-1.git0c70c8f
- Update version to 2016.1.8

* Sun Dec 13 2015 mosquito <sensor.wen@gmail.com> - 2015.11.4-1.git9157181
- Update version to 2015.11.4

* Tue Jun 30 2015 mosquito <sensor.wen@gmail.com> - 2015.6.21-1.gitb8415f8
- Update version to 2015.6.21

* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 2015.4.14-1.gite902a7c
- Update version to 2015.4.14
- Rename version name

* Thu Mar 05 2015 mosquito <sensor.wen@gmail.com> - 2015.2.18git20150218-1
- Update version to 2015.2.18git20150218

* Tue Dec 30 2014 mosquito <sensor.wen@gmail.com> - 2014.12.29git20141229-1
- Update version to 2014.12.29git20141229

* Fri Dec 26 2014 mosquito <sensor.wen@gmail.com> - 2014.12.24git20141224-1
- Update version to 2014.12.24git20141224

* Tue Dec 09 2014 mosquito <sensor.wen@gmail.com> - 2014.12.5git20141205-2
- Rebuild for python3

* Sun Dec 07 2014 mosquito <sensor.wen@gmail.com> - 2014.12.5git20141205-1
- Update version to 2014.12.5git20141205

* Wed Dec 3 2014 mosquito <sensor.wen@gmail.com> - 2014.9.25-2
- Rebuild for python3

* Tue Dec 2 2014 mosquito <sensor.wen@gmail.com> - 2014.9.25-1
- Support python3

* Mon Jun 30 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 3.200.3-7
- Replace python-setuptools-devel BR with python-setuptools

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.200.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.200.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 19 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 3.200.3-4
- Merge "remove-newlines" (from alt tags) patch (Debian #299027).
- Include html2text script as python-html2script.
- Minor spec cleanup.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.200.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.200.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Michael Schwendt <mschwendt@fedoraproject.org> - 3.200.3-1
- TODO: decide on the new /usr/bin/html2text this one wants to install
- update to 3.200.3

* Tue Apr 12 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.02-2
- add disttag

* Mon Apr 11 2011 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 3.02-1
- update to 3.02
- download tarball from github
- use setuptools

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.38-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.38-2.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sun Jul 04 2010 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.38-1
- update to 2.38

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.35-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.35-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 13 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.35-1
- update to 2.35

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.34-2.1
- Rebuild for Python 2.6

* Sat Oct 11 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.34-1
- update to 2.34

* Sat Sep 27 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.33-1
- update to 2.33

* Fri Aug 01 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.32-1
- update to 2.32

* Sun Jul 27 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.31-1
- update to 2.31

* Fri Jul 04 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.30-1
- update to 2.30 (GPLv3 now)

* Fri Nov 02 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.29-1
- update to 2.29

* Thu Oct 04 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.28-1
- update to 2.28 (just one line actually different)

* Thu Oct 04 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.26-3
- BR python (fixes #317211)

* Fri Aug 03 2007 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info>
- Update License field due to the "Licensing guidelines changes"

* Sat Mar 24 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.26-2
- Use sed instead of dos2unix

* Sat Mar 24 2007 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 2.26-1
- Initial package
