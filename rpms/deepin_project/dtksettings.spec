%global commit 34d321e517524d7eb3110dee2c9d3049771ede05
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           dtksettings
Version:        0.1.7
Release:        1.git%{shortcommit}%{?dist}
Summary:        Dtk module to generate user configuration and UI dialog from json
License:        GPLv3
URL:            https://github.com/linuxdeepin/dtksettings
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildRequires:  qt5-qtbase-devel

%description
This package provides a Dtk module which can generate user configuration and UI
dialog from json.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q -n %{name}-%{commit}

%build
%qmake_qt5 PREFIX=%{_prefix} LIB_INSTALL_DIR=%{_libdir}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.md
%license LICENSE
%{_bindir}/dtk-settings-tool
%{_libdir}/lib*.so.*

%files devel
%{_includedir}/libdtk-*/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%changelog
* Sat Jul 29 2017 mosquito <sensor.wen@gmail.com> - 0.1.7-2.git34d321e
- Add LICENSE file

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 0.1.7-1.git32225b9
- Update to 0.1.7

* Sat May 20 2017 mosquito <sensor.wen@gmail.com> - 0.1.6-1.git63c6cb7
- Update to 0.1.6

* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 0.1.3-1.git02002c9
- Update to 0.1.3

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 0.1.2-1.git13efd5f
- Initial build
