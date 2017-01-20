%global _commit 69bcc88227ff39de1c52fbbfd094684481a56426
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-icon-theme
Version:        15.12.32
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Icons
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-icon-theme
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  inkscape
#flattr-icon-theme faenza-icon-theme

%description
Deepin Icons

%prep
%setup -q -n %{name}-%{_commit}
sed -i 's|flattr|Flattr|' deepin/index.theme

%build
mkdir build
%{__python2} tools/convert.py deepin build

%install
%{make_install} PREFIX=%{_prefix}

%files
%{_datadir}/icons/deepin/

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.32-1.git69bcc88
- Update to 15.12.32
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
