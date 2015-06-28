%global debug_package %{nil}
%global project libQtShadowsocks
%global repo %{project}

# commit
%global _commit 96fc948cd05e7fee20a1f977f021898ec2f89ba2
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		libQtShadowsocks
Version:	1.6.1
Release:	1.git%{_shortcommit}%{?dist}
Summary:	A lightweight and ultra-fast shadowsocks library

License:	LGPLv3+
URL:		https://github.com/librehat/libQtShadowsocks
Source0:	https://github.com/librehat/libQtShadowsocks/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qttools
BuildRequires: botan-devel
Requires: qt5-qtbase
Requires: botan
#AutoReq: no

%description
A lightweight and ultra-fast shadowsocks library written in C++/Qt.

%package devel
Summary:	libQtShadowsocks header files
Requires:	libQtShadowsocks

%description devel
Development files (headers) of libQtShadowsocks.

%package -n shadowsocks-libQtShadowsocks
Summary:	A CLI Shadowsocks client
Requires:	libQtShadowsocks

%description -n shadowsocks-libQtShadowsocks
A shadowsocks CLI client using libQtShadowsocks.

%prep
%setup -q -n %repo-%{_commit}

%build
%ifarch x86_64
%{_qt5_qmake} DEFINES+="LIB64"
%else
%{_qt5_qmake}
%endif

make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/QtShadowsocks.pc
%{_includedir}/qtshadowsocks/*

%files -n shadowsocks-%{name}
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/shadowsocks-*

%changelog
* Tue Jun 02 2015 mosquito <sensor.wen@gmail.com> - 1.6.1-1.git96fc948
- Initial build
