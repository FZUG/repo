Name:           deepin-screenshot
Version:        4.0.8
Release:        1%{?dist}
Summary:        Deepin Screenshot Tool
Summary(zh_CN): 深度截图工具
License:        GPLv3
Group:          Applications/Internet
Url:            https://github.com/linuxdeepin/deepin-screenshot
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  libXtst-devel
BuildRequires:  xcb-util-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
#Requires:       deepin-daemon

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
%setup -q

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%preun
if [ $1 -eq 0 ]; then
  /usr/sbin/alternatives --remove x-window-screenshot %{_bindir}/%{name}
fi

%post
if [ $1 -eq 1 ]; then
  /usr/sbin/alternatives --install %{_bindir}/x-window-screenshot \
    x-window-screenshot %{_bindir}/%{name} 20
fi

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/dman/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/deepin/apps/scalable/%{name}.svg

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 4.0.8-1.gitb7483cf
- Update to 4.0.8
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 4.0.0-1.gitcb50df2
- Update to 4.0.0
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
