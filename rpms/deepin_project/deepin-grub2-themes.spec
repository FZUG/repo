%global commit 5d651320b739b6793af3dc47879c44826aaa7925
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-grub2-themes
Version:        1.0.0
Release:        1%{?dist}
Summary:        Deepin grub2 themes
License:        LGPLv3
URL:            https://github.com/linuxdeepin/deepin-grub2-themes
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

%description
Deepin grub2 themes

%prep
%setup -q -n %{name}-%{commit}

%install
%make_install TARGET="%{buildroot}/boot/grub2/themes"

%files
/boot/grub/themes/deepin/

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.0-1.git5d65132
- Update to 1.0.0
* Sat Dec 03 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.0-1
- Initial package build
