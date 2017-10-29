Name:           deepin-screenshot
Version:        4.0.10
Release:        1%{?dist}
Summary:        Deepin Screenshot Tool
Summary(zh_CN): 深度截图工具
License:        GPLv3
Url:            https://github.com/linuxdeepin/deepin-screenshot
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-appdata.xml

BuildRequires:  pkgconfig(dtkwidget) = 2.0
BuildRequires:  pkgconfig(dtkwm)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib
Requires:       desktop-file-utils
Requires:       hicolor-icon-theme
Recommends:     deepin-shortcut-viewer

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
install -Dm644 %SOURCE1 %{buildroot}%{_datadir}/appdata/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop ||:
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.appdata.xml

%preun
if [ $1 -eq 0 ]; then
  /usr/sbin/alternatives --remove x-window-screenshot %{_bindir}/%{name}
fi

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:
if [ $1 -eq 1 ]; then
  /usr/sbin/alternatives --install %{_bindir}/x-window-screenshot \
    x-window-screenshot %{_bindir}/%{name} 20
fi

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/dman/%{name}/
%{_datadir}/appdata/%{name}.appdata.xml
%{_datadir}/dbus-1/services/com.deepin.Screenshot.service
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/icons/deepin/apps/scalable/%{name}.svg

%changelog
* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 4.0.10-1
- Update to 4.0.10

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 4.0.9-1
- Update to 4.0.9

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
