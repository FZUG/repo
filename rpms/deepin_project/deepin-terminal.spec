%global _commit 76b20cd5310fae1a4e43dc7001d438899eaf3bf6
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global _terminals gnome-terminal mate-terminal xfce4-terminal lxterminal qterminal qterminal-qt5 terminology yakuake fourterm roxterm lilyterm termit xterm mrxvt

Name:           deepin-terminal
Version:        2.4.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Default terminal emulation application for Deepin
License:        GPL3
URL:            https://github.com/manateelazycat/deepin-terminal
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  vala
BuildRequires:  fontconfig-devel
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  json-glib-devel
BuildRequires:  libgee-devel
BuildRequires:  libsecret-devel
BuildRequires:  libwnck3-devel
BuildRequires:  vte291-devel
# right-click menu style
Requires:       deepin-menu
# run command by create_from_commandline
Requires:       deepin-shortcut-viewer
Requires:       xdg-utils
Recommends:     deepin-manual

%description
Default terminal emulation application for Deepin

%prep
%setup -q -n %{name}-%{_commit}
sed -i 's|return __FILE__;|return "%{_datadir}/%{name}/project_path.c";|' project_path.c

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%make_build

%install
%make_install

%find_lang %{name}

%preun
if [ $1 -eq 0 ]; then
  %{_sbindir}/alternatives --remove x-terminal-emulator %{_bindir}/%{name}
fi

%post
if [ $1 -ge 1 ]; then
  %{_sbindir}/alternatives --install %{_bindir}/x-terminal-emulator \
    x-terminal-emulator %{_bindir}/%{name} 20
fi

%triggerin -- konsole5 %_terminals
if [ $1 -ge 1 ]; then
  PRI=20
  for i in konsole %{_terminals}; do
    PRI=$((PRI-1))
    test -x %{_bindir}/$i && \
    %{_sbindir}/alternatives --install %{_bindir}/x-terminal-emulator \
      x-terminal-emulator %{_bindir}/$i $PRI
  done
fi

%triggerpostun -- konsole5 %_terminals
if [ $2 -eq 0 ]; then
  for i in konsole %{_terminals}; do
    test -x %{_bindir}/$i || \
    %{_sbindir}/alternatives --remove x-terminal-emulator %{_bindir}/$i &>/dev/null ||:
  done
fi

%files -f %{name}.lang
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/applications/%{name}.desktop

%changelog
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 2.4.2-1.git76b20cd
- Update to 2.4.2
* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 2.2.2-1.git3ec5488
- Update to 2.2.2
* Sat Feb 11 2017 mosquito <sensor.wen@gmail.com> - 2.1.12-1.git4f7069e
- Update to 2.1.12
* Sun Feb  5 2017 mosquito <sensor.wen@gmail.com> - 2.1.9-3.git1ded038
- Rewrite Req depends
* Sat Jan 28 2017 mosquito <sensor.wen@gmail.com> - 2.1.9-2.git1ded038
- Add trigger for terminal emulator
* Sat Jan 28 2017 mosquito <sensor.wen@gmail.com> - 2.1.9-1.git1ded038
- Update to 2.1.9
* Sun Jan 22 2017 mosquito <sensor.wen@gmail.com> - 2.1.7-2.git32f96be
- Add x-terminal-emulator command for dde-file-manager
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.1.7-1.git32f96be
- Update to 2.1.7
* Thu Jan 12 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 2.1.6-1
- Updated to version 2.1.6
* Thu Dec 15 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 2.1.5-2
- Fixed icon path
* Mon Dec 12 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 2.1.5-1
- Initial package build
