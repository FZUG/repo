%global _commit 90453e308fbf7222b5c45f65a7497f5fcaf00fc4
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-wm
Version:        1.9.14
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Window Manager
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-wm
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  intltool
BuildRequires:  gnome-common
BuildRequires:  gnome-desktop3-devel
BuildRequires:  granite-devel
BuildRequires:  vala
BuildRequires:  vala-tools
BuildRequires:  bamf-devel
BuildRequires:  clutter-gtk-devel
BuildRequires:  deepin-mutter-devel
BuildRequires:  upower-devel
BuildRequires:  libgee-devel
BuildRequires:  libgudev-devel
BuildRequires:  libwnck3-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libxkbcommon-x11-devel
BuildRequires:  libxkbfile-devel
Requires:       deepin-desktop-schemas
Requires:       gnome-desktop
Requires:       libcanberra-gtk3

%description
Deepin Window Manager

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}

%prep
%setup -q -n %{name}-%{_commit}

# fix background path
sed -i 's|default_background.jpg|default.png|' \
    src/Background/BackgroundSource.vala

%build
./autogen.sh
%configure --disable-schemas-compile
%make_build

%install
%make_install PREFIX="%{_prefix}"

#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%find_lang %{name}

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/lib*.so.*
%{_libdir}/%{name}/
%{_datadir}/%{name}/
%{_datadir}/glib-2.0/schemas/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/vala/vapi/%{name}*

%files devel
%{_includedir}/%{name}/%{name}.h
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.9.14-1.git90453e3
- Update to 1.9.14
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.9.12-1.git42cd230
- Update to 1.9.12
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 1.9.5-1.git3d3e077
- Update to 1.9.5
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.9.2-1.git4cb2f7e
- Update to 1.9.2
* Wed Jan 04 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.0-2
- Split the package to main and devel
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.2.0-1
- Update to version 1.2.0
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.2-1
- Initial package build
