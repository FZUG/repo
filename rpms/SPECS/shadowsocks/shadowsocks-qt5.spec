%global debug_package %{nil}
%global project shadowsocks-qt5
%global repo %{project}

# commit
%global _commit 7ef006f307ab37ef67daba1dd020abd4be8d0a0d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: shadowsocks-qt5
Version: 2.4.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: A cross-platform shadowsocks GUI client
Summary(zh_CN): 跨平台 shadowsocks GUI 客户端

Group: Applications/Internet
License: LGPLv3+
URL: https://github.com/librehat/shadowsocks-qt5
Source0: https://github.com/librehat/shadowsocks-qt5/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: pkgconfig
BuildRequires: qt5-qtbase-devel >= 5.2.0
BuildRequires: qt5-qttools
BuildRequires: qrencode-devel
BuildRequires: botan-devel >= 1.10
BuildRequires: libQtShadowsocks-devel >= 1.6.0
BuildRequires: zbar-devel
BuildRequires: libappindicator-devel

%description
Shadowsocks-Qt5 is a native and cross-platform shadowsocks GUI client
with advanced features.

%description -l zh_CN
Shadowsocks-Qt5 是一个本地跨平台 shadowsocks GUI 客户端.

%prep
%setup -q -n %repo-%{_commit}

%build
%{_qt5_qmake} INSTALL_PREFIX=%{_prefix}
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

%post
update-desktop-database -q || true
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor || true
ldconfig

%postun
update-desktop-database -q || true
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor || true
ldconfig

%files
%defattr(-,root,root,-)
%doc README.md LICENSE
%{_bindir}/ss-qt5
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*

%changelog
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 0.13-1
- Initial build
