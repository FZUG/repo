Name:           deepin-shortcut-viewer
Version:        1.3.1
Release:        2%{?dist}
Summary:        Deepin Shortcut Viewer
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-shortcut-viewer
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(dtkwidget1) = 1.1
Provides:       bundled(CuteLogger)

%description
The program displays a shortcut key window when a JSON data is passed.

%prep
%setup -q
sed -i 's|dtkwidget|dtkwidget1|; s|dtkbase|dtkbase1|' %{name}.pro

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT="%{buildroot}"

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}

%changelog
* Sun Aug 20 2017 mosquito <sensor.wen@gmail.com> - 1.3.1-2
- Use dtkwidget1 library

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.3.1-1.git729e82d
- Update to 1.3.1

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.2-1.git760b082
- Update to 1.0.2

* Sun Dec 04 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.02-1
- Updated to version 1.02-1

* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.01-1
- Initial package build
