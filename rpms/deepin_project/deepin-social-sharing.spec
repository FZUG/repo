%global debug_package %{nil}
%global _commit c2dd99bfa687cab4344ccb981c319e4a2bd87659
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-social-sharing
Version:        1.1.4
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin social sharing service
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-social-sharing
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  deepin-gettext-tools
Requires:       deepin-qml-widgets
Requires:       python2-requests-oauthlib
Requires:       python-qt5

%description
Deepin social sharing service

%prep
%setup -q -n %{name}-%{_commit}

# fix python version
find src -type f | xargs sed -i '1s|python$|python2|'

%build
%make_build

%install
%make_install

%files
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo
%{_datadir}/dbus-1/services/*.service

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.1.4-1.gitc2dd99b
- Update to 1.1.4
* Mon Dec 19 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.1.4-1
- Initial package build
