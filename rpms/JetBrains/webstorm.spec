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
%global srcdir   WebStorm-%{buildid}
%global appfile  WebStorm-%{buildid}.tar.gz
%global appurl   https://download.jetbrains.com/webstorm/%{appfile}
%global tranfile resources_zh_CN_WebStorm_2018.3_r1.jar
%global tranurl  https://github.com/pingfangx/jetbrains-in-chinese/raw/master/WebStorm/%{tranfile}
# curl %%appurl.sha256 | awk '{print$1}'
%global sha256   8cbd95c813fd898b0bd9fe064adb4652c5cb2f9c5af5ddcebd2805179be35cd9
%global buildid  183.5153.15
%global pkgver   2018.3.3

Name:     webstorm
Version:  %{pkgver}.%{buildid}
Release:  1.net%{?dist}
Summary:  The smartest JavaScript IDE
License:  Apache
URL:      https://www.jetbrains.com/webstorm
%BuildReq axel wget rsync
Requires: axel wget rsync
Requires: jre-1.8.0-openjdk
Requires: nodejs

%description
%{summary}.

%prep
%wget %{appfile} %{appurl}
tar -xvf %{appfile}
%setup -D -T -n %{srcdir}
%wget %{tranfile} %{tranurl}

%install
# i18n
mv %{tranfile} lib/resources_zh_CN.jar

# base
install -d %{buildroot}{%{approot},%{_bindir}}
rsync -rtl . %{buildroot}%{approot} \
    --exclude=jre64 \
    --exclude=license

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
GenericName=JavaScript IDE
Comment=%{summary}.
Name=WebStorm
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

# i18n
mv %{tranfile} lib/resources_zh_CN.jar

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
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%ghost %{approot}

%changelog
* Tue Jan  8 2019 mosquito <sensor.wen@gmail.com> - 2018.3.3.183.5153.15-1.net
- Initial build
