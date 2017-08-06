%global project dde-daemon
%global repo %{project}

Name:           deepin-daemon
Version:        3.1.17
Release:        1%{?dist}
Summary:        Daemon handling the DDE session settings
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-daemon
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
Source1:        deepin-daemon.sysusers

BuildRequires:  git
BuildRequires:  gettext
BuildRequires:  golang
BuildRequires:  deepin-gir-generator
BuildRequires:  deepin-go-dbus-factory
BuildRequires:  golang-deepin-go-lib-devel
BuildRequires:  deepin-api-devel
BuildRequires:  libgnome-keyring-devel
BuildRequires:  systemd-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  pam-devel
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
Requires:       deepin-grub2-themes
Requires:       deepin-notifications
Requires:       acpid
Requires:       bluez-libs
Requires:       gvfs
Requires:       iw
Requires:       libudisks2
Requires:       deepin-polkit-agent
Requires:       qt5-qtaccountsservice
Requires:       rfkill
Requires:       upower
Requires:       xdotool
Recommends:     NetworkManager-vpnc-gnome
Recommends:     NetworkManager-pptp-gnome
Recommends:     NetworkManager-l2tp-gnome
Recommends:     NetworkManager-strongswan-gnome
Recommends:     NetworkManager-openvpn-gnome
Recommends:     NetworkManager-openconnect-gnome
Recommends:     iso-codes
Recommends:     mobile-broadband-provider-info
Recommends:     google-noto-mono-fonts
Recommends:     google-noto-sans-fonts

%description
Daemon handling the DDE session settings

%prep
%setup -q -n %{repo}-%{version}

# Fix library exec path
sed -i '/deepin/s|lib|libexec|' Makefile
sed -i 's|lib/NetworkManager|libexec|' network/utils_test.go
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

# Fix grub.cfg path
sed -i '/ScriptFile/s|grub/|grub2/|' grub2/log.go
sed -i 's|default_background.jpg|default.png|' accounts/user.go

# https://github.com/niemeyer/gopkg/issues/50
git config --global http.https://gopkg.in.followRedirects true

%build
export GOPATH="$(pwd)/build:%{gopath}"
go get gopkg.in/alecthomas/kingpin.v2 \
    github.com/disintegration/imaging \
    github.com/BurntSushi/freetype-go/freetype \
    github.com/BurntSushi/freetype-go/freetype/truetype \
    github.com/BurntSushi/graphics-go/graphics \
    github.com/fsnotify/fsnotify \
    github.com/axgle/mahonia \
    github.com/msteinert/pam \
    github.com/nfnt/resize \
    golang.org/x/sys/unix \
    gopkg.in/yaml.v2
%make_build

%install
%make_install

install -Dm644 %{S:1} %{buildroot}/usr/lib/sysusers.d/deepin-daemon.conf

# fix systemd/logind config
install -d %{buildroot}/usr/lib/systemd/logind.conf.d/
cat > %{buildroot}/usr/lib/systemd/logind.conf.d/10-%{name}.conf <<EOF
[Login]
HandlePowerKey=ignore
HandleSuspendKey=ignore
EOF

%find_lang %{repo}

%post
if [ $1 -ge 1 ]; then
  systemd-sysusers deepin-daemon.conf
  %{_sbindir}/alternatives --install %{_bindir}/x-terminal-emulator \
    x-terminal-emulator %{_libexecdir}/%{name}/default-terminal 30
fi

%preun
if [ $1 -eq 0 ]; then
  %{_sbindir}/alternatives --remove x-terminal-emulator \
    %{_libexecdir}/%{name}/default-terminal
fi

%postun
if [ $1 -eq 0 ]; then
  rm -f /var/cache/deepin/mark-setup-network-services
  rm -f /var/log/deepin.log 
fi

%files -f %{repo}.lang
%doc README.md
%license LICENSE
%{_libexecdir}/%{name}/
%{_prefix}/lib/sysusers.d/%{name}.conf
%{_prefix}/lib/systemd/logind.conf.d/10-%{name}.conf
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/%{repo}/
%{_datadir}/dde/data/
%{_datadir}/polkit-1/actions/*.policy
%{_var}/cache/appearance/thumbnail/

%changelog
* Wed Aug  2 2017 mosquito <sensor.wen@gmail.com> - 3.1.17-1
- Update to 3.1.17

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 3.1.16.1-1
- Update to 3.1.16.1

* Thu Jul 20 2017 mosquito <sensor.wen@gmail.com> - 3.1.14-1.git0f8418a
- Update to 3.1.14

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.13-1.git03541ad
- Update to 3.1.13

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.1.9-1.git82313d2
- Update to 3.1.9

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.3-1.git87df955
- Update to 3.1.3

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
