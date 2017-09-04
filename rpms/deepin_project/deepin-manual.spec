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
Source1:        https://raw.github.com/linuxdeepin/%{name}/master/LICENSE

BuildArch:      noarch
BuildRequires:  npm
BuildRequires:  sassc
Requires:       deepin-qml-widgets
Requires:       python3-qt5
Requires:       pygobject2
Requires:       python3-dae

%description
Deepin User Manual.

%prep
%setup -q
cp %{S:1} .
sed -E '/daemon|bin\/nodejs/d; s|sass |sassc |; s|--unix-newlines||' \
    -i Makefile

%build
%make_build

%install
%make_install
install -d %{buildroot}%{_datadir}/dman/dman
cp -r manual %{buildroot}%{_datadir}/dman/dman

%files
%doc README.md
%license LICENSE
%{_bindir}/dman
%{_datadir}/%{name}/
%dir %{_datadir}/dman/
%{_datadir}/dman/dman/
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.6-1
- Initial package build
