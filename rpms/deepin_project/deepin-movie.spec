Name:           deepin-movie
Version:        3.2.9
Release:        1%{?dist}
Summary:        Deepin movie based on mpv
Summary(zh_CN): 深度影音
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-movie-reborn
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake(Qt5Concurrent)
BuildRequires:  cmake(Qt5DBus)
BuildRequires:  cmake(Qt5LinguistTools)
BuildRequires:  cmake(Qt5Network)
BuildRequires:  cmake(Qt5Sql)
BuildRequires:  cmake(Qt5Widgets)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  pkgconfig(dtkcore)
BuildRequires:  pkgconfig(dtkwidget) >= 2.0.6
BuildRequires:  pkgconfig(dvdnav)
BuildRequires:  pkgconfig(libffmpegthumbnailer)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavresample)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libpulse-simple)
BuildRequires:  pkgconfig(mpv)
BuildRequires:  pkgconfig(openssl)
BuildRequires:  pkgconfig(xtst)
BuildRequires:  pkgconfig(xcb-aux)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-proto)
BuildRequires:  pkgconfig(xcb-shape)

%description
Deepin movie for deepin desktop environment.

%description -l zh_CN
深度影音播放器, 后端基于MPV, 支持解码大多数视频格式.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q -n %{name}-reborn-%{version}
sed -i '/dtk2/s|lib|libexec|' src/CMakeLists.txt

%build
%cmake -DCMAKE_BUILD_TYPE=Release
%make_build

%install
%make_install

%find_lang %{name} --with-qt

%files -f %{name}.lang
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/libdmr.so.*
%{_datadir}/%{name}/translations/%{name}*.qm
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg

%files devel
%{_includedir}/libdmr/*.h
%{_libdir}/pkgconfig/libdmr.pc
%{_libdir}/libdmr.so

%changelog
* Fri Aug 10 2018 mosquito <sensor.wen@gmail.com> - 3.2.9-1
- Update to 3.2.9

* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 3.2.8-1
- Update to 3.2.8

* Tue Mar 20 2018 mosquito <sensor.wen@gmail.com> - 3.2.3-1
- Update to 3.2.3

* Fri Feb 16 2018 mosquito <sensor.wen@gmail.com> - 3.2.0.3-1
- Update to 3.2.0.3

* Wed Jan 10 2018 mosquito <sensor.wen@gmail.com> - 3.2.0.2-1
- Update to 3.2.0.2

* Thu Dec 28 2017 Zamir SUN <sztsian@gmail.com> - 3.2.0-1
- Update to 3.2.0

* Wed Dec 20 2017 mosquito <sensor.wen@gmail.com> - 3.1.1-1
- Update to 3.1.1

* Mon Nov 27 2017 mosquito <sensor.wen@gmail.com> - 3.0.1-1
- Update to 3.0.1

* Wed Nov 15 2017 mosquito <sensor.wen@gmail.com> - 2.9.96-1
- Update to 2.9.96

* Fri Oct 27 2017 mosquito <sensor.wen@gmail.com> - 2.9.94-1
- Update to 2.9.94

* Fri Oct 13 2017 mosquito <sensor.wen@gmail.com> - 2.9.16-1
- Update to 2.9.16

* Thu Sep 21 2017 mosquito <sensor.wen@gmail.com> - 2.9.12-1
- Update to 2.9.12

* Thu Aug 24 2017 mosquito <sensor.wen@gmail.com> - 2.9.10-1
- Update to 2.9.10

* Sun Aug 06 2017 Zamir SUN <sztsian@gmail.com> - 2.2.14-2
- Remove group tag
- Fix rpmlint shebang error

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 2.2.14-1.git69123ed
- Update to 2.2.14

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 2.2.13-1.gita1ba8c3
- Update to 2.2.13

* Sat Jan 28 2017 mosquito <sensor.wen@gmail.com> - 2.2.11-2.git7896696
- Fix cannot register existing type 'GdkDisplayManager'

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 2.2.11-1.git7896696
- Update to 2.2.11

* Thu Jul 16 2015 mosquito <sensor.wen@gmail.com> - 2.2.2-2.git53adfc6
- python-peewee(>=2.3.0,<=2.4.4)
- remove some depends

* Sat Jul  4 2015 mosquito <sensor.wen@gmail.com> - 2.2.2-1.git53adfc6
- Initial build
