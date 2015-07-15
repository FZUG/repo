%global debug_package %{nil}
%global project deepin-movie
%global repo %{project}

# commit
%global _commit 53adfc630db338acfc4bd188b7b8468f8c3380e3
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name: deepin-movie
Version: 2.2.2
Release: 2.git%{_shortcommit}%{?dist}
Summary: Deepin Movie
Summary(zh_CN): 深度影音

License: GPLv3
Group: Applications/Multimedia
URL: https://github.com/linuxdeepin/deepin-movie
Source0: https://github.com/linuxdeepin/deepin-movie/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: python-devel

Requires: python-qt5
Requires: mediainfo
Requires: python-xpyb
Requires: python-magic
Requires: fontconfig-devel
Requires(post): python-pip

Requires: qtav-qml-module
Requires: python-xpybutil
Requires: deepin-utils
Requires: deepin-menu
Requires: deepin-qml-widgets
Requires: dde-qml-dbus-factory

# arch deps
Requires: qt5-qtquickcontrols
Requires: qt5-qtgraphicaleffects
Requires: enca

%description
Deepin movie with linuxdeepin desktop environment.

%description -l zh_CN
深度影音播放器, 后端基于QtAV, 支持解码大多数视频格式.

%prep
%setup -q -n %repo-%{_commit}

%build

%install
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_datadir}/{applications,%{name}}
install -D src/views/image/%{name}.svg \
  %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
cp -r src/* %{buildroot}%{_datadir}/%{name}/
rm -rf %{buildroot}%{_datadir}/%{name}/tests
cp %{name}.desktop %{buildroot}%{_datadir}/applications/
ln -sfv %{_datadir}/%{name}/main.py %{buildroot}%{_bindir}/%{name}

# generate locale
pushd locale
for i in *.po
do
    mkdir -p %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/
    msgfmt $i -o %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/%{name}.mo
done
popd

%find_lang %{name}

%post
if [ $1 -eq 1 ]; then
pip install -U -q ass pysrt 'peewee>=2.3.0,<=2.4.4' &>/dev/null ||:
fi
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%postun
if [ $1 -eq 0 ]; then
pip uninstall -y -q ass pysrt peewee &>/dev/null ||:
fi
update-desktop-database -q ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*

%changelog
* Thu Jul 16 2015 mosquito <sensor.wen@gmail.com> - 2.2.2-2.git53adfc6
- python-peewee(>=2.3.0,<=2.4.4)
- remove some depends
* Sat Jul  4 2015 mosquito <sensor.wen@gmail.com> - 2.2.2-1.git53adfc6
- Initial build
