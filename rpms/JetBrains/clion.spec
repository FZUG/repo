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
%global srcdir   %{name}-%{pkgver}
%global appfile  CLion-%{pkgver}.tar.gz
%global appurl   https://download.jetbrains.com/cpp/%{appfile}
%global tranfile resources_zh_CN_CLion_2018.3_r1.jar
%global tranurl  https://github.com/pingfangx/jetbrains-in-chinese/raw/master/CLion/%{tranfile}
# curl %%appurl.sha256 | awk '{print$1}'
%global sha256   b42557e2b09383121a4347fc74c1f903fe08607ef0f3ceb279dd20c519e583e5
%global buildid  183.4886.39
%global pkgver   2018.3.2

Name:     clion
Version:  %{pkgver}.%{buildid}
Release:  1.net%{?dist}
Summary:  A cross-platform IDE for C and C++
License:  Apache
URL:      https://www.jetbrains.com/clion
%BuildReq gcc-c++
%BuildReq axel wget rsync
%BuildReq python3-devel
%BuildReq python3-setuptools
Requires: axel wget rsync
Requires: jre-1.8.0-openjdk
Requires: cmake
Requires: clang-tools-extra
Requires: gcc-c++
Requires: gdb
Requires: lldb
Requires: gtest
Requires: python3

%description
%{summary}.

%prep
%wget %{appfile} %{appurl}
tar -xvf %{appfile}
%setup -D -T -n %{srcdir}
%wget %{tranfile} %{tranurl}

%build
# compile PyDev debugger used by CLion to speedup debugging
python3 plugins/python/helpers/pydev/setup_cython.py build_ext --inplace
cp plugins/python/helpers/pydev/_pydevd_frame_eval/pydevd_frame*.so \
   plugins/python/helpers/pydev/_pydevd_bundle/pydevd_cython*.so help/

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
    --exclude=license \
    --exclude=bin/clang \
    --exclude=bin/cmake \
    --exclude=bin/gdb \
    --exclude=bin/lldb

# exec
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh -l
[ -f ~/.bash_profile ] && . ~/.bash_profile
sh %{approot}/bin/%{name}.sh
EOF

# desktop file
install -d %{buildroot}%{_datadir}/applications
install -Dm644 bin/%{name}.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
GenericName=C/C++ IDE
Comment=%{summary}.
Name=CLion
Exec=%{name}
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
pref="../../../../../help"
dest="plugins/python/helpers/pydev"
ln -s ${pref}/pydevd_frame_evaluator.cpython-37m-x86_64-linux-gnu.so ${dest}/_pydevd_frame_eval/
ln -s ${pref}/pydevd_cython.cpython-37m-x86_64-linux-gnu.so ${dest}/_pydevd_bundle/

# base
install -d %{tmproot}%{approot}
rsync -rtl . %{tmproot}%{approot} \
    --exclude=jre64 \
    --exclude=license \
    --exclude=bin/clang \
    --exclude=bin/cmake \
    --exclude=bin/gdb \
    --exclude=bin/lldb
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/%{srcdir}
fi

%files
%license license/*
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%dir %{approot}
%{approot}/product-info.json
%{approot}/*.txt
%{approot}/bin
%{approot}/help
%ghost %{approot}/lib
%ghost %{approot}/plugins

%changelog
* Tue Jan  8 2019 mosquito <sensor.wen@gmail.com> - 2018.3.2.183.4886.39-1.net
- Initial build
