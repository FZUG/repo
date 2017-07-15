%global _commit 95af7cd15c013a32b10b24ce534074993774cef4
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-desktop-schemas
Version:        3.1.13
Release:        1.git%{_shortcommit}%{?dist}
Summary:        GSettings deepin desktop-wide schemas
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-desktop-schemas
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python
BuildRequires:  glib2
Requires:       dconf
Requires:       deepin-gtk-theme
Requires:       deepin-sound-theme
Requires:       deepin-artwork-themes

%description
GSettings deepin desktop-wide schemas

%prep
%setup -q -n %{name}-%{_commit}

# fix default background url
sed -i '/picture-uri/s|default_background.jpg|default.png|' \
    overrides/common/com.deepin.wrap.gnome.desktop.override

%build
%make_build ARCH=x86

%install
%make_install PREFIX=%{_prefix}

%check
make test

%files
%doc README.md
%{_datadir}/glib-2.0/schemas/*

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 3.1.13-1.git95af7cd
- Update to 3.1.13
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 3.1.6-1.gita41ca06
- Update to 3.1.6
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.1-1.gitf6ffe70
- Update to 3.1.1
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.0.13-1.git10efc5e
- Update to 3.0.13
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.13-1
- Update to version 3.0.13
* Sat Dec 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.12-1
- Update to version 3.0.12
* Thu Oct 27 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.11-1
- Update to version 3.0.11
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.10-1
- Initial package build
