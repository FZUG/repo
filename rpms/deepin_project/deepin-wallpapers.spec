%global md5() {$(echo -n %1 | md5sum | awk '{print$1}')}

Name:           deepin-wallpapers
Version:        1.7.5
Release:        1%{?dist}
Summary:        Deepin Wallpapers provides wallpapers of dde
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-wallpapers
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  deepin-api

%description
%{summary}.

%prep
%setup -q -n %{name}-%{version}
sed -i 's|lib|libexec|' Makefile

%build
%make_build

%install
install -d %{buildroot}%{_datadir}/wallpapers/deepin/
cp deepin/* deepin-private/* deepin-community/* %{buildroot}%{_datadir}/wallpapers/deepin/

install -d %{buildroot}%{_var}/cache/
cp -ar image-blur %{buildroot}%{_var}/cache/

install -d %{buildroot}%{_datadir}/backgrounds/deepin/
ln -sv ../../wallpapers/deepin/Hummingbird_by_Shu_Le.jpg \
  %{buildroot}%{_datadir}/backgrounds/deepin/desktop.jpg
ln -sv %{md5 %{_datadir}/wallpapers/deepin/Hummingbird_by_Shu_Le.jpg}.jpg \
  %{buildroot}%{_var}/cache/image-blur/%{md5 %{_datadir}/backgrounds/deepin/desktop.jpg}.jpg

%files
%doc README.md
%license LICENSE
%{_datadir}/backgrounds/deepin/
%{_datadir}/wallpapers/deepin/
%{_var}/cache/image-blur/

%changelog
* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 1.7.5-1
- Update to 1.7.5

* Fri Jul 20 2018 mosquito <sensor.wen@gmail.com> - 1.7.4-1
- Update to 1.7.4

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 1.7-1
- Update to 1.7

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.6-1
- Update to 1.6

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.4-1.gita54c282
- Update to 1.4

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.3-1.gitdbc981b
- Update to 1.3

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
