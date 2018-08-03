Name:           deepin-calculator
Version:        1.0.5
Release:        1%{?dist}
Summary:        An easy to use calculator for ordinary users
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-calculator
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(Qt5Core)
BuildRequires:  pkgconfig(Qt5Gui)
BuildRequires:  pkgconfig(Qt5Widgets)
BuildRequires:  pkgconfig(Qt5Svg)
BuildRequires:  pkgconfig(dtkwidget) >= 2.0
BuildRequires:  desktop-file-utils
Requires:       hicolor-icon-theme

%description
%{summary}.

%prep
%setup -q
sed -i 's|lrelease|lrelease-qt5|' translations/translate_generation.sh
sed -i 's|59 Temple Place, Suite 330|51 Franklin Street, Fifth Floor|;
        s|Boston, MA 02111-1307 USA.|Boston, MA 02110-1335, USA.|' math/*.{c,h}

%build
%qmake_qt5 PREFIX=%{_prefix}
%make_build

%install
%make_install INSTALL_ROOT=%{buildroot}

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop ||:

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%changelog
* Thu Aug  2 2018 mosquito <sensor.wen@gmail.com> - 1.0.5-1
- Update to 1.0.5

* Mon Jul 23 2018 mosquito <sensor.wen@gmail.com> - 1.0.4-1
- Update to 1.0.4

* Tue Mar 20 2018 mosquito <sensor.wen@gmail.com> - 1.0.2-1
- Update to 1.0.2

* Sat Dec  9 2017 mosquito <sensor.wen@gmail.com> - 1.0.1-1
- Update to 1.0.1

* Sat Dec  2 2017 mosquito <sensor.wen@gmail.com> - 1.0.0-1
- Update to 1.0.0

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 0.9.0-1
- Initial package build
