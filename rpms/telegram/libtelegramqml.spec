%global __strip_shared %(test $(rpm -E%?fedora) -ge 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}
%global project TelegramQML
%global repo %{project}
%global with_library 0

# commit
%global _commit 351f3e4fc258701382261e6c1fc22afcbc60e218
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    libtelegramqml
Version: 2.0.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: Telegram API tools for QtQML and Qml
Summary(zh_CN): Telegram Qml API 工具

License: GPLv3
Group:   Development/Libraries
Url:     https://github.com/Aseman-Land/TelegramQML
Source0: %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: libqtelegram-ae-devel >= 6.0
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Sql)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: pkgconfig(Qt5Declarative)
BuildRequires: qt5-qtgraphicaleffects
BuildRequires: qt5-qtquickcontrols

%description
Telegram API tools for QtQML and Qml, based on Cutegram-Core and libqtelegram.
It's free and released under the GPLv3 license.

%if 0%{?with_library}
%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.
%endif

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir build && pushd build
# library mode(BUILD_MODE+=lib)，plugin mode
%{qmake_qt5} -r PREFIX=%{_prefix} \
    INSTALL_LIBS_PREFIX=%{_libdir} \
    INSTALL_HEADERS_PREFIX=%{_includedir} \
    OPENSSL_LIB_DIR=%{_libdir}/openssl \
    OPENSSL_INCLUDE_PATH=%{_includedir}/openssl \
    LIBQTELEGRAM_LIB_DIR=%{_libdir} \
    LIBQTELEGRAM_INCLUDE_PATH=%{_includedir}/libqtelegram-ae \
%if 0%{?with_library}
    BUILD_MODE+=lib \
%endif
    ..
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot} -C build

# strip shared files
%{__strip_shared}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%if 0%{?with_library}
%{_libdir}/%{name}.so.*
%else
%{_qt5_prefix}/qml/TelegramQml/%{name}.so
%{_qt5_prefix}/qml/TelegramQml/plugins.qmltypes
%{_qt5_prefix}/qml/TelegramQml/qmldir
%endif

%if 0%{?with_library}
%files devel
%defattr(-,root,root,-)
%{_includedir}/telegramqml
%{_libdir}/%{name}.so
%endif

%changelog
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 2.0.0-1.git351f3e4
- Update to 2.0.0-1.git351f3e4
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 0.9.2-1.gitf7e7ef4
- Update to 0.9.2-1.gitf7e7ef4
* Wed Dec  9 2015 mosquito <sensor.wen@gmail.com> - 0.9.1-1.git8c5bafc
- Update to 0.9.1-1.git8c5bafc
- Strip shared files
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 0.8.0-2.gitbc568f3
- Update to 0.8.0-2.gitbc568f3
* Thu Jul 23 2015 mosquito <sensor.wen@gmail.com> - 0.8.0-1.gitf48b220
- Initial build
