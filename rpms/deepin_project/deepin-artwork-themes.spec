%global commit 276dd326eee81b337af44f6d4bdc09c8f1d91a9c
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-artwork-themes
Version:        15.12.4
Release:        1%{?dist}
Summary:        Deepin artwork themes
License:        LGPL3
URL:            https://github.com/linuxdeepin/deepin-artwork-themes
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
Requires:       deepin-desktop-base
Requires:       deepin-icon-theme

%description
Deepin artwork themes

%prep
%setup -q -n %{name}-%{commit}

%build
make build

%install
%make_install PREFIX=%{_prefix}

%files
%{_datadir}/personalization/*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.4-1.git276dd32
- Update to 15.12.4
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 15.12.4-1
- Update package to 15.12.4
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 15.12.3-1
- Initial package build
