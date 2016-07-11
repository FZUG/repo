%global __strip_shared %(test $(rpm -E%?fedora) -eq 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}
%global project libqtelegram-aseman-edition
%global repo %{project}

# commit
%global _commit e4c49667feaecedaff74af672419445bc022daa1
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    libqtelegram-ae
Version: 10.0.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: Telegram protocol access library
Summary(zh_CN): Telegram 协议库

License: GPLv3
Group:   Development/Libraries
Url:     https://github.com/Aseman-Land/libqtelegram-aseman-edition
Source0: %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Multimedia)

%description
This is a fork of libqtelegram by Aseman team.

This is a Qt asynchronous library to be used as Telegram client.
Using signal-slot mechanism to communicate to telegram servers,
exposes an easy to use API for applications to interact to.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt5-qtbase-devel >= 5.4.0

%description devel
This is a fork of libqtelegram by Aseman team.

This is a Qt asynchronous library to be used as Telegram client.
Using signal-slot mechanism to communicate to telegram servers,
exposes an easy to use API for applications to interact to.

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir dist && pushd dist
%{qmake_qt5} -r PREFIX=%{_prefix} \
    CONFIG+=typeobjects \
    OPENSSL_LIB_DIR=%{_libdir}/openssl \
    OPENSSL_INCLUDE_PATH=%{_includedir}/openssl \
    INSTALL_LIBS_PREFIX=%{_libdir} \
    INSTALL_HEADERS_PREFIX=%{_includedir} ..
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot} -C dist

# strip shared files
%{__strip_shared}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}
%{_libdir}/%{name}.so

%changelog
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 10.0.0-1.gite4c4966
- Update to 10.0.0-1.gite4c4966
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 6.1-1.git4ad3aae
- Update to 6.1-1.git4ad3aae
* Wed Dec  9 2015 mosquito <sensor.wen@gmail.com> - 6.0-1.git569d31b
- Update to 6.0-1.git569d31b
- Strip shared files
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 0.5.0-2.gitd54aebe
- Update to 0.5.0-2.gitd54aebe
* Thu Jul 23 2015 mosquito <sensor.wen@gmail.com> - 0.5.0-1.gitef383c9
- Initial build
