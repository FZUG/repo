%global project ~system-settings-touch
%global _revision 82

# for fedora 24
%global _qt5_qmldir %{_qt5_archdatadir}/qml

Name:           gsettings-qt
Version:        0.1.20160329
Release:        1%{?dist}
Summary:        Qml bindings for GSettings
License:        GPL
URL:            https://launchpad.net/gsettings-qt
Source0:        http://bazaar.launchpad.net/%{project}/%{name}/trunk/tarball/%{_revision}

BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtdeclarative-devel
BuildRequires:  glib2-devel

%description
Qml bindings for GSettings.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q -n %{project}/%{name}/trunk

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

# remove test
rm -rf %{buildroot}%{_libdir}/qt5/tests

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/lib%{name}.so.*

%files devel
%{_qt5_headerdir}/QGSettings/*
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/lib%{name}.so
%dir %{_qt5_qmldir}/GSettings.1.0/
%{_qt5_qmldir}/GSettings.1.0/libGSettingsQmlPlugin.so
%{_qt5_qmldir}/GSettings.1.0/plugins.qmltypes
%{_qt5_qmldir}/GSettings.1.0/qmldir

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.1.20160329-1-1
- Update to 0.1.20160329

* Tue Jan 03 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 0.1.20160329-2
- Major rewrite of SPEC file

* Sun Oct 02 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.1.20160329-1
- Initial package build
