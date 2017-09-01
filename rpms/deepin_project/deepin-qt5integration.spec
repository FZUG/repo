%global repo qt5integration

Name:           deepin-qt5integration
Version:        0.2.3
Release:        1%{?dist}
Summary:        Qt platform theme integration plugins for DDE
# The entire source code is GPLv3+ except styles/ which is BSD,
# dstyleplugin/ platformplugin/ which is GPLv3, dstyleplugin/dstyleanimation* which is LGPL
License:        GPLv3 and BSD and LGPLv2+
URL:            https://github.com/linuxdeepin/qt5integration
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
Source1:        https://download.qt.io/official_releases/qt/5.9/5.9.1/submodules/qtbase-opensource-src-5.9.1.tar.xz

# full build requires
BuildRequires:  pkgconfig(atk)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(dbus-1)
BuildRequires:  pkgconfig(dtkwidget) = 2.0
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(gtk+-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(mtdev)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(Qt5Xdg)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-image)
BuildRequires:  pkgconfig(xcb-keysyms)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xkbcommon-x11)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  qt5-qtbase-common
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtstyleplugins

%description
Multiple Qt plugins to provide better Qt5 integration for DDE is included.

%prep
%setup -q -a1 -n %{repo}-%{version}

# qtxcb private header files
sed -i '/exist/,$d' platformplugin/linux.pri
install -d platformplugin/libqt5xcbqpa-dev/
cp qtbase-opensource-src-5.9.1/src/plugins/platforms/xcb/*.h \
  platformplugin/libqt5xcbqpa-dev/

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%doc README.md
%license LICENSE
%{_qt5_plugindir}/platforms/libdxcb.so
%{_qt5_plugindir}/platformthemes/libqdeepin.so
%{_qt5_plugindir}/styles/libdstyleplugin.so

%changelog
* Tue Aug 22 2017 mosquito <sensor.wen@gmail.com> - 0.2.3-1
- Update to 0.2.3

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 0.2.2-1
- Update to 0.2.2

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 0.2.1-1.git2cd7432
- Update to 0.2.1

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 0.1.8-1.gitb03be20
- Update to 0.1.8

* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 0.1.2-1.gitecde076
- Update to 0.1.2

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 0.1.1-1.gitaa563fd
- Update to 0.1.1

* Sat Jan 21 2017 mosquito <sensor.wen@gmail.com> - 0.0.6-1.git40401af
- Update to 0.0.6

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.0.5-1.gitc0dc3cf
- Initial build
