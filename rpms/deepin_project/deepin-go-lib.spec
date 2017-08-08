%global debug_package  %{nil}
%global project        go-lib
%global repo           %{project}
%global import_path    pkg.deepin.io/lib

Name:           golang-deepin-go-lib
Version:        1.0.5
Release:        2%{?dist}
Summary:        Go bindings for Deepin Desktop Environment development
License:        GPLv3
URL:            https://github.com/linuxdeepin/go-lib
Source0:        %{url}/archive/%{version}/%{repo}-%{version}.tar.gz
BuildRequires:  golang

%description
DLib is a set of Go bindings/libraries for DDE development.
Containing dbus (forking from guelfey), glib, gdkpixbuf, pulse and more.

%package devel
Summary:        %{summary}
BuildArch:      noarch
Requires:       golang(github.com/BurntSushi/xgb)
Requires:       golang(github.com/howeyc/fsnotify)
Requires:       golang(github.com/smartystreets/goconvey/convey)
Requires:       golang(gopkg.in/check.v1)
Requires:       golang(golang.org/x/image/bmp)
Requires:       golang(golang.org/x/image/tiff)
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       deepin-%{repo} = %{version}-%{release}
Obsoletes:      deepin-%{repo} < %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%setup -q -n %{repo}-%{version}

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

sort -u -o devel.file-list devel.file-list

%files devel -f devel.file-list
%doc README.md
%license LICENSE
%dir %{gopath}/src/%{import_path}/

%changelog
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
