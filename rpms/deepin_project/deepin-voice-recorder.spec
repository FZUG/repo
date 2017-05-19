%global _commit 2a95a46109a80ecf5da47af0fef82b397fdfa9f8
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-voice-recorder
Version:        1.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Voice Recorder
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-voice-recorder
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtmultimedia-devel
BuildRequires:  ffmpeg-devel

%description
Deepin Voice Recorder

%prep
%setup -q -n %{name}-%{_commit}
sed -i 's|=lupdate|=lupdate-qt5|;s|=lrelease|=lrelease-qt5|' deepin-voice-recorder.pro

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
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.2-1.git2a95a46
- Initial build
