%global commit 10ccdc2cf25e8e172bf3b86d07085c014cde3012
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-icon-theme
Version:        15.12.46
Release:        1.git%{shortcommit}%{?dist}
Summary:        Deepin Icons
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-icon-theme
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel

%description
Deepin Icons

%prep
%setup -q -n %{name}-%{commit}

%build

%install
%{make_install} PREFIX=%{_prefix}

%files
%{_datadir}/icons/deepin/
%{_datadir}/icons/Sea/

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 15.12.46-1.git10ccdc2
- Update to 15.12.46
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 15.12.42-1.git59ca728
- Update to 15.12.42
* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 15.12.33-1.git2f50a33
- Update to 15.12.33
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.32-1.git69bcc88
- Update to 15.12.32
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
