# http://community.wps.cn/wiki/Fedora_rpm_制作步骤
# https://cheeselee.fedorapeople.org/wps-office.spec

%global __provides_exclude_from ^/opt/kingsoft/%{name}/office6/.*\\.so$
%global __requires_exclude_from ^/opt/kingsoft/%{name}/office6/.*\\.so$
%global __provides_exclude (font|lib)
%global __requires_exclude (Qt|app|libc++|libav|bz2|media|sw|draw|krt|kso|spell|wpsio|xer|wpp)

%global debug_package %{nil}
%global _tmppath /var/tmp
%global tmproot %{_tmppath}/%{name}-%{version}_tmproot
# %%global is different from %%define!
%define test()  %(test $(rpm -E%?_arch) = x86_64 && echo "%1" || echo "%2")
%global arch    %{test x86_64 x86}
%global appfile %{name}_%{version}_%{arch}.tar.xz
%global appurl  http://kdl.cc.ksosoft.com/wps-community/download/%{rev}/%{appfile}
%global msfonts symbol-fonts_1.2_all.deb
%global msfonts_url http://linux.linuxidc.com/linuxconf/download.php?file=Li9saW51eGZpbGVzLzIwMTTE6tfKwc8vNNTCLzIwyNUvVWJ1bnR1IDE0LjA0ILCy17AgV1BTL3N5bWJvbC1mb250c18xLjJfYWxsLmRlYg==

# Usage: wget appfile appurl
%global wget() %{expand:
SHA=$(test -f %1 && sha1sum %1 ||:)
CODE=$(curl -sI %2|awk '{print$2;exit}')
if [[ (! -f %1 || "${SHA/ */}" != "%sha1sum") && "$CODE" == "200" ]]; then
    wget --unlink -O %1 %2 || axel -o %1 -a %2
fi}

%global rev     6757
%global sha1sum %{test 03a781599dfcf001fc3bcf1d49699bd1a44aaceb
                       3c6095380c32252afd7838f295259b14a0bf726e}

Name:           wps-office
Version:        10.1.0.6757
Release:        1.net
Summary:        WPS Office Suite
Summary(zh_CN): 金山 WPS Office 办公套件
License:        Proprietary
URL:            https://wps-community.org
BuildRequires:  axel wget dpkg
BuildRequires:  desktop-file-utils
Requires:       axel wget dpkg
Requires:       desktop-file-utils
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
%wget %{appfile} %{appurl}
test -f %{msfonts} || wget -O %{msfonts} %{msfonts_url}
dpkg-deb -X %{msfonts} .

# Extract archive
AppFile=%{appfile}
tar -xvf %{appfile}
mv ${AppFile%.tar.xz} %{name}

%install
pushd %{name}
# Main
install -d %{buildroot}/opt/kingsoft/%{name}
cp -r office6 %{buildroot}/opt/kingsoft/%{name}

# Icons, Mime, Desktop
install -d %{buildroot}%{_datadir}
cp -r resource/* %{buildroot}%{_datadir}

# MS Fonts
install -d %{buildroot}%{_datadir}/fonts/%{name}
find ../usr -type f | xargs cp -t %{buildroot}%{_datadir}/fonts/%{name}

# Execution files
for i in wps wpp et; do
  install -Dm755 ${i} %{buildroot}%{_bindir}/${i}
done

%pre
if [ $1 -ge 1 ]; then
# Download wps
cd %{_tmppath}
%wget %{appfile} %{appurl}

# Extract archive
AppFile=%{appfile}
tar -xf %{appfile}
mv ${AppFile%.tar.xz} %{name}

# Main
install -d %{tmproot}/opt/kingsoft/%{name}
cp -r %{name}/office6 %{tmproot}/opt/kingsoft/%{name}
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/%{name}
fi
/usr/bin/fc-cache %{_datadir}/fonts/%{name} ||:

%postun
if [ $1 -eq 0 ]; then
    /usr/bin/fc-cache %{_datadir}/fonts/%{name} ||:
fi

%files
%doc %{name}/README.txt
%{_bindir}/*
%{_datadir}/fonts/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/desktop-directories/%{name}*
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%{_datadir}/mime/packages/*.xml
%{_datadir}/templates/*.desktop
%ghost /opt/kingsoft

%changelog
* Sun Dec 30 2018 mosquito <sensor.wen@gmail.com> - 10.1.0.6757-1
- Release 10.1.0.6757

* Wed Jun 29 2016 mosquito <sensor.wen@gmail.com> - 10.1.0.5672-2
- Fix symbol fonts url

* Wed Jun 29 2016 mosquito <sensor.wen@gmail.com> - 10.1.0.5672-1
- Release 10.1.0.5672
- Check download url

* Thu Jun 23 2016 mosquito <sensor.wen@gmail.com> - 10.1.0.5503-2
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
