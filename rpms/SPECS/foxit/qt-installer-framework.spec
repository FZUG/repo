%global __strip_shared %(test $(rpm -E%?fedora) -eq 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}

Name:    qt-installer-framework
Version: 2.0.1
Release: 1%{?dist}
Summary: The Qt Installer Framework used for the Qt SDK installer
Summary(zh_CN): Qt 安装框架, 用于创建 Qt 安装包

Group:   Applications/System
License: LGPLv2+
URL:     http://wiki.qt.io/Qt-Installer-Framework
Source0: http://download.qt.io/official_releases/%{name}/%{version}/%{name}-opensource-%{version}-src.tar.gz

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qttools-static
BuildRequires: qt5-qtdeclarative-devel

%description
The Qt Installer Framework provides a set of tools and utilities to
create installers for the supported desktop Qt platforms: Linux,
Microsoft Windows, and Mac OS X.

The Qt Installer Framework is used e.g. for the Qt SDK installers,
and Qt Creator installer.

%prep
%setup -q -n %{name}-opensource-%{version}-src

%build
mkdir build; pushd build
%{qmake_qt5} ..
make %{?_smp_mflags}
# build requires: qt5-qtdoc, qt5-qtbase-doc, qt5-qtdeclarative-doc
#make docs INSTALL_ROOT=.

%install
pushd build
install -d %{buildroot}{%{_bindir},%{_libdir}}
cp -a bin/* %{buildroot}%{_bindir}
cp -a lib/*.so* %{buildroot}%{_libdir}

# stripe shared files
%{__strip_shared}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc 3RDPARTY Changelog README
%license LGPL_EXCEPTION.txt LICENSE.FDL LICENSE.LGPL*
%{_bindir}/*
%{_libdir}/libinstaller.so*

%changelog
* Wed Dec 23 2015 mosquito <sensor.wen@gmail.com> - 2.0.1-1
- Initial build
