Name:           deepin-file-manager-backend
Version:        0.1.16
Release:        2%{?dist}
Summary:        Deepin file manager backend
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-file-manager-backend
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  git
BuildRequires:  gettext
BuildRequires:  gcc-go
BuildRequires:  libgo-devel
BuildRequires:  libcanberra-devel
BuildRequires:  librsvg2-devel
BUildRequires:  libX11-devel
BuildRequires:  gdk-pixbuf2-xlib-devel
BuildRequires:  poppler-glib-devel
BuildRequires:  deepin-metacity-devel
BuildRequires:  deepin-dbus-generator
BuildRequires:  deepin-gir-generator
BuildRequires:  deepin-go-dbus-factory
BuildRequires:  golang(pkg.deepin.io/dde/api)
BuildRequires:  golang(pkg.deepin.io/lib)
BuildRequires:  golang(github.com/mattn/go-sqlite3)
BuildRequires:  golang(github.com/howeyc/fsnotify)
BuildRequires:  golang(github.com/alecthomas/kingpin)

%description
Deepin file manager backend

%prep
%setup -q

sed -i 's|/usr/lib|%{_libexecdir}|' services/*.service desktop/desktop.go
sed -i '3s|lib|libexec|' Makefile
sed -i 's|DFMB|%{name}|' locale/Makefile i18n.go

%build
export GOPATH="$(pwd)/build:%{gopath}"
export CGO_LDTHREAD=-lpthread
go get -u gopkg.in/alecthomas/kingpin.v2
make USE_GCCGO=0

%install
%make_install

%find_lang %{name}

%post
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas/ &>/dev/null ||:

%files -f %{name}.lang
%{_libexecdir}/deepin-daemon/%{name}
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/com.deepin.filemanager.gschema.xml

%changelog
* Fri Feb 3 2017 mosquito <sensor.wen@gmail.com> - 0.1.16-2.git2032d5a
- Fix not work wallpaper choose

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.1.16-1.git2032d5a
- Update to 0.1.16

* Sat Oct 01 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.1.16-1
- Initial package build
