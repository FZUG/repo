%global project dde-calendar
%global repo %{project}

%global commit d2c7b9e26b34ee5c30d393290fb0bba469c98a0b
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-calendar
Version:        1.0.11
Release:        1.git%{shortcommit}%{?dist}
Summary:        Calendar for Deepin Desktop Environment
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-calendar
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  deepin-tool-kit-devel
BuildRequires:  deepin-gettext-tools
Provides:       %{repo}%{?_isa} = %{version}-%{release}

%description
Calendar for Deepin Desktop Environment

%prep
%setup -q -n %{repo}-%{commit}
sed -i 's|lrelease|lrelease-qt5|g' translate_generation.sh

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%{_bindir}/%{repo}
%{_datadir}/%{repo}/
%{_datadir}/applications/%{repo}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{repo}.svg

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.0.11-1.gitd2c7b9e
- Update to 1.0.11
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.0.7-1.gita8a4f5b
- Update to 1.0.7
* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 1.0.4-1.gitb59053f
- Update to 1.0.4
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.3-1.gitd7e42a1
- Update to 1.0.3
* Mon Dec 19 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.3-1
- Update to version 1.0.3
* Fri Dec 09 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.2-2
- Rebuild with newer deepin-tool-kit
* Sun Oct 09 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.2-1
- Initial package build
