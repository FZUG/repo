Name:           deepin-anything
Version:        0.0.2
Release:        1%{?dist}
Summary:        Deepin Anything file search tool
License:        GPLv3
Url:            https://github.com/linuxdeepin/deepin-anything
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(Qt5Gui)
Requires:       dkms

%description
%{summary}.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q
sed -i 's|/lib/systemd/system|%{_unitdir}|' server/src/src.pro
sed -i '/CONFIG +=/s|$| debug|' server/{src/src,lib/lib}.pro
sed -i 's|/usr/lib/$(DEB_HOST_MULTIARCH)|$(LIBDIR)|
        s|^DEB.*|LIBDIR =\nQMAKE_BIN=|
        s|qmake|$(QMAKE_BIN)|
        s|library all|library debug|
        s|release|debug|' Makefile

%build
%make_build VERSION=%{version} LIBDIR=%{_libdir} QMAKE_BIN=%{qmake_qt5}

%install
%make_install VERSION=%{version} LIBDIR=%{_libdir}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}-server
%{_libdir}/%{name}-server-lib/plugins/handlers/README.txt
%{_libdir}/lib*.so.*
%{_unitdir}/%{name}-server.service

%{_prefix}/lib/modules-load.d/anything.conf
%{_usrsrc}/%{name}-%{version}/

%files devel
%{_includedir}/%{name}/
%{_includedir}/%{name}-server/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%changelog
* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 0.0.2-1
- Initial package build
