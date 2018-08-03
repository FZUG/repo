%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         linuxdeepin
%global   repo            go-dbus-factory
# https://github.com/linuxdeepin/go-dbus-factory
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          6184b97809e25755a9931b344ca47c63555117a6
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.2.git%{shortcommit}%{?dist}
Summary:        GO DBus factory for Deepin Desktop Environment
License:        GPLv3
URL:            https://%{provider_prefix}
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}.

%package devel
Summary:        %{summary}
BuildArch:      noarch
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.api.cursorhelper) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.api.device) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.api.localehelper) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.api.pinyin) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.api.xeventmonitor) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.accounts) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.apps) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.audio) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.daemon) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.display) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.gesture) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.greeter) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.helper.backlight) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.inputdevices) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.network) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.sessionwatcher) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.daemon.timedated) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.dde.daemon.dock) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.dde.daemon.launcher) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.dde.launcher) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.lastore) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.sessionmanager) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.system.power) = %{version}-%{release}
Provides:       golang(%{import_path}/com.deepin.wm) = %{version}-%{release}
Provides:       golang(%{import_path}/net.hadess.sensorproxy) = %{version}-%{release}
Provides:       golang(%{import_path}/net.reactivated.fprint) = %{version}-%{release}
Provides:       golang(%{import_path}/object_manager) = %{version}-%{release}
Provides:       golang(%{import_path}/org.ayatana.bamf) = %{version}-%{release}
Provides:       golang(%{import_path}/org.bluez) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.colormanager) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.dbus) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.login1) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.miracle.wfd) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.miracle.wifi) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.modemmanager1) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.networkmanager) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.notifications) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.policykit1) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.screensaver) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.secrets) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.timedate1) = %{version}-%{release}
Provides:       golang(%{import_path}/org.freedesktop.udisks2) = %{version}-%{release}
Provides:       golang(%{import_path}/org.mpris.mediaplayer2) = %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
install -d %{buildroot}%{gopath}/src/%{import_path}/
cp -a com.* org.* net.* object_manager %{buildroot}%{gopath}/src/%{import_path}/

%files devel
%doc README.md
%{gopath}/src/%{import_path}/

%changelog
* Thu Aug  2 2018 mosquito <sensor.wen@gmail.com> - 0-0.2.git6184b97
- Update to 6184b97

* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 0-0.1.git67aca0b
- Initial package build
