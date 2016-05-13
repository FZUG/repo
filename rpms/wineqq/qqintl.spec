%global debug_package %{nil}
%global _tmppath /var/tmp
%global tmproot %{_tmppath}/%{name}-%{version}_tmproot
%global appfile %{name}_%{version}-2_i386.deb
%global appurl  http://packages.deepin.com/deepin/pool/non-free/d/deepin%{name}/%{appfile}
%global sha1sum c51fb6d5cbb02513319ee478f7b6f0403839b83f

# Usage: DownloadPkg appfile appurl
%global DownloadPkg() \
Download() {\
    SHA=$(test -f %1 && sha1sum %1 ||:)\
    if [[ ! -f %1 || "${SHA/ */}" != "%sha1sum" ]]; then\
        axel -o %1 -a %2; Download\
    fi\
}\
Download\
%{nil}

Name:    wine-qqintl
Version: 0.1.3
Release: 2.net
Summary: Tencent QQ International Edition
Summary(zh_CN): 腾讯 QQ 国际版
Group:   Applications/Communications
License: Proprietary
URL:     http://www.qq.com

BuildRequires: axel dpkg tar
Requires: axel dpkg tar
%ifarch %{ix86}
Requires: wine-core alsa-lib gtk2 lcms2 libpng12
Requires: libSM ncurses-libs cpus-libs pulseaudio-libs
Requires: libmpg123 alsa-plugins-pulseaudio
%else
Requires: wine-core(x86-32)
Requires: alsa-lib(x86-32)
Requires: gtk2(x86-32)
Requires: lcms2(x86-32)
Requires: libpng12(x86-32)
Requires: libSM(x86-32)
Requires: ncurses-libs(x86-32)
Requires: cups-libs(x86-32)
Requires: pulseaudio-libs(x86-32)
Requires: libmpg123(x86-32)
Requires: alsa-plugins-pulseaudio(x86-32)
%endif
Requires: wqy-microhei-fonts

%description
 QQ is an abbreviation of Tencent QQ, a popular instant messaging software
 service developed by Tencent Holdings Limited. QQ also offers a variety of
 services, including online social games, music, shopping, microblogging,
 and group and voice chat.

%description -l zh_CN
 QQ 即 Tencent QQ, 是腾讯有限公司开发的即时通讯软件的缩写. QQ 还提供各种服务,
 包括在线社交游戏, 音乐, 购物, 微博, 以及群组和语音聊天.

%prep
# Download qqintl
%DownloadPkg %{appfile} %{appurl}

# Extract archive
dpkg-deb -X %{appfile} .

%build

%install
# Remove some files
rm -rf usr/share/deepinwine/qqintl/wine usr/share/doc

# Main
install -d %{buildroot}%{_datadir}
cp -r usr/share/{deepinwine,applications,icons} %{buildroot}%{_datadir}/

# Link files
install -d %{buildroot}%{_bindir}
ln -sfv %{_datadir}/deepinwine/qqintl/%{name} %{buildroot}%{_bindir}/%{name}

%pre
if [ $1 -ge 1 ]; then
# Download qqintl
cd %{_tmppath}
%DownloadPkg %{appfile} %{appurl}

# Extract archive
mkdir %{tmproot} &>/dev/null ||:
dpkg-deb -x %{appfile} .

# Remove some files
rm -rf usr/share/deepinwine/qqintl/wine usr/share/doc

# Main
install -d %{tmproot}%{_datadir}
cp -r usr/share/deepinwine %{tmproot}%{_datadir}/
sed -i '/WINEDIR=/s|=.*|=/usr|' %{tmproot}%{_datadir}/deepinwine/qqintl/%{name}
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/usr/* /usr; rm -rf %{tmproot} %{_tmppath}/usr
fi
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
%{_bindir}/%{name}
%ghost %{_datadir}/deepinwine/qqintl
%{_datadir}/applications/qqintl.desktop
%{_datadir}/icons/hicolor/*/apps/qqintl.png

%changelog
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 0.1.3-2
- Change tmp directory
* Mon Dec 21 2015 mosquito <sensor.wen@gmail.com> - 0.1.3-1
- Initial build
