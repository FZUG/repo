Name:           deepin-sound-theme
Version:        15.10.1
Release:        1%{?dist}
Summary:        Deepin sound theme
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-sound-theme
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
Source1:        https://raw.github.com/linuxdeepin/%{name}/master/README.md
Source2:        https://raw.github.com/linuxdeepin/%{name}/master/LICENSE
BuildArch:      noarch

%description
Sound files for the Deeping Desktop Environment.

%prep
%setup -q
cp -a %{S:1} %{S:2} .

%build

%install
%make_install

%files
%doc README.md
%license LICENSE
%dir %{_datadir}/sounds/deepin/
%dir %{_datadir}/sounds/deepin/stereo/
%{_datadir}/sounds/deepin/index.theme
%{_datadir}/sounds/deepin/stereo/*.ogg

%changelog
* Sun Aug  6 2017 mosquito <sensor.wen@gmail.com> - 15.10.1-1
- Rebuild

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.10.1-1.git0045de4
- Update to 15.10.1

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
