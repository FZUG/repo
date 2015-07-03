%global debug_package %{nil}
%global project deepin-screenshot
%global repo %{project}

# commit
%global _commit 753410c090e78e1b540f460c14b43e0a5b881c33
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:       deepin-screenshot
Version:    3.0.2
Release:    1.git%{_shortcommit}%{?dist}
Summary:    Deepin Screenshot Tool
Summary(zh_CN): 深度截图工具

License:    GPLv3
Group:      Applications/Internet
Url:        https://github.com/linuxdeepin/deepin-screenshot
Source0:    https://github.com/linuxdeepin/deepin-screenshot/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires:  gettext
BuildRequires:  python-devel
Requires:  qt5-qtdeclarative
Requires:  qt5-qtmultimedia
Requires:  qt5-qtgraphicaleffects
Requires:  python-qt5
Requires:  gnome-python2-libwnck
Requires:  python-xpybutil
Requires:  deepin-menu
Requires:  deepin-qml-widgets

%description
Provide a quite easy-to-use screenshot tool. Features:
  * Global hotkey to triggle screenshot tool
  * Take screenshot of a selected area
  * Easy to add text and line drawings onto the screenshot

%description -l zh_CN
简单易用的截图工具. 特性:
  * 支持全局热键激活截图工具
  * 支持区域截图
  * 支持为截图添加文本和图形

%prep
%setup -q -n %repo-%{_commit}

%build

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/%{name}
cp -r {image,sound,src} %{buildroot}%{_datadir}/%{name}
install -Dm 644 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
ln -sfv %{_datadir}/%{name}/src/main.py %{buildroot}%{_bindir}/%{name}
chmod 755 %{buildroot}%{_datadir}/%{name}/src/*.py

# locale files
pushd locale
for i in `ls *.po`
 do
   install -d %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/
   msgfmt $i -o %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/%{name}.mo
 done
popd

%find_lang %{name}

%preun
if [ $1 -eq 0 ]; then
    update-alternatives --remove x-window-screenshot %{_bindir}/%{name}
fi

%post
if [ $1 -eq 1 ]; then
    update-alternatives --install %{_bindir}/x-window-screenshot x-window-screenshot \
        %{_bindir}/%{name} 20
fi

%files -f %{name}.lang
%defattr(-,root,root,-)
#%%doc AUTHORS ChangeLog README
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}
%{_bindir}/%{name}

%changelog
* Fri Jul  3 2015 mosquito <sensor.wen@gmail.com> - 3.0.2-1.git753410c
- Update version to 3.0.2-1.git753410c
* Wed Dec 31 2014 mosquito <sensor.wen@gmail.com> - 2.1git20141231-1
- Update version to 2.1git20141231
* Mon Dec 15 2014 mosquito <sensor.wen@gmail.com> - 2.1git20141212-1
- Update version to 2.1git20141212
* Tue Nov  4 2014 mosquito <sensor.wen@gmail.com> - 2.1git20141104-1
- Update version to 2.1git20141104
* Mon Oct  6 2014 mosquito <sensor.wen@gmail.com> - 2.1git20140926-2
- Fixed depends
* Sun Oct  5 2014 mosquito <sensor.wen@gmail.com> - 2.1git20140926-1
- Initial build
