# https://github.com/archlinuxcn/repo/blob/master/sandbox/PKGBUILD
# https://wiki.debian.org/Sandbox
%global debug_package %{nil}

Name:       sandbox
Version:    2.11
Release:    1%{?dist}
Summary:    Gentoo sandbox tool to run programs in a "sandboxed" environment
Group:      Applications/System
License:    GPLv2+
URL:        https://www.gentoo.org
Source0:    https://gitweb.gentoo.org/proj/%{name}.git/snapshot/%{name}-%{version}.tar.xz

BuildRequires: libtool, libtool-ltdl-devel
BuildRequires: autoconf, automake, m4

%description
Gentoo Sandbox is a library (and utility) to run programs in a "sandboxed"
environment. This is used as a QA measure to try and prevent applications from
modifying files they should not.

For example, in the Gentoo world we use it so we can build applications as root
and make sure that the build system does not do crazy things outside of its
build directory.  Such as install files to the live root file system or modify
config files on the fly.

For people who are familiar with the Debian "fakeroot" project or the RPM based
"InstallWatch", sandbox is in the same vein of projects.

%description -l zh_CN
Gentoo Sandbox 为应用程序提供隔离的沙箱环境. 它常作为 QA 的额外保护措施, 阻止
应用程序修改工作目录之外的文件.

例如, 在 Gentoo 系统中, 我们在编译目录构建程序, 使用 Sandbox 确保构建过程不
影响编译目录外的系统配置.

Sandbox 与人们所熟悉的 Debian 的 "fakeroot", 和基于 RPM 的 "InstallWatch" 有
异曲同工的作用.

%prep
%setup -q
# change banner
sed -i '/path/s|Gentoo|Fedora|' src/sandbox.c

%build
autoreconf --install --force
%configure
make %{?_smp_mflags}

%install
%make_install
mv %{buildroot}%{_bindir}/{%{name},%{name}-shell}
sed -i '/Exec/s|%{name}|%{name}-shell|' \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

# change SANDBOX_LIB variable
sed -i '/GNU/aexport SANDBOX_LIB=%{_libdir}/lib%{name}.so\nunset LD_PRELOAD' \
    %{buildroot}%{_datadir}/%{name}/%{name}.bashrc

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:
/sbin/ldconfig

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:
/sbin/ldconfig

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc AUTHORS README NEWS
%license COPYING
%{_sysconfdir}/%{name}*
%{_bindir}/%{name}-shell
%{_libdir}/lib%{name}.so
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}*
%{_datadir}/%{name}/%{name}.bashrc

%changelog
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 2.11-1
- Release 2.11
* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 2.10-1
- Release 2.10
* Mon Oct 26 2015 mosquito <sensor.wen@gmail.com> - 2.9-1
- Initial build
