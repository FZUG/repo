%global commit 8f4a8ab0a3d94765cce0c4af2aa809bfa48ad9c4
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-gettext-tools
Version:        1.0.6
Release:        1%{?dist}
Summary:        Deepin Gettext Tools
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-gettext-tools
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  perl(Config::Tiny)
BuildRequires:  perl(Exporter::Tiny)
BuildRequires:  perl(XML::LibXML)
BuildRequires:  perl(XML::LibXML::PrettyPrint)
Requires:       gettext
Requires:       qt5-linguist
Requires:       perl(Config::Tiny)
Requires:       perl(Exporter::Tiny)
Requires:       perl(XML::LibXML)
Requires:       perl(XML::LibXML::PrettyPrint)

%description
The tools of gettext function wrapper.

desktop-ts-convert - handling desktop file translations.
policy-ts-convert - convert PolicyKit Policy file to the ts file.
update-pot - scan msgid and generate pot file according to the ini file.
generate-mo - scan po files and generate mo files according to the ini file.

%prep
%setup -q -n %{name}-%{commit}

# fix shebang
find -iname "*.py" | xargs sed -i '1s|.*|#!%{__python3}|'
sed -i '1s|.*|#!%{__perl}|' desktop_ts/src/desktop_ts_convert.pl

sed -i 's|sudo cp|cp|' src/generate_mo.py
sed -i 's|lconvert|lconvert-qt5|; s|deepin-lupdate|lupdate-qt5|' src/update_pot.py

%build

%install
install -d %{buildroot}%{_bindir}
install -m755 desktop_ts/src/desktop_ts_convert.pl %{buildroot}%{_bindir}/deepin-desktop-ts-convert
install -m755 policy_ts/src/policy_ts_convert.py %{buildroot}%{_bindir}/deepin-policy-ts-convert
install -m755 src/generate_mo.py %{buildroot}%{_bindir}/deepin-generate-mo
install -m755 src/update_pot.py %{buildroot}%{_bindir}/deepin-update-pot

%check
/bin/perl desktop_ts/src/desktop_ts_convert.pl --help
/bin/python3 src/generate_mo.py --help
/bin/python3 src/update_pot.py --help

%files
%doc README.md
%license LICENSE
%{_bindir}/deepin-desktop-ts-convert
%{_bindir}/deepin-policy-ts-convert
%{_bindir}/deepin-update-pot
%{_bindir}/deepin-generate-mo

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.0.6-1.git8f4a8ab
- Update to 1.0.6
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.4-1.git4303c4a
- Rebuild
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.4-1
- Update to version 1.0.4
* Wed Oct 12 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.3-1
- Initial package build
