%global __provides_exclude_from ^%{approot}/.*
%global __requires_exclude_from ^%{approot}/.*
%global debug_package %{nil}
%global __jar_repack  %{nil}
%global __os_install_post %{nil}
%global _build_id_links none

%global _tmppath /var/tmp
%global tmproot  %{_tmppath}/%{name}-%{version}_tmproot
%global approot  /opt/JetBrains/%{name}
%global appfile  %{name}-%{buildid}.tar.gz
%global appurl   https://download.jetbrains.com/python/%{appfile}
# curl %%appurl.sha256 | awk '{print$1}'
%define sha256   316637cfeefcf239046e301ac9668a09e32c7badd3bb78bd5d971ad81f4e7613
%global buildid  183.5153.12
%global pkgver   2018.3.3

# Usage: wget appfile appurl
%global wget() %{expand:
SHA=$(test -f %1 && sha256sum %1 ||:)
if [[ ! -f %1 || "${SHA/ */}" != "%sha256" ]]; then
    wget --unlink -O %1 %2 || axel -o %1 -a %2
fi}

Name:    pycharm-community
Version: %{pkgver}.%{buildid}
Release: 1.net%{?dist}
Summary: Powerful Python and Django IDE. Community version
License: Apache
URL:     https://www.jetbrains.com/pycharm

BuildRequires: gcc-c++
BuildRequires: axel wget tar
BuildRequires: python2-devel
BuildRequires: python2-setuptools
BuildRequires: python3-devel
BuildRequires: python3-setuptools
Requires:      axel wget tar
Requires:      jre-1.8.0-openjdk
Requires:      python3-ipython
Requires:      python3-jupyter-core
Requires:      python3-coverage
Requires:      python3-pytest
Requires:      python3-tox

%description
%{summary}.

%prep
%wget %{appfile} %{appurl}
tar -xvf %{appfile}
%setup -D -T -n %{name}-%{pkgver}

%build
# compile PyDev debugger used by PyCharm to speedup debugging
python2 helpers/pydev/setup_cython.py build_ext --inplace
python3 helpers/pydev/setup_cython.py build_ext --inplace

%install
# delete some conflicts files
find -name "*.dll" -or -name "*.dylib" -or -type f \
     -name "*win32*" -or -name "*darwin*" | xargs rm -f
rm -rf jre64

# enable anti-aliasing text in pycharm options
# https://wiki.archlinux.org/index.php/Java_Runtime_Environment_Fonts
echo $'-Dawt.useSystemAAFontSettings=on\n-Dswing.aatext=true' >> bin/pycharm64.vmoptions

# base
install -d %{buildroot}{%{approot},%{_bindir}}
cp helpers/pydev/_pydevd_frame_eval/pydevd_frame*.so \
   helpers/pydev/_pydevd_bundle/pydevd_cython*.so help/
cp -dr --no-preserve=ownership * %{buildroot}%{approot}

# exec
cat > %{buildroot}%{_bindir}/pycharm-eap <<EOF
#!/bin/sh -l
[ -f ~/.bash_profile ] && . ~/.bash_profile
sh %{approot}/bin/pycharm.sh
EOF

# desktop file
install -d %{buildroot}%{_datadir}/applications
install -Dm644 bin/pycharm.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
GenericName=Python and Django IDE
Comment=%{summary}.
Name=PyCharm
Exec=pycharm-eap
Icon=%{name}
Terminal=false
Categories=Development;IDE;
StartupNotify=true
StartupWMClass=jetbrains-pycharm
EOF

%pre
if [ $1 -ge 1 ]; then
# Download pycharm
cd %{_tmppath}
%wget %{appfile} %{appurl}
tar -xf %{appfile}
cd %{name}-%{pkgver}

# delete some conflicts files
find -name "*.dll" -or -name "*.dylib" -or -type f \
     -name "*win32*" -or -name "*darwin*" | xargs rm -f
rm -rf jre64 license

# base
install -d %{tmproot}%{approot}
ln -s ../../../help/pydevd_frame_evaluator.cpython-37m-x86_64-linux-gnu.so helpers/pydev/_pydevd_frame_eval/
ln -s ../../../help/pydevd_cython.cpython-37m-x86_64-linux-gnu.so helpers/pydev/_pydevd_bundle/
cp -dr --no-preserve=ownership * %{tmproot}%{approot}
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/%{name}-%{pkgver}
fi

%files
%license license/*
%attr(755,root,root) %{_bindir}/pycharm-eap
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%dir %{approot}
%{approot}/product-info.json
%{approot}/*.txt
%{approot}/bin
%{approot}/help
%ghost %{approot}/helpers
%ghost %{approot}/index
%ghost %{approot}/lib
%ghost %{approot}/plugins
%exclude %{approot}/license

%changelog
* Tue Jan  8 2019 mosquito <sensor.wen@gmail.com> - 2018.3.3.183.5153.12-1.net
- Release 2018.3.3.183.5153.12

* Tue May 22 2018 Hui Tang <duriantang@gmail.com> 2018.1.3-1.net
- Release 2018.1.3
- Workaround .build-id conflicts.

* Sat May  5 2018 Hui Tang <duriantang@gmail.com> 2018.1.2-1.net
- Release 2018.1.2
- Use Bundled JRE

* Sat Aug 06 2016 nrechn <nrechn@gmail.com> - 2016.2-1
- Release 2016.2

* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 2016.1-1
- Release 2016.1

* Fri Jan 29 2016 mosquito <sensor.wen@gmail.com> - 5.0.4-1
- Release 5.0.4

* Sat Dec 26 2015 mosquito <sensor.wen@gmail.com> - 5.0.3-1
- Initial build
