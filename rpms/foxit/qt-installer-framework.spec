%global tgzname %{name}-opensource-src-%{version}

Name:    qt-installer-framework
Version: 3.0.6
Release: 1%{?dist}
Summary: The Qt Installer Framework used for the Qt SDK installer
License: GPLv3
URL:     http://wiki.qt.io/Qt-Installer-Framework
Source0: http://download.qt.io/official_releases/%{name}/%{version}/%{tgzname}.tar.gz

BuildRequires: pkgconfig(Qt5Core)
BuildRequires: pkgconfig(Qt5UiTools)
BuildRequires: pkgconfig(Qt5Quick)
BuildRequires: qt5-qtdoc
BuildRequires: qt5-doctools
BuildRequires: qt5-qtbase-doc
BuildRequires: qt5-qtdeclarative-doc

%description
The Qt Installer Framework provides a set of tools and utilities to
create installers for the supported desktop Qt platforms: Linux,
Microsoft Windows, and Mac OS X.

The Qt Installer Framework is used e.g. for the Qt SDK installers,
and Qt Creator installer.

%package doc
Summary: Documentation for %{name}

%description doc
Documentation for %{name}.

%prep
%setup -q -c %{name}

%build
%qmake_qt5
%make_build
make docs

%install
%make_install INSTALL_ROOT=%{buildroot}

install -Dm644 doc/ifw.qch %{buildroot}%{_qt5_docdir}/ifw.qch
cp -r doc/html %{buildroot}%{_qt5_docdir}/ifw

%files
%license LICENSE.FDL LICENSE.GPL3*
%doc Changelog README
%{_qt5_bindir}/archivegen
%{_qt5_bindir}/binarycreator
%{_qt5_bindir}/devtool
%{_qt5_bindir}/installerbase
%{_qt5_bindir}/repogen
%{_libdir}/lib7z.a
%{_libdir}/libinstaller.a

%files doc
%{_qt5_docdir}/ifw/
%{_qt5_docdir}/ifw.qch

%changelog
* Thu Dec 20 2018 mosquito <sensor.wen@gmail.com> - 3.0.6-1
- Release 3.0.6

* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 2.0.3-1
- Release 2.0.3

* Wed Dec 23 2015 mosquito <sensor.wen@gmail.com> - 2.0.1-1
- Initial build