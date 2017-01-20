%global project dde-daemon
%global repo %{project}

%global _commit cfbe9c8ffafb7dbf13a13f694f3148cf12eb7750
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-daemon
Version:        3.0.25.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Daemon handling the DDE session settings

License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-daemon
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source1:        deepin-daemon.sysusers
Source2:        polkit-gnome-authentication-agent-1-deepin.desktop

BuildRequires:  git
BuildRequires:  gettext
BuildRequires:  golang
BuildRequires:  deepin-gir-generator
BuildRequires:  deepin-go-dbus-factory
BuildRequires:  deepin-go-lib
BuildRequires:  deepin-api-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  systemd-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libbamf3)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  golang-github-BurntSushi-xgb-devel
BuildRequires:  golang-github-BurntSushi-xgbutil-devel
BuildRequires:  golang-github-howeyc-fsnotify-devel
BuildRequires:  golang-github-mattn-go-sqlite3-devel
BuildRequires:  golang-github-alecthomas-kingpin-devel

Requires:       deepin-desktop-base
Requires:       deepin-desktop-schemas
Requires:       deepin-notifications
Requires:       acpid
Requires:       bluez-libs
Requires:       gvfs
Requires:       iso-codes
Requires:       libudisks2
Requires:       mobile-broadband-provider-info
Requires:       polkit-gnome
Requires:       qt5-qtaccountsservice
Requires:       rfkill
Requires:       upower
Recommends:     NetworkManager
Recommends:     deepin-grub2-themes
Provides:       %{repo}%{?_isa} = %{version}-%{release}

%description
Daemon handling the DDE session settings

%prep
%setup -q -n %{repo}-%{_commit}

# Fix library exec path
sed -i '/deepin/s|lib|libexec|' Makefile
sed -i 's|/usr/lib|%{_libexecdir}|' \
    misc/*services/*.service \
    misc/applications/deepin-toggle-desktop.desktop \
    misc/dde-daemon/keybinding/system_actions.json \
    keybinding/shortcuts/system_shortcut.go \
    session/power/constant.go \
    session/power/lid_switch.go \
    bin/dde-system-daemon/main.go \
    bin/search/main.go \
    accounts/user.go

%build
export GOPATH="$(pwd)/build:%{gopath}"
go get gopkg.in/alecthomas/kingpin.v2 \
    github.com/disintegration/imaging \
    github.com/BurntSushi/freetype-go/freetype \
    github.com/BurntSushi/freetype-go/freetype/truetype \
    github.com/BurntSushi/graphics-go/graphics \
    github.com/fsnotify/fsnotify \
    golang.org/x/sys/unix
%make_build

%install
%make_install

install -Dm644 %{S:1} %{buildroot}/usr/lib/sysusers.d/deepin-daemon.conf
install -Dm644 %{S:2} %{buildroot}/etc/xdg/autostart/polkit-gnome-authentication-agent-1-deepin.desktop

%find_lang %{repo}

%post
systemd-sysusers deepin-daemon.conf

%preun
rm -f /var/cache/deepin/mark-setup-network-services

%files -f %{repo}.lang
%doc README.md
%license LICENSE
%{_sysconfdir}/xdg/autostart/*.desktop
%{_libexecdir}/%{name}/
%{_prefix}/lib/sysusers.d/%{name}.conf
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/%{repo}/
%{_datadir}/dde/data/
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/polkit-1/actions/*.policy
%{_var}/cache/appearance/thumbnail/

%changelog
* Fri Jan 20 2017 mosquito <sensor.wen@gmail.com> - 3.0.25.2-1.gitcfbe9c8
- Update to 3.0.25.2
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.25.1-1.gitde04735
- Update to 3.0.25.1
* Sun Dec 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.24-2
- Changed GOLANG dependencies
* Sun Dec 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.24-1
- Upgrade to version 3.0.24
* Mon Oct 31 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.23-1
- Upgrade to version 3.0.23
* Sun Sep 25 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.22-1
- Initial package build
