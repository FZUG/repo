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
%global srcdir   idea-IC-%{buildid}
%global appfile  ideaIC-%{buildid}-no-jdk.tar.gz
%global appurl   https://download.jetbrains.com/idea/%{appfile}
%global tranfile resources_zh_CN_IntelliJIDEA_2018.3_r1.jar
%global tranurl  https://github.com/pingfangx/jetbrains-in-chinese/raw/master/IntelliJIDEA/%{tranfile}
# curl %%appurl.sha256 | awk '{print$1}'
%global sha256   51193c9d7b411b7a29a5bfd9a2ccebf4111348453f5f1d045278f5c8a808cecb
%global buildid  183.5153.8
%global pkgver   2018.3.3

Name:     intellij-idea
Version:  %{pkgver}.%{buildid}
Release:  1.net%{?dist}
Summary:  Capable and Ergonomic IDE for JVM
License:  Apache
URL:      https://www.jetbrains.com/idea
%BuildReq axel wget rsync
Requires: axel wget rsync
Requires: java-1.8.0-openjdk-devel

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
    --exclude=license

# exec
cat > %{buildroot}%{_bindir}/idea <<EOF
#!/bin/sh -l
[ -f ~/.bash_profile ] && . ~/.bash_profile
sh %{approot}/bin/idea.sh
EOF

# desktop file
install -d %{buildroot}%{_datadir}/applications
install -Dm644 bin/idea.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
GenericName=IntelliJIDEA IDE
Comment=%{summary}.
Name=IntelliJIDEA
Exec=idea
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
    --exclude=license
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/%{srcdir}
fi

%files
%license license/*
%attr(755,root,root) %{_bindir}/idea
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%ghost %{approot}

%changelog
* Tue Jan  8 2019 mosquito <sensor.wen@gmail.com> - 2018.3.3.183.4886.39-1.net
- Initial build
