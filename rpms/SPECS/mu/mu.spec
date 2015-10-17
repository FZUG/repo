%global debug_package %{nil}
%global project Mu
%global repo %{project}

# commit
%global _commit c1c72c78fcf42e75751bf6c66cdadf272d0d4879
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    mu
Version: 0.9.147
Release: 1.git%{_shortcommit}%{?dist}
Summary: Incredible music manager
Summary(zh_CN): 为音乐而生的播放器
Group:   Applications/Multimedia
License: GPLv2
Url:     https://kreogist.github.io/Mu
Source0: https://github.com/Kreogist/Mu/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: qt5-qtbase-devel
BuildRequires: phonon-qt5-devel
BuildRequires: ffmpeg-devel
BuildRequires: desktop-file-utils
Requires: phonon-qt5-backend-gstreamer
Requires: gstreamer1-plugins-bad-free
Requires: gstreamer1-plugins-ugly
Requires: gstreamer1-libav

%description
Kreogist Mu is a cross-platform incredible music manager/player based on Qt.

Feature:
- Support manage all your music including the following formats:
 mp3, m4a, wav, flac, ape, ogg, tta, aiff, aifc, aif, mp4, mpa,
 mp2, mp1, midi, mid, mp3pro, mpc, aac, cda, wma, fla, tak, mp+,
 aa, ra, mac, rmi, dtswav, dts, snd, au, ac3, xm, and umx.
- Support play all your music including the following formats:
 mp3, m4a, wav, flac, ape, mpc, wv, ac3, spx, wma.
- Support read ID3v1, ID3v2, APEv2 format tag, and read metadata
 information from FLAC, WMA, M4A and WAV files.
- Support import m3u, ttpl, wpl, xspf and iTunes xml format playlists.
- Support automatically download lyrics from TTPlayer, TTPod,
 XiaMi, QQMusic and Baidu.

%description -l zh_CN
Kreogist Mu 是一款跨平台媒体管理器, 基于 Qt 开发.

功能特性:
- 支持管理绝大部分音频媒体文件, 如 mp3, m4a, wav, flac, ape, ogg,
 tta, aiff, aifc, aif, mp4, mpa, mp2, mp1, midi, mid, mp3pro, mpc,
 aac, cda, wma, fla, tak, mp+, aa, ra, mac, rmi, dtswav, dts, snd,
 au, ac3, xm, umx 等.
- 支持播放大部分音频格式: mp3, m4a, wav, flac, ape, mpc, wv, ac3,
 spx, wma 等.
- 支持从 flac, wma, m4a, wav 读取 ID3v1, ID3v2, APEv2 标签.
- 支持导入 m3u, ttpl, wpl, xspf 和 iTunes xml 格式的播放列表.
- 支持自动从 TTPlayer, TTPod, XiaMi, QQMusic 和 Baidu 下载歌词.

更多功能期待您的发现.

%prep
%setup -q -n %repo-%{_commit}
sed -i '/-m64/d' src/src.pro

%build
export CPATH="`pkg-config --variable=includedir libavformat`"
mkdir build
pushd build
CONFIG+="release linux" \
%{_qt5_qmake} ..
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT

install -Dm 0755 build/bin/%{name} %{buildroot}%{_bindir}/%{name}
install -Dm 0644 src/resource/icon/%{name}.png \
   %{buildroot}%{_datadir}/pixmaps/%{name}.png
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=μ
GenericName=Music Manager
Comment=Fantastic music manager
Exec=%{name}
Icon=%{name}
Terminal=false
Categories=AudioVideo;Audio;Music;Player;Qt;
StartupNotify=false
MimeType=audio/flac;audio/aac;audio/mp2;audio/mp4;audio/mpeg;audio/x-ape;audio/x-musepack;audio/x-aif;audio/x-aiff;audio/oga;audio/ogg;audio/x-flac+ogg;audiox-vorbis+ogg;audio/x-opus+ogg;audio/x-speex;audio/x-tta;audio/x-wav;audio/x-wavpack;application/x-cue;x-content/audio-player
EOF

%post
update-desktop-database -q ||:

%files
%defattr(-,root,root,-)
%doc AUTHOR NEWS Readme.md
%license LICENSE
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*
%{_bindir}/%{name}

%changelog
* Sat Oct 17 2015 mosquito <sensor.wen@gmail.com> - 0.9.147-1.gitc1c72c7
- Update to 0.9.147-1.gitc1c72c7
* Wed Feb  4 2015 mosquito <sensor.wen@gmail.com> - 0.7.0git20150203-1
- Initial build
