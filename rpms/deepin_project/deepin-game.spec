%global _commit 2252a7f6ab4a8eee68e3b6e9303b88ca7db42dc5
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-game
Version:        2014.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Game Center
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-game
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  deepin-gettext-tools
Requires:       python2-deepin-ui
Requires:       python2-deepin-storm
Requires:       python2-jswebkit
Requires:       dbus-python
Requires:       hicolor-icon-theme

%description
Deepin Game Center

%prep
%setup -q -n %{name}-%{_commit}
# fix python version
find src -type f | xargs sed -i '1s|python$|python2|'

%build
deepin-generate-mo tools/locale_config.ini

%install
%make_install PREFIX=%{_prefix}

%files
%{_bindir}/*
%{_datadir}/*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2014.2-1.git2252a7f
- Update to 2014.2
* Mon Dec 26 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 2014.2-1
- Initial package build
