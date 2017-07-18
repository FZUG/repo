%global commit 94a22cfe461a1d2d52ff69ababe14c649347260d
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-desktop-base
Version:        2016.12.6
Release:        1.git%{shortcommit}%{?dist}
Summary:        Base component for Deepin
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-desktop-base
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz
BuildArch:      noarch
Requires:       deepin-wallpapers

%description
Base component for Deepin

%prep
%setup -q -n %{name}-%{commit}

%build
%make_build

%install
%make_install PREFIX=%{_prefix}

# Remove Deepin distro's lsb-release
rm %{buildroot}/etc/lsb-release

# Don't override systemd timeouts
rm -r %{buildroot}/etc/systemd

# Make a symlink for deepin-version
ln -s /usr/lib/deepin/desktop-version %{buildroot}/etc/deepin-version

# Remove apt-specific templates
rm -r %{buildroot}%{_datadir}/python-apt

%files
%{_sysconfdir}/appstore.json
%{_sysconfdir}/deepin-version
%{_usr}/lib/deepin/desktop-version
%{_datadir}/backgrounds/deepin/desktop.jpg
%{_datadir}/distro-info/deepin.csv
%{_datadir}/i18n/*.json
%{_datadir}/plymouth/deepin-logo.png
%{_var}/cache/image-blur/

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 2016.12.6-1.git94a22cf
- Update to 2016.12.6
* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 2016.11.30-1.gita0f52f3
- Update to 2016.11.30
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2016.11.29-1.git477c9a7
- Update to 2016.11.29
* Fri Dec 16 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 2016.11.28-1
- Update package to version 2016.11.28
* Sat Dec 03 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 2016.02.03-1
- Update package to version 2016.02.03
* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 2016.02.02-1
- Initial package build
