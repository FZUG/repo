%global __strip_shared %(test $(rpm -E%?fedora) -eq 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}
%global project QtAV
%global repo %{project}

%global _commit 519af919f6f6ebcb971dc9918c216a8715621c6e
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global with_llvm 0

Name:    qtav
Version: 1.9.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: A media playback framework based on Qt and FFmpeg
Summary(zh_CN): 基于Qt和FFmpeg的跨平台高性能音视频播放框架

License: LGPLv2.1
Group:   Development/Libraries
Url:     http://www.qtav.org
Source0: https://github.com/wang-bin/QtAV/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: libass-devel
BuildRequires: ffmpeg-devel
BuildRequires: openal-soft-devel
BuildRequires: libXv-devel
BuildRequires: libva-devel
BuildRequires: portaudio-devel
BuildRequires: pulseaudio-libs-devel
%if 0%{?with_llvm}
BuildRequires: clang
%endif

%description
QtAV is a multimedia playback library based on Qt and FFmpeg.
It can help you to write a player with less effort than ever before.

%description -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台多媒体播放库.
它能够帮助您花费较少的精力来编写高质量影音播放器.


%package sdk
Summary: FFmpeg powered multimedia playback SDK for Qt
Summary(zh_CN): 基于 FFmpeg 和 Qt 驱动的多媒体播放 SDK
Buildarch: noarch
Requires: qtav-devel = %{version}-%{release}
Requires: qtav-private-devel = %{version}-%{release}
Requires: qtav-qml-module = %{version}-%{release}

%description sdk
QtAV can help you to write a player with less effort than ever before.

Features include:
  * Hardware decoding suppprt: DXVA2, VAAPI, VDA, CedarX, CUDA.
  * OpenGL and ES2 support for Hi10P and other 16-bit YUV videos.
  * Video capture in rgb and yuv format.
  * OSD and custom filters.
  * filters in libavfilter, for example stero3d, blur.
  * Subtitle.
  * Transform video using GraphicsItemRenderer. (rotate, shear, etc)
  * Playing frame by frame (currently support forward playing).
  * Playback speed control. At any speed.
  * Variant streams: locale file, http, rtsp, etc.
  * Choose audio channel.
  * Choose media stream, e.g. play a desired audio track.
  * Multiple render engine support. Currently supports QPainter, GDI+, Direct2D, XV and OpenGL(and ES2).
  * Dynamically change render engine when playing.
  * Multiple video outputs for 1 player.
  * Region of interest(ROI), i.e. video cropping.
  * Video eq: brightness, contrast, saturation, hue.
  * QML support as a plugin. Most playback APIs are compatible with QtMultiMedia module.

%description sdk -l zh_CN
QtAV 能够帮助您花费较少的精力来编写高质量影音播放器.

功能特性:
  * 硬解码支持: DXVA2, VAAPI, VDA, CedarX, CUDA.
  * OpenGL, ES2 支持 Hi10P 和其他 16-bit YUV 视频.
  * 视频捕捉支持 rgb 和 yuv 格式.
  * 支持 OSD 和自定义过滤器.
  * 支持 libavfilter 过滤器, 可实现例如 stero3d, blur 特效.
  * 字幕.
  * 使用 GraphicsItemRenderer 转换视频. (旋转, 剪切等)
  * 逐帧播放 (目前仅支持向前播放).
  * 可控制播放速度. 支持任何速度.
  * 支持播放流媒体: 本地文件, http, rtsp 等.
  * 选择音频信道.
  * 选择媒体流, 如播放期望的音轨.
  * 多渲染引擎支持. 目前支持 QPainter, GDI+, Direct2D, XV 和 OpenGL(ES2).
  * 播放时动态修改渲染引擎.
  * 单播放器输出多视频.
  * Region of interest(ROI), 即视频裁剪.
  * 视频效果: 亮度, 对比度, 饱和度, 色调.
  * QML 支持插件. 大多数播放 API 兼容 QtMultiMedia 模式.


%package -n lib%{name}
Summary: QtAV library
Summary(zh_CN): QtAV 库

%description -n lib%{name}
QtAV is a multimedia playback library based on Qt and FFmpeg.
It can help you to write a player with less effort than ever before.

This package contains the QtAV library.

%description -n lib%{name} -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台多媒体播放库.
它能够帮助您花费较少的精力来编写高质量影音播放器.

此包包含 QtAV 程序库.


%package -n lib%{name}widgets
Summary: QtAV Widgets module
Summary(zh_CN): QtAV Widgets 模块
Requires: libqtav = %{version}-%{release}

%description -n lib%{name}widgets
QtAV is a multimedia playback library based on Qt and FFmpeg.
It can help you to write a player with less effort than ever before.

This package contains a set of widgets to play media.

%description -n lib%{name}widgets -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台多媒体播放库.
它能够帮助您花费较少的精力来编写高质量影音播放器.

此包包含 Widgets 模块.


%package devel
Summary: QtAV development files
Summary(zh_CN): QtAV 开发文件
Requires: libqtav = %{version}-%{release}
Requires: libqtavwidgets = %{version}-%{release}
Requires: qt5-qtbase-devel

%description devel
QtAV is a multimedia playback library based on Qt and FFmpeg.
It can help you to write a player with less effort than ever before.

This package contains the header development files for building some
QtAV applications using QtAV headers.

%description devel -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台多媒体播放库.
它能够帮助您花费较少的精力来编写高质量影音播放器.

此包包含编译基于 QtAV 开发的应用程序所需的头文件.


%package private-devel
Summary: QtAV private development files
Summary(zh_CN): QtAV 私有开发文件
Buildarch: noarch
Requires: qtav-devel = %{version}-%{release}

%description private-devel
QtAV is a multimedia playback library based on Qt and FFmpeg.
It can help you to write a player with less effort than ever before.

This package contains the private header development files for building some
QtAV applications using QtAV private headers.

%description private-devel -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台多媒体播放库.
它能够帮助您花费较少的精力来编写高质量影音播放器.

此包包含编译基于 QtAV private 头文件开发的应用程序所需的头文件.


%package qml-module
Summary: QtAV QML module
Summary(zh_CN): QtAV QML 模块

%description qml-module
QtAV is a multimedia playback library based on Qt and FFmpeg.
It can help you to write a player with less effort than ever before.

This package contains the QtAV QML module for Qt declarative.

%description qml-module -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台多媒体播放库.
它能够帮助您花费较少的精力来编写高质量影音播放器.

此包包含 QtAV QML 模块, 用于 Qt declarative.


%package players
Summary: QtAV/QML players
Summary(zh_CN): QtAV/QML 播放器
License: GPLv3
Requires: libqtav = %{version}-%{release}
Requires: libqtavwidgets = %{version}-%{release}
Requires: qtav-qml-module = %{version}-%{release}

%description players
QtAV is a multimedia playback framework based on Qt and FFmpeg.
High performance. User & developer friendly.

This package contains the QtAV based players.

%description players -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台高性能多媒体播放库.

此包包含基于 QtAV 开发的播放器.


%prep
%setup -q -n %repo-%{_commit}

%build
export QT_SELECT=qt5
export CPATH="`pkg-config --variable=includedir libavformat`"
mkdir build; pushd build
# debug mode: CONFIG+=debug
%if 0%{?with_llvm}
%{qmake_qt5} "CONFIG+=recheck" -spec linux-clang ..
%else
%{qmake_qt5} "CONFIG+=recheck" ..
%endif
make %{?_smp_mflags}

%install
%make_install INSTALL_ROOT=%{buildroot} -C build

rm -rf %{buildroot}%{_datadir}/{doc,icons}
rm -rf %{buildroot}%{_qt5_archdatadir}/bin/libcommon.*
rm -rf %{buildroot}%{_qt5_headerdir}/*.h

# link execution files
install -d %{buildroot}%{_bindir}
ln -sfv %{_qt5_bindir}/player %{buildroot}%{_bindir}
ln -sfv %{_qt5_bindir}/QMLPlayer %{buildroot}%{_bindir}
install -D src/QtAV.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/QtAV.svg

# library links
ln -sfv %{_libdir}/libQtAV.so %{buildroot}%{_libdir}/libQt5AV.so
ln -sfv %{_libdir}/libQtAVWidgets.so %{buildroot}%{_libdir}/libQt5AVWidgets.so

# strip files
%{__strip_shared}

%post devel -p /sbin/ldconfig
%post qml-module -p /sbin/ldconfig
%post -n lib%{name} -p /sbin/ldconfig
%post -n lib%{name}widgets -p /sbin/ldconfig

%post players
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun devel -p /sbin/ldconfig
%postun qml-module -p /sbin/ldconfig
%postun -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name}widgets -p /sbin/ldconfig

%postun players
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans players
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files sdk
%defattr(-,root,root,-)
%doc README.md Changelog
%license lgpl-2.1.txt

%files -n lib%{name}
%defattr(-,root,root,-)
%doc README.md Changelog
%license lgpl-2.1.txt
%{_libdir}/libQtAV.so.*

%files -n lib%{name}widgets
%defattr(-,root,root,-)
%doc README.md Changelog
%license lgpl-2.1.txt
%{_libdir}/libQtAVWidgets.so.*

%files devel
%defattr(-,root,root,-)
%doc README.md Changelog
%license lgpl-2.1.txt
%{_qt5_headerdir}/QtAV/*.h
%{_qt5_headerdir}/QtAV/QtAV
%{_qt5_headerdir}/QtAVWidgets/*.h
%{_qt5_headerdir}/QtAVWidgets/QtAVWidgets
%{_libdir}/libQtAV.so
%{_libdir}/libQtAV.prl
%{_libdir}/libQt5AV.so
%{_libdir}/libQtAVWidgets.so
%{_libdir}/libQtAVWidgets.prl
%{_libdir}/libQt5AVWidgets.so
%{_qt5_archdatadir}/mkspecs/features/av.prf
%{_qt5_archdatadir}/mkspecs/features/avwidgets.prf
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_av.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_avwidgets.pri

%files private-devel
%defattr(-,root,root,-)
%doc README.md Changelog
%license lgpl-2.1.txt
%{_qt5_headerdir}/QtAV/%{_qt5_version}/QtAV/private/*.h
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_av_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_avwidgets_private.pri

%files qml-module
%defattr(-,root,root,-)
%doc README.md Changelog
%license lgpl-2.1.txt
%{_qt5_archdatadir}/qml/QtAV/libQmlAV.so
%{_qt5_archdatadir}/qml/QtAV/plugins.qmltypes
%{_qt5_archdatadir}/qml/QtAV/qmldir
%{_qt5_archdatadir}/qml/QtAV/Video.qml

%files players
%defattr(-,root,root,-)
%doc README.md Changelog
%license gpl-3.0.txt
%{_qt5_bindir}/player
%{_qt5_bindir}/QMLPlayer
%{_bindir}/player
%{_bindir}/QMLPlayer
%{_datadir}/applications/player.desktop
%{_datadir}/applications/QMLPlayer.desktop
%{_datadir}/icons/hicolor/*/apps/QtAV.svg


%changelog
* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 1.9.0-1.git519af91
- Update version to 1.9.0-1.git519af91
* Tue Dec  8 2015 mosquito <sensor.wen@gmail.com> - 1.8.0-3.git83f5236
- Update version to 1.8.0-3.git83f5236
- Hardened package
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 1.8.0-2.git37f4a54
- Update version to 1.8.0-2.git37f4a54
* Thu Sep  3 2015 mosquito <sensor.wen@gmail.com> - 1.8.0-1.git8f8ae59
- Update version to 1.8.0-1.git8f8ae59
* Sat Jul 11 2015 mosquito <sensor.wen@gmail.com> - 1.7.0-1.git68322f8
- Update version to 1.7.0-1.git68322f8
- fix qtav gcc5 -O2 build error
* Sat Jul  4 2015 mosquito <sensor.wen@gmail.com> - 1.6.0-1.gitbd257ec
- Update version to 1.6.0-1.gitbd257ec
* Thu Mar  5 2015 mosquito <sensor.wen@gmail.com> - 1.5.0git20150304-1
- Update version to 1.5.0git20150304
* Tue Feb  3 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150203-1
- Update version to 1.4.2git20150203
* Thu Jan 29 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150128-1
- Update version to 1.4.2git20150128
* Sun Jan 25 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150123-1
- Update version to 1.4.2git20150123
* Wed Jan 21 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150121-1
- Update version to 1.4.2git20150121
* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150117-1
- Update version to 1.4.2git20150117
* Fri Jan 16 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150115-1
- Update version to 1.4.2git20150115
* Mon Jan 12 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150110-1
- Update version to 1.4.2git20150110
* Wed Jan  7 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20150106-1
- Update version to 1.4.2git20150106
* Thu Jan  1 2015 mosquito <sensor.wen@gmail.com> - 1.4.2git20141231-1
- Update version to 1.4.2git20141231
* Tue Dec 30 2014 mosquito <sensor.wen@gmail.com> - 1.4.2git20141230-1
- Update version to 1.4.2git20141230
* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 1.4.2git20141227-1
- Update version to 1.4.2git20141227
* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141223-1
- Update version to 1.4.1git20141223
* Tue Dec 16 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141215-1
- Update version to 1.4.1git20141215
* Mon Dec  8 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141207-1
- Update version to 1.4.1git20141207
* Wed Dec  3 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141202-1
- Update version to 1.4.1git20141202
* Tue Dec  2 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141201-1
- Update version to 1.4.1git20141201
* Fri Nov 28 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141128-1
- Update version to 1.4.1git20141128
* Tue Nov 25 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141125-1
- Update version to 1.4.1git20141125
* Tue Nov 18 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141118-1
- Update version to 1.4.1git20141118
* Sun Nov 16 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141115-1
- Update version to 1.4.1git20141115
* Sat Nov 15 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141114-1
- Update version to 1.4.1git20141114
* Thu Nov 13 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141112-2
- Fixed library name for qtav-devel
* Wed Nov 12 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141112-1
- Update version to 1.4.1git20141112
* Tue Nov 11 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141111-1
- Update version to 1.4.1git20141111
* Tue Nov 11 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141110-2
- Rebuild
* Mon Nov 10 2014 mosquito <sensor.wen@gmail.com> - 1.4.1git20141110-1
- Update version to 1.4.1git20141110
* Tue Nov  4 2014 mosquito <sensor.wen@gmail.com> - 1.4.0git20141104-1
- Update version to 1.4.0git20141104
* Mon Oct 13 2014 mosquito <sensor.wen@gmail.com> - 1.4.0git20141013-1
- Update version to 1.4.0git20141013
* Fri Oct  3 2014 mosquito <sensor.wen@gmail.com> - 1.4.0git20141001-1
- Initial build
