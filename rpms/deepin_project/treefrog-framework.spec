Name:           treefrog-framework
Version:        1.18.0
Release:        2%{?dist}
Summary:        High-speed C++ MVC Framework for Web Application
License:        BSD
URL:            https://github.com/treefrogframework/treefrog-framework
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  libbson-devel
BuildRequires:  mongo-c-driver-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  sqlite

%description
High-speed C++ MVC Framework for Web Application.

%package devel
Summary:        Header and development files
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
Header files and libraries for building and developing apps with treefrog.

%prep
%setup -q

# use system libraries
rm -rf 3rdparty/
sed -i '/mongoc.a/s|=.*|= -lmongoc-1.0\nINCLUDEPATH += %{_includedir}/libbson-1.0 %{_includedir}/libmongoc-1.0|' src/corelib.pro

# remove rpaths in executables
sed -i -E 's|\S+-rpath\S+||' tools/*/*.pro
sed -i '/unix:LIBS/s|=.*$|= -L%{_libdir} -ltreefrog|;
  /unix:INCLUDEPATH/s|=.*$|= %{_includedir}/treefrog|' defaults/appbase.pri
sed -i 's|qmake|%{_qt5_qmake}|' src/test/testall.sh

# define google namespace for ppc64le
sed -i '/stacktrace.h/a#include "gconfig.h"' tools/tfserver/stacktrace_powerpc-inl.h

%build
pushd src
%qmake_qt5 target.path=%{_libdir} header.path=%{_includedir}/treefrog use_gui=1
%make_build
popd
pushd tools
%qmake_qt5 header.path="$PWD/../include $PWD/../src" lib.path="$PWD/../src"
%make_build
popd

%install
%make_install INSTALL_ROOT=%{buildroot} -C src
%make_install INSTALL_ROOT=%{buildroot} -C tools

%check
QT_VER=%{_qt5_version}
if [ "${QT_VER//./}" -gt "571" ]; then
src/test/testall.sh
# releasetest failed to run:
# https://github.com/treefrogframework/treefrog-framework/issues/157
#PATH=%%{buildroot}%%{_bindir}:$PATH \
#LD_LIBRARY_PATH=%%{buildroot}%%{_libdir}:${LD_LIBRARY_PATH} \
#bash -x tools/test/releasetest/releasetest
fi

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc README.* CHANGELOG.md
%license copyright
%{_bindir}/*
%{_libdir}/*.so.*
%{_datadir}/treefrog/

%files devel
%{_libdir}/*.so
%{_includedir}/*

%changelog
* Fri Aug  4 2017 mosquito <sensor.wen@gmail.com> - 1.18.0-2
- Add testsuit

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 1.18.0-1
- Initial package build
