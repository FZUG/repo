%global __provides_exclude_from ^%{approot}/.*
%global __requires_exclude_from ^%{approot}/.*
%global debug_package %{nil}
%global __jar_repack  %{nil}
%global __os_install_post %{nil}
%global _build_id_links none

# Usage: wget appfile appurl
%define wget() %{expand:
SHA=$(test -f %1 && sha256sum %1 ||:)
if [[ ! -f %1 || "${SHA/ */}" != "%sha256" ]]; then
    wget --unlink -O %1 %2 || axel -o %1 -a %2
fi}

%global BuildReq BuildRequires:
%global _tmppath /var/tmp
%global tmproot  %{_tmppath}/%{name}-%{version}_tmproot
%global approot  /opt/JetBrains/%{name}
%global srcdir   pycharm-%{pkgver}
%global appfile  %{name}-%{buildid}.tar.gz
%global appurl   https://download.jetbrains.com/python/%{appfile}
%global tranfile resources_zh_CN_PyCharm_2018.3_r1.jar
%global tranurl  https://github.com/pingfangx/jetbrains-in-chinese/raw/master/PyCharm/%{tranfile}
# curl %%appurl.sha256 | awk '{print$1}'
%global sha256   86ac90acbac387b0477ead89b0b132849ae446f3acbf3c4af8e2ad8923ef98c9
%global buildid  183.5153.12
%global pkgver   2018.3.3

Name:     pycharm-professional
Version:  %{pkgver}.%{buildid}
Release:  1.net%{?dist}
Summary:  Powerful Python and Django IDE. Professional version
License:  Proprietary
URL:      http://www.jetbrains.com/pycharm
%BuildReq gcc-c++
%BuildReq axel wget rsync
%BuildReq python3-devel
%BuildReq python3-setuptools
Requires: axel wget rsync
Requires: jre-1.8.0-openjdk
Requires: python3-ipython
Requires: python3-jupyter-core
Requires: python3-coverage
Requires: python3-pytest
Requires: python3-tox

%description
%{summary}.

%prep
%wget %{appfile} %{appurl}
tar -xvf %{appfile}
%setup -D -T -n %{srcdir}
%wget %{tranfile} %{tranurl}

%build
# compile PyDev debugger used by PyCharm to speedup debugging
python3 helpers/pydev/setup_cython.py build_ext --inplace
cp helpers/pydev/_pydevd_frame_eval/pydevd_frame*.so \
   helpers/pydev/_pydevd_bundle/pydevd_cython*.so help/

%install
# delete some conflicts files
find -name "*.dll" -or -name "*.dylib" -or -type f \
     -name "*win32*" -or -name "*darwin*" | xargs rm -f

# i18n
mv %{tranfile} lib/resources_zh_CN.jar

# base
install -d %{buildroot}{%{approot},%{_bindir}}
rsync -rtl . %{buildroot}%{approot} \
    --exclude=jre64 \
    --exclude=license

# exec
cat > %{buildroot}%{_bindir}/pycharm-pro <<EOF
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
Exec=pycharm-pro
Icon=%{name}
Terminal=false
Categories=Development;IDE;
StartupNotify=true
EOF

%pre
if [ $1 -ge 1 ]; then
# download
cd %{_tmppath}
%wget %{appfile} %{appurl}
tar -xf %{appfile}
cd %{srcdir}
%wget %{tranfile} %{tranurl}

# delete some conflicts files
find -name "*.dll" -or -name "*.dylib" -or -type f \
     -name "*win32*" -or -name "*darwin*" | xargs rm -f

# i18n
mv %{tranfile} lib/resources_zh_CN.jar

# link
ln -s ../../../help/pydevd_frame_evaluator.cpython-37m-x86_64-linux-gnu.so helpers/pydev/_pydevd_frame_eval/
ln -s ../../../help/pydevd_cython.cpython-37m-x86_64-linux-gnu.so helpers/pydev/_pydevd_bundle/

# base
install -d %{tmproot}%{approot}
rsync -rtl . %{tmproot}%{approot} \
    --exclude=jre64 \
    --exclude=license
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/%{srcdir}
fi

%files
%license license/*
%attr(755,root,root) %{_bindir}/pycharm-pro
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%dir %{approot}
%{approot}/product-info.json
%{approot}/*.txt
%{approot}/bin
%{approot}/help
%ghost %{approot}/debug-eggs
%ghost %{approot}/helpers
%ghost %{approot}/index
%ghost %{approot}/lib
%ghost %{approot}/plugins

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
