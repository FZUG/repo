%global project dde-api
%global repo %{project}
%global import_path pkg.deepin.io/dde/api

Name:           deepin-api
Version:        3.1.11
Release:        2%{?dist}
Summary:        Go-lang bingding for dde-daemon
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-api
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  bzr
BuildRequires:  git
BuildRequires:  gcc-go
BuildRequires:  gtk3-devel
BuildRequires:  gdk-pixbuf2-xlib-devel
BuildRequires:  cairo-devel
BuildRequires:  libXi-devel
BuildRequires:  libcroco-devel
BuildRequires:  libcanberra-devel
BuildRequires:  librsvg2-devel
BuildRequires:  libgudev-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  polkit-qt5-1-devel
BuildRequires:  deepin-gir-generator
BuildRequires:  deepin-go-dbus-factory
BuildRequires:  golang-deepin-go-lib-devel
BuildRequires:  golang-github-BurntSushi-xgb-devel
BuildRequires:  golang-github-BurntSushi-xgbutil-devel
BuildRequires:  golang-github-alecthomas-kingpin-devel
BuildRequires:  golang-github-disintegration-imaging-devel
BuildRequires:  systemd
%{?systemd_requires}
Requires:       deepin-desktop-base
Requires:       rfkill
Provides:       %{repo}%{?_isa} = %{version}-%{release}
Obsoletes:      %{repo}%{?_isa} < %{version}-%{release}

%description
Go-lang bingding for dde-daemon

%package -n golang-%{name}-devel
Summary:        %{summary}
BuildArch:      noarch
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}
Obsoletes:      %{name}-devel < %{version}-%{release}

%description -n golang-%{name}-devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%setup -q -n %{repo}-%{version}

sed -i 's|/usr/lib|%{_libexecdir}|' misc/*services/*.service \
    misc/systemd/system/deepin-shutdown-sound.service \
    lunar-calendar/main.go \
    thumbnails/gtk/gtk.go

sed -i 's|libdir|LIBDIR|g' Makefile

%build
export GOPATH="$(pwd)/build:%{gopath}"
#make build-dep
make

%install
export GOPATH="$(pwd)/build:%{gopath}"
%make_install SYSTEMD_LIB_DIR="/usr/lib" LIBDIR="/libexec"

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
%systemd_post deepin-shutdown-sound.service

%preun
%systemd_preun deepin-shutdown-sound.service

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
%systemd_postun_with_restart deepin-shutdown-sound.service

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

%files
%doc README.md
%license LICENSE
%{_libexecdir}/%{name}/
%{_unitdir}/*.service
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/icons/hicolor/*/actions/*
%{_polkit_qt_policydir}/com.deepin.api.locale-helper.policy

%files -n golang-%{name}-devel
%{gopath}/src/%{import_path}/

%changelog
* Tue Aug  8 2017 mosquito <sensor.wen@gmail.com> - 3.1.11-2
- Rename deepin-api-devel to golang-deepin-api-devel

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 3.1.11-1
- Update to 3.1.11

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.10-1.git79125e7
- Update to 3.1.10

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.1.7-1.git4c8e030
- Update to 3.1.7

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.2-1.gitf93dbd7
- Update to 3.1.2

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.16.1-1.gitcfdb295
- Update to 3.0.16.1

* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.16-1
- Update to version 3.0.16

* Sun Dec 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.15-1
- Update to version 3.0.15

* Wed Dec 07 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.14-2
- Changed compilation procedure

* Wed Sep 28 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.14-1
- Initial package build
