%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%global _commit 8f4a8ab0a3d94765cce0c4af2aa809bfa48ad9c4
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-gettext-tools
Version:        1.0.6
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Gettext Tools
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-gettext-tools
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python-devel
BuildRequires:  perl(Config::Tiny)
BuildRequires:  perl(Exporter::Tiny)
BuildRequires:  perl(XML::LibXML)
BuildRequires:  perl(XML::LibXML::PrettyPrint)
Requires:       python
Requires:       gettext
Requires:       perl(Config::Tiny)
Requires:       perl(Exporter::Tiny)
Requires:       perl(XML::LibXML)
Requires:       perl(XML::LibXML::PrettyPrint)

%description
Deepin Gettext Tools

%prep
%setup -q -n %{name}-%{_commit}

# fix python version
find -iname "*.py" | xargs sed -i '1s|python$|python2|'
sed -i 's|sudo cp|cp|' src/generate_mo.py

%build

%install
%make_install

%check
/bin/perl desktop_ts/src/desktop_ts_convert.pl --help
/bin/python2 src/generate_mo.py --help
/bin/python2 src/update_pot.py --help

%files
%{_bindir}/deepin-*
%{_prefix}/lib/%{name}/*

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.0.6-1.git8f4a8ab
- Update to 1.0.6
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.4-1.git4303c4a
- Rebuild
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.4-1
- Update to version 1.0.4
* Wed Oct 12 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.3-1
- Initial package build
