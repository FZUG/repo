%global debug_package %{nil}
%define helpdate 2015-02-09
%define zhcndate 20150118
%global project grub4dos
%global repo %{project}

# commit
%global _commit 31be3fea231b8fd5748e832d24ce454e793cd1a7
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		grub4dos
Version:	0.4.6a.20150807
Release:	1.git%{_shortcommit}%{?dist}
Summary:	This is GNU GRUB, the GRand Unified Bootloader
Summary(zh_CN):	多功能启动引导管理器

# https://raw.githubusercontent.com/chenall/grub4dos/master/COPYING
License:	GPLv2
Group:		Applications/System
Url:		https://code.google.com/p/grub4dos-chenall
Source0:	https://github.com/chenall/grub4dos/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
# http://ipxe.org (git clone --depth 1 git://git.ipxe.org/ipxe.git)
# find . -name ".git*" | xargs rm -f
Source1:	ipxe-a0f60d2.tar.xz
# https://code.google.com/p/grub4dos-help-doc
# http://bbs.wuyou.net/forum.php?mod=viewthread&tid=185938
Source2:	%{name}-help-%{helpdate}.chm
Source3:	https://grub4dos-chenall.googlecode.com/files/unifont.hex.gz
# git checkout 558e12a9b38613d827117c8da9b8e905c4c0eb2b , patch-chinese.diff
Source4:	patch-chinese-%{zhcndate}.diff

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	upx
BuildRequires:	nasm
BuildRequires:	xz-devel
BuildRequires:	/usr/bin/xxd
%ifarch x86_64
BuildRequires:	glibc-devel(x86-32)
BuildRequires:	libstdc++(x86-32)
BuildRequires:	libgcc(x86-32)
%endif

%description
This is GNU GRUB, the GRand Unified Bootloader. GRUB is intended to
provide important bootloader features that are missing from typical
personal computer BIOSes:

  - provides fully-featured command line and graphical interfaces
  - recognizes fdisk partitions and BSD disklabels
  - can dynamically read Linux ext2fs, ReiserFS, JFS and XFS, BSD ufs,
    MS-DOS FAT16 and FAT32, Minix fs, and VSTa fs filesystems, plus
    hardcoded blocklists
  - can boot Multiboot-compliant kernels (such as GNU Mach), as well
    as standard Linux and *BSD kernels

See the file NEWS for a description of recent changes to GRUB.

If you are interested in the network support, see the file
README.netboot under the directory netboot.

See the file INSTALL for instructions on how to build and install the
GRUB data and program files. See the GRUB manual for details about
using GRUB as your boot loader. Type "info grub" in the shell prompt.

Please visit the official web page of GNU GRUB, for more information.
The URL is <http://www.gnu.org/software/grub/grub.html>.

%description -l zh_CN
GNU GRUB 分为 GNU GRUB Legacy 和 GNU GRUB2. GNU GRUB 0.97 目前
已停止开发, 并改名为 GNU GRUB Lagecy. GNU GRUB2 取代原来的 GNU
GRUB Legacy.

GRUB4DOS 是 GNU GRUB Lagecy 的分支. 该项目最早由 不点 在 2003 年
发起. 目前主要由chenall, 不点, bean 和另外几位中国人维护.

特性:

  - 提供完整的命令行和图形接口
  - 可识别 fdisk 分区和 BSD 磁盘标签
  - 可动态读取 Linux ext2fs, ReiserFS, JFS 和 XFS, BSD ufs,
    MS-DOS FAT16 和 FAT32, Minix fs, VSTa fs 文件系统
  - 可多重引导 kernels (如 GNU Mach), 以及标准 Linux 及
    *BSD kernels

Grub4dos 相关信息: <https://code.google.com/p/grub4dos-chenall>
GNU GRUB 相关信息: <http://www.gnu.org/software/grub/grub.html>

%prep
%setup -q -a0 -a1 -n %{repo}-%{_commit}
cp %{S:2} .

%build
# Build grub4dos (build, autogen.sh, bootstrap.sh)
aclocal
autoheader
autoconf
automake -W no-portability -a -c

./configure --enable-preset-menu=preset_menu.lst --prefix=%{_prefix}
make clean
make

# Backup files
COPY_FILES="stage2/badgrub.exe stage2/grub.exe grub.pif \
stage2/grldr stage2/grldr.mbr stage2/grldr.pbr stage2/grldr_cd.bin \
stage2/bootlace.com stage2/hmload.com"
mkdir en
cp $COPY_FILES en/

# Generate bootlace64.com
Seek=$((0x`xxd -s 64 en/bootlace.com | awk -F: '/7f45/{print $1}'`)) # objdump, od, hexdump...
#Seek=$((0x`objdump -s en/bootlace.com | awk -F"4| " '/7f45/{print $3}'`))
dd if=en/bootlace.com of=bootlace.head bs=1 count=64 skip=$Seek
dd if=en/bootlace.com of=bootlace.body bs=1 skip=64
cat bootlace.head bootlace.body > en/bootlace64.com
# xxd -s $Seek -l 64 en/bootlace.com | sed -r '1,4s|^.{5}|00000|' > bootlace.dump
# xxd -s 64 en/bootlace.com >> bootlace.dump
# xxd -r bootlace.dump > en/bootlace64.com

# Build chinese version
patch -p1 < %{S:4}
make clean
make

# Build ipxegrldr
pushd ipxe/src
make %{?_smp_mflags} bin/undionly.kpxe \
 EMBED="%{_builddir}/%{repo}-%{_commit}/ipxegrldr.ipxe,%{_builddir}/%{repo}-%{_commit}/en/grldr"
popd

%install
# Install grub4dos files
install -Dm 0644 stage2/eltorito.sys %{buildroot}%{_datadir}/%{name}/eltorito.sys
cp en/* %{buildroot}%{_datadir}/%{name}/
chmod a-x %{buildroot}%{_datadir}/%{name}/bootlace.com

# Install chinese version
install -d %{buildroot}%{_datadir}/%{name}/chinese
cp stage2/badgrub.exe stage2/grldr stage2/grub.exe %{buildroot}%{_datadir}/%{name}/chinese/

# Install ipxegrldr
install ipxe/src/bin/undionly.kpxe %{buildroot}%{_datadir}/%{name}/ipxegrldr

# Install multi-language unifont file
install %{S:3} %{buildroot}%{_datadir}/%{name}/

# Example file
mkdir %{buildroot}%{_datadir}/%{name}/sample
cp menu.lst default config.sys %{buildroot}%{_datadir}/%{name}/sample/

# Example menu2.lst
cat > %{buildroot}%{_datadir}/%{name}/sample/menu2.lst <<EOF
## /menu.lst, /boot/grub/menu.lst, /grub/menu.lst
color blue/green yellow/red white/magenta white/magenta
timeout 30
## menu border color
color border=0xEEFFEE
## set vbe mode
graphicsmode -1 640:800 480:600 24:32 || graphicsmode -1 -1 -1 24:32
## loading splashimage
splashimage /boot/grub/splashimage.xpm || splashimage /boot/grub/splashimage.bmp
default /default
## Menu AutoNumber
write 0x8274 0x2001
## multi-language unifont
font /unifont.hex.gz
## 加载 unifont.hex.gz 即可使用中文菜单

title install fedora linux
kernel (hd0,0)/vmlinuz_fc20 repo=http://192.168.1.101/
initrd (hd0,0)/initrd_fc20.img

title install xubuntu linux
kernel (hd0,0)/vmlinuz boot=casper iso-scan/filename=/xubuntu-13.04-desktop-i386.iso quiet splash ro locale=zh_CN.UTF-8
initrd (hd0,0)/initrd.lz

title install linux
kernel (hd0,0)/vmlinuz
initrd (hd0,0)/initrd.img

title into linux rescue mode
kernel (hd0,0)/vmlinuz rescue
initrd (hd0,0)/initrd.img

title PE LiveISO
find --set-root --ignore-floppies --ignore-cd /PE.ISO
map /PE.ISO (0xff)
map --hook
chainloader (0xff)
savedefault --wait=2

title boot from local drive
checkrange 0x80 read 0x8280 && map (hd1) (hd0)
checkrange 0x80 read 0x8280 && map --hook
chainloader (hd0)+1

title commandline
commandline

title back to dos
quit

title reboot (重启)
reboot

title halt (关机)
halt

title maxdos.img
find --set-root --ignore-floppies --ignore-cd /boot/maxdos.img
map --mem /boot/maxdos.img (fd0)
map --hook
chainloader (fd0)+1
rootnoverify (fd0)

title change SYSLINUX menu
chainloader --force /boot/syslinux/syslinux.bin

title boot seagate update CC4H
find --set-root /CC4H.ISO
map /CC4H.ISO (0xff) || map --mem /CC4H.ISO (0xff)
map --hook
chainloader (0xff)
EOF

# Link files
mkdir %{buildroot}%{_bindir}
ln -sfv %{_datadir}/%{name}/bootlace.com %{buildroot}%{_bindir}/bootlace
ln -sfv %{_datadir}/%{name}/bootlace64.com %{buildroot}%{_bindir}/bootlace64

%post
chmod 0755 %{_datadir}/%{name}/bootlace.com
chmod 0755 %{_datadir}/%{name}/bootlace64.com

%files
%defattr(-,root,root,-)
%doc COPYING README* THANKS
%doc ChangeLog* %{name}-help-%{helpdate}.chm
%{_bindir}/bootlace*
%{_datadir}/%{name}

%changelog
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150807-1
- Update version to 0.4.6a.20150807
* Tue Jun 30 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150617-1
- Update version to 0.4.6a.20150617
* Tue May 19 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150518-1
- Update version to 0.4.6a.20150518
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150505-2
- Add buildrequire xz-devel
- Update docs
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150505-1
- Update version to 0.4.6a.20150505
- Rebuilt for GCC 5 C++11 ABI change
* Thu Mar 05 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150304-1
- Update version to 0.4.6a.20150304
* Fri Feb 06 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150205-1
- Update version to 0.4.6a.20150205
* Sun Jan 25 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150124-1
- Update version to 0.4.6a.20150124
* Fri Jan 23 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150122-1
- Update version to 0.4.6a.20150122
* Wed Jan 21 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150120-1
- Update version to 0.4.6a.20150120
* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150118-1
- Update version to 0.4.6a.20150118
- Add chinese version
* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150116-1
- Update version to 0.4.6a.20150116
* Fri Jan 16 2015 mosquito <sensor.wen@gmail.com> - 0.4.6a.20150114-1
- Update version to 0.4.6a.20150114
* Wed Jan 14 2015 mosquito <senosr.wen@gmail.com> - 0.4.6a.20150111
- Initial package
