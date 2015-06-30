%global debug_package %{nil}
%global project doubanfm-qt
%global repo %{project}

# commit
%global _commit c20734e86aac8175b3a801b5249ab834560ee1d1
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		doubanfm-qt
Version:	2.2
Release:	1.git%{_shortcommit}%{?dist}
Summary:	A douban.fm client written in Qt5
Summary(zh_CN):	基于 Qt5 编写的 douban.fm 客户端

Group:		Applications/Multimedia
License:	MIT
URL:		https://github.com/zonyitoo/doubanfm-qt
Source0:	https://github.com/zonyitoo/doubanfm-qt/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qtbase-gui
BuildRequires:	qt5-qtmultimedia-devel
BuildRequires:	pulseaudio-libs-devel
Requires:	gstreamer-plugins-ugly
Requires:	gstreamer1-plugins-ugly

%description
A douban.fm client written in pure Qt5.

%description -l zh_CN
基于 Qt5 编写的 douban.fm 客户端

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir build
pushd build
%{_qt5_qmake} ../%{name}.pro
make %{?_smp_mflags}

%install
# install douban.fm
install -Dm 0755 build/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 0644 QDoubanFM.png %{buildroot}%{_datadir}/icons/%{name}.png

# desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Encoding=UTF-8
Name=DoubanFM (qt5)
Name[zh_CN]=豆瓣FM (qt5)
Name[zh_TW]=豆瓣FM (qt5)
GenericName=DoubanFM Qt5 Client
GenericName[zh_CN]=DoubanFM Qt5 客户端
GenericName[zh_TW]=DoubanFM Qt5 客户端
Comment=A DoubanFM Client written in Qt5
Comment[zh_CN]=基于 Qt5 开发的 douban.fm 客户端
Comment[zh_TW]=基于 Qt5 开发的 douban.fm 客户端
Exec=%{name}
Icon=%{name}
Terminal=false
Categories=AudioVideo;Player;
EOF

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc ChangeLog Copyright README.md
%{_bindir}/%{name}
%{_datadir}/icons/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Wed Jul  1 2015 mosquito <sensor.wen@gmail.com> - 2.2-1.gitc20734e
- Update version to 2.2-1.gitc20734e
* Wed Jan  7 2015 mosquito <sensor.wen@gmail.com> - 2.2git20140611-2
- Add depends
* Tue Nov  4 2014 mosquito <sensor.wen@gmail.com> - 2.2git20140611-1
- Update version to 2.2git20140611
* Tue Oct 28 2014 mosquito <sensor.wen@gmail.com> - 2.2git20140503-1
- Initial build
