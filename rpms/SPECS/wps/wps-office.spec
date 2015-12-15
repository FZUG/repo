# http://community.wps.cn/wiki/Fedora_rpm_制作步骤
# https://cheeselee.fedorapeople.org/wps-office.spec

%global __provides_exclude_from ^/opt/kingsoft/%{name}/office6/.*\\.so$
%global __requires_exclude_from ^/opt/kingsoft/%{name}/office6/.*\\.so$
%global __provides_exclude (font|lib)
%global __requires_exclude (Qt|app|libc++|draw|krt|kso|spell|wpsio|xer)

%global debug_package %{nil}
%global tmproot /tmp/%{name}-%{version}
%global arch    %(test $(rpm -E%?_arch) = x86_64 && echo "x86_64" || echo "x86")
%global appfile %{name}_%{version}~a19p1_%{arch}.tar.xz
%global appurl  http://kdl.cc.ksosoft.com/wps-community/download/a19/%{appfile}
%global sha1sum %(test %arch = x86_64 &&
           echo "512b94132d18a896684e4470acc61c6f2f6d3a60" ||
           echo "4529daf48c06c50ddbbe2ce4eb1362b0ddb4920a")
%global msfonts http://linux.linuxidc.com/2014年资料/4月/20日/Ubuntu 14.04 安装 WPS/symbol-fonts_1.2_all.deb

Name:           wps-office
Version:        9.1.0.4975
Release:        1.a19p1.net
Summary:        WPS Office Suite
Summary(zh_CN): 金山 WPS Office 办公套件
Group:          Applications/Editors
License:        Proprietary
URL:            http://wps-community.org

BuildRequires:  axel wget dpkg
BuildRequires:  desktop-file-utils
Requires:       axel wget dpkg
Requires:       desktop-file-utils
Requires:       /usr/bin/gtk-update-icon-cache
Requires:       /usr/bin/update-mime-database
# http://sourceforge.net/projects/mscorefonts2
#Requires:       msttcore-fonts-installer

%description
 WPS Office including Writer, Presentation, and Spreadsheets, is a powerful
 office suite, which is able to process word file, produce wonderful slides,
 and analyze data as well. It is deeply compatible with all of the latest
 Microsoft Office file formats. It can easily open and read the documents
 created with Microsoft Office.

 This is the Linux version, and it's now an BETA package.
 Welcome to our website: http://wps-community.org

%description -l zh_CN
 WPS Office 包含文字、演示、表格三大组件，是一个功能强大的办公套装软件，
 能够用来处理 Word 文件、创作精美的幻灯片和分析数据。WPS Office 深度兼
 容 Microsoft Office 办公套件的文件格式，可以打开和读取其创建的文件。

 这是 Linux 版本的安装包，目前是测试版本。
 更多信息请参考:
 - http://wps-community.org
 - http://community.wps.cn

%prep
# Download opera
Download() {
    SHA=$(test -f %{appfile} && sha1sum %{appfile} ||:)
    if [[ ! -f %{appfile} || "${SHA/ */}" != "%sha1sum" ]]; then
        axel -a %appurl; Download
    fi
}
Download

# symbol-fonts
test -f symbol-fonts_1.2_all.deb || wget --http-user=www.linuxidc.com --http-password=www.linuxidc.com "%{msfonts}"
dpkg-deb -X symbol-fonts_1.2_all.deb .

# Extract archive
tar -xvf %{appfile}
mv %{name}_%{version}~a19p1_%{arch} %{name}

%build

%install
pushd %{name}
# Main
install -d %{buildroot}/opt/kingsoft/%{name}
cp -r office6 %{buildroot}/opt/kingsoft/%{name}

# Fonts
install -d %{buildroot}%{_datadir}/fonts/%{name}
cp -r fonts/* %{buildroot}%{_datadir}/fonts/%{name}
find ../usr -type f | xargs cp -t %{buildroot}%{_datadir}/fonts/%{name}

# Icons, Mime, Desktop
cp -r resource/icons %{buildroot}%{_datadir}
cp -r resource/mime %{buildroot}%{_datadir}
cp -r resource/applications %{buildroot}%{_datadir}

# Fonts config
install -d %{buildroot}%{_datadir}/fontconfig/conf.avail
install -d %{buildroot}%{_sysconfdir}/fonts/conf.d
install -m 0644 fontconfig/*.conf %{buildroot}%{_datadir}/fontconfig/conf.avail/
ln -sfv %{_datadir}/fontconfig/conf.avail/40-%{name}.conf \
  %{buildroot}%{_sysconfdir}/fonts/conf.d/40-%{name}.conf

# Execution files
for i in wps wpp et wps_error_check.sh; do
  install -Dm 0755 ${i} %{buildroot}%{_bindir}/${i}
done

%pre
if [ $1 -ge 1 ]; then
# Download opera
cd /tmp
Download() {
    SHA=$(test -f %{appfile} && sha1sum %{appfile} ||:)
    if [[ ! -f %{appfile} || "${SHA/ */}" != "%sha1sum" ]]; then
        axel -a %appurl; Download
    fi
}
Download

# symbol-fonts
test -f symbol-fonts_1.2_all.deb || wget -t 5 --http-user=www.linuxidc.com --http-password=www.linuxidc.com "%{msfonts}" ||:
dpkg-deb -x symbol-fonts_1.2_all.deb . ||:

# Extract archive
mkdir %{tmproot} &>/dev/null ||:
tar -xf %{appfile}
mv %{name}_%{version}~a19p1_%{arch} %{name}
cd %{name}

# Main
install -d %{tmproot}/opt/kingsoft/%{name}
cp -r office6 %{tmproot}/opt/kingsoft/%{name}

# Fonts
install -d %{tmproot}%{_datadir}/fonts/%{name}
cp -r fonts/* %{tmproot}%{_datadir}/fonts/%{name}
find ../usr -type f | xargs cp -t %{tmproot}%{_datadir}/fonts/%{name}

# Icons, Mime, Desktop
cp -r resource/icons %{tmproot}%{_datadir}
cp -r resource/mime %{tmproot}%{_datadir}
cp -r resource/applications %{tmproot}%{_datadir}

# Fonts config
install -d %{tmproot}%{_datadir}/fontconfig/conf.avail
install -d %{tmproot}%{_sysconfdir}/fonts/conf.d
install -m 0644 fontconfig/*.conf %{tmproot}%{_datadir}/fontconfig/conf.avail/

# Execution files
for i in wps wpp et wps_error_check.sh; do
  install -Dm 0755 ${i} %{tmproot}%{_bindir}/${i}
done
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} /tmp/%{name} /tmp/usr
    ln -sf %{_datadir}/fontconfig/conf.avail/40-%{name}.conf %{_sysconfdir}/fonts/conf.d/
fi

/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:
/usr/bin/fc-cache %{_datadir}/fonts/%{name} ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
    /usr/bin/update-mime-database %{_datadir}/mime &>/dev/null ||:
    /usr/bin/fc-cache %{_datadir}/fonts/%{name} ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
/usr/bin/update-mime-database %{_datadir}/mime &>/dev/null ||:

%files
%doc %{name}/README.txt
%ghost %{_bindir}/*
%ghost %{_sysconfdir}/fonts/conf.d/*.conf
%ghost %{_datadir}/fontconfig/conf.avail/*.conf
%ghost %{_datadir}/fonts/%{name}
%ghost %{_datadir}/applications/*.desktop
%ghost %{_datadir}/mime/packages/*.xml
%ghost %{_datadir}/icons/hicolor/*/apps/*.png
%ghost %{_datadir}/icons/hicolor/*/mimetypes/*.png
%ghost /opt/kingsoft

%changelog
* Tue Dec 15 2015 mosquito <sensor.wen@gmail.com> - 9.1.0.4975-1
- Initial build
