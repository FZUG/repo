%global debug_package %{nil}

Name:     FoxitReader
Version:  1.1.0
Release:  1%{?dist}
Summary:  Foxit Reader is a free PDF document viewer
Summary(zh_CN): 福昕 PDF 阅读器

Group:    Applications/Text
License:  Proprietary
URL:      http://www.foxitsoftware.com
Source0:  http://cdn02.foxitsoftware.com/pub/foxit/reader/desktop/linux/1.x/1.1/enu/%{name}-%{version}.tar.bz2
Source1:  fx-icon.png
Source2:  FoxitReader_ru.po

ExclusiveArch: %{ix86}
BuildRequires: gettext
Requires: /usr/bin/gtk-update-icon-cache
Requires: desktop-file-utils
Provides: foxitreader = %{version}-%{release}

%description
Foxit Reader is a free PDF document viewer for the Linux platform, with
a new streamlined interface, user-customized toolbar, incredibly small
size, breezing-fast launch speed and rich features. This empowers PDF
document users with Zoom function, Navigation function, Bookmarks,
Thumbnails, Text Selection Tool, Snapshot, and Full Screen capabilities.
Foxit Reader for Desktop Linux is provided by Foxit Corporation free for
non-commercial use.

%prep
%setup -q -n 1.1-release

%install
install -d %{buildroot}%{_bindir}
install -m 0755 %{name} %{buildroot}%{_bindir}

install -d %{buildroot}%{_datadir}/foxit
install -m 0644 fum.fhd fpdfcjk.bin %{buildroot}%{_datadir}/foxit

install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=%{name}
GenericName=%{name}
Comment=PDF Viewer
Comment[ru]=Просмотр PDF
Comment[zh_CN]=PDF 浏览器
Exec=%{name} %F
Icon=fx-icon
Terminal=false
Categories=GNOME;GTK;Qt;KDE;Application;Office;Viewer;
X-Desktop-File-Install-Version=1.1
MimeType=application/pdf;application/x-gzpdf;application/x-bzpdf;
EOF

install -d %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/
install -m 0644 %{S:1} %{buildroot}%{_datadir}/icons/hicolor/48x48/apps

for lang in de fr ja zh_CN zh_TW; do
  install -d %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  install -m 0644 po/$lang/*.mo %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
done
install -d %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES
msgfmt -o %{buildroot}%{_datadir}/locale/ru/LC_MESSAGES/%{name}.mo %{S:2}

%find_lang %{name}

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database -q ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database -q ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files -f %{name}.lang
%doc Readme.txt
%{_bindir}/%{name}
%{_datadir}/foxit/fum.fhd
%{_datadir}/foxit/fpdfcjk.bin
%{_datadir}/icons/hicolor/*/apps/fx-icon.png
%{_datadir}/applications/%{name}.desktop

%changelog
* Mon Dec 14 2015 mosquito <sensor.wen@gmail.com> - 1.1.0-1
- Initial build
