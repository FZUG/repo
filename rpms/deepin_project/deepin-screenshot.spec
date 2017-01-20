%global _commit b0cc9f8b4913b430a256b60959692848fd6f70aa
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-screenshot
Version:        3.1.10
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Screenshot Tool
Summary(zh_CN): 深度截图工具

License:        GPLv3
Group:          Applications/Internet
Url:            https://github.com/linuxdeepin/deepin-screenshot
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  python-devel
BuildRequires:  deepin-gettext-tools
Requires:       qt5-qtsvg
Requires:       qt5-qtdeclarative
Requires:       qt5-qtmultimedia
Requires:       qt5-qtquickcontrols
Requires:       qt5-qtgraphicaleffects
Requires:       python-qt5
Requires:       gnome-python2-libwnck
Requires:       python2-xpybutil
Requires:       deepin-menu
Requires:       deepin-qml-widgets

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
%setup -q -n %{name}-%{_commit}

# fix python version
find -iname "*.py" | xargs sed -i '1s|python$|python2|'

%build
%make_build

%install
%make_install

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
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.1.10-1.gitb0cc9f8
- Update to 3.1.10
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
