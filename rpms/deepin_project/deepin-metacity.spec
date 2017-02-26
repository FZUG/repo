%global _commit 4a903359313a016c7d82a7f4a422cadb929242a4
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-metacity
Version:        3.22.3
Release:        1.git%{_shortcommit}%{?dist}
Summary:        2D window manager for Deepin
License:        GPL
URL:            https://github.com/linuxdeepin/deepin-metacity
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  intltool
BuildRequires:  itstool
BuildRequires:  libtool
BuildRequires:  yelp-tools
BuildRequires:  autoconf-archive
BuildRequires:  bamf-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  gsettings-desktop-schemas-devel
BuildRequires:  json-glib-devel
BuildRequires:  libcanberra-devel
BuildRequires:  libgtop2-devel
BuildRequires:  startup-notification-devel
BuildRequires:  zenity
Requires:       dconf
Requires:       deepin-desktop-schemas

%description
2D window manager for Deepin

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}

%prep
%setup -q -n %{name}-%{_commit}

%build
./autogen.sh
%configure \
    --disable-static \
    --disable-schemas-compile
%make_build

%install
%make_install PREFIX=%{_prefix}
#Remove libtool archives.
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%files
%doc README
%license COPYING
%{_bindir}/%{name}*
%{_libdir}/lib%{name}*.so.*
%{_datadir}/GConf/gsettings/%{name}-schemas.convert
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/
%{_datadir}/glib-2.0/schemas/com.deepin.*.xml
%{_datadir}/gnome-control-center/keybindings/50-%{name}-*.xml
%{_datadir}/gnome/wm-properties/%{name}-wm.desktop
%{_datadir}/help/
%{_datadir}/locale/
%{_datadir}/themes/
%{_mandir}/man1/%{name}*

%files devel
%{_includedir}/%{name}/
%{_libdir}/pkgconfig/lib%{name}*.pc
%{_libdir}/lib%{name}*.so

%changelog
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.22.3-1.git4a90335
- Update to 3.22.3
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.22.0-1.gitb633b85
- Update to 3.22.0
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 3.22.0-1
- Update to version 3.22.0
* Thu Jan 05 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.6-2
- Split the package to main and devel
* Fri Dec 16 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.6-1
- Update to version 3.20.6
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.20.5-1
- Initial package build
