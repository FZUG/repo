Name:           deepin-artwork-themes
Version:        15.12.4
Release:        2%{?dist}
Summary:        Deepin artwork themes
License:        GPL3
URL:            https://github.com/linuxdeepin/deepin-artwork-themes
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Source1:        https://raw.github.com/linuxdeepin/%{name}/master/LICENSE

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       deepin-desktop-base
Requires:       deepin-icon-theme

%description
Deepin artwork themes

%prep
%setup -q
cp -a %{SOURCE1} .

%build
%make_build build

%install
%make_install PREFIX=%{_prefix}

%files
%doc README.md
%license LICENSE
%dir %{_datadir}/personalization
%{_datadir}/personalization/*

%changelog
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 15.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Aug  6 2017 mosquito <sensor.wen@gmail.com> - 15.12.4-1
- Rebuild

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.4-1.git276dd32
- Update to 15.12.4

* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 15.12.4-1
- Update package to 15.12.4

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 15.12.3-1
- Initial package build
