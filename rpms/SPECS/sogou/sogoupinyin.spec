%global debug_package %{nil}
%define _xinitrcdir %{_sysconfdir}/X11/xinit/xinitrc.d

Name:		sogoupinyin
Version:	1.2.0.0056
Release:	2%{?dist}
Summary:	Sogou Pinyin input method
Summary(zh_CN):	搜狗拼音输入法

License:	Proprietary and GPLv2
URL:		http://pinyin.sogou.com/linux
Group:		Applications/System
Source0:	http://download.ime.sogou.com/1432523940/%{name}_%{version}_amd64.deb
Source1:	http://download.ime.sogou.com/1432524151/%{name}_%{version}_i386.deb

BuildRequires:	dpkg
Requires:	fcitx >= 4.2.8.3
Requires:	fcitx-configtool
Conflicts:	fcitx-sogoupinyin
Obsoletes:	sogou-pinyin < %{version}-%{release}

%description
Sogou Pinyin Input Method

Based on web search engine technology, Sogou Pinyin input method is
the next-generation input method designed for Internet users. As it
is backed with search engine technology, user input method can be
extremely fast, and it is much more advanced than other input method
engines in terms of the volume of the vocabulary database and its
accuracy. Sogou input method is the most popular input methods in
China, and Sogou promises it will always be free of charge.

%description -l zh_CN
搜狗拼音输入法 - 专注输入法 20 年
支持全拼简拼, 模糊拼音, 细胞词库, 云输入, 皮肤, 中英混输.
通过结合搜索引擎技术, 提高输入准确率. 更多惊喜等您体验.


%prep
# Extract DEB package
%ifarch x86_64
dpkg-deb -X %{SOURCE0} %{_builddir}/%{name}-%{version}
%else
dpkg-deb -X %{SOURCE1} %{_builddir}/%{name}-%{version}
%endif

%build

%install
pushd %{_builddir}/%{name}-%{version}

# 55-sogoupinyin.sh script
install -d %{buildroot}%{_xinitrcdir}
cat > %{buildroot}%{_xinitrcdir}/55-%{name}.sh <<EOF
#!/bin/sh
set -e

[ -x /usr/bin/fcitx ] || exit 0

if [ -x /usr/bin/im-config ] && [ ! -f $HOME/.xinputrc ]; then
    /usr/bin/im-config -n fcitx && export XMODIFIERS="@im=fcitx" || true
elif [ -x /usr/bin/imsettings-switch ] && [ ! -f $HOME/.config/imsettings/xinputrc ]; then
    /usr/bin/imsettings-switch -qf fcitx.conf && export XMODIFIERS="@im=fcitx" || true
elif [ ! -x /usr/bin/im-config ] && [ ! -x /usr/bin/imsettings-switch ]; then
    if [ "$XMODIFIERS" != "@im=fcitx" ]; then
	export XMODIFIERS="@im=fcitx"
    fi
fi

if [ "$XMODIFIERS" == "@im=fcitx" ]; then
    if [ -f /usr/lib/gtk-2.0/*/immodules/im-fcitx.so ] || \
       [ -f /usr/lib64/gtk-2.0/*/immodules/im-fcitx.so ]; then
	if [ -f /usr/lib/gtk-3.0/*/immodules/im-fcitx.so ] || \
	   [ -f /usr/lib64/gtk-3.0/*/immodules/im-fcitx.so ]; then
		export GTK_IM_MODULE=fcitx
	fi
    fi
    if [ -f /usr/lib/qt4/plugins/inputmethods/qtim-fcitx.so ] || \
       [ -f /usr/lib64/qt4/plugins/inputmethods/qtim-fcitx.so ]; then
	export QT_IM_MODULE=fcitx
	if [ -f /usr/lib/qt5/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so ] || \
	   [ -f /usr/lib64/qt5/plugins/platforminputcontexts/libfcitxplatforminputcontextplugin.so ]; then
		export QT_IM_MODULE=fcitx
	fi
    fi
fi
EOF

# binary files
install -d %{buildroot}%{_bindir}
install -m 0755 usr/bin/* %{buildroot}%{_bindir}/

# library files
install -d %{buildroot}%{_libdir}/fcitx
install -m 0644 usr/lib/*-linux-gnu/fcitx/* %{buildroot}%{_libdir}/fcitx/

# include files
install -d %{buildroot}%{_includedir}/fcitx/module/{autoeng-ng,punc-ng}
install -m 0644 usr/include/fcitx/module/autoeng-ng/AutoEng.h \
 %{buildroot}%{_includedir}/fcitx/module/autoeng-ng/
install -m 0644 usr/include/fcitx/module/punc-ng/* \
 %{buildroot}%{_includedir}/fcitx/module/punc-ng/

# desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/fcitx-ui-sogou-qimpanel.desktop <<EOF
[Desktop Entry]
Name=Sogou Pinyin
Name[zh_CN]=搜狗拼音
GenericName=Sogou Pinyin Input Method
GenericName[zh_CN]=搜狗拼音输入法
Comment=a popular pinyin input method
Comment[zh_CN]=20 年稳定专业的输入法
MimeType=application/x-sogouskin;application/x-scel;
Keywords=ime;imf;input;
Exec=sogou-qimpanel %U
Icon=fcitx-sogoupinyin
Terminal=false
Type=Application
Categories=System;Utility;
StartupNotify=false
X-GNOME-Autostart-Phase=Applications
X-GNOME-Autostart-Notify=false
X-GNOME-Autostart-Delay=2
X-GNOME-AutoRestart=true
X-KDE-autostart-phase=1
X-KDE-autostart-after=panel
EOF

# fcitx files
install -d %{buildroot}%{_datadir}/fcitx
cp -r usr/share/fcitx/* %{buildroot}%{_datadir}/fcitx/

# sogou input method schemes
install -d %{buildroot}%{_datadir}/fcitx-%{name}
cp -r usr/share/fcitx-%{name}/* %{buildroot}%{_datadir}/fcitx-%{name}/

# glib schemas
install -Dm 0644 usr/share/glib-2.0/schemas/50_%{name}.gschema.override \
   %{buildroot}%{_datadir}/glib-2.0/schemas/50_%{name}.gschema.override

# icon files
for i in 16x16 48x48 64x64 128x128; do
install -d %{buildroot}%{_datadir}/icons/hicolor/$i/apps
install -m 0644 usr/share/icons/hicolor/$i/apps/*.png \
 %{buildroot}%{_datadir}/icons/hicolor/$i/apps/fcitx-%{name}.png
done
install -d %{buildroot}%{_datadir}/pixmaps
install -m 0644 usr/share/pixmaps/*.png %{buildroot}%{_datadir}/pixmaps/

# locale file
install -Dm 644 usr/share/locale/zh_CN/LC_MESSAGES/fcitx-%{name}.mo \
 %{buildroot}%{_datadir}/locale/zh_CN/LC_MESSAGES/fcitx-%{name}.mo

# mime file
install -Dm 644 usr/share/mime/packages/fcitx-ui-sogou-qimpanel.xml \
 %{buildroot}%{_datadir}/mime/packages/fcitx-ui-sogou-qimpanel.xml

# skin, cell files
install -d %{buildroot}%{_datadir}/sogou-qimpanel
cp -r usr/share/sogou-qimpanel/* %{buildroot}%{_datadir}/sogou-qimpanel/

# doc files
install -d %{buildroot}%{_datadir}/doc/%{name}
cp usr/share/doc/%{name}/* %{buildroot}%{_datadir}/doc/%{name}/

# version information
install -d %{buildroot}%{_datadir}/%{name}
echo "%{version}" > %{buildroot}%{_datadir}/%{name}/sogou-version

# rename files
pushd %{buildroot}%{_datadir}/sogou-qimpanel/cell/defaultCell
for i in *;do
  j=`echo "$i"|sed 's|【.*】||'`
  if [ "$i" != "$j" ];then
    mv "$i" "$j"
  fi
done
popd

pushd %{buildroot}%{_datadir}/sogou-qimpanel/recommendSkin/skin
rm -rf "三国杀"* *"路飞" *"团兵"*
for i in *;do
  j=$(echo "$i"|sed 's|[【〖].*[】〗]||')
  if [ "$i" == "【优客】简约" ];then
    j="优客简约"
  fi
  if [ "$i" != "$j" ];then
    mv "$i" "$j"
  fi
done
popd

%post
/sbin/ldconfig
INPUTRC=$(readlink /etc/alternatives/xinputrc|awk -F'/' '{print $6}')
if [ "$INPUTRC" != "fcitx.conf" ]; then
    alternatives --set xinputrc /etc/X11/xinit/xinput.d/fcitx.conf
fi

# install
if [ "$1" -eq "1" ]; then
    ln -s %{_datadir}/applications/fcitx-ui-sogou-qimpanel.desktop %{_sysconfdir}/xdg/autostart/ &>/dev/null ||:
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null ||:
    update-desktop-database -q ||:
    update-mime-database %{_datadir}/mime ||:
fi

%preun
# uninstall
if [ "$1" -eq "0" ];then
    rm -rf %{_sysconfdir}/xdg/autostart/fcitx-ui-sogou-qimpanel.desktop ||:
    pkill sogou > /dev/null 2>&1 ||:
fi

%postun
# uninstall
if [ "$1" -eq "0" ]; then
    glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null ||:
    update-desktop-database -q ||:
    update-mime-database %{_datadir}/mime ||:
    INPUTRC=`readlink /etc/alternatives/xinputrc|awk -F'/' '{print $6}'`
    if [ "$INPUTRC" == "fcitx.conf" ]; then
	alternatives --auto xinputrc
    fi
    /sbin/ldconfig
fi

%files
%defattr(-,root,root,-)
%{_bindir}/sogou-*
%{_bindir}/uk-*
%{_libdir}/fcitx/
%{_xinitrcdir}/
%{_includedir}/fcitx/module/
%{_datadir}/applications/*.desktop
%{_datadir}/fcitx/
%{_datadir}/fcitx-%{name}/
%{_datadir}/glib-2.0/
%{_datadir}/icons/hicolor/*/apps/fcitx-%{name}.png
%{_datadir}/locale/
%{_datadir}/mime/packages/
%{_datadir}/pixmaps/
%{_datadir}/sogou-qimpanel/
%{_datadir}/%{name}/
%{_datadir}/doc/%{name}/


%changelog
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 1.2.0.0056-2
- Remove depends
* Tue May 26 2015 mosquito <sensor.wen@gmail.com> - 1.2.0.0056-1
- Update version 1.2.0.0056
* Tue May  5 2015 mosquito <sensor.wen@gmail.com> - 1.2.0.0048-1
- Update version 1.2.0.0048
* Thu Feb  5 2015 mosquito <sensor.wen@gmail.com> - 1.2.0.0042-2
- Fix version information
- Rename skin directory
* Tue Feb  3 2015 mosquito <sensor.wen@gmail.com> - 1.2.0.0042-1
- Update version 1.2.0.0042
* Sat Oct 11 2014 mosquito <sensor.wen@gmail.com> - 1.1.0.0037-3
- Fix uninstall script
* Fri Sep 12 2014 mosquito <sensor.wen@gmail.com> - 1.1.0.0037-2
- Add i386 version
* Fri Aug 22 2014 mosquito <sensor.wen@gmail.com> - 1.1.0.0037-1
- For fedora 20 repackaged
- update version 1.1.0.0037
  * a new input method status bar
  * update the input method thesaurus
  * optimize performance, memory reduce about 40%
  * optimize the keypad function
  * improve stability
  * Fixed select the default skin, cycle start 'sogou-qimpanel' problem
* Fri Jul 4 2014 mosquito <sensor.wen@gmail.com> - 1.0.0.0033-2
- Update post and preun scripts
* Sun Jun 22 2014 mosquito <sensor.wen@gmail.com> - 1.0.0.0033-1
- For fedora 20 repackaged
* Tue Jun 17 2014 i@marguerite.su (SuSE)
- update version 1.0.0.0033
  * number input from keypad
  * run faster
  * optimize details of menus/attribute settings
* Fri Apr 18 2014 i@marguerite.su (SuSE)
- initial version 1.0.0.0011
