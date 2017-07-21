%global commit 8b3ae9dcb9737e8d43c82ddeac126f6c964defca
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-system-monitor
Version:        0.0.9
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
BuildRequires:  qt5-linguist
BuildRequires:  libpcap-devel
BuildRequires:  libcap-devel
BuildRequires:  ncurses-devel

%description
%{summary}

%prep
%setup -q -n %{name}-%{commit}
sed -i 's|=lupdate|=lupdate-qt5|;s|=lrelease|=lrelease-qt5|' %{name}.pro

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%doc README.md
%license LICENSE
%caps(cap_kill,cap_net_raw,cap_dac_read_search,cap_sys_ptrace=+ep) %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/%{name}/translations/*.qm

%changelog
* Sat Jul 15 2017 mosquito <sensor.wen@gmail.com> - 0.0.4-1.gita73357d
- Initial build
