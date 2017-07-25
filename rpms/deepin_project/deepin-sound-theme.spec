%global commit 0045de406a143b798ac3b2fbe2b318b4a4894176
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-sound-theme
Version:        15.10.1
Release:        1%{?dist}
Summary:        Deepin sound theme
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-sound-theme
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildArch:      noarch

%description
Deepin sound theme

%prep
%setup -q -n %{name}-%{commit}

%build

%install
%make_install PREFIX=%{_prefix}

%files
%defattr(-,root,root,-)
%dir %{_datadir}/sounds/deepin/
%dir %{_datadir}/sounds/deepin/stereo/
%{_datadir}/sounds/deepin/index.theme
%{_datadir}/sounds/deepin/stereo/*.ogg

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.10.1-1.git0045de4
- Update to 15.10.1
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
