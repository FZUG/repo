%global repo dde-daemon
%global ds_url https://github.com/linuxdeepin/default-settings

Name:           deepin-daemon
Version:        3.2.22
Release:        1%{?dist}
Summary:        Daemon handling the DDE session settings
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-daemon
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
Source1:        %{ds_url}/archive/2016.9.8/default-settings-2016.9.8.tar.gz
Source2:        deepin-daemon.sysusers
Patch0:         https://raw.github.com/jouyouyun/tap-gesture-patches/master/patches/dde-daemon_3.2.3.patch

ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# https://github.com/golang/go/issues/21947
ExcludeArch:    ppc64le aarch64
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires:  deepin-gettext-tools
BuildRequires:  deepin-gir-generator
BuildRequires:  fontpackages-devel
BuildRequires:  librsvg2-tools
BuildRequires:  pam-devel
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(gnome-keyring-1)
BuildRequires:  pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(libbamf3)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libnl-3.0)
BuildRequires:  pkgconfig(libnl-genl-3.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libsystemd)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(gudev-1.0)
BuildRequires:  pkgconfig(librsvg-2.0)
BuildRequires:  pkgconfig(libinput)
BuildRequires:  pkgconfig(poppler-glib)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  pkgconfig(xkbfile)
BuildRequires:  golang-deepin-dbus-factory-devel
BuildRequires:  golang(pkg.deepin.io/lib)
BuildRequires:  golang(pkg.deepin.io/lib/fsnotify)
BuildRequires:  golang(pkg.deepin.io/dde/api/dxinput)
BuildRequires:  golang(github.com/linuxdeepin/go-dbus-factory)
BuildRequires:  golang(github.com/linuxdeepin/go-x11-client)
BuildRequires:  golang(github.com/BurntSushi/xgb)
BuildRequires:  golang(github.com/BurntSushi/xgbutil)
BuildRequires:  golang(github.com/axgle/mahonia)
BuildRequires:  golang(github.com/msteinert/pam)
BuildRequires:  golang(github.com/nfnt/resize)
BuildRequires:  golang(github.com/cryptix/wav)
BuildRequires:  golang(gopkg.in/alecthomas/kingpin.v2)
BuildRequires:  golang(gopkg.in/yaml.v2)

Requires:       deepin-desktop-base
Requires:       deepin-desktop-schemas
Requires:       deepin-notifications
%ifnarch s390 s390x %{arm}
Requires:       deepin-grub2-themes
Requires:       acpid
%endif
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
%setup -q -a1 -n %{repo}-%{version}
%patch0 -p1 -b dde-daemon-3.2.3

# Fix library exec path
sed -i '/deepin/s|lib|libexec|' Makefile
sed -i '/systemd/s|lib|usr/lib|' Makefile
sed -i 's|lib/NetworkManager|libexec|' network/utils_test.go
sed -i 's|/usr/lib|%{_libexecdir}|' \
    misc/*services/*.service \
    misc/etc/pam.d/deepin-auth \
    misc/applications/deepin-toggle-desktop.desktop \
    misc/dde-daemon/gesture.json \
    misc/dde-daemon/keybinding/system_actions.json \
    keybinding/shortcuts/system_shortcut.go \
    session/power/constant.go \
    session/power/lid_switch.go \
    service_trigger/manager.go \
    bin/dde-system-daemon/main.go \
    bin/search/main.go

# Fix grub.cfg path
sed -i 's|boot/grub|boot/grub2|' grub2/{theme,log,entry,grub_params}.go

%build
export GOPATH="$(pwd)/build:%{gopath}"
BUILDID="0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')"
%make_build GOBUILD="go build -compiler gc -ldflags \"-B $BUILDID\""

%install
%make_install

install -Dm644 %{S:2} %{buildroot}/usr/lib/sysusers.d/deepin-daemon.conf

# fix systemd/logind config
install -d %{buildroot}/usr/lib/systemd/logind.conf.d/
cat > %{buildroot}/usr/lib/systemd/logind.conf.d/10-%{name}.conf <<EOF
[Login]
HandlePowerKey=ignore
HandleSuspendKey=ignore
EOF

# install default settings
pushd default-settings-2016.9.8
install -Dm644 usr.share.d/deepin-default-settings/fontconfig.json \
    %{buildroot}%{_datadir}/deepin-default-settings/fontconfig.json

install -d %{buildroot}%{_fontconfig_templatedir} %{buildroot}%{_fontconfig_confdir}
cp usr.share.d/fontconfig/conf.avail/*.conf %{buildroot}%{_fontconfig_templatedir}/
for i in $(ls %{buildroot}%{_fontconfig_templatedir} | grep conf$); do
  ln -sf %{_fontconfig_templatedir}/$i %{buildroot}%{_fontconfig_confdir}/$i
done
popd

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
%{_sysconfdir}/pam.d/deepin-auth
%{_sysconfdir}/pam.d/deepin-auth-keyboard
%{_libexecdir}/%{name}/
%{_sysusersdir}/%{name}.conf
%{_prefix}/lib/systemd/logind.conf.d/10-%{name}.conf
%{_unitdir}/deepin-accounts-daemon.service
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_datadir}/dbus-1/system.d/*.conf
%{_datadir}/icons/hicolor/*/status/*
%{_datadir}/%{repo}/
%{_datadir}/dde/
%{_datadir}/polkit-1/actions/*.policy
%{_datadir}/deepin-default-settings/
%{_fontconfig_templatedir}/*.conf
%{_fontconfig_confdir}/*.conf
%{_var}/cache/appearance/
%{_var}/lib/polkit-1/localauthority/10-vendor.d/com.deepin.daemon.Accounts.pkla

%changelog
* Thu Aug  2 2018 mosquito <sensor.wen@gmail.com> - 3.2.22-1
- Update to 3.2.22

* Fri Jul 20 2018 mosquito <sensor.wen@gmail.com> - 3.2.21-1
- Update to 3.2.21

* Sat Mar 24 2018 mosquito <sensor.wen@gmail.com> - 3.2.12-1
- Update to 3.2.12

* Tue Mar 20 2018 mosquito <sensor.wen@gmail.com> - 3.2.11-1
- Update to 3.2.11

* Mon Mar 19 2018 mosquito <sensor.wen@gmail.com> - 3.2.9-2
- Nothing providers grub2 in s390x and armv7hl.

* Fri Feb 16 2018 mosquito <sensor.wen@gmail.com> - 3.2.9-1
- Update to 3.2.9

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 3.2.8-2
- Rebuilt for switch to libxcrypt

* Fri Dec 22 2017 mosquito <sensor.wen@gmail.com> - 3.2.8-1
- Update to 3.2.8

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 3.2.7-1
- Update to 3.2.7

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 3.2.2-1
- Update to 3.2.2

* Sat Oct 14 2017 mosquito <sensor.wen@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Wed Aug 30 2017 mosquito <sensor.wen@gmail.com> - 3.1.19-2
- Add fontconfig settings

* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.19-1
- Update to 3.1.19

* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 3.1.18-1
- Update to 3.1.18

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
