Name:           sway
Version:        0.6
Release:        1%{?dist}
Summary:        i3-compatible window manager for Wayland
Group:          User Interface/X
License:        MIT
URL:            https://github.com/SirCmpwn/sway/
Source0:        https://github.com/SirCmpwn/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(wlc)
BuildRequires:  wayland-devel
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  asciidoc
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  gdk-pixbuf2-devel
BuildRequires:  pam-devel
Recommends:     ImageMagick
Recommends:     ffmpeg

%description
Sway is a tiling window manager supporting Wayland compositor protocol and 
i3-compatible configuration.

%prep
%autosetup -n %{name}-%{version}

%build
%cmake \
       -DCMAKE_INSTALL_SYSCONFDIR=/etc \
       -DBUILD_SHARED_LIBS:BOOL=OFF \
       .
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%dir /etc/sway
%config(noreplace)/etc/sway/config
%config %{_sysconfdir}/pam.d/swaylock
%{_mandir}/man1/sway*.1*
%{_mandir}/man5/sway*.5*
%{_bindir}/sway
%{_bindir}/swaybar
%{_bindir}/swaybg
%{_bindir}/swaygrab
%{_bindir}/swaylock
%{_bindir}/swaymsg
/usr/share/sway/*
/usr/share/zsh/site-functions/_sway*
/usr/share/wayland-sessions/sway.desktop

%changelog
* Thu May 09 2016 nrechn <neil@gyz.io> - 0.6-1
- Initial packaging

