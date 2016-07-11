%global __strip_shared %(test $(rpm -E%?fedora) -ge 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}
%global project Cutegram
%global repo %{project}
%global with_binary 0

# commit
%global _commit d6329cb7bb2d45d06af5c7ac30a433844fa7a49d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    cutegram
Version: 2.9.5
Release: 1.git%{_shortcommit}%{?dist}
Summary: Cutegram telegram client
Summary(zh_CN): Cutegram telegram 客户端

License: GPLv3
Group:   Applications/Internet
Url:     https://github.com/Aseman-Land/Cutegram
Source0: %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: libqtelegram-ae-devel >= 6.0
#BuildRequires: libtelegramqml-devel >= 0.9.0
BuildRequires: pkgconfig(openssl)
BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Gui)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5Network)
BuildRequires: pkgconfig(Qt5Qml)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: pkgconfig(Qt5Sql)
BuildRequires: pkgconfig(Qt5WebKit)
BuildRequires: pkgconfig(Qt5WebKitWidgets)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: pkgconfig(Qt5Xml)
BuildRequires: desktop-file-utils
BuildRequires: git

Requires: aseman-qt-tools
Requires: libtelegramqml
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
%{qmake_qt5} PREFIX=%{_prefix} \
%if 0%{?with_binary}
    CONFIG+=binaryMode \
%endif
    OPENSSL_LIB_DIR=%{_libdir}/openssl \
    OPENSSL_INCLUDE_PATH=%{_includedir}/openssl \
    LIBQTELEGRAM_LIB_DIR=%{_libdir} \
    LIBQTELEGRAM_INCLUDE_PATH=%{_includedir}/libqtelegram-ae \
    TELEGRAMQML_LIB_DIR=%{_libdir} \
    TELEGRAMQML_INCLUDE_PATH=%{_includedir}/telegramqml ..
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot} -C build
desktop-file-validate %{buildroot}%{_datadir}/applications/Cutegram.desktop

%if 0%{?with_binary}
install -Dm755 build/%{name} %{buildroot}%{_bindir}/%{name}
%else
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} << EOF
qmlscene %{_datadir}/%{name}/3.0/main.qml
EOF
%endif

# stripe shared files
%{__strip_shared}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%attr(755,-,-) %{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{repo}.desktop

%changelog
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 2.9.5-1.gitabc33b6
- Update to 2.9.5-1.gitabc33b6
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 2.7.1-1.git1dbe279
- Update to 2.7.1-1.git1dbe279
* Wed Dec  9 2015 mosquito <sensor.wen@gmail.com> - 2.7.0-1.gitbd3bd34
- Update to 2.7.0-1.gitbd3bd34
- Strip shared files
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 2.5.0-2.git79fc6b0
- Fix include path
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 2.5.0-1.git79fc6b0
- Update to 2.5.0-1.git79fc6b0
* Thu Jul 23 2015 mosquito <sensor.wen@gmail.com> - 2.5.0-1.git2083574
- Initial build
