%global project qt5integration
%global repo %{project}

%global _commit c0dc3cf6e52433bc3a39a6e72060a5ecf7d1d8e6
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-qt5integration
Version:        0.0.5
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Qt platform theme integration plugins for DDE
License:        GPLv3
URL:            https://github.com/linuxdeepin/qt5integration
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

# full build requires
BuildRequires:  git
BuildRequires:  dbus-devel
BuildRequires:  deepin-tool-kit-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  qt5-qtbase-static
BuildRequires:  qt5-qtsvg-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  libqtxdg-devel
BuildRequires:  libICE-devel
BuildRequires:  libSM-devel
BuildRequires:  libX11-devel
BuildRequires:  libXext-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrender-devel
BuildRequires:  atk-devel
BuildRequires:  cairo-devel
BuildRequires:  fontconfig-devel
BuildRequires:  freetype-devel
BuildRequires:  gtk2-devel
BuildRequires:  glib2-devel
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  libinput-devel
BuildRequires:  mtdev-devel
BuildRequires:  pango-devel
BuildRequires:  xcb-util-wm-devel
BuildRequires:  xcb-util-image-devel
BuildRequires:  xcb-util-keysyms-devel
BuildRequires:  xcb-util-renderutil-devel
BuildRequires:  libxcb-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  libxkbcommon-devel

%description
Multiple Qt plugins to provide better Qt5 integration for DDE is included.

%prep
%setup -q -n %{repo}-%{_commit}

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%{_qt5_plugindir}/platforms/libdxcb.so
%{_qt5_plugindir}/platformthemes/libqdeepin.so
%{_qt5_plugindir}/styles/libdstyleplugin.so

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.0.5-1.gitc0dc3cf
- Initial build
