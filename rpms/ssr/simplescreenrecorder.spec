%global debug_package %{nil}
%global project ssr
%global repo %{project}

# commit
%global _commit c20e56a8eabb2677b0c538d0d056ff48d4cfc971
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           simplescreenrecorder
Version:        0.3.8
Release:        1.git%{_shortcommit}%{?dist}
Summary:        A feature-rich screen recorder that supports X11 and OpenGL
Summary(zh_CN): 一个功能丰富的屏幕录像软件, 支持录制 X11 和 OpenGL 程序

License:        GPLv3
Group:          Applications/Multimedia
Url:            http://www.maartenbaert.be/simplescreenrecorder
Source0:        https://github.com/MaartenBaert/ssr/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(Qt5)
BuildRequires:  pkgconfig(Qt5X11Extras)
BuildRequires:  pkgconfig(alsa)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(jack)
BuildRequires:  pkgconfig(gl)
BuildRequires:  pkgconfig(glu)
BuildRequires:  pkgconfig(xi)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)
BuildRequires:  pkgconfig(xfixes)
BuildRequires:  qt5-linguist
BuildRequires:  libappstream-glib

Requires: hicolor-icon-theme
Obsoletes: %{name}-lib

%description
SimpleScreenRecorder is a feature-rich screen recorder that supports X11 and OpenGL.
It has a Qt-based graphical user interface. It can record the entire screen or part
 of it, or record OpenGL applications directly. The recording can be paused and resumed
 at any time. Many different file formats and codecs are supported.

%description -l zh_CN
SimpleScreenRecorder 是一个功能丰富的屏幕录像软件, 支持录制 X11 和 OpenGL 程序.
我的图形界面基于 Qt 开发. 我还能够记录整个或部分屏幕, 并可以直接记录 OpenGL 应用程序.
此外, 在任何时候都能方便的暂停和恢复记录. 并且我还支持许多不同的文件格式和编码器.

%prep
%autosetup -n %{repo}-%{_commit}

%build
export LDFLAGS="$LDFLAGS `pkg-config --libs-only-L libavformat libavcodec libavutil libswscale`"
export CPPFLAGS="$CPPFLAGS -fPIC `pkg-config --cflags-only-I libavformat libavcodec libavutil libswscale`"
%configure \
    --with-qt5 \
    --disable-static \
%ifnarch %{ix86} x86_64
    --disable-x86-asm \
%endif
%ifarch %{arm} aarch64
    --disable-glinjectlib
%endif
%nil
%make_build

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la
mkdir -p %{buildroot}%{_libdir}/%{name}
%ifnarch %{arm} aarch64
    mv %{buildroot}%{_libdir}/libssr-glinject.so \
       %{buildroot}%{_libdir}/%{name}/libssr-glinject.so
%endif

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

%files
%defattr(-,root,root,-)
%doc README.md AUTHORS.md CHANGELOG.md notes.txt todo.txt
%license COPYING
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_bindir}/ssr-glinject
%{_libdir}/%{name}/
%{_mandir}/man1/%{name}.1.*
%{_mandir}/man1/ssr-glinject.1.*
%{_datadir}/appdata/%{name}.appdata.xml

%changelog
* Thu Dec 01 2016 mosquito <sensor.wen@gmail.com> - 0.3.8-1.gitc20e56a
- Update version to 0.3.8-1.gitc20e56a

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
