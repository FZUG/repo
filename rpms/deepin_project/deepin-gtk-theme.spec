%global _commit 9fd5f709d8bd3c05a493e0c4eddc4688de9ac66c
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-gtk-theme
Version:        15.12.8
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin GTK Theme
License:        LGPLv3
URL:            https://github.com/linuxdeepin/deepin-gtk-theme
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz
BuildArch:      noarch

%description
Deepin GTK Theme

%prep
%setup -q -n %{name}-%{_commit}

%build

%install
%make_install PREFIX=%{_prefix}

%files
%{_datadir}/themes/deepin/
%{_datadir}/themes/deepin-dark/

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.8-1.git9fd5f70
- Update to 15.12.8
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
