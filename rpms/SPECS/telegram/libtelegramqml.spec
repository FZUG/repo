%global debug_package %{nil}
%global project TelegramQML
%global repo %{project}

# commit
%global _commit f48b220c59fac6ff08d26906bafc8027a8f9a47d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: libtelegramqml
Version: 0.8.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: Telegram API tools for QtQML and Qml
Summary(zh_CN): Telegram Qml API 工具

License: GPLv3
Group: Development/Libraries
Url: https://github.com/Aseman-Land/TelegramQML
Source0: https://github.com/Aseman-Land/TelegramQML/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: libqtelegram-ae-devel
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Sql)
BuildRequires: pkgconfig(Qt5Xml)

%description
Telegram API tools for QtQML and Qml, based on Cutegram-Core and libqtelegram.
It's free and released under the GPLv3 license.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q -n %repo-%{_commit}

%build
sed -i -e '/$$LIB_PATH/iisEmpty(LIBDIR){' \
       -e '/$$LIB_PATH/a}else{target.path=$$LIBDIR}' \
       -e '/INSTALL_PREFIX/s|tele|libtele|' telegramqml.pro

mkdir build && pushd build
# library mode(BUILD_MODE+=lib)，plugin mode
%{_qt5_qmake} PREFIX=%{_prefix} LIBDIR=%{_libdir} BUILD_MODE+=lib ..
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot} -C build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_libdir}/%{name}.so.*

%files devel
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_includedir}/%{name}
%{_libdir}/%{name}.so

%changelog
* Thu Jul 23 2015 mosquito <sensor.wen@gmail.com> - 0.8.0-1.gitf48b220
- Initial build
