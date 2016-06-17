%global debug_package %{nil}

Name:           sway
Version:        0.8
Release:        1%{?dist}
Summary:        i3-compatible window manager for Wayland
Group:          User Interface/X
License:        MIT
URL:            https://github.com/SirCmpwn/sway/
Source0:        https://github.com/SirCmpwn/%{name}/archive/%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  pkgconfig(wlc)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(gdk-pixbuf-2.0)
BuildRequires:  pkgconfig(json-c)
BuildRequires:  pkgconfig(libpcre)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  asciidoc
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
    -DCMAKE_INSTALL_SYSCONFDIR=%{_sysconfdir} \
    -DBUILD_SHARED_LIBS:BOOL=OFF \
    -Dzsh-completions=YES \
    .
%make_build

%install
%make_install

%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/config
%config %{_sysconfdir}/pam.d/%{name}lock
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man5/%{name}*.5*
%{_bindir}/%{name}
%{_bindir}/%{name}bar
%{_bindir}/%{name}bg
%{_bindir}/%{name}grab
%{_bindir}/%{name}lock
%{_bindir}/%{name}msg
%{_datadir}/%{name}/*
%{_datadir}/zsh/site-functions/_%{name}*
%{_datadir}/wayland-sessions/%{name}.desktop

%changelog
* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 0.8-1
- Upddate to 0.8

* Mon May 23 2016 nrechn <neil@gyz.io> - 0.7-1
- Upddate to 0.7

* Mon May 09 2016 nrechn <neil@gyz.io> - 0.6-1
- Initial packaging

