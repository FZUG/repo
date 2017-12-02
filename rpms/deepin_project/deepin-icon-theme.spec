Name:           deepin-icon-theme
Version:        15.12.52
Release:        1%{?dist}
Summary:        Icons for the Deepin Desktop Environment
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-icon-theme
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python-devel

%description
Icons for the Deepin Desktop Environment.

%prep
%setup -q

%build

%install
%make_install PREFIX=%{_prefix}

%post
touch --no-create %{_datadir}/icons/deepin &>/dev/null || :
touch --no-create %{_datadir}/icons/Sea &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/deepin &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/deepin &>/dev/null || :
  touch --no-create %{_datadir}/icons/Sea &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/Sea &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/deepin &>/dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/Sea &>/dev/null || :

%files
%license LICENSE
%{_datadir}/icons/deepin/
%{_datadir}/icons/Sea/

%changelog
* Sat Dec  2 2017 mosquito <sensor.wen@gmail.com> - 15.12.52-1
- Update to 15.12.52

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 15.12.49-1
- Update to 15.12.49

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 15.12.46-1
- Update to 15.12.46

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 15.12.42-1.git59ca728
- Update to 15.12.42

* Tue Mar  7 2017 mosquito <sensor.wen@gmail.com> - 15.12.33-1.git2f50a33
- Update to 15.12.33

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 15.12.32-1.git69bcc88
- Update to 15.12.32

* Sun Sep 18 2016 Jaroslav <cz.guardian@gmail.com> Stepanek
- Initial package build
