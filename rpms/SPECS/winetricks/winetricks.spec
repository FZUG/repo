%global debug_package %{nil}
%global project winetricks

%global repo %{project}
%global _commit 4c2dc6ce393082a53b7045ba9b70af7320c3a170
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global zh_repo winetricks-zh
%global zh_commit 37e58cf75bdf0efcf8dfcb8f0e8ce1348a2ed604
%global zh_scommit %(c=%{zh_commit}; echo ${c:0:7})

Name:    winetricks
Version: 20160219
Release: 1.git%{_shortcommit}%{?dist}
Summary: an easy way to install program in Wine
Summary(zh_CN): 快速为 Wine 安装应用程序

Group:   Applications/Internet
License: GPL
URL:     http://winetricks.org
Source0: https://github.com/Winetricks/winetricks/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source1: https://github.com/hillwoodroc/winetricks-zh/archive/%{zh_commit}/%{zh_repo}-%{zh_scommit}.tar.gz

BuildArch: noarch
Requires: cabextract p7zip unzip wget
Requires: zenity xdg-utils sudo gksu-polkit
Requires: wine

%description
Winetricks is an easy way to work around problems in Wine.

It has a menu of supported games/apps for which it can do
all the workarounds automatically. It also lets you install
missing DLLs or tweak various Wine settings individually.

Help: http://wiki.winehq.org/winetricks

%description -l zh_CN
Winetricks 是一个 Shell 脚本, 用于在 Wine 中安装应用.

它包含一个游戏/应用菜单, 可自动完成所有安装, 开箱即用.
它可以安装程序所需 DLL 库或单独调整各种 Wine 设置.

帮助: http://wiki.winehq.org/winetricks_cn

%prep
%setup -q -a1 -n %repo-%{_commit}

%build
# Builtin Verbs: Runtimes, Fonts, Apps, Benchmarks, Games
Total=$(cat src/winetricks|wc -l)
LineNum=$(($(grep -n Apps src/winetricks|cut -d: -f1)+2))
head -n $LineNum src/winetricks > top
tail -n $(expr $Total - $LineNum) src/winetricks > bottom

# delete qq
sed -i '/qq apps/,+93d' bottom

pushd %{zh_repo}-%{zh_commit}/verb
for i in *.verb; do
    cat $i >> ../../top
    echo -e "\n#----------------------------------------------------------------\n" >> ../../top
done
popd
cat top bottom > %{name}

%install
install -Dm 755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dm 644 src/%{name}.1 %{buildroot}%{_mandir}/man1/%{name}.1

# Verbs
install -d %{buildroot}%{_datadir}/%{name}/verbs
cp %{zh_repo}-%{zh_commit}/verb/* %{buildroot}%{_datadir}/%{name}/verbs/

%files
%defattr(-,root,root,-)
%doc README.md
%license src/COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}/verbs
%{_mandir}/man1/%{name}.1.gz

%changelog
* Sat Feb 27 2016 mosquito <sensor.wen@gmail.com> - 20160219-1.git4c2dc6c
- Update to 20160219-1.git4c2dc6c
* Mon Jan 18 2016 mosquito <sensor.wen@gmail.com> - 20160109-1.git07ba4a0
- Update to 20160109-1.git07ba4a0
* Tue Dec 22 2015 mosquito <sensor.wen@gmail.com> - 20151116-1.gitca1a031
- Update to 20151116-1.gitca1a031
* Sat Jul  4 2015 mosquito <sensor.wen@gmail.com> - 20150702-1.git7ac3ae0
- Initial build
