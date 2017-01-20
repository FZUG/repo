# Deepin packages for Fedora

These files are based on [cz-guardian/fedora-deepin](https://github.com/cz-guardian/fedora-deepin/) and [Arch packages](https://www.archlinux.org/packages/?q=deepin). You can visit the [Deepin Copr](https://copr.fedorainfracloud.org/coprs/mosquito/deepin/) to install them. Thanks for all of the community developers and packagers.


## Installation instructions
    sudo dnf install http://download1.rpmfusion.org/free/fedora/releases/$(rpm -E %fedora)/Everything/$(uname -i)/os/Packages/r/rpmfusion-free-release-$(rpm -E %fedora)-1.noarch.rpm
    sudo dnf copr enable mosquito/deepin
    sudo dnf update
    sudo dnf install deepin-desktop deepin-session-ui deepin-screenshot deepin-terminal
    sudo systemctl disable gdm.service && sudo systemctl enable lightdm.service
    sudo sed -i "/SELINUX=/s|enforcing|disabled|" /etc/selinux/config

After this is done, simply reboot into your new nice environment.


## fedora-deepin repository content

This repository contains the following .specs for integrating the deepin desktop environment into Fedora. You can simply compile them in order.
* deepin-gsettings
* python2-javascriptcore
* deepin-gettext-tools
* python2-deepin-ui
* python2-deepin-util
* deepin-music
* python2-xpybutil
* deepin-screenshot
* deepin-go-lib
* deepin-dbus-generator
* deepin-dbus-factory
* deepin-movie
* deepin-menu
* deepin-qml-widgets
* python2-ass
* python3-dae
* python2-pysrt
* python2-deepin-storm
* gsettings-qt
* golang-github-*
* deepin-tool-kit
* deepin-sound-theme
* deepin-social-sharing
* deepin-shortcut-viewer
* deepin-notifications
* deepin-nautilus-properties
* deepin-cogl
* deepin-mutter
* deepin-metacity
* deepin-image-viewer
* deepin-icon-theme
* deepin-gtk-theme
* deepin-grub2-themes
* deepin-gir-generator
* deepin-game
* deepin-desktop-schemas
* deepin-desktop-base
* deepin-artwork-themes
* deepin-calendar
* deepin-account-faces
* deepin-terminal
* deepin-wallpapers
* deepin-qt-dbus-factory
* deepin-file-manager
* deepin-qt5integration
* deepin-dock
* deepin-desktop
* deepin-launcher
* deepin-wm-switcher
* deepin-wm
* deepin-manual
* deepin-api
* startdde
* deepin-file-manager-backend
* deepin-control-center
* deepin-daemon
* deepin-session-ui


## Resources
* [Deepin Github](https://github.com/linuxdeepin/), [Official site](https://www.deepin.org/en/)
* [fedora-deepin repository list](https://copr.fedorainfracloud.org/coprs/mosquito/deepin/packages/)
* [fedora-deepin (jstepanek)](https://copr.fedorainfracloud.org/coprs/jstepanek/deepin/): thanks @cz-guardian
* [arch-deepin](https://github.com/fasheng/arch-deepin/): [Deepin Desktop Environment on Arch](https://bbs.archlinux.org/viewtopic.php?id=181861)
* [manjaro-deepin](https://github.com/manjaro/packages-community/): [issue 98](https://github.com/fasheng/arch-deepin/issues/98)
* [debian-deepin](https://github.com/debiancn/repo/issues/31)
