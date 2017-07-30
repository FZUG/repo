%global debug_package %{nil}

Name:           startdde
Version:        3.1.13
Release:        1%{?dist}
Summary:        Starter of deepin desktop environment
License:        GPLv3
URL:            https://github.com/linuxdeepin/startdde
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  golang
BuildRequires:  libgo-devel
BuildRequires:  coffee-script
BuildRequires:  deepin-gir-generator
BuildRequires:  deepin-go-dbus-factory
BuildRequires:  deepin-go-lib
BuildRequires:  deepin-api-devel
BuildRequires:  webkitgtk-devel
BuildRequires:  libcanberra-devel
BuildRequires:  golang-github-BurntSushi-xgb-devel
BuildRequires:  golang-github-BurntSushi-xgbutil-devel
BuildRequires:  golang-github-howeyc-fsnotify-devel
Requires:       deepin-daemon
Requires:       deepin-wm-switcher

%description
Starter of deepin desktop environment

%prep
%setup -q

sed -i '/polkit-1/s|lib|libexec|' watchdog/dde_polkit_agent.go
sed -i '/deepin-daemon/s|lib|libexec|g' Makefile session.go \
    dde-readahead/dde-readahead.service

# Fix systemd path
sed -i 's|/lib/systemd|/usr/lib/systemd|g' Makefile

%build
export GOPATH="%{gopath}"
%make_build

%install
%make_install

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libexecdir}/deepin-daemon/dde-readahead
%{_unitdir}/dde-readahead.service
%{_unitdir}/multi-user.target.wants/dde-readahead.service
%{_datadir}/xsessions/deepin.desktop

%changelog
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
