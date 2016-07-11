%global debug_package %{nil}
%global _xinitrcdir %{_sysconfdir}/X11/xinit/xinitrc.d
%global _xinputdir  %{_sysconfdir}/X11/xinit/xinput.d

# sogoupinyin-selinux conditional
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%global  with_selinux  1
%endif

%if 0%{?with_selinux}
%global  selinuxtype   targeted
%global  moduletype    apps
%global  modulename    %{name}

# Usage: _format var format
# Expand 'modulename' into various formats as needed
# Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulename}; do %1+=%2; %1+=" "; done;

# Relabel files
%global relabel_files() %{_sbindir}/restorecon -R %{_bindir}/sogou* %{_datadir}/sogou* %{_datadir}/fcitx-%{name} /tmp/*sogou* /home/*/.config/{SogouPY*/,sogou-qimpanel/,Trolltech.conf} &>/dev/null ||:

# Version of SELinux we were using
%if 0%{?fedora} >= 21
%global  selinux_policyver 3.13.1-105
%else
%global  selinux_policyver 3.13.1-39
%endif
%endif # with_selinux

Name:       sogoupinyin
Version:    2.0.0.0078
Release:    1%{?dist}
Summary:    Sogou Pinyin input method
Summary(zh_CN): 搜狗拼音输入法

License:    Proprietary and GPLv2
URL:        http://pinyin.sogou.com/linux
Group:      Applications/System
Source0:    http://cdn2.ime.sogou.com/dl/index/1465191139/%{name}_%{version}_amd64.deb
Source1:    http://cdn2.ime.sogou.com/dl/index/1465186614/%{name}_%{version}_i386.deb
Source11:   %{name}.te
Source12:   %{name}.fc
Source13:   %{name}.if
Source14:   Makefile

# https://github.com/FZUG/repo/issues/50
Patch0:     sogou-diag_dpkg.patch

BuildRequires: dpkg
Requires(post): /usr/bin/glib-compile-schemas
Requires(post): /usr/bin/gtk-update-icon-cache
Requires(post): /usr/bin/update-mime-database
Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:   imsettings im-chooser
Requires:   fcitx-qt4 fcitx-qt5
Requires:   fcitx-gtk2 fcitx-gtk3
Requires:   fcitx-configtool
Conflicts:  fcitx-sogoupinyin
Obsoletes:  sogou-pinyin < %{version}-%{release}

# RE: rhbz#1195804 - ensure min NVR for selinux-policy
%if 0%{?with_selinux}
Requires:   selinux-policy >= %{selinux_policyver}
Requires(pre): %{name}-selinux >= %{version}-%{release}
%endif # with_selinux

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
支持全拼简拼双拼, 模糊拼音, 细胞词库, 云输入, 皮肤, 中英混输.
通过结合搜索引擎技术, 提高输入准确率. 更多惊喜等您体验.

如果您安装了 %{name}-selinux 并将 SELinux 设为 enforcing 模式, 则 SELinux 会
保护您 home 目录的私有文件, 避免被 %{name} 访问. 同时, SELinux 默认也会阻止您
安装皮肤和词库.

皮肤保存在~/.config/sogou-qimpanel/skin/, 按以下方式安装:
  $ sudo setsebool sogou_enable_homedirs=1
  $ sogou-qimpanel Skin.ssf

词库保存在~/.config/SogouPY/scd/, 按以下方式安装:
  $ sudo setsebool sogou_enable_homedirs=1
  $ sogou-qimpanel Cell.scel

禁止 sogou 访问网络:
  $ sudo setsebool -P sogou_access_network=0 # 默认: true

允许 sogou 访问 home 目录:
  $ sudo setsebool sogou_enable_homedirs=1   # 默认: false

%if 0%{?with_selinux}
%package selinux
Summary: SELinux policies for %{name}
BuildArch: noarch
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
Requires(post): selinux-policy-base >= %{selinux_policyver}
Requires(post): selinux-policy-targeted >= %{selinux_policyver}
Requires(post): policycoreutils
%if 0%{?fedora} > 22
Requires(post): policycoreutils-python-utils
%else
Requires(post): policycoreutils-python
%endif
Requires(post): libselinux-utils

%description selinux
SELinux policy modules for use with %{name}.

If you do not want to %{name} access the network. Execute this command.
  $ sudo setsebool -P sogou_access_network=0 # default: true

Allow sogou access home dirs:
  $ sudo setsebool sogou_enable_homedirs=1   # default: false

%description selinux -l zh_CN
适用于 %{name} 的 SELinux 策略模块.

如果您不希望 %{name} 访问网络, 请执行以下命令:
  $ sudo setsebool -P sogou_access_network=0 # 默认: true

允许 sogou 访问 home 目录:
  $ sudo setsebool sogou_enable_homedirs=1   # 默认: false
%endif # with_selinux

%prep
# Extract DEB package
%ifarch x86_64
dpkg-deb -X %{SOURCE0} %{_builddir}/%{name}-%{version}
%else
dpkg-deb -X %{SOURCE1} %{_builddir}/%{name}-%{version}
%endif

# patch sogou-diag
pushd %{_builddir}/%{name}-%{version}
%patch0 -p1

%if 0%{?with_selinux}
pushd %{_builddir}/%{name}-%{version}
mkdir selinux
cp %{S:11} %{S:12} %{S:13} %{S:14} selinux/
%endif # with_selinux

%build
%if 0%{?with_selinux}
pushd %{_builddir}/%{name}-%{version}
pushd selinux
make
popd
%endif # with_selinux

%install
pushd %{_builddir}/%{name}-%{version}

# 55-sogoupinyin.sh script
install -d %{buildroot}%{_xinitrcdir}
cat > %{buildroot}%{_xinitrcdir}/55-%{name}.sh <<EOF
#!/bin/sh
set -e

[ -x /usr/bin/fcitx ] || exit 0

if [ -x /usr/bin/im-config ] && [ ! -f \$HOME/.xinputrc ]; then
    /usr/bin/im-config -n fcitx && export XMODIFIERS="@im=fcitx" || :
elif [ -x /usr/bin/imsettings-switch ] && [ ! -f \$HOME/.config/imsettings/xinputrc ]; then
    /usr/bin/imsettings-switch -qf fcitx.conf && export XMODIFIERS="@im=fcitx" || :
elif [ ! -x /usr/bin/im-config ] && [ ! -x /usr/bin/imsettings-switch ]; then
    if [ "\$XMODIFIERS" == "" ] || [ "\$XMODIFIERS" == "@im=xim" ]; then
        export XMODIFIERS="@im=fcitx"
    fi
fi

if [ "\$XMODIFIERS" == "@im=fcitx" ]; then
    if [ -f /usr/lib/*/gtk-2.0/*/immodules/im-fcitx.so ] || \\
       [ -f /usr/lib*/gtk-2.0/*/immodules/im-fcitx.so ]; then
        if [ -f /usr/lib/*/gtk-3.0/*/immodules/im-fcitx.so ] || \\
           [ -f /usr/lib*/gtk-3.0/*/immodules/im-fcitx.so ]; then
            export GTK_IM_MODULE=fcitx
        fi
    fi
    if [ -f /usr/lib/*/qt4/plugins/inputmethods/qtim-fcitx.so ] || \\
       [ -f /usr/lib*/qt4/plugins/inputmethods/qtim-fcitx.so ]; then
        export QT4_IM_MODULE=fcitx
        if [ -f /usr/lib/*/qt5/plugins/*inputcontexts/libfcitx*.so ] || \\
           [ -f /usr/lib*/qt5/plugins/*inputcontexts/libfcitx*.so ]; then
            export QT_IM_MODULE=fcitx
        fi
    fi
fi
EOF

# fcitx environment variable configurage file
install -d %{buildroot}%{_sysconfdir}/sysconfig
cat > %{buildroot}%{_sysconfdir}/sysconfig/%{name} <<EOF
# If your system does not start automatically Sogou Pinyin,
# create ~/.profile file and add the following command.
#    source /etc/sysconfig/sogoupinyin
export XIM=fcitx
export XIM_PROGRAM=/usr/bin/fcitx
export GTK_IM_MODULE=fcitx
export QT_IM_MODULE=fcitx
export XMODIFIERS="@im=fcitx"
while (test ! -d /proc/\`pidof sogou-qimpanel||echo None\`); do
    FCITX=\$(pidof fcitx &>/dev/null && echo y || echo n)
    SOGOU=\$(pidof sogou-qimpanel &>/dev/null && echo y || echo n)
    if [[ \$FCITX == "y" && \$SOGOU == "n" ]]; then
        /usr/bin/sogou-qimpanel &>/dev/null &
    fi
    sleep 15
done &
EOF

# binary files
install -d %{buildroot}%{_bindir}
install -m 0755 usr/bin/* %{buildroot}%{_bindir}/

# library files
install -d %{buildroot}%{_libdir}/fcitx
install -m 0644 usr/lib/*-linux-gnu/fcitx/*.so %{buildroot}%{_libdir}/fcitx/

# desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/fcitx-ui-sogou-qimpanel.desktop <<EOF
[Desktop Entry]
Name=Sogou Pinyin
Name[zh_CN]=搜狗拼音
GenericName=Sogou Pinyin Input Method
GenericName[zh_CN]=搜狗拼音输入法
Comment=a popular pinyin input method
Comment[zh_CN]=搜狗拼音输入法
MimeType=application/x-sogouskin;application/x-scel;
Keywords=ime;imf;input;
Exec=sogou-qimpanel %U
Icon=fcitx-sogoupinyin
Terminal=false
Type=Application
NoDisplay=true
Categories=System;Utility;
StartupNotify=false
X-GNOME-Autostart-Phase=Applications
X-GNOME-Autostart-Notify=false
X-GNOME-Autostart-Delay=2
X-GNOME-AutoRestart=true
X-KDE-autostart-phase=1
X-KDE-autostart-after=panel
X-MATE-Autostart-Phase=Applications
X-MATE-Autostart-Delay=2
X-MATE-Autostart-Notify=false
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
mv usr/share/doc/%{name}/* .

# version information
install -d %{buildroot}%{_datadir}/%{name}
echo "%{version}" > %{buildroot}%{_datadir}/%{name}/sogou-version

# rename files
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

%if 0%{?with_selinux}
# install SELinux interfaces
%_format INTERFACES $x.if
install -d %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 selinux/$INTERFACES \
    %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}

# install policy modules
%if 0%{?fedora} > 22
%_format MODULES $x.cil.bz2
%else
%_format MODULES $x.pp.bz2
%endif
install -d %{buildroot}%{_datadir}/selinux/packages
install -m 644 selinux/$MODULES %{buildroot}%{_datadir}/selinux/packages
%endif # with_selinux

%post
USER=$(logname||who|awk '/:0/{print $1}')

# stop ibus-daemon
test -x /usr/bin/ibus-daemon && chmod a-x /usr/bin/ibus-daemon ||:
pkill ibus &>/dev/null ||:

# set xinputrc
INPUTRC=$(readlink /etc/alternatives/xinputrc|awk -F'/' '{print $6}')
if [ "x$INPUTRC" != "xfcitx.conf" ]; then
    alternatives --set xinputrc %{_xinputdir}/fcitx.conf
    mkdir -p /home/${USER}/.config/imsettings &>/dev/null ||:
    ln -sf %{_xinputdir}/fcitx.conf /home/${USER}/.config/imsettings/xinputrc
    chown -R $USER:$USER /home/${USER}/.config/imsettings
fi

# install
if [ $1 -eq 1 ]; then
    ln -s %{_datadir}/applications/fcitx-ui-sogou-qimpanel.desktop \
          %{_sysconfdir}/xdg/autostart/ &>/dev/null ||:
fi
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:
/sbin/ldconfig

%if 0%{?with_selinux}
%post selinux
# Install all modules in a single transaction
%_format MODULES %{_datadir}/selinux/packages/$x.*.bz2
%{_sbindir}/semodule -n -s %{selinuxtype} -i $MODULES
if %{_sbindir}/selinuxenabled ; then
    %{_sbindir}/load_policy
    %relabel_files
    if [ $1 -eq 1 ]; then
        %{_sbindir}/setsebool -P -N sogou_access_network=1
        %{_sbindir}/setsebool -P -N sogou_enable_homedirs=0
    fi
fi
%endif # with_selinux

%preun
# uninstall
if [ $1 -eq 0 ];then
    rm -rf %{_sysconfdir}/xdg/autostart/fcitx-ui-sogou-qimpanel.desktop ||:
    pkill sogou &>/dev/null ||:
fi

%postun
# uninstall
if [ $1 -eq 0 ]; then
    test ! -x /usr/bin/ibus-daemon && chmod a+x /usr/bin/ibus-daemon &>/dev/null ||:
    INPUTRC=$(readlink /etc/alternatives/xinputrc|awk -F'/' '{print $6}')
    if [ "$INPUTRC" == "fcitx.conf" ]; then
        alternatives --auto xinputrc
    fi

    /usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null ||:
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
    /usr/bin/update-mime-database %{_datadir}/mime &>/dev/null ||:
    /sbin/ldconfig
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%if 0%{?with_selinux}
%postun selinux
if [ $1 -eq 0 ]; then
    %{_sbindir}/semodule -n -r %{modulename} &>/dev/null ||:
    if %{_sbindir}/selinuxenabled ; then
        %{_sbindir}/load_policy
        %relabel_files
    fi
fi
%endif # with_selinux

%posttrans
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas &>/dev/null ||:
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &>/dev/null ||:

%files
%defattr(-,root,root,-)
%doc %{name}-%{version}/changelog.gz
%license %{name}-%{version}/{copyright,license*}
%attr(755,root,root) %{_xinitrcdir}/55-%{name}.sh
%{_sysconfdir}/sysconfig/%{name}
%{_bindir}/sogou-*
%{_libdir}/fcitx/*.so
%{_datadir}/fcitx/
%{_datadir}/fcitx-%{name}/SogouInput/
%{_datadir}/glib-2.0/schemas/*.gschema.override
%{_datadir}/icons/hicolor/*/apps/fcitx-%{name}.png
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/*.desktop
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/mime/packages/*.xml
%{_datadir}/sogou-qimpanel/
%{_datadir}/%{name}/

%if 0%{?with_selinux}
%files selinux
%defattr(-,root,root,-)
%{_datadir}/selinux/*
%endif # with_selinux

%changelog
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 2.0.0.0078-1
- Update version 2.0.0.0078
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 2.0.0.0072-1
- Update version 2.0.0.0072
* Sun Mar 27 2016 mosquito <sensor.wen@gmail.com> - 2.0.0.0068-4
- Fix https://github.com/FZUG/repo/issues/81
* Fri Dec 25 2015 mosquito <sensor.wen@gmail.com> - 2.0.0.0068-3
- Update SELinux module (sogoupinyin 1.1.0)
  Fix the sogou-qimpanel-watchdog does not enable sogou-qimpanel
- Update post script
  Fix xinitrc script(55-sogoupinyin.sh)
  Add fcitx environment variable file
  see https://github.com/FZUG/repo/issues/49
- Patch sogou-diag
  see https://github.com/FZUG/repo/issues/50
* Wed Dec 23 2015 mosquito <sensor.wen@gmail.com> - 2.0.0.0068-2
- Fix sogou-qimpanel do not run
  see https://github.com/FZUG/repo/issues/49
* Sun Dec 13 2015 mosquito <sensor.wen@gmail.com> - 2.0.0.0068-1
- Update version 2.0.0.0068
- Update post script
* Sun Oct 25 2015 mosquito <sensor.wen@gmail.com> - 2.0.0.0066-2
- Add SELinux module (sogoupinyin 1.0.0)
* Sat Oct 17 2015 mosquito <sensor.wen@gmail.com> - 2.0.0.0066-1
- Update version 2.0.0.0066
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
