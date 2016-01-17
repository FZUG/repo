%global debug_package %{nil}
%global project libQtShadowsocks
%global repo %{project}

# commit
%global _commit d2c76c5db3ebbadc07b8809fa3500ddb92cd9eaf
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    libQtShadowsocks
Version: 1.8.4
Release: 1.git%{_shortcommit}%{?dist}
Summary: A lightweight and ultra-fast shadowsocks library

License: LGPLv3+
URL:     https://github.com/librehat/libQtShadowsocks
Source0: https://github.com/librehat/libQtShadowsocks/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qttools
BuildRequires: botan-devel

%description
A lightweight and ultra-fast shadowsocks library written in C++/Qt.

%package devel
Summary: %{name} header files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files (headers) of %{name}.

%package -n shadowsocks-%{name}
Summary: A CLI Shadowsocks client
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n shadowsocks-%{name}
A shadowsocks CLI client using %{name}.

%prep
%setup -q -n %repo-%{_commit}

%build
%ifarch x86_64
%{qmake_qt5} DEFINES+="LIB64"
%else
%{qmake_qt5}
%endif
make %{?_smp_mflags}

%install
%make_install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/QtShadowsocks.pc
%{_includedir}/qtshadowsocks/*

%files -n shadowsocks-%{name}
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/shadowsocks-*

%changelog
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 1.8.4-1.gitd2c76c5
- Update to 1.8.4-1.gitd2c76c5
* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 1.8.2-1.git3c3aa83
- Update to 1.8.2-1.git3c3aa83
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 1.6.1-1.git7b71ee0
- Update to 1.6.1-1.git7b71ee0
* Tue Jun 02 2015 mosquito <sensor.wen@gmail.com> - 1.6.1-1.git96fc948
- Initial build
