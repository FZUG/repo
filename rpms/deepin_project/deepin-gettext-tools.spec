%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global debug_package %{nil}
%global __requires_exclude ^perl

%global _commit 4303c4a4f2b4eed0744d16576fb2c0d09f54aa88
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-gettext-tools
Version:        1.0.4
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin Gettext Tools

License:        GPLv3
URL:            https://github.com/linuxdeepin/%{name}
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

BuildRequires:  python-devel
Requires:       python
Requires:       gettext

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

%files
%{_bindir}/deepin-*
%{_prefix}/lib/%{name}/*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 1.0.4-1.git4303c4a
- Rebuild
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.4-1
- Update to version 1.0.4
* Wed Oct 12 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 1.0.3-1
- Initial package build
