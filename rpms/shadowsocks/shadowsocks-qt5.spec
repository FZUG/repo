%global debug_package %{nil}
%global project shadowsocks-qt5
%global repo %{project}

# commit
%global _commit 92a51a4712b9a70a35d765b486f3a218856c82f6
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    shadowsocks-qt5
Version: 2.8.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: A cross-platform shadowsocks GUI client
Summary(zh_CN): 跨平台 shadowsocks GUI 客户端

Group:   Applications/Internet
License: LGPLv3+
URL:     https://github.com/librehat/shadowsocks-qt5
Source0: %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

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
%setup -q -n %{repo}-%{_commit}

%build
%{qmake_qt5} INSTALL_PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:
/sbin/ldconfig

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:
/sbin/ldconfig

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/ss-qt5
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.8.0-1.git92a51a4
- Update to 2.8.0-1.git92a51a4
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 2.7.0-1.git4540be9
- Update to 2.7.0-1.git4540be9
* Mon Apr 18 2016 mosquito <sensor.wen@gmail.com> - 2.6.1-2.gitba70fd1
- Rebuild for Qt 5.6.0
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 2.6.1-1.gitba70fd1
- Update to 2.6.1-1.gitba70fd1
* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 2.6.0-1.git7ec8a63
- Update to 2.6.0-1.git7ec8a63
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 2.4.1-1.git6cd4372
- Update to 2.4.1-1.git6cd4372
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 2.4.0-1.git7ef006f
- Initial build
