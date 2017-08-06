%global commit c4c7727893ba10dc83872e6237eb0783b664e626
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-artwork-themes
Version:        15.12.4
Release:        1.git%{shortcommit}%{?dist}
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
%doc README.md
%license LICENSE
%{_datadir}/personalization/*

%changelog
* Sun Aug  6 2017 mosquito <sensor.wen@gmail.com> - 15.12.4-1.gitc4c7727
- Rebuild

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.4-1.git276dd32
- Update to 15.12.4

* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 15.12.4-1
- Update package to 15.12.4

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 15.12.3-1
- Initial package build
