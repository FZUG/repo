# Set correct python version
%global __python %{__python3}
%global debug_package %{nil}

Name:           deepin-manual
Version:        1.0.6
Release:        1%{?dist}
Summary:        Deepin User Manual
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-manual
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  npm sassc
Requires:       deepin-qml-widgets
Requires:       python3-qt5
Requires:       pygobject2
Requires:       python3-dae
#Requires:       python3-jieba

%description
Deepin User Manual

%prep
%setup -q

sed -e 's|ln -sf /usr/bin/nodejs ./symdir/node||' \
    -e 's|sass |sassc |' \
    -e 's|--unix-newlines||' \
    -i Makefile

%build
%make_build

%install
%make_install

cp -r manual %{buildroot}%{_datadir}/dman/dman
rm -r %{buildroot}%{_datadir}/dman/dman-daemon/
rm %{buildroot}/etc/xdg/autostart/dman-daemon.desktop
rmdir %{buildroot}/etc{/xdg/autostart,/xdg,}

%files
%doc README.md
%license LICENSE
%{_bindir}/dman
%{_datadir}/%{name}/
%{_datadir}/dman/dman/
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.6-1.git3ae465e
- Update to 1.0.6

* Wed Dec 21 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.5-1
- Initial package build
