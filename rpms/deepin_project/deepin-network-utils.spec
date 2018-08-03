%global repo dde-network-utils

Name:           deepin-network-utils
Version:        0.0.4
Release:        1%{?dist}
Summary:        Deepin desktop-environment - network utils
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-network-utils
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  pkgconfig(dframeworkdbus) >= 2.0
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  qt5-linguist

%description
Deepin desktop-environment - network utils.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q -n %{repo}-%{version}
sed -i 's|lrelease|lrelease-qt5|' translate_generation.sh
sed -i 's|/lib$|/%{_lib}|' dde-network-utils.pro

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md
%{_libdir}/lib*.so.*
%{_datadir}/%{repo}/

%files devel
%{_includedir}/libddenetworkutils/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%changelog
* Thu Aug  2 2018 mosquito <sensor.wen@gmail.com> - 0.0.4-1
- Update to 0.0.4

* Mon Jul 23 2018 mosquito <sensor.wen@gmail.com> - 0.0.3-1
- Initial package build
