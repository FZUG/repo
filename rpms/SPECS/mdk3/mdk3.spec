%global debug_package %{nil}

Name:       mdk3
Version:    6
Release:    1%{?dist}
Summary:    An 802.11 wireless network security testing tool

Group:      Applications/System
License:    GPLv2
URL:        http://aspj.aircrack-ng.org
Source0:    http://aspj.aircrack-ng.org/%{name}-v%{version}.tar.bz2

%description
 An 802.11 wireless network security testing tool.

%description -l zh_CN
 802.11 无线网络安全测试工具.

%prep
%setup -q -n %{name}-v%{version}

%build
make

%install
make install PREFIX=%{_prefix} DESTDIR=%{buildroot}

%files
%doc AUTHORS COPYING CHANGELOG docs/*
%{_sbindir}/%{name}

%changelog
* Fri Jul  3 2015 mosquito <sensor.wen@gmail.com> - 6-1
- Rebuild for fedora 22
* Fri Feb 13 2015 Felix Kaiser <felix.kaiser@fxkr.net> - 6-1
- Initial package
