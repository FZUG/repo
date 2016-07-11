%global __strip_shared %(test $(rpm -E%?fedora) -eq 23 && echo "/usr/lib/rpm/brp-strip-shared %{__strip}" ||:)
%global debug_package %{nil}
%global project QtAV
%global repo %{project}

%global _commit ba14c2ae9448bda7b252d8cdea0fb6f45ec84270
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global with_llvm 0

Name:    qtav
Version: 1.11.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: A media playback framework based on Qt and FFmpeg
Summary(zh_CN): 基于Qt和FFmpeg的跨平台高性能音视频播放框架

License: LGPLv2+ and GPLv3 and BSD
Group:   Development/Libraries
Url:     http://www.qtav.org/
Source0: https://github.com/wang-bin/QtAV/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: desktop-file-utils
BuildRequires: qt5-qtbase-devel
BuildRequires: qt5-qtdeclarative-devel
BuildRequires: libass-devel
BuildRequires: ffmpeg-devel
BuildRequires: openal-soft-devel
BuildRequires: libXv-devel
BuildRequires: libva-devel
BuildRequires: pulseaudio-libs-devel
%if 0%{?with_llvm}
BuildRequires: clang
%endif
Requires: hicolor-icon-theme

%description
QtAV is a multimedia playback library based on Qt and FFmpeg.
It can help you to write a player with less effort than ever before.

Features include:
  * Hardware decoding support: DXVA2, VAAPI, VDA, CedarX, CUDA.
  * OpenGL and ES2 support for Hi10P and other 16-bit YUV videos.
  * Real time preview.
  * Video capture in RGB and YUV format.
  * OSD and custom filters.
  * Filters in libavfilter, for example stero3d, blur.
  * Subtitle track select. Dynamic change FFmpeg and libass engine.
  * Transform video using GraphicsItemRenderer. (rotate, shear, etc)
  * Playing frame by frame.
  * Playback speed control.
  * Variant streams: locale file, HTTP, RTSP, etc. and your custom streams.
  * Audio channel, tracks and external audio tracks.
  * Choose media stream, e.g. play a desired audio track.
  * Multiple render engine support. Currently supports QPainter, GDI+,
    Direct2D, XV and OpenGL(and ES2).
  * Dynamically change render engine when playing.
  * Dynamically change video decoder.
  * Multiple video outputs for 1 player.
  * Video eq(software and OpenGL): brightness, contrast, saturation, hue.
  * QML support as a plugin. Most playback APIs are compatible with
    QtMultiMedia module.
  * Compatiblity: QtAV can be built with both Qt4 and Qt5, FFmpeg(>=1.0)
    and Libav (>=9.0). Latest FFmpeg release is recommended.

%description -l zh_CN
QtAV 是一款基于 Qt 和 FFmpeg 的跨平台多媒体播放库.
它能够帮助您花费较少的精力来编写高质量影音播放器.

功能特性:
  * 硬解码支持: DXVA2, VAAPI, VDA, CedarX, CUDA.
  * OpenGL, ES2 支持 Hi10P 和其他 16-bit YUV 视频.
  * 实时预览.
  * 视频捕捉支持 RGB 和 YUV 格式.
  * 支持 OSD 和自定义过滤器.
  * 支持 libavfilter 过滤器, 可实现例如 stero3d, blur 特效.
  * 可选字幕. 动态更改 FFmpeg 和 libass 引擎.
  * 使用 GraphicsItemRenderer 转换视频. (旋转, 剪切等)
  * 逐帧播放.
  * 可控制播放速度. 支持任何速度.
  * 支持播放流媒体: 本地文件, HTTP, RTSP 以及自定义流.
  * 选择音频声道, 音轨和外部音轨.
  * 选择媒体流, 如播放期望的音轨.
  * 多渲染引擎支持. 目前支持 QPainter, GDI+, Direct2D, XV 和 OpenGL(ES2).
  * 播放时动态更改渲染引擎.
  * 动态更改视频解码器.
  * 单播放器输出多视频.
  * Region of interest(ROI), 即视频裁剪.
  * 视频效果(软件和OpenGL): 亮度, 对比度, 饱和度, 色调.
  * QML 支持插件. 大多数播放 API 兼容 QtMultiMedia 模式.
  * 兼容性: QtAV 支持使用 Qt4 或 Qt5, FFmpeg(>=1.0) 或 Libav(>=9.0) 编译.
    建议使用最新版本的 FFmpeg.


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
#Requires: libqtav%%{?_isa} = %%{version}-%%{release}

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
Requires: libqtav%{?_isa} = %{version}-%{release}
Requires: libqtavwidgets%{?_isa} = %{version}-%{release}
Requires: qtav-qml-module%{?_isa} = %{version}-%{release}
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
#Requires: libqtav%%{?_isa} = %%{version}-%%{release}
#Requires: libqtavwidgets%%{?_isa} = %%{version}-%%{release}
Requires: qtav-qml-module%{?_isa} = %{version}-%{release}

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
%{qmake_qt5} CONFIG+="no_rpath recheck config_libass_link" -spec linux-clang ..
%else
%{qmake_qt5} CONFIG+="no_rpath recheck config_libass_link" ..
%endif
make %{?_smp_mflags}

%install
%make_install INSTALL_ROOT=%{buildroot} -C build

rm -rf %{buildroot}%{_datadir}/{doc,icons}
rm -rf %{buildroot}%{_qt5_archdatadir}/bin/libcommon.*
rm -rf %{buildroot}%{_qt5_headerdir}/*.h

# link execution files
install -d %{buildroot}%{_bindir}
ln -sfv %{_qt5_bindir}/Player %{buildroot}%{_bindir}
ln -sfv %{_qt5_bindir}/QMLPlayer %{buildroot}%{_bindir}
install -Dm644 src/QtAV.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/QtAV.svg

# library links
ln -sfv %{_libdir}/libQtAV.so %{buildroot}%{_libdir}/libQt5AV.so
ln -sfv %{_libdir}/libQtAVWidgets.so %{buildroot}%{_libdir}/libQt5AVWidgets.so

# strip files
%{__strip_shared}

%post -n lib%{name} -p /sbin/ldconfig
%post -n lib%{name}widgets -p /sbin/ldconfig

%post players
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun -n lib%{name} -p /sbin/ldconfig
%postun -n lib%{name}widgets -p /sbin/ldconfig

%postun players
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans players
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

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
%dir %{_qt5_headerdir}/QtAV/
%dir %{_qt5_headerdir}/QtAVWidgets/
%{_qt5_headerdir}/QtAV/*
%{_qt5_headerdir}/QtAVWidgets/*
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
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_av_private.pri
%{_qt5_archdatadir}/mkspecs/modules/qt_lib_avwidgets_private.pri

%files qml-module
%defattr(-,root,root,-)
%doc README.md Changelog
%license lgpl-2.1.txt
%dir %{_qt5_archdatadir}/qml/QtAV/
%{_qt5_archdatadir}/qml/QtAV/libQmlAV.so
%{_qt5_archdatadir}/qml/QtAV/plugins.qmltypes
%{_qt5_archdatadir}/qml/QtAV/qmldir
%{_qt5_archdatadir}/qml/QtAV/Video.qml

%files players
%defattr(-,root,root,-)
%doc README.md Changelog
%license gpl-3.0.txt
%{_qt5_bindir}/Player
%{_qt5_bindir}/QMLPlayer
%{_bindir}/Player
%{_bindir}/QMLPlayer
%{_datadir}/applications/Player.desktop
%{_datadir}/applications/QMLPlayer.desktop
%{_datadir}/icons/hicolor/*/apps/QtAV.svg


%changelog
* Mon Jul 11 2016 mosquito <sensor.wen@gmail.com> - 1.11.0-1.gitba14c2a
- Update version to 1.11.0-1.gitba14c2a
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 1.10.0-2.gitc8f88a0
- Update version to 1.10.0-2.gitc8f88a0
* Sun Mar  6 2016 mosquito <sensor.wen@gmail.com> - 1.10.0-1.git1f53443
- Update version to 1.10.0-1.git1f53443
* Thu Feb 11 2016 mosquito <sensor.wen@gmail.com> - 1.9.0-3.gited374dc
- Update version to 1.9.0-3.gited374dc
- added BReq desktop-file-utils, Req hicolor-icon-theme
- removed BReq portaudio-devel
- removed empty sdk sub-package
- append private-devel files to devel sub-package
- removed ldconfig for devel sub-package
- added QMAKE flag CONFIG+=no_rpath
* Sat Feb  6 2016 mosquito <sensor.wen@gmail.com> - 1.9.0-2.gitfafd3b0
- Update version to 1.9.0-2.gitfafd3b0
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
