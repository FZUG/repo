%global debug_package %{nil}
%global _commit 2032d5abab8ebf5acc662aba80cfdf2cf862b892
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           deepin-file-manager-backend
Version:        0.1.16
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin file manager backend
License:        GPLv3
URL:            https://github.com/linuxdeepin/deepin-file-manager-backend
Source0:        %{url}/archive/%{_commit}/%{name}-%{_shortcommit}.tar.gz

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
BuildRequires:  deepin-go-lib
BuildRequires:  deepin-api-devel
BuildRequires:  golang-github-mattn-go-sqlite3-devel
BuildRequires:  golang-github-howeyc-fsnotify-devel
BuildRequires:  golang-github-alecthomas-kingpin-devel

%description
Deepin file manager backend

%prep
%setup -q -n %{name}-%{_commit}

sed -i 's|lib|libexec|' services/*.service
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
/usr/bin/glib-compile-schemas %{_datadir}/glib-2.0/schemas/

%files -f %{name}.lang
%{_libexecdir}/deepin-daemon/%{name}
%{_datadir}/dbus-1/services/*.service
%{_datadir}/glib-2.0/schemas/com.deepin.filemanager.gschema.xml

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.1.16-1.git2032d5a
- Update to 0.1.16
* Sat Oct 01 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.1.16-1
- Initial package build
