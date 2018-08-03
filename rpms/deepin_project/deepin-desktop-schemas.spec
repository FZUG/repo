Name:           deepin-desktop-schemas
Version:        3.2.18
Release:        1%{?dist}
Summary:        GSettings deepin desktop-wide schemas
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-desktop-schemas
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python
BuildRequires:  glib2
Requires:       dconf
Requires:       deepin-gtk-theme
Requires:       deepin-icon-theme
Requires:       deepin-sound-theme
Requires:       deepin-artwork-themes

%description
%{summary}.

%prep
%setup -q

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
%license LICENSE
%{_datadir}/glib-2.0/schemas/*

%changelog
* Thu Aug  2 2018 mosquito <sensor.wen@gmail.com> - 3.2.18-1
- Update to 3.2.18

* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 3.2.15-1
- Update to 3.2.15

* Tue Mar 20 2018 mosquito <sensor.wen@gmail.com> - 3.2.9-1
- Update to 3.2.9

* Fri Feb 16 2018 mosquito <sensor.wen@gmail.com> - 3.2.6-1
- Update to 3.2.6

* Sat Feb 10 2018 mosquito <sensor.wen@gmail.com> - 3.2.5-1
- Update to 3.2.5

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 mosquito <sensor.wen@gmail.com> - 3.2.4-1
- Update to 3.2.4

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 3.2.3-1
- Update to 3.2.3

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 3.1.19-1
- Update to 3.1.19

* Mon Oct 23 2017 mosquito <sensor.wen@gmail.com> - 3.1.18-1
- Update to 3.1.18

* Fri Oct 13 2017 mosquito <sensor.wen@gmail.com> - 3.1.17-1
- Update to 3.1.17

* Sat Aug 26 2017 mosquito <sensor.wen@gmail.com> - 3.1.16-1
- Update to 3.1.16

* Tue Aug  1 2017 mosquito <sensor.wen@gmail.com> - 3.1.15-1
- Update to 3.1.15

* Thu Jul 20 2017 mosquito <sensor.wen@gmail.com> - 3.1.14-1.giteeea1d4
- Update to 3.1.14

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
