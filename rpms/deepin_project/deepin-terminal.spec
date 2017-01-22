%global _commit 32f96be99e94a021e5a8ad30a41c306ac928a1e3
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-terminal
Version:        2.1.7
Release:        2.git%{_shortcommit}%{?dist}
Summary:        Default terminal emulation application for Deepin
License:        GPL3
URL:            https://github.com/manateelazycat/deepin-terminal
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  cmake
BuildRequires:  vala
BuildRequires:  gettext
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  json-glib-devel
BuildRequires:  libsecret-devel
BuildRequires:  vte291-devel
BuildRequires:  libgee-devel
BuildRequires:  libwnck3-devel
Requires:       vala

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
  /usr/sbin/alternatives --remove x-terminal-emulator %{_bindir}/%{name}
fi

%post
if [ $1 -eq 1 ]; then
  /usr/sbin/alternatives --install %{_bindir}/x-terminal-emulator \
    x-terminal-emulator %{_bindir}/%{name} 20
fi

%files -f %{name}.lang
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/dman/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/applications/%{name}.desktop

%changelog
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
