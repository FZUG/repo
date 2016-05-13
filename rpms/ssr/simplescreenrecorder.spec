%global debug_package %{nil}
%global project ssr
%global repo %{project}

# commit
%global _commit c580a19e6ab21146bffa74fe2ff5f774c53ec20f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           simplescreenrecorder
Version:        0.3.6
Release:        1.git%{_shortcommit}%{?dist}
Summary:        A feature-rich screen recorder that supports X11 and OpenGL
Summary(zh_CN): 一个功能丰富的屏幕录像软件, 支持录制 X11 和 OpenGL 程序

License:        GPLv3
Group:          Applications/Multimedia
Url:            http://www.maartenbaert.be/simplescreenrecorder
Source0:        https://github.com/MaartenBaert/ssr/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(QtCore) >= 4.8
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
Requires:       %{name}-lib = %{version}-%{release}

%description
SimpleScreenRecorder is a feature-rich screen recorder that supports X11 and OpenGL.
It has a Qt-based graphical user interface. It can record the entire screen or part
 of it, or record OpenGL applications directly. The recording can be paused and resumed
 at any time. Many different file formats and codecs are supported.
.
This package contains the main program.

%description -l zh_CN
SimpleScreenRecorder 是一个功能丰富的屏幕录像软件, 支持录制 X11 和 OpenGL 程序.
我的图形界面基于 Qt 开发. 我还能够记录整个或部分屏幕, 并可以直接记录 OpenGL 应用程序.
此外, 在任何时候都能方便的暂停和恢复记录. 并且我还支持许多不同的文件格式和编码器.
.
此包包含主程序.

%package lib
Summary:        %{name} GLInject library
Summary(zh_CN): %{name} 的 GLInject 库
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}

%description lib
SimpleScreenRecorder is a feature-rich screen recorder that supports X11 and OpenGL.
It has a Qt-based graphical user interface. It can record the entire screen or part
 of it, or record OpenGL applications directly. The recording can be paused and resumed
 at any time. Many different file formats and codecs are supported.
.
This package contains the GLInject library.

%description lib -l zh_CN
SimpleScreenRecorder 是一个功能丰富的屏幕录像软件, 支持录制 X11 和 OpenGL 程序.
我的图形界面基于 Qt 开发. 我还能够记录整个或部分屏幕, 并可以直接记录 OpenGL 应用程序.
此外, 在任何时候都能方便的暂停和恢复记录. 并且我还支持许多不同的文件格式和编码器.
.
此包包含 GLInject 库.

%prep
%setup -q -n %repo-%{_commit}

%build
export LDFLAGS="$LDFLAGS `pkg-config --libs-only-l libavformat libavcodec libavutil libswscale`"
export CPPFLAGS="$CPPFLAGS `pkg-config --cflags-only-I libavformat libavcodec libavutil libswscale`"
%configure \
%ifarch %{ix86} x86_64
    --disable-assert
%else
    --disable-x86-asm \
    --disable-glinjectlib
%endif
make %{?_smp_mflags}

%install
%make_install
rm -f %{buildroot}%{_libdir}/*.la
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
install -Dm 0644 %{buildroot}/%{_datadir}/icons/hicolor/256x256/apps/%{name}.png \
    %{buildroot}/%{_datadir}/pixmaps/%{name}.png

%post
update-desktop-database -q ||:
gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor ||:
/sbin/ldconfig

%postun
update-desktop-database -q ||:
gtk-update-icon-cache -q -t -f %{_datadir}/icons/hicolor ||:
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc *.txt *.md data/resources/about.htm
%license COPYING
%{_bindir}/%{name}
%{_bindir}/ssr-glinject
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_mandir}/man1/*

%files lib
%defattr(-,root,root,-)
%{_libdir}/libssr-glinject.so

%changelog
* Sun Dec 06 2015 mosquito <sensor.wen@gmail.com> - 0.3.6-1.gitc580a19
- Update version to 0.3.6-1.gic580a19

* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 0.3.3-2.git55d2c5c
- Update version to 0.3.3-2.git55d2c5c

* Sat May 09 2015 mosquito <sensor.wen@gmail.com> - 0.3.3-1.git3f84692
- Update version to 0.3.3-1.git3f84692

* Sat May 09 2015 mosquito <sensor.wen@gmail.com> - 0.3.3-1.gite2e9336
- Rename version name

* Fri Jan 23 2015 mosquito <sensor.wen@gmail.com> - 0.3.3git20150122-1
- Update version to 0.3.3git20150122

* Sun Jan 18 2015 mosquito <sensor.wen@gmail.com> - 0.3.2git20150117-1
- Update version to 0.3.2git20150117

* Mon Jan 12 2015 mosquito <sensor.wen@gmail.com> - 0.3.2git20150111-1
- Update version to 0.3.2git20150111

* Wed Jan 07 2015 mosquito <sensor.wen@gmail.com> - 0.3.2git20150104-1
- Update version to 0.3.2git20150104

* Sat Jan 03 2015 mosquito <sensor.wen@gmail.com> - 0.3.1git20150102-1
- Add Hebrew translation

* Wed Dec 31 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141231-1
- Add German translation

* Tue Dec 30 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141229-1
- Update version to 0.3.1git20141229

* Mon Dec 29 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141228-1
- Update version to 0.3.1git20141228

* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141218-1
- Update version to 0.3.1git20141218

* Sun Dec 07 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141204-1
- Update version to 0.3.1git20141204

* Thu Dec 04 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141203-1
- Update version to 0.3.1git20141203

* Mon Dec 01 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141130-1
- Update version to 0.3.1git20141130

* Tue Nov 25 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141124-1
- Update version to 0.3.1git20141124
- Fixed https://github.com/MaartenBaert/ssr/issues/267

* Mon Nov 24 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20141030-1
- Update version to 0.3.1git20141030

* Sun Nov 23 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20140926-2
- Delete 32-bit require

* Sat Nov 22 2014 mosquito <sensor.wen@gmail.com> - 0.3.1git20140926-1
- Add 32-bit require

* Tue Oct 14 2014 Nick Thom <nickth@fedoraproject.com> - 0.3.1
- Version Update

* Fri Jul 18 2014 Nick Thom <nickth@fedoraproject.com> - 0.3.0
- Initial package
