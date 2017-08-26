%global debug_package %{nil}

Name:           deepin-grub2-themes
Version:        1.0.0
Release:        1%{?dist}
Summary:        Deepin grub2 themes
License:        CC-BY-SA
URL:            https://github.com/linuxdeepin/deepin-grub2-themes
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch
# matches grub2 pkg archs
ExcludeArch:    s390 s390x %{arm}
%ifnarch aarch64
Requires:       grub2
%else
Requires:       grub2-efi
%endif

%description
Deepin grub2 themes

%prep
%setup -q

%install
%make_install TARGET="%{buildroot}/boot/grub2/themes"

%files
%license LICENSE
/boot/grub2/themes/deepin/

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.0-1
- Update to 1.0.0

* Sat Dec 03 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.0-1
- Initial package build
