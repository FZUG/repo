%global commit 61405025aaa97e37e45c1d70e3719034da88b967
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-gtk-theme
Version:        17.10.3
Release:        1.git%{shortcommit}%{?dist}
Summary:        Deepin GTK Theme
License:        LGPLv3
URL:            https://github.com/linuxdeepin/deepin-gtk-theme
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildArch:      noarch

%description
Deepin GTK Theme

%prep
%setup -q -n %{name}-%{commit}

%build

%install
%make_install PREFIX=%{_prefix}

%files
%{_datadir}/themes/deepin/
%{_datadir}/themes/deepin-dark/

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 17.10.3-1.git6140502
- Update to 17.10.3
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 17.10.2-1.giteba2cf4
- Update to 17.10.2
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.8-1.git9fd5f70
- Update to 15.12.8
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
