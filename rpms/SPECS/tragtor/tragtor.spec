%global debug_package %{nil}

Name:		tragtor
Version:	0.9.2
Release:	1%{?dist}
Summary:	A GUI for FFmpeg for audio and video-conversion
Summary(zh_CN):	基于 FFmpeg 的音视频转换器

Group:		Applications/Multimedia
License:	LGPL v2.1
URL:		http://mein-neues-blog.de/tragtor-gui-for-ffmpeg
Source0:	http://repository.mein-neues-blog.de:9000/archive/%{name}-%{version}_all.tar.gz
Buildarch:	noarch
Requires:	pygtk2 ffmpeg id3v2

%description
traGtor is a graphical user interface (GUI) for the awesome conversion tool
ffmpeg for the use with Linux-OS. It is written in Python and uses the
GTK-Engine (standard in GNOME desktops) for displaying its interface. The goal
of traGtor is not to bring you all of the features ffmpeg offers, but to be
a fast and user friendly choice for converting a single media file into any
other format. For a full ffmpeg featuring GUI please refer to the other great
projects listed below. This GUI is written for not dealing too much with
command lines, options and parameters and so on, and refers mostly to the
real keyboard haters.

One may edit the command line sent to ffmpeg to fit all of his needs, but for
those cases the more command line oriented tools (with nice GUIs too) could be
the better choice. But if you need a tool for click oriented and flawless
conversion like stripping an mp3 from a youtube movie, resizing and recoding
a clip to fit your mobiles screen or just changing the format of a movie-file
to be able to play it in a flash-media-player traGor may be Mr.Right for you.

%prep
%setup -q -c %{name}

%build

%install
# desktop file
cat > usr/share/applications/tragtor.desktop << EOF
[Desktop Entry]
Name=traGtor
GenericName=traGtor
Comment=a GUI for FFmpeg for audio and video-conversion
Type=Application
Exec=tragtor %F
Icon=tragtor
Terminal=false
Categories=AudioVideo;AudioVideoEditing;
MimeType=video/dv;video/mpeg;video/x-mpeg;video/msvideo;video/quicktime;video/x-anim;video/x-avi;video/x-ms-asf;video/x-ms-wmv;video/x-msvideo;video/x-nsv;video/x-flc;video/x-fli;application/ogg;application/x-ogg;application/x-matroska;audio/x-mp3;audio/x-mpeg;audio/mpeg;audio/x-wav;audio/x-mpegurl;audio/x-scpls;audio/x-m4a;audio/x-ms-asf;audio/x-ms-asx;audio/x-ms-wax;application/vnd.rn-realmedia;audio/x-real-audio;audio/x-pn-realaudio;application/x-flac;audio/x-flac;application/x-shockwave-flash;misc/ultravox;audio/vnd.rn-realaudio;audio/x-pn-aiff;audio/x-pn-au;audio/x-pn-wav;audio/x-pn-windows-acm;image/vnd.rn-realpix;video/vnd.rn-realvideo;audio/x-pn-realaudio-plugin;application/x-extension-mp4;audio/mp4;video/mp4;video/mp4v-es;x-content/video-vcd;x-content/video-svcd;x-content/video-dvd;x-content/audio-cdda;x-content/audio-player;video/x-flv;
X-KDE-StartupNotify=true
EOF

# program version
sed -i '/_TITLE/s|0.8|%{version}|' usr/share/%{name}/%{name}.py

install -Dm 755 usr/bin/tragtor %{buildroot}%{_bindir}/%{name}
install -Dm 644 usr/share/applications/tragtor.desktop \
    %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm 644 usr/share/pixmaps/tragtor.svg \
    %{buildroot}%{_datadir}/pixmaps/%{name}.svg
cp -r usr/share/tragtor %{buildroot}%{_datadir}/

%files
%defattr(-,root,root,-)
%doc usr/share/doc/%{name}/*
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.svg

%changelog
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 0.9.2-1
- Update version 0.9.2
* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 0.9.1-1
- Update version 0.9.1
* Thu Mar 05 2015 mosquito <sensor.wen@gmail.com> - 0.9.0-1
- Update version 0.9.0
* Thu Dec 11 2014 mosquito <sensor.wen@gmail.com> - 0.8.82-1
- Update version 0.8.82
* Wed Sep 25 2013 Huaren Zhong <huaren.zhong@gmail.com> - 0.8.55
- Rebuild for Fedora
* Sat Jul 14 2012 - joerg.lorenzen@ki.tng.de
- update to version 0.8.55
* Tue Jul 03 2012 - joerg.lorenzen@ki.tng.de
- update to version 0.8.54
* Mon May 07 2012 - joerg.lorenzen@ki.tng.de
- update to version 0.8.53
* Sun Apr 22 2012 - joerg.lorenzen@ki.tng.de
- update to version 0.8.52
* Tue Apr 17 2012 - joerg.lorenzen@ki.tng.de
- update to version 0.8.50
* Tue Mar 06 2012 - joerg.lorenzen@ki.tng.de
- update to version 0.8.48
* Sun Nov 27 2011 - joerg.lorenzen@ki.tng.de
- update to version 0.8.45
* Sun Nov 27 2011 - joerg.lorenzen@ki.tng.de
- update to version 0.8.43
* Fri Oct 14 2011 - joerg.lorenzen@ki.tng.de
- update to version 0.8.41
* Fri Jul 22 2011 - joerg.lorenzen@ki.tng.de
- Initial package, version 0.8.37
