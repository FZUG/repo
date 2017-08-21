%global project dde-polkit-agent
%global repo %{project}

Name:           deepin-polkit-agent
Version:        0.1.0
Release:        1%{?dist}
Summary:        Deepin Polkit Agent
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-polkit-agent
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  pkgconfig(dtkwidget) = 2.0
BuildRequires:  pkgconfig(dframeworkdbus)
BuildRequires:  pkgconfig(polkit-qt5-1)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  qt5-linguist

%description
Deepin Polkit Agent

%prep
%setup -q -n %{repo}-%{version}
sed -i 's|lrelease|lrelease-qt5|' translate_generation.sh
sed -i 's|lib|libexec|' dde-polkit-agent.pro polkit-dde-authentication-agent-1.desktop

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%doc README.md
%license LICENSE
%{_sysconfdir}/xdg/autostart/*.desktop
%{_libexecdir}/polkit-1-dde/%{repo}
%{_datadir}/%{repo}/

%changelog
* Mon Aug 21 2017 mosquito <sensor.wen@gmail.com> - 0.1.0-1
- Update to 0.1.0

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 0.0.10-1.git680c12f
- Update to 0.0.10

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 0.0.8-1.git7e0fcbc
- Initial package build
