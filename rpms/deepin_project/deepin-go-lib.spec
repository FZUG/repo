%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         linuxdeepin
%global   repo            go-lib
# https://github.com/linuxdeepin/go-lib
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     pkg.deepin.io/lib
%global   commit          70367c8d6653a07b6c09bb5a65f24e795e3161b9
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-deepin-go-lib
Version:        1.1.0
Release:        1%{?dist}
Summary:        Go bindings for Deepin Desktop Environment development
License:        GPLv3
URL:            https://%{provider_prefix}
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
DLib is a set of Go bindings/libraries for DDE development.
Containing dbus (forking from guelfey), glib, gdkpixbuf, pulse and more.

%package devel
Summary:        %{summary}
BuildArch:      noarch
# Required for tests
BuildRequires:  deepin-gir-generator
BuildRequires:  dbus-x11
BuildRequires:  iso-codes
BuildRequires:  mobile-broadband-provider-info
BuildRequires:  golang(github.com/BurntSushi/xgb/xproto)
BuildRequires:  golang(github.com/BurntSushi/xgbutil)
BuildRequires:  golang(github.com/BurntSushi/xgbutil/xevent)
BuildRequires:  golang(github.com/BurntSushi/xgbutil/xprop)
BuildRequires:  golang(github.com/BurntSushi/xgbutil/xwindow)
BuildRequires:  golang(golang.org/x/image/bmp)
BuildRequires:  golang(golang.org/x/image/tiff)
BuildRequires:  golang(gopkg.in/check.v1)
BuildRequires:  golang(gopkg.in/alecthomas/kingpin.v2)
BuildRequires:  golang(github.com/smartystreets/goconvey/convey)
BuildRequires:  pkgconfig(gobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gdk-3.0)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gdk-x11-3.0)
BuildRequires:  pkgconfig(gdk-pixbuf-xlib-2.0)
BuildRequires:  pkgconfig(libpulse)
BuildRequires:  pkgconfig(libcanberra)

Requires:       golang(github.com/BurntSushi/xgb/xproto)
Requires:       golang(github.com/BurntSushi/xgbutil)
Requires:       golang(github.com/BurntSushi/xgbutil/xevent)
Requires:       golang(github.com/BurntSushi/xgbutil/xprop)
Requires:       golang(github.com/BurntSushi/xgbutil/xwindow)
Requires:       golang(golang.org/x/image/bmp)
Requires:       golang(golang.org/x/image/tiff)

Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/app) = %{version}-%{release}
Provides:       golang(%{import_path}/appinfo) = %{version}-%{release}
Provides:       golang(%{import_path}/appinfo/desktopappinfo) = %{version}-%{release}
Provides:       golang(%{import_path}/arch) = %{version}-%{release}
Provides:       golang(%{import_path}/archive) = %{version}-%{release}
Provides:       golang(%{import_path}/archive/gzip) = %{version}-%{release}
Provides:       golang(%{import_path}/archive/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/backlight/common) = %{version}-%{release}
Provides:       golang(%{import_path}/backlight/display) = %{version}-%{release}
Provides:       golang(%{import_path}/backlight/keyboard) = %{version}-%{release}
Provides:       golang(%{import_path}/calendar) = %{version}-%{release}
Provides:       golang(%{import_path}/calendar/lunar) = %{version}-%{release}
Provides:       golang(%{import_path}/calendar/util) = %{version}-%{release}
Provides:       golang(%{import_path}/dbus) = %{version}-%{release}
Provides:       golang(%{import_path}/dbus/interfaces) = %{version}-%{release}
Provides:       golang(%{import_path}/dbus/introspect) = %{version}-%{release}
Provides:       golang(%{import_path}/dbus/property) = %{version}-%{release}
Provides:       golang(%{import_path}/encoding/kv) = %{version}-%{release}
Provides:       golang(%{import_path}/event) = %{version}-%{release}
Provides:       golang(%{import_path}/fsnotify) = %{version}-%{release}
Provides:       golang(%{import_path}/gdkpixbuf) = %{version}-%{release}
Provides:       golang(%{import_path}/gettext) = %{version}-%{release}
Provides:       golang(%{import_path}/graphic) = %{version}-%{release}
Provides:       golang(%{import_path}/initializer) = %{version}-%{release}
Provides:       golang(%{import_path}/initializer/v2) = %{version}-%{release}
Provides:       golang(%{import_path}/iso) = %{version}-%{release}
Provides:       golang(%{import_path}/keyfile) = %{version}-%{release}
Provides:       golang(%{import_path}/locale) = %{version}-%{release}
Provides:       golang(%{import_path}/log) = %{version}-%{release}
Provides:       golang(%{import_path}/mime) = %{version}-%{release}
Provides:       golang(%{import_path}/mobileprovider) = %{version}-%{release}
Provides:       golang(%{import_path}/notify) = %{version}-%{release}
Provides:       golang(%{import_path}/notify/dbusnotify) = %{version}-%{release}
Provides:       golang(%{import_path}/pinyin) = %{version}-%{release}
Provides:       golang(%{import_path}/polkit) = %{version}-%{release}
Provides:       golang(%{import_path}/polkit/policykit1) = %{version}-%{release}
Provides:       golang(%{import_path}/procfs) = %{version}-%{release}
Provides:       golang(%{import_path}/profile) = %{version}-%{release}
Provides:       golang(%{import_path}/proxy) = %{version}-%{release}
Provides:       golang(%{import_path}/pulse) = %{version}-%{release}
Provides:       golang(%{import_path}/sound) = %{version}-%{release}
Provides:       golang(%{import_path}/strv) = %{version}-%{release}
Provides:       golang(%{import_path}/tasker) = %{version}-%{release}
Provides:       golang(%{import_path}/timer) = %{version}-%{release}
Provides:       golang(%{import_path}/users/group) = %{version}-%{release}
Provides:       golang(%{import_path}/users/passwd) = %{version}-%{release}
Provides:       golang(%{import_path}/users/shadow) = %{version}-%{release}
Provides:       golang(%{import_path}/utils) = %{version}-%{release}
Provides:       golang(%{import_path}/xdg/basedir) = %{version}-%{release}
Provides:       golang(%{import_path}/xdg/userdir) = %{version}-%{release}
Provides:       deepin-%{repo} = %{version}-%{release}
Obsoletes:      deepin-%{repo} < %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%package unit-test-devel
Summary:        Unit tests for %{name} package
# test subpackage tests code from devel subpackage
Requires:       %{name}-devel = %{version}-%{release}

%description unit-test-devel
%{summary}.

This package contains unit tests for project
providing packages with %{import_path} prefix.

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
# source codes for building projects
install -d %{buildroot}%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.[h|c]" -or -iname "*.go" \! -iname "*_test.go"); do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d %{buildroot}%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done

# testing files for this project
install -d %{buildroot}%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go" -or -iname "testdata*"); do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list
    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done

sort -u -o devel.file-list devel.file-list
sort -u -o unit-test-devel.file-list unit-test-devel.file-list

%check
export GOPATH=%{buildroot}%{gopath}:%{gopath}

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/app
%gotest %{import_path}/appinfo ||:
%gotest %{import_path}/appinfo/desktopappinfo ||:
%gotest %{import_path}/arch
%gotest %{import_path}/archive
%gotest %{import_path}/archive/gzip
%gotest %{import_path}/archive/utils
%gotest %{import_path}/backlight/common
%gotest %{import_path}/backlight/display
%gotest %{import_path}/backlight/keyboard
%gotest %{import_path}/calendar
%gotest %{import_path}/calendar/lunar
%gotest %{import_path}/calendar/util
%gotest %{import_path}/dbus
%gotest %{import_path}/dbus/interfaces
%gotest %{import_path}/dbus/introspect
%gotest %{import_path}/dbus/property
%gotest %{import_path}/encoding/kv
%gotest %{import_path}/event
%gotest %{import_path}/gdkpixbuf ||:
#%%gotest %%{import_path}/gettext
%gotest %{import_path}/graphic
%gotest %{import_path}/initializer
%gotest %{import_path}/initializer/v2
%gotest %{import_path}/iso
%gotest %{import_path}/keyfile
%gotest %{import_path}/locale
%gotest %{import_path}/log
%gotest %{import_path}/mime
%gotest %{import_path}/mobileprovider
%gotest %{import_path}/notify
%gotest %{import_path}/notify/dbusnotify
%gotest %{import_path}/pinyin
%gotest %{import_path}/polkit
%gotest %{import_path}/polkit/policykit1
%gotest %{import_path}/procfs
%gotest %{import_path}/profile
%gotest %{import_path}/proxy
%gotest %{import_path}/pulse
%gotest %{import_path}/sound
%gotest %{import_path}/strv
%gotest %{import_path}/tasker
%gotest %{import_path}/timer
%gotest %{import_path}/users/group ||:
%gotest %{import_path}/users/passwd ||:
%gotest %{import_path}/users/shadow
%gotest %{import_path}/utils
%gotest %{import_path}/xdg/basedir
%gotest %{import_path}/xdg/userdir

%files devel -f devel.file-list
%doc README.md
%license LICENSE
%dir %{gopath}/src/%{import_path}/

%files unit-test-devel -f unit-test-devel.file-list
%doc README.md
%license LICENSE

%changelog
* Thu Aug 24 2017 mosquito <sensor.wen@gmail.com> - 1.1.0-1
- Update to 1.1.0

* Sun Aug  6 2017 mosquito <sensor.wen@gmail.com> - 1.0.5-2
- Rename to golang-deepin-go-lib

* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 1.0.5-1.git3c9791f
- Update to 1.0.5

* Fri May 19 2017 mosquito <sensor.wen@gmail.com> - 1.0.3-1.gitb084e27
- Update to 1.0.3

* Sun Feb 26 2017 mosquito <sensor.wen@gmail.com> - 0.5.5-1.git01150d5
- Update to 0.5.5

* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.5.3-1.git44767e8
- Update to 0.5.3

* Sun Jul 12 2015 mosquito <sensor.wen@gmail.com> - 0.3.0-1.git98ac007
- Update to 0.3.0-1.git98ac007

* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.4git20140928-1
- Initial build
