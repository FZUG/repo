%global commit 729e82d50a05d88eae61ccbf24f5b2b78eba34db
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-shortcut-viewer
Version:        1.3.1
Release:        1.git%{shortcommit}%{?dist}
Summary:        Deepin Shortcut Viewer
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-shortcut-viewer
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  qt5-qtbase-devel
BuildRequires:  deepin-tool-kit-devel
Provides:       bundled(CuteLogger)

%description
Deepin Shortcut Viewer

%prep
%setup -q -n %{name}-%{commit}

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
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.3.1-1.git729e82d
- Update to 1.3.1
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.2-1.git760b082
- Update to 1.0.2
* Sun Dec 04 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.02-1
- Updated to version 1.02-1
* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.01-1
- Initial package build
