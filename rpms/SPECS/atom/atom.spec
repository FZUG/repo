# https://copr.fedoraproject.org/coprs/helber/atom
%{?nodejs_find_provides_and_requires}
%global debug_package %{nil}
%global _hardened_build 1
%global __requires_exclude (libnode)
%global npm_ver 2.7.6
%global project atom
%global repo %{project}

# commit
%global _commit 2cf2ccbc0410ee11ac7f76494c2733e638432681
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    atom
Version: 1.4.1
Release: 2.git%{_shortcommit}%{?dist}
Summary: A hackable text editor for the 21st century

Group:   Applications/Editors
License: MIT
URL:     https://atom.io/
Source0: https://github.com/atom/atom/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

%if 0%{?fedora} >= 19 || 0%{?rhel} >= 7
ExclusiveArch: %{nodejs_arches} noarch
%else
ExclusiveArch: %{ix86} x86_64 %{arm} noarch
%endif

BuildRequires: npm
BuildRequires: node-gyp
BuildRequires: nodejs-packaging
BuildRequires: libgnome-keyring-devel
BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: git-core
Requires:      nodejs
Requires:      http-parser

%description
Atom is a text editor that's modern, approachable, yet hackable to the core
- a tool you can customize to do anything but also use productively without
ever touching a config file.

Visit https://atom.io to learn more.

%prep
%setup -q -n %repo-%{_commit}

%build
# Hardened package
export CFLAGS="%{optflags} -fPIC -pie"
export CXXFLAGS="%{optflags} -fPIC -pie"
## Upgrade npm
# Install new npm to INSTALL_PREFIX for build package
npm config set registry="http://registry.npmjs.org/"
npm config set ca ""
npm config set strict-ssl false
npm install -g --ca=null --prefix %{buildroot}%{_prefix} npm@%{npm_ver}
# Export PATH to new npm version
export PATH="%{buildroot}%{_bindir}:$PATH"
script/build 2>&1
npm config delete ca

%install
script/grunt install --install-dir "%{buildroot}%{_prefix}"
%{__sed} -i -e 's|=.*atom|=atom|g' -e 's|atom.png|atom|g' \
    %{buildroot}%{_datadir}/applications/atom.desktop

# copy over icons in sizes that most desktop environments like
for i in 1024 512 256 128 64 48 32 24 16; do
    install -D -m 0644 /tmp/atom-build/icons/${i}.png \
      %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc README.md docs/
%license LICENSE.md
%{_bindir}/atom
%{_bindir}/apm
%dir %{_datadir}/atom
%{_datadir}/atom/*
%{_datadir}/applications/atom.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%exclude %{_datadir}/%{name}/libgcrypt.so.*
%exclude %{_datadir}/%{name}/libnotify.so.*

%changelog
* Wed Jan 27 2016 mosquito <sensor.wen@gmail.com> - 1.4.1-2.git2cf2ccb
- Fix https://github.com/FZUG/repo/issues/64
* Tue Jan 26 2016 mosquito <sensor.wen@gmail.com> - 1.4.1-1.git2cf2ccb
- Release 1.4.1
* Sun Jan 17 2016 mosquito <sensor.wen@gmail.com> - 1.4.0-1.gite0dbf94
- Release 1.4.0
* Sun Dec 20 2015 mosquito <sensor.wen@gmail.com> - 1.3.2-1.git473e885
- Release 1.3.2
* Sat Dec 12 2015 mosquito <sensor.wen@gmail.com> - 1.3.1-1.git3937312
- Release 1.3.1
* Thu Nov 26 2015 mosquito <sensor.wen@gmail.com> - 1.2.4-1.git05ef4c0
- Release 1.2.4
* Sat Nov 21 2015 mosquito <sensor.wen@gmail.com> - 1.2.3-1.gitfb5b1ba
- Release 1.2.3
* Sat Nov 14 2015 mosquito <sensor.wen@gmail.com> - 1.2.1-1.git7e902bc
- Release 1.2.1
* Wed Nov 04 2015 mosquito <sensor.wen@gmail.com> - 1.1.0-1.git402f605
- Release 1.1.0
* Thu Sep 17 2015 Helber Maciel Guerra <helbermg@gmail.com> - 1.0.13-1
- Change lib to libnode
* Tue Sep 01 2015 Helber Maciel Guerra <helbermg@gmail.com> - 1.0.10-1
- Release 1.0.10
* Thu Aug 27 2015 Helber Maciel Guerra <helbermg@gmail.com> - 1.0.8-1
- Clean and test spec for epel, centos and fedora
- Release 1.0.8
* Tue Aug 11 2015 Helber Maciel Guerra <helbermg@gmail.com> - 1.0.6-1
- Release 1.0.6
* Thu Aug 06 2015 Helber Maciel Guerra <helbermg@gmail.com> - 1.0.5-1
- Release 1.0.5
* Wed Jul 08 2015 Helber Maciel Guerra <helbermg@gmail.com> - 1.0.1-1
- Release 1.0.1
* Thu Jun 25 2015 Helber Maciel Guerra <helbermg@gmail.com> - 1.0.0-1
- Release 1.0.0
* Wed Jun 10 2015 Helber Maciel Guerra <helbermg@gmail.com> - 0.208.0-1
- Fix atom.desktop
* Tue Jun 09 2015 Helber Maciel Guerra <helbermg@gmail.com> - 0.207.0-1
- Fix desktop icons and some rpmlint.
* Fri Oct 31 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.141.0-1
- release 0.141.0
* Thu Oct 23 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.139.0-1
- release 0.139.0
* Wed Oct 15 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.137.0-2
- release 0.137.0
* Tue Oct 07 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.136.0-1
- release 0.136.0
* Tue Sep 30 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.133.0-2
- Build OK
* Fri Aug 22 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.123.0-2
- Change package name to atom.
* Thu Aug 21 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.123.0-1
- RPM package is just working.
* Sat Jul 26 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.119.0-1
- Try without nodejs.
* Tue Jul 01 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.106.0-1
- Try new version
* Sun May 25 2014 Helber Maciel Guerra <helbermg@gmail.com> - 0.99.0
- Initial package
