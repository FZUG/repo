%global project dde-polkit-agent
%global repo %{project}

Name:           deepin-polkit-agent
Version:        0.0.10
Release:        1%{?dist}
Summary:        Deepin Polkit Agent
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-polkit-agent
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  polkit-qt5-1-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel

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
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 0.0.10-1.git680c12f
- Update to 0.0.10

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 0.0.8-1.git7e0fcbc
- Initial package build
