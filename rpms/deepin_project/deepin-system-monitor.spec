%global commit a73357d04bf3d5cafd91867b61732b94cadbd577
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-system-monitor
Version:        0.0.4
Release:        1.git%{shortcommit}%{?dist}
Summary:        A more user-friendly system monitor
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-system-monitor
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  pkgconfig(dtkbase)
BuildRequires:  pkgconfig(dtkutil)
BuildRequires:  pkgconfig(dtkwidget)
BuildRequires:  pkgconfig(libprocps)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Network)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  libpcap-devel
BuildRequires:  libcap-devel
BuildRequires:  ncurses-devel

%description
%{summary}

%prep
%setup -q -n %{name}-%{commit}

%build
%qmake_qt5
%make_build

%install
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}

%files
%doc README.md
%caps(cap_kill,cap_net_raw,cap_dac_read_search,cap_sys_ptrace=+ep) %{_bindir}/%{name}

%changelog
* Sat Jul 15 2017 mosquito <sensor.wen@gmail.com> - 0.0.4-1.gita73357d
- Initial build
