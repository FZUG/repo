%global _commit 760b0825bb1ecbbef3f9c17b2bc77940fc3011df
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-shortcut-viewer
Version:        1.0.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Shortcut Viewer
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-shortcut-viewer
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  qt5-qtbase-devel

%description
Deepin Shortcut Viewer

%prep
%setup -q -n %{name}-%{_commit}

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT="%{buildroot}"

%files
%{_bindir}/%{name}

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.2-1.git760b082
- Update to 1.0.2
* Sun Dec 04 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.02-1
- Updated to version 1.02-1
* Mon Oct 10 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.01-1
- Initial package build
