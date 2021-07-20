Name:           pineapple-calendar
Version:        0.1.1
Release:        1%{?dist}
Summary:        Plasma addon that provides Simple Chinese Luni-solar calendar support

License:        LGPLv2+
URL:            https://github.com/BLumia/pineapple-calendar
Source0:        https://github.com/BLumia/pineapple-calendar/archive/refs/tags/0.1.1.tar.gz

BuildRequires:  kf5-plasma-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  libicu-devel
BuildRequires:  cmake
Requires:       kf5-plasma

%description
Plasma addon that provides Simple Chinese Luni-solar calendar support

%prep
%autosetup

%build
%cmake_kf5 -DBUILD_PLASMOID=ON -DBUILD_TESTING=OFF
%cmake_build

%install
%cmake_install

%files
%{_kf5_qmldir}/net/blumia/calendar/*
%{_kf5_datadir}/plasma/plasmoids/net.blumia.pineapple.calendar
%{_kf5_metainfodir}/net.blumia.pineapple.calendar.appdata.xml
%{_kf5_datadir}/kservices5/plasma-applet-net.blumia.pineapple.calendar.desktop


%changelog
* Wed Jul 21 2021 Liu Sen <liusen@disroot.org> - 0.1.1-1
- First build
