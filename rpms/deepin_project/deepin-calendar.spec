%global project dde-calendar
%global reponame %{project}

Name:           deepin-calendar
Version:        1.0.11
Release:        2%{?dist}
Summary:        Calendar for Deepin Desktop Environment
License:        GPLv3+
URL:            https://github.com/linuxdeepin/dde-calendar
Source0:        %{url}/archive/%{version}/%{reponame}-%{version}.tar.gz

BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
BuildRequires:  deepin-tool-kit-devel
BuildRequires:  deepin-gettext-tools
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
Calendar for Deepin Desktop Environment.

%prep
%setup -q -n %{reponame}-%{version}
sed -i 's|lrelease|lrelease-qt5|g' translate_generation.sh

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{reponame}.desktop

%files
%doc README.md
%license LICENSE
%{_bindir}/%{reponame}
%{_datadir}/%{reponame}/
%{_datadir}/applications/%{reponame}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{reponame}.svg

%changelog
* Sun Aug 06 2017 Zamir SUN <sztsian@gmail.com> - 1.0.11-2
- Add check for desktop file

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
