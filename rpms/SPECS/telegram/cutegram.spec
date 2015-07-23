%global debug_package %{nil}
%global project Cutegram
%global repo %{project}

# commit
%global _commit 2083574ee436c9726186d13e9c1eba11e502d52b
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: cutegram
Version: 2.5.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: Cutegram telegram client
Summary(zh_CN): Cutegram telegram 客户端

License: GPLv3
Group: Applications/Internet
Url: http://aseman.co/cutegram
Source0: https://github.com/Aseman-Land/Cutegram/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: libqtelegram-ae-devel
BuildRequires: libtelegramqml-devel
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5WebKitWidgets)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5WebKit)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Sql)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: pkgconfig(Qt5DBus)

Requires: qt5-qtquickcontrols
Requires: qt5-qtgraphicaleffects
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
%if 0%{?fedora} > 21
Requires(post): gtk-update-icon-cache
Requires(postun): gtk-update-icon-cache
%endif

%description
Cutegram is created to make a better client for Telegram on GNU/Linux
desktops. It has smart and beautiful user interface that supports drag
and drop to send files and delete or forward messages.

%description -l zh_CN
Cutegram 是一款 Telegram 第三方客户端. 它拥有智能美观的用户界面, 支持
发送文件, 查看删除消息.

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir build && pushd build
%{_qt5_qmake} PREFIX=%{_prefix} \
    LIBQTELEGRAM_LIB_DIR=%{_libdir} \
    LIBQTELEGRAM_INCLUDE_PATH=%{_includedir}/libqtelegram-ae \
    TELEGRAMQML_LIB_DIR=%{_libdir} \
    TELEGRAMQML_INCLUDE_PATH=%{_includedir}/libtelegramqml ..
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot} -C build

%post
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
ldconfig

%postun
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/icons/*
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop
%exclude %{_datadir}/%{name}/icons

%changelog
* Thu Jul 23 2015 mosquito <sensor.wen@gmail.com> - 2.5.0-1.git2083574
- Initial build
