%global debug_package %{nil}

Name:    isatapd
Version: 0.9.7
Release: 1%{?dist}
Summary: ISATAP client for Linux
Group:   System Environment/Daemons
License: GPLv2
URL:     http://www.saschahlusiak.de/linux/isatap.htm
Source0: http://www.saschahlusiak.de/linux/%{name}-%{version}.tar.gz

%description
isatapd creates and maintains an ISATAP tunnel (rfc5214) in Linux.

It uses the in-kernel ISATAP support first introduced in linux-2.6.25.
It does NOT operate the tunnel or handle any IPv6 traffic other than
router solicitations and router advertisements.

%prep
%setup -q

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%doc README ChangeLog
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.*

%changelog
* Thu Jun 16 2016 Zhenbo Li <litimetal@gmail.com> - 0.9.7-1
- Initial build
