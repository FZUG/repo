# http://community.wps.cn/wiki/Fedora_rpm_制作步骤
# https://cheeselee.fedorapeople.org/wps-office.spec

%global __provides_exclude_from ^/opt/kingsoft/%{name}/office6/.*\\.so$
%global __requires_exclude_from ^/opt/kingsoft/%{name}/office6/.*\\.so$
%global __provides_exclude (font|lib)
%global __requires_exclude (Qt|app|libc++|draw|krt|kso|spell|wpsio|xer|wpp)

%global debug_package %{nil}
%global _tmppath /var/tmp
%global tmproot %{_tmppath}/%{name}-%{version}_tmproot
%global arch    %(test $(rpm -E%?_arch) = x86_64 && echo "x86_64" || echo "x86")
%global appfile %{name}_%{version}~a20p2_%{arch}.tar.xz
%global appurl  https://repo.fdzh.org/FZUG/nonfree/23/source/SRPMS/%{appfile}
%global sha1sum %(test %arch = x86_64 &&
           echo "23db41f471aae1bde2ba196f0b0ed93eaa7fc97c" ||
           echo "6cf08f24b6c22c36cddf88598073b4fa4256e828")
%global msfonts http://linux.linuxidc.com/2014年资料/4月/20日/Ubuntu 14.04 安装 WPS/symbol-fonts_1.2_all.deb
%global getopts -t 5 --http-user=www.linuxidc.com --http-password=www.linuxidc.com

# Usage: DownloadPkg appfile appurl
%global DownloadPkg() \
Download() {\
    SHA=$(test -f %1 && sha1sum %1 ||:)\
    if [[ ! -f %1 || "${SHA/ */}" != "%sha1sum" ]]; then\
        axel -o %1 -a %2; Download\
    fi\
}\
Download\
test -f symbol-fonts_1.2_all.deb || wget %{getopts} "%{msfonts}"
%{nil}

Name:           wps-office
Version:        10.1.0.5503
Release:        2.a20p2.net
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
%DownloadPkg %{appfile} %{appurl}

# symbol-fonts
dpkg-deb -X symbol-fonts_1.2_all.deb .

# Extract archive
tar -xvf %{appfile}
mv %{name}_%{version}~a20p2_%{arch} %{name}

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
install -m 0644 fontconfig/*.conf %{buildroot}%{_datadir}/fontconfig/conf.avail/

# Execution files
for i in wps wpp et; do
  install -Dm 0755 ${i} %{buildroot}%{_bindir}/${i}
done

%pre
if [ $1 -ge 1 ]; then
# Download wps
cd %{_tmppath}
%DownloadPkg %{appfile} %{appurl}

# symbol-fonts
dpkg-deb -x symbol-fonts_1.2_all.deb . ||:

# Extract archive
mkdir %{tmproot} &>/dev/null ||:
tar -xf %{appfile}
mv %{name}_%{version}~a20p2_%{arch} %{name}
cd %{name}

# Main
install -d %{tmproot}/opt/kingsoft/%{name}
cp -r office6 %{tmproot}/opt/kingsoft/%{name}

# Fonts
install -d %{tmproot}%{_datadir}/fonts/%{name}
cp -r fonts/* %{tmproot}%{_datadir}/fonts/%{name}
find ../usr -type f | xargs cp -t %{tmproot}%{_datadir}/fonts/%{name}
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/%{name} %{_tmppath}/usr
    ln -sf %{_datadir}/fontconfig/conf.avail/40-%{name}.conf %{_sysconfdir}/fonts/conf.d/
fi
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:
/usr/bin/fc-cache %{_datadir}/fonts/%{name} ||:

%postun
if [ $1 -eq 0 ]; then
    rm -rf %{_sysconfdir}/fonts/conf.d/40-%{name}.conf
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
%{_bindir}/*
%{_datadir}/fontconfig/conf.avail/*.conf
%ghost %{_datadir}/fonts/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/mime/packages/*.xml
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%ghost /opt/kingsoft

%changelog
* Thu Jun 24 2016 mosquito <sensor.wen@gmail.com> - 10.1.0.5503-2
- Fix download url
* Fri Feb  5 2016 mosquito <sensor.wen@gmail.com> - 10.1.0.5503-1
- Release 10.1.0.5503
* Sun Jan 17 2016 mosquito <sensor.wen@gmail.com> - 10.1.0.5460-1
- Release 10.1.0.5460
- Change tmp directory
* Mon Dec 28 2015 mosquito <sensor.wen@gmail.com> - 10.1.0.5444-1
- Release 10.1.0.5444
* Tue Dec 15 2015 mosquito <sensor.wen@gmail.com> - 9.1.0.4975-1
- Initial build
