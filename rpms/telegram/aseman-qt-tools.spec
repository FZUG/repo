%global debug_package %{nil}
%global project aseman-qt-tools
%global repo %{project}

# commit
%global _commit 439f68d35da04fa7e1aa8b73b7cdf10d48b34c69
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    aseman-qt-tools
Version: 1.0.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: the shared tools and functions in the aseman's projects
Summary(zh_CN): aseman 项目共享工具

License: GPLv3
Group:   Development/Libraries
Url:     https://github.com/Aseman-Land/aseman-qt-tools
Source0: %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: pkgconfig(Qt5DBus)
BuildRequires: pkgconfig(Qt5Multimedia)
BuildRequires: pkgconfig(Qt5Positioning)
BuildRequires: pkgconfig(Qt5Sensors)
BuildRequires: pkgconfig(Qt5Widgets)
BuildRequires: qtkeychain-qt5-devel

%description
AsemanQtTools, is the shared tools and functions, we used
in the aseman's projects.

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir build && cd build
# Disable the wallet and keychains support, DEFINES+=DISABLE_KEYCHAIN
%{qmake_qt5} \
    QT+=dbus \
    QT+=multimedia \
    QT+=positioning \
    QT+=sensors \
    QT+=widgets \
    ..
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot} -C build

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_qt5_prefix}/qml/AsemanTools/

%changelog
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 1.0.0-1.git5afa8ec
- Initial build
