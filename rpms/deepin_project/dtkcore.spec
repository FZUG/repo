Name:           dtkcore
Version:        0.3.3
Release:        1%{?dist}
Summary:        Deepin tool kit core modules
License:        GPLv3
URL:            https://github.com/linuxdeepin/dtkcore
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  qt5-qtbase-devel

%description
Deepin tool kit core modules.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q

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
%{_libdir}/lib*.so.*

%files devel
%doc src/Specification.md
%{_includedir}/libdtk-*/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%changelog
* Sat Jul 29 2017 mosquito <sensor.wen@gmail.com> - 0.3.3-1
- Initial build
