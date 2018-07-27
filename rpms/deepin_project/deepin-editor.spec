Name:           deepin-editor
Version:        0.0.5
Release:        1%{?dist}
Summary:        Simple editor for Linux Deepin
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-editor
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  freeimage-devel
BuildRequires:  cmake(KF5Codecs)
BuildRequires:  cmake(KF5SyntaxHighlighting)
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(dtkwm)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(xcb-aux)
BuildRequires:  pkgconfig(polkit-qt5-1)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5DBus)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  qt5-linguist
Requires:       deepin-notifications
Requires:       deepin-qt5integration

%description
%{summary}.

%prep
%setup -q

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop ||:

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-daemon
%{_datadir}/%{name}/words.db
%{_datadir}/applications/%{name}.desktop
%{_datadir}/dbus-1/system.d/com.deepin.editor.conf
%{_datadir}/dbus-1/system-services/com.deepin.editor.daemon.service
%{_datadir}/polkit-1/actions/com.deepin.editor.policy

%changelog
* Mon Jul 23 2018 mosquito <sensor.wen@gmail.com> - 0.0.5-1
- Initial package build
