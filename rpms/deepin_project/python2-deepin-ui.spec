%global project deepin-ui
%global repo %{project}

%global _commit 03bcd2050aef4e8f6a91bb5ef0b194bebd558715
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           python2-%{repo}
Version:        1.0.5
Release:        1.git%{_shortcommit}%{?dist}
Summary:        UI toolkit for Linux Deepin

License:        GPLv3
Group:          Development/Libraries
Url:            https://github.com/martyr-deepin/deepin-ui
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  pkgconfig
BuildRequires:  python-devel
BuildRequires:  python2-setuptools
BuildRequires:  pygtk2-devel
BuildRequires:  cairo-devel
BuildRequires:  webkitgtk-devel
BuildRequires:  deepin-gettext-tools
BuildRequires:  hicolor-icon-theme
Requires:       libsoup
Requires:       pywebkitgtk
Requires:       pygtk2
Requires:       pycairo
Requires:       python-pillow
Requires:       python-xlib
Requires:       python2-scipy
Requires:       python2-deepin-utils
Requires:       python2-deepin-gsettings
Provides:       python-%{repo} = %{version}-%{release}

%description
UI toolkit libs for Linux Deepin, Awesome and Beautiful UI libs with LinuxDeepin.

%package demo
Summary:        UI toolkit for Linux Deepin
Group:          Development/Languages
Requires:       %{name} = %{version}

%description demo
UI toolkit libs demos for Linux Deepin, Awesome and Beautiful UI libs with LinuxDeepin.

%prep
%setup -q -n %{repo}-%{_commit}

# fix python version
find -iname "*.py" | xargs sed -i '1s|python$|python2|'

%build
%{__python2} setup.py build
deepin-generate-mo dtk/tools/locale_config.ini

%install
%{__python} setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}

# locale files
rm -rf dtk/locale/deepin-ui.pot
pushd dtk/locale
for i in `ls *.po`
 do
    install -d %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/
    msgfmt $i -o %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/%{repo}.mo
 done
popd

# deepin-ui-demo files install
install -d %{buildroot}%{_datadir}/%{repo}-demo
cp -R demos/* %{buildroot}%{_datadir}/%{repo}-demo

install -d %{buildroot}%{_bindir}
ln -s %{_datadir}/%{repo}-demo/demo.py %{buildroot}%{_bindir}/%{repo}-demo
chmod 755 %{buildroot}%{_datadir}/%{repo}-demo/demo.py

%find_lang %{repo}

%files -f %{repo}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING FAQ TODO README
%{python_sitelib}/dtk*

%files demo
%defattr(-,root,root,-)
%{_bindir}/%{repo}-demo
%{_datadir}/%{repo}-demo

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.5-1.git03bcd20
- Update to 1.0.5
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
