%global commit d2d7974839fdaaca38bdd06dfaa24ca3a1a8bde3
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-sound-theme
Version:        15.10.1
Release:        1.git%{shortcommit}%{?dist}
Summary:        Deepin sound theme
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-sound-theme
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildArch:      noarch

%description
Sound files for the Deeping Desktop Environment.

%prep
%setup -q -n %{name}-%{commit}

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
* Sun Aug  6 2017 mosquito <sensor.wen@gmail.com> - 15.10.1-1.gitd2d7974
- Rebuild

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.10.1-1.git0045de4
- Update to 15.10.1

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
