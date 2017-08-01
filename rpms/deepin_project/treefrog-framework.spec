%global debug_package %{nil}

Name:           treefrog-framework
Version:        1.18.0
Release:        1%{?dist}
Summary:        High-speed C++ MVC Framework for Web Application
License:        BSD
URL:            https://github.com/treefrogframework/treefrog-framework
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  libbson-devel
BuildRequires:  mongo-c-driver-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  qt5-qtbase-postgresql
BuildRequires:  qt5-qtbase-mysql
BuildRequires:  qt5-qtbase-odbc

%description
High-speed C++ MVC Framework for Web Application.

%package devel
Summary:        Header and development files
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
Header files and libraries for building and developing apps with %{name}.

%prep
%setup -q
rm -rf 3rdparty
sed -i '/mongoc.a/s|=.*|= -lmongoc-1.0\nINCLUDEPATH += %{_includedir}/libbson-1.0 %{_includedir}/libmongoc-1.0|' src/corelib.pro
sed -i -E 's|\s{6}exit||; /#.*MongoDB/,+13d' configure

%build
%configure
%make_build -C src

%install
%make_install INSTALL_ROOT=%{buildroot} -C src

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.*
%license copyright
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/

%changelog
* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 1.18.0-1
- Initial package build
