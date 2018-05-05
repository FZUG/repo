%global __provides_exclude_from ^%{approot}/.*
%global __requires_exclude_from ^%{approot}/.*
%global debug_package %{nil}
%global __jar_repack  %{nil}
%global __os_install_post %{nil}

%global _tmppath /var/tmp
%global tmproot %{_tmppath}/%{name}-%{version}_tmproot
%global approot /opt/JetBrains/%{name}
%global appfile %{name}-%{version}.tar.gz
%global appurl  https://download.jetbrains.com/python/%{appfile}
# http://download.jetbrains.com/python/Name-Version.tar.gz.sha256
%global sha256  6557e3d9309d4c84501ddba11345b6103cfbad074c6e160c6bc7e85e73ae8e21

# Usage: DownloadPkg appfile appurl
%global DownloadPkg() \
Download() {\
    SHA=$(test -f %1 && sha256sum %1 ||:)\
    if [[ ! -f %1 || "${SHA/ */}" != "%sha256" ]]; then\
        axel -o %1 -a %2; Download\
    fi\
}\
Download\
%{nil}

Name:    pycharm-professional
Version: 2018.1.2
Release: 1.net
Summary: Powerful Python and Django IDE. Professional version
Group:   Development/Tools
License: Proprietary
URL:     http://www.jetbrains.com/pycharm

BuildRequires: axel
BuildRequires: tar
Requires: axel
Requires: tar

%description
 Powerful Python and Django IDE. Professional version.

%prep
%DownloadPkg %{appfile} %{appurl}
tar -xvf %{appfile}

%build

%install
pushd pycharm-%{version}

# delete some conflicts files for i686
%ifarch %{ix86}
FILELIST="lib/libpty/linux/x86_64 bin/libyjpagent-linux64.so bin/fsnotifier64 "
%else
FILELIST="lib/libpty/linux/x86 bin/libyjpagent-linux.so bin/fsnotifier "
%endif
FILELIST+=`echo help/*Mac.pdf lib/libpty/{macosx,win}`
rm -rf $FILELIST
find -name "*.dll" -or -name "*.dylib" | xargs rm -rf

# base
install -d %{buildroot}{%{approot},%{_bindir}}
cp -dr --no-preserve=ownership * %{buildroot}%{approot}
install -d %{buildroot}%{_datadir}/{applications,pixmaps}
install -Dm 644 %{buildroot}%{approot}/bin/pycharm.png \
                %{buildroot}%{_datadir}/pixmaps/%{name}.png

# exec
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/sh -l
[ -f ~/.bash_profile ] && . ~/.bash_profile
sh %{approot}/bin/pycharm.sh
EOF

# app desktop
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
GenericName=Python and Django IDE
Comment=Powerful Python and Django IDE. Professional version.
Name=PyCharm
Exec=/usr/bin/%{name}
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
%DownloadPkg %{appfile} %{appurl}

# Extract archive
mkdir %{tmproot} &>/dev/null ||:
tar -xf %{appfile}
cd pycharm-%{version}

# delete some conflicts files for i686
%ifarch %{ix86}
FILELIST="lib/libpty/linux/x86_64 bin/libyjpagent-linux64.so bin/fsnotifier64 "
%else
FILELIST="lib/libpty/linux/x86 bin/libyjpagent-linux.so bin/fsnotifier "
%endif
FILELIST+=`echo help/*Mac.pdf lib/libpty/{macosx,win} license`
rm -rf $FILELIST
find -name "*.dll" -or -name "*.dylib" | xargs rm -rf

# enable anti-aliasing text in pycharm options
%ifarch %{ix86}
#echo '-Dawt.useSystemAAFontSettings=on' >> bin/pycharm.vmoptions
echo '-Dswing.aatext=true' >> bin/pycharm.vmoptions
%else
#echo '-Dawt.useSystemAAFontSettings=on' >> bin/pycharm64.vmoptions
echo '-Dswing.aatext=true' >> bin/pycharm64.vmoptions
%endif

# base
install -d %{tmproot}%{approot}
cp -dr --no-preserve=ownership * %{tmproot}%{approot}
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/pycharm-%{version}
fi
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

/bin/cat << EOF

==> Please set the Anti-aliasing font settings for Java app
==> adding the following line to the users file ~/.bash_profile
==> (not in ~/.bashrc):
==>
==> export _JAVA_OPTIONS='-Dawt.useSystemAAFontSettings=setting'
==>
==> Replace 'setting' with on, lcd, gasp, etc. By default is
==> configured with lcd.
==>
==> Please read the following link for more options:
==> https://wiki.archlinux.org/index.php/Java_Runtime_Environment_Fonts

EOF

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
%license pycharm-%{version}/license/*
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%ghost %{approot}/
%exclude %{approot}/license

%changelog
* Sat May  5 2018 Hui Tang <duriantang@gmail.com> 2018.1.2-1.net
- Release 2018.1.2
* Sat Aug 06 2016 nrechn <nrechn@gmail.com> - 2016.2-1
- Release 2016.2
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 2016.1-1
- Release 2016.1
* Fri Jan 29 2016 mosquito <sensor.wen@gmail.com> - 5.0.4-1
- Release 5.0.4
* Sat Dec 26 2015 mosquito <sensor.wen@gmail.com> - 5.0.3-1
- Initial build
