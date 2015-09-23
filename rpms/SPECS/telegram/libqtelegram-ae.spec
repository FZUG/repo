%global debug_package %{nil}
%global project libqtelegram-aseman-edition
%global repo %{project}

# commit
%global _commit d54aebed628b5864f5e84b36918c2dc651d5fba2
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: libqtelegram-ae
Version: 0.5.0
Release: 2.git%{_shortcommit}%{?dist}
Summary: Telegram protocol access library
Summary(zh_CN): Telegram 协议库

License: GPLv3
Group: Development/Libraries
Url: https://github.com/Aseman-Land/libqtelegram-aseman-edition
Source0: https://github.com/Aseman-Land/libqtelegram-aseman-edition/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: pkgconfig(openssl)
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

%description devel
This is a fork of libqtelegram by Aseman team.

This is a Qt asynchronous library to be used as Telegram client.
Using signal-slot mechanism to communicate to telegram servers,
exposes an easy to use API for applications to interact to.

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir dist && pushd dist
%{_qt5_qmake} PREFIX=%{_prefix} LIBDIR=%{_libdir} ..
make %{?_smp_mflags}

%install
%make_install INSTALL_ROOT=%{buildroot} -C dist

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%{_qt5_headerdir}/%{name}
%{_libdir}/%{name}.so

%changelog
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 0.5.0-2.gitd54aebe
- Update to 0.5.0-2.gitd54aebe
* Thu Jul 23 2015 mosquito <sensor.wen@gmail.com> - 0.5.0-1.gitef383c9
- Initial build
