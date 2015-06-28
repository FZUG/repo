%global debug_package %{nil}
%global project PointDownload
%global repo %{project}

# commit
%global _commit cd07f1db20a7e930303a54a8d76eaf1f5a34d552
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		pointdownload
Version:	1.2.0
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Efficient download tool
Summary(zh_CN):	一款美观高效的下载工具

Group:		Applications/Internet
License:	GPLv3
URL:		https://github.com/PointTeam/PointDownload
Source0:	https://github.com/PointTeam/PointDownload/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	zip
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qtbase-gui
BuildRequires:	qt5-qtmultimedia-devel
BuildRequires:	qt5-qtwebkit-devel
BuildRequires:	qt5-qtdeclarative-devel
Requires:	qt5-qtbase >= 5.2.1
Requires:	qt5-qtbase-gui
Requires:	qt5-qtdeclarative >= 5.2.1
Requires:	qt5-qtmultimedia
Requires:	qt5-qtwebkit
Requires:	qt5-qtgraphicaleffects
Requires:	qt5-qtquickcontrols
Requires:	libappindicator
Requires:	glibc(x86-32)
Requires:	zlib(x86-32)
Requires(post):	libcap
Requires(post):	xdg-utils
Conflicts:  xware-desktop

%description
Efficient and easy to use to download for HTTP, HTTPs, FTP,
P2P (BT, Magnet, ed2k, Thunder etc.) download.

%description -l zh_CN
点载 - 一款美观易用的下载工具, 支持下载 HTTP, HTTPs, FTP,
P2P (BT, Magnet, ed2k, Thunder) 等协议的链接.

%prep
%setup -q -n %repo-%{_commit}

%build
# change PointPopup and PointDownload and XwareStartUp path
sed -i 's|/opt/Point/PopupWindow/PointPopup|%{_datadir}/%{name}/pointpopup|g' \
  PointDownload/Download/unifiedinterface.h \
  PointChromeExtension/pointdownload.json \
  PointFirefoxExtension.xpi/chrome/content/saveas.js \
  PointFirefoxExtension.xpi/chrome/content/main.js
sed -i 's|/opt/Point/PointDownload/PointDownload|%{_bindir}/%{name}|g' \
  PointPopup/control/datacontroler.h
sed -i 's|/opt/Point/PointDownload/point.png|%{_datadir}/icons/point.png|g' \
  PointDownload/Controler/topcontrl.cpp
sed -i 's|/opt/Point/Extensions/PointChromeExtension.crx|%{_datadir}/%{name}/extensions/PointChromeExtension.crx|g' \
  PointChromeExtension/nkbchchceepbameamioagcjlhnghdoff.json
sed -i 's|/opt/Point/PointDownload/XwareStartUp|%{_datadir}/%{name}/xwarestartup|g' \
  PointDownload/Download/XwareTask/XwareConstants.h

mkdir build
pushd build
%{_qt5_qmake} ../%{name}.pro
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

# DESTDIR is error, please see Makefile
#pushd build
#make install INSTALL_ROOT=@{buildroot}
#popd

# main files
install -d %{buildroot}%{_datadir}/%{name}/{qml,extensions}
cp -rf PointDownload/qml/PointDownload/* %{buildroot}%{_datadir}/%{name}/qml/
install -Dm 0755 build/*Download/PointDownload %{buildroot}%{_bindir}/%{name}
install -Dm 0755 build/*Popup/PointPopup %{buildroot}%{_datadir}/%{name}/pointpopup
install -Dm 0755 build/Xware*/XwareStartUp %{buildroot}%{_datadir}/%{name}/xwarestartup

# package extensions
rm -rf PointFirefoxExtension.xpi/*.xpi
pushd PointFirefoxExtension.xpi
zip -r PointFirefoxExtension.xpi ./
popd
#zip -j PointChromeExtension.crx PointChromeExtension/Extension/*
install -m 0644 PointChromeExtension/*.crx %{buildroot}%{_datadir}/%{name}/extensions/
install -m 0644 PointChromeExtension/*.json %{buildroot}%{_datadir}/%{name}/extensions/
install -m 0644 PointFirefoxExtension.xpi/*.xpi %{buildroot}%{_datadir}/%{name}/extensions/

# desktop files
install -d %{buildroot}%{_datadir}/{icons,applications}
install -m 0644 point.png %{buildroot}%{_datadir}/icons/

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Name=Point
Name[zh_CN]=点载
GenericName=Download client
Comment=Point
Exec=%{name}
Icon=point
Categories=Network;FileTransfer;P2P;Qt;
MimeType=application/x-bittorrent;x-scheme-handler/magnet;
Terminal=false
EOF

cat > %{buildroot}%{_datadir}/applications/pointpopup.desktop << EOF
[Desktop Entry]
Type=Application
Name=Point
Name[zh_CN]=点载
GenericName=Download client
Comment=Point
Exec=%{_datadir}/%{name}/pointpopup %U
Icon=point
Categories=Network;FileTransfer;P2P;Qt;
MimeType=application/x-bittorrent;x-scheme-handler/magnet;
Terminal=false
NoDisplay=true
EOF

# doc files
cp PointDownload/README* PointDownload-README.md
cp PointChromeExtension/README* PointChromeExtension-README.md
cp XwareMask/README* XwareMask-README.md

%pre
# $1 -eq 1: pre_install
# $1 -eq 2: pre_upgrade

pkill Embed
pkill point

%preun
# $1 -eq 0: preun_uninstall
# $1 -eq 1: preun_upgrade

pkill Embed
pkill point

%post
# $1 -eq 1: post_install
# $1 -eq 2: post_upgrade

if [ 0$1 -eq 1 ]; then
    USER=$(cat /etc/passwd|awk -F: '($3>=1000)&&($1!="nfsnobody"){print $1}')

    echo "============================================================"
    echo -e "欢迎使用 PointDownload\n"
    setcap CAP_SYS_ADMIN=+ep %{_datadir}/%{name}/xwarestartup

    echo " - 正在配置Chrome浏览器扩展..."
    mkdir -p /etc/opt/chrome/native-messaging-hosts
    mkdir -p /opt/google/chrome/extensions
    cp %{_datadir}/%{name}/extensions/pointdownload.json /etc/opt/chrome/native-messaging-hosts/
    cp %{_datadir}/%{name}/extensions/nkbchchceepbameamioagcjlhnghdoff.json /opt/google/chrome/extensions/

    echo " - 正在配置Firefox浏览器扩展..."
    mkdir -p %{_libdir}/mozilla/extensions/\{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}/
    cp %{_datadir}/%{name}/extensions/PointFirefoxExtension.xpi %{_libdir}/mozilla/extensions/\{ec8030f7-c20a-464f-9b0e-13a3a9e97384\}/PointTeam@qq.com.xpi

    echo " - 正在更新默认程序类型..."
    for i in $USER; do
	su -c "mkdir -p /home/${i}/.local/share/applications/" "$i"
	su -c "xdg-mime default pointpopup.desktop \
    	application/x-bittorrent \
    	x-scheme-handler/ed2k \
    	x-scheme-handler/thunder \
    	x-scheme-handler/magnet" "$i"
    done
    echo -e " - PointDownload安装完成。\n"
    echo "项目主页 https://github.com/PointTeam/PointDownload/wiki"
    echo "============================================================"
fi

if [ 0$1 -eq 2 ]; then
    setcap CAP_SYS_ADMIN=+ep %{_datadir}/%{name}/xwarestartup
    exit 0
fi

%postun
# $1 -eq 0: postun_uninstall
# $1 -eq 1: postun_upgrade

if [ 0$1 -eq 0 ]; then
    USER=$(cat /etc/passwd|awk -F: '($3>=1000)&&($1!="nfsnobody"){print $1}')

    echo "============================================================"
    echo -e "卸载 PointDownload\n"
    echo " - 正在删除Chrome扩展配置文件..."
    rm -rf /etc/opt/chrome/native-messaging-hosts/pointdownload.json
    rm -rf /opt/google/chrome/extensions/nkbchchceepbameamioagcjlhnghdoff.json
    echo " - 正在删除Firefox配置文件..."
    rm -rf %{_libdir}/mozilla/extensions/{ec8030f7-c20a-464f-9b0e-13a3a9e97384}/PointTeam@qq.com.xpi
    echo " - 正在删除默认程序类型..."
    for i in $USER; do
	sed -i '/^.*pointpopup.desktop$/d' \
	"/home/${i}/.local/share/applications/mimeapps.list"
    done
    echo -e " - PointDownload卸载完成。\n"
    echo "用户配置文件、下载列表文件以及下载组件执行文件位于~/.PointConfig，请手动删除。"
    echo "============================================================"
fi

%files
%defattr(-,root,root,-)
%doc COPYING README.md PointDownload-README.md
%doc PointChromeExtension-README.md XwareMask-README.md
%{_bindir}/%{name}
%{_datadir}/applications/point*.desktop
%{_datadir}/icons/point.png
%{_datadir}/%{name}/pointpopup
%{_datadir}/%{name}/xwarestartup
%{_datadir}/%{name}/extensions
%{_datadir}/%{name}/qml

%changelog
* Sat May 09 2015 mosquito <sensor.wen@gmail.com> - 1.2.0-1
- Rename version name
* Wed Jan 07 2015 mosquito <sensor.wen@gmail.com> - 1.2.0git20150105-1
- Update version to 1.2.0git20150105
* Fri Dec 05 2014 mosquito <sensor.wen@gmail.com> - 1.2.0git20141204-1
- Update version to 1.2.0git20141204
* Tue Dec 02 2014 mosquito <sensor.wen@gmail.com> - 1.2.0git20141128-1
- Update version to 1.2.0git20141128
* Mon Nov 10 2014 mosquito <sensor.wen@gmail.com> - 1.2.0git20141106-1
- Update to 1.2.0git20141106
* Thu Oct 30 2014 mosquito <sensor.wen@gmail.com> - 1.2.0git20141029-1
- Update to 1.2.0git20141029
* Sat Oct 11 2014 mosquito <sensor.wen@gmail.com> - 1.2.0git20141002-1
- Update to 1.2.0git20141002
* Sat Sep 27 2014 mosquito <sensor.wen@gmail.com> - 1.2.0git20140922-2
- Change package name
* Thu Sep 25 2014 mosquito <sensor.wen@gmail.com> - 1.2.0git20140922-1
- Initial build
  * Initial Release 1.2.0
  * This version has a lot of great change
  * Make UI more easier to use
  * Add Xware(Thunder) support
