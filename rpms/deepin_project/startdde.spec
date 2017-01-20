%global _commit d3ba123465f529eb93d662e06d34b01bbc9640ca
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           startdde
Version:        3.0.14.1
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Starter of deepin desktop environment
License:        GPLv3
URL:            https://github.com/linuxdeepin/startdde
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-go
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
%setup -q -n %{name}-%{_commit}

sed -i 's|/usr/lib|%{_libexecdir}|g' Makefile session.go \
    dde-readahead/dde-readahead.service

# Fix systemd path
sed -i 's|/lib/systemd|/usr/lib/systemd|g' Makefile

%build
export GOPATH="%{gopath}"
%make_build

%install
%make_install

# Fix broken symlink
rm -f %{buildroot}%{_unitdir}/multi-user.target.wants/dde-readahead.service
ln -s %{_unitdir}/dde-readahead.service \
  %{buildroot}%{_unitdir}/multi-user.target.wants/dde-readahead.service

%files
%{_bindir}/%{name}
%{_libexecdir}/deepin-daemon/dde-readahead
%{_unitdir}/dde-readahead.service
%{_unitdir}/multi-user.target.wants/dde-readahead.service
%{_datadir}/xsessions/deepin.desktop

%changelog
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
