%global _commit c4040d0f2e98c40e9c897cdfd3cf20af62cadce2
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-screen-recorder
Version:        1.8
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Screen Recorder
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-screen-recorder
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcb-util)
Requires:       byzanz
Requires:       ffmpeg

%description
Deepin Screen Recorder

%prep
%setup -q -n %{name}-%{_commit}
sed -i 's|=lupdate|=lupdate-qt5|;s|=lrelease|=lrelease-qt5|' deepin-screen-recorder.pro

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
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.svg

%changelog
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.8-1.gitc4040d0
- Update to 1.8
* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 1.3-1.git8e0a4b3
- Update to 1.3
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 0.8-1.git9eda269
- Initial build
