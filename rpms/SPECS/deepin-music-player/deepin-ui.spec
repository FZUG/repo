%global debug_package %{nil}
%global project deepin-ui
%global repo %{project}

# commit
%global _commit 8d758066245fcb5829f403f9452e571fcfca2b4b
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		deepin-ui
Version:	1.0.4
Release:	1.git%{_shortcommit}%{?dist}
Summary:	UI toolkit for Linux Deepin

License:	GPLv3
Group:		Development/Libraries
Url:		https://github.com/linuxdeepin/deepin-ui
Source0:	https://github.com/linuxdeepin/deepin-ui/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:	noarch
BuildRequires:	gettext
BuildRequires:	pkgconfig
BuildRequires:	cairo-devel
BuildRequires:	webkitgtk-devel
BuildRequires:	python-devel
BuildRequires:	pygtk2-devel
BuildRequires:	python-setuptools
BuildRequires:	hicolor-icon-theme
Requires:	pywebkitgtk
Requires:	deepin-utils
Requires:	deepin-gsettings

%description
UI toolkit libs for Linux Deepin, Awesome and Beautiful UI libs with LinuxDeepin.

%package demo
Summary:	UI toolkit for Linux Deepin
Group:		Development/Languages
Requires:	%{name} = %{version}

%description demo
UI toolkit libs demos for Linux Deepin, Awesome and Beautiful UI libs with LinuxDeepin.

%prep
%setup -q -n %repo-%{_commit}

%build

%install
export CFLAGS="$RPM_OPT_FLAGS"
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

# locale files
rm -rf dtk/locale/deepin-ui.pot
pushd dtk/locale
for i in `ls *.po`
 do
    install -d %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/
    msgfmt $i -o %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/%{name}.mo
 done
popd

# deepin-ui-demo files install
install -d %{buildroot}%{_datadir}/%{name}-demo
cp -R demos/* %{buildroot}%{_datadir}/%{name}-demo

install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{name}-demo/demo.py %{buildroot}%{_bindir}/%{name}-demo
chmod 755 %{buildroot}%{_datadir}/%{name}-demo/demo.py

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING FAQ TODO README
%{python_sitelib}/dtk*

%files demo
%defattr(-,root,root,-)
%{_bindir}/%{name}-demo
%{_datadir}/%{name}-demo

%changelog
* Wed Jul  1 2015 mosquito <sensor.wen@gmail.com> - 1.0.4-1.git8d75806
- Update version to 1.0.4-1.git8d75806
* Sat Nov  8 2014 mosquito <sensor.wen@gmail.com> - 1.0.3git20141104-2
- Update version to 1.0.3git20141104
* Thu Nov  6 2014 mosquito <sensor.wen@gmail.com> - 1.0.3git20141104-1
- Update version to 1.0.3git20141104
* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 1.0.3git20140703-1
- Rebuild for Fedora and rhel
* Fri Jun 21 2013 Huaren Zhong <huaren.zhong@gmail.com>
- Rebuild for Fedora
* Wed Oct 10 2012 hillwood@linuxfan.org
- Fix permission for all theme.txt files
* Tue Oct  9 2012 hillwood@linuxfan.org
- Add deepin-ui-demo package , it was lost before.
* Sun Oct  7 2012 douglarek@outlook.com
- Updated to 1.0.3git20120929
  * Fix menu item clicked bug
  * Add delete tab feature in TabBox
  * Add ComboButton
  Also more features and bugs fixed
* Wed Sep 26 2012 hillwood@linuxfan.org
- update to 1.0.2git20120911
- add new Paned widget and new ui and animation
- TreeView is more powerful
- Optimize Icon View memory usage
- and more ....
* Tue Sep  4 2012 cfarrell@suse.com
- license update: GPL-3.0+
  No indication of GPL-3.0 "only" licenses in the package
* Sun Sep  2 2012 hillwood@linuxfan.org
- Initial package 1.0git20120817
