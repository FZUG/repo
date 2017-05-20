%global project dde-polkit-agent
%global repo %{project}

%global _commit 7e0fcbc9a4109069ed30a6efadc722a177a513e5
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-polkit-agent
Version:        0.0.8
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Polkit Agent
License:        GPLv3
URL:            https://github.com/linuxdeepin/dde-polkit-agent
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  deepin-tool-kit-devel
BuildRequires:  polkit-qt5-1-devel
BuildRequires:  qt5-linguist
BuildRequires:  qt5-qtbase-devel
Provides:       %{repo}%{?_isa} = %{version}-%{release}

%description
Deepin Polkit Agent

%prep
%setup -q -n %{repo}-%{_commit}
sed -i 's|lrelease|lrelease-qt5|' translate_generation.sh
sed -i 's|lib|libexec|' dde-polkit-agent.pro polkit-dde-authentication-agent-1.desktop

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%files
%{_sysconfdir}/xdg/autostart/*.desktop
%{_libexecdir}/polkit-1-dde/%{repo}
%{_datadir}/%{repo}/

%changelog
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 0.0.8-1.git7e0fcbc
- Initial package build
