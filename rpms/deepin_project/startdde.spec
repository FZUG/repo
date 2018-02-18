Name:           startdde
Version:        3.1.24
Release:        1%{?dist}
Summary:        Starter of deepin desktop environment
License:        GPLv3
URL:            https://github.com/linuxdeepin/startdde
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
BuildRequires:  golang
BuildRequires:  deepin-gir-generator
BuildRequires:  golang-deepin-dbus-factory-devel
BuildRequires:  golang(pkg.deepin.io/dde/api/dxinput)
BuildRequires:  golang(pkg.deepin.io/lib)
BuildRequires:  golang(github.com/cryptix/wav)
BuildRequires:  golang(github.com/BurntSushi/xgb)
BuildRequires:  golang(github.com/BurntSushi/xgbutil)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(systemd)
%{?systemd_requires}
Requires:       deepin-daemon
Requires:       deepin-wm-switcher
Requires:       deepin-wm
Requires:       deepin-metacity

%description
Startdde is used for launching DDE components and invoking user's
custom applications which compliant with xdg autostart specification.

%prep
%setup -q

sed -i '/polkit-1/s|lib|libexec|' watchdog/dde_polkit_agent.go
sed -i '/deepin-daemon/s|lib|libexec|g' Makefile session.go

# Fix systemd path
sed -i 's|/lib/systemd|/usr/lib/systemd|g' Makefile

%build
export GOPATH="%{gopath}"
BUILD_ID="0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
%make_build GOBUILD="go build -compiler gc -ldflags \"${LDFLAGS} -B $BUILD_ID\" -a -v -x"

%install
%make_install

%post
%systemd_post dde-readahead.service

%preun
%systemd_preun dde-readahead.service

%postun
%systemd_postun_with_restart dde-readahead.service

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/xsessions/deepin.desktop

%changelog
* Fri Feb 16 2018 mosquito <sensor.wen@gmail.com> - 3.1.24-1
- Update to 3.1.24

* Thu Dec 21 2017 mosquito <sensor.wen@gmail.com> - 3.1.23-1
- Update to 3.1.23

* Sat Dec  2 2017 mosquito <sensor.wen@gmail.com> - 3.1.22-1
- Update to 3.1.22

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 3.1.17-1
- Update to 3.1.17

* Fri Oct 13 2017 mosquito <sensor.wen@gmail.com> - 3.1.16-1
- Update to 3.1.16

* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.15-1
- Update to 3.1.15

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 3.1.14-1
- Update to 3.1.14

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.13-1.git08de5b9
- Update to 3.1.13

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.1.8-1.gita9130d0
- Update to 3.1.8

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.2-1.gitd7c1216
- Update to 3.1.2

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.14.1-1.gitd3ba123
- Update to 3.0.14.1

* Wed Dec 28 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.13-2
- Updated GO dependencies
- Fixed wrong system path for dde-readahead

* Sun Dec 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.13-1
- Update to package 3.0.13

* Sat Oct 01 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.12-1
- Update to package 3.0.12

* Sat Oct 01 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.11-1
- Initial package build
