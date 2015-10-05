%global debug_package %{nil}
%global __python %{__python3}
%global project XwareDesktop
%global repo %{project}

# commit
%global _commit 2baa049c2f7ed0060cb6eeb858e432aa3f7d862d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		xware-desktop
Version:	0.13
Release:	2.git%{_shortcommit}%{?dist}
Summary:	An attempt to bring Xware (Xunlei on routers) to desktop Linux.
Summary(zh_CN):	Xware (迅雷路由器固件) 的 Linux 桌面前端.

Group:		Applications/Internet
License:	GPLv3
URL:		https://github.com/Xinkai/XwareDesktop/wiki
Source0:	https://github.com/Xinkai/XwareDesktop/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Patch0:		xware-desktop_makefile.patch

BuildRequires:	glibc-devel(x86-32)
BuildRequires:	glibc(x86-32)
BuildRequires:	libgcc(x86-32)
BuildRequires:	fakeroot
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
BuildRequires:	python3-sip
BuildRequires:	python3-sip-devel
BuildRequires:	python3-qt5
BuildRequires:	python-qt5-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	coffee-script
BuildRequires:	chrpath >= 0.14
BuildRequires:	findutils
BuildRequires:	sed

Requires:	glibc(x86-32)
Requires:	zlib(x86-32)
Requires:	python3-qt5 >= 5.2
Requires:	python3 >= 3.3
Requires:	qt5-qtwebkit >= 5.2
Requires:	qt5-qtmultimedia >= 5.2
Requires:	python3-inotify
Requires:	python3-enum34
Requires(post):	desktop-file-utils
Requires(post):	libcap
Requires(post):	chrpath >= 0.14
Conflicts:  pointdownload

%description
An attempt to bring Xware (Xunlei on routers) to desktop Linux.

%description -l zh_CN
Xware (迅雷路由器固件) 的 Linux 桌面前端.

%prep
%setup -q -n %repo-%{_commit}
%patch0 -p1
sed -i 's|qmake|%{_qt5_qmake}|g' src/frontend/Extensions/sip/configure.py

%build
QT_SELECT=5 \
make all %{?_smp_mflags} \
    PREFIX=%{_datadir}/%{name} \
    QMAKE=%{_qt5_qmake}

%install
make install DESTDIR=%{buildroot} PREFIX=%{_datadir}/%{name}

# change rpath/runpath
chrpath -r %{_datadir}/%{name}/frontend/Extensions \
    %{buildroot}%{_datadir}/%{name}/frontend/Extensions/DBusTypes.so

# python3 library
export PYTHONPATH=%{buildroot}%{python3_sitelib}
install -d %{buildroot}%{python3_sitelib}
%if 0%{?fedora} <= 20 || 0%{?rhel} >= 7
  easy_install-3.3 -d %{buildroot}%{python3_sitelib} pathlib asyncio
%else
  easy_install-3.4 -d %{buildroot}%{python3_sitelib} pathlib asyncio
%endif

%post
if [ $1 -eq 1 ]; then
    update-desktop-database -q ||:
    gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

    echo "================================================="
    echo -e "《欢迎使用 Xware Desktop》\n"
    echo "初始设置："
    echo "  1. 设置下载文件夹"
    echo "     文件 -> 设置 -> 挂载 -> 添加，选择下载文件夹[TDDOWNLOADS]"
    echo "  2. 托管 xwared 并启动"
    echo "     文件 -> 设置 -> 启动与登录 -> xwared托管，选择「由systemd托管」或「由upstart托管」，重启后 xwared会自动启动"
    echo "  3. 手动启动/关闭 xwared"
    echo "     - systemd：systemctl --user [start|stop] xwared"
    echo "     - upstart：[start|stop] xwared"
    echo "     - 直接执行：/usr/share/xware-desktop/xwared &"
    echo "  4. 使用迅雷帐号登陆，并激活设备即可"
    echo "  5. 浏览器整合"
    echo "     xware-desktop 可接受url参数，格式为"
    echo -e "\txware-desktop URL_File1 URL_File2 ..."
    echo "     以 Firefox 的 Flashgot 为例，添加一个新下载器，程序设置为 xware-desktop URL"
    echo "  6. 调整窗口大小"
    echo "     编辑 ~/.xware-desktop/profile/etc/frontend.ini，在 [legacy] 添加以下条目："
    echo -e "\twebviewminsizeoverride = 400,200 # 设置最小宽,高"
    echo -e "\twebviewzoom = 0.8  # 设置缩放比例"
    echo "================================================="
fi

%files
%defattr(-,root,root,-)
%doc README.md
%{_bindir}/%{name}
%{_datadir}/%{name}
%caps(cap_sys_admin=+ep) %{_datadir}/%{name}/chmns
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor
%{python3_sitelib}

%changelog
* Mon Oct  5 2015 mosquito <sensor.wen@gmail.com> - 0.13-1.git2baa049
- Update version to 0.13-1.git2baa049
* Wed May  6 2015 mosquito <sensor.wen@gmail.com> - 0.13-1.git0c69374
- Rename version name
* Tue Feb  3 2015 mosquito <sensor.wen@gmail.com> - 0.13git20150201-1
- Update version to 0.13git20150201
* Thu Jan 29 2015 mosquito <sensor.wen@gmail.com> - 0.13git20150126-1
- Update version to 0.13git20150126
* Sun Jan 25 2015 mosquito <sensor.wen@gmail.com> - 0.13git20150124-1
- Update version to 0.13git20150124
* Wed Jan 21 2015 mosquito <sensor.wen@gmail.com> - 0.13git20150119-1
- Update version to 0.13git20150119
* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 0.13git20150116-1
- Update version to 0.13git20150116
* Tue Dec 30 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141229-1
- Update version to 0.13git20141229
* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141226-1
- Update version to 0.13git20141226
* Fri Dec 26 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141225-1
- Update version to 0.13git20141225
* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141218-1
- Update version to 0.13git20141218
* Thu Dec 18 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141216-1
- Update version to 0.13git20141216
* Tue Dec 16 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141215-1
- Update version to 0.13git20141215
* Fri Dec 12 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141212-1
- Update version to 0.13git20141212
* Sun Nov 16 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141115-1
- Update version to 0.13git20141115
* Thu Nov 13 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141113-1
- Update version to 0.13git20141113
* Wed Oct 29 2014 mosquito <sensor.wen@gmail.com> - 0.13git20141029-1
- Update version to 0.13
* Fri Oct 10 2014 mosquito <sensor.wen@gmail.com> - 0.12git20140909-2
- Add comments
* Thu Oct  9 2014 mosquito <sensor.wen@gmail.com> - 0.12git20140909-1
- Initial build
