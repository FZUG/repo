%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         linuxdeepin
%global   repo            go-x11-client
# https://github.com/linuxdeepin/go-x11-client
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          70dbb86c0a0cb10ebc4e6cbbb21dfa5d5aff5570
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.3.git%{shortcommit}%{?dist}
Summary:        A X11 client Go bindings for Deepin Desktop Environment
License:        GPLv3
URL:            https://%{provider_prefix}
Source0:        %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}.

%package devel
Summary:        %{summary}
BuildArch:      noarch
BuildRequires:  golang(gopkg.in/check.v1)
BuildRequires:  golang(golang.org/x/text/encoding/charmap)
BuildRequires:  golang(github.com/stretchr/testify/assert)
Requires:       golang(golang.org/x/text/encoding/charmap)
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/composite) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/damage) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/dpms) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/ge) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/input) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/randr) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/record) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/render) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/screensaver) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/shm) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/test) = %{version}-%{release}
Provides:       golang(%{import_path}/ext/xfixes) = %{version}-%{release}
Provides:       golang(%{import_path}/util/atom) = %{version}-%{release}
Provides:       golang(%{import_path}/util/keybind) = %{version}-%{release}
Provides:       golang(%{import_path}/util/keysyms) = %{version}-%{release}
Provides:       golang(%{import_path}/util/mousebind) = %{version}-%{release}
Provides:       golang(%{import_path}/util/wm/ewmh) = %{version}-%{release}
Provides:       golang(%{import_path}/util/wm/icccm) = %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%package unit-test-devel
Summary:        Unit tests for %{name} package
BuildArch:      noarch
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
install -d -p %{buildroot}%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done

# testing files for this project
install -d %{buildroot}%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test.file-list
for file in $(find . -iname "*_test.go"); do
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

%gotest %{import_path}

%files devel -f devel.file-list
%doc README
%license LICENSE
%dir %{gopath}/src/%{import_path}/ext
%dir %{gopath}/src/%{import_path}/util
%dir %{gopath}/src/%{import_path}/util/wm

%files unit-test-devel -f unit-test-devel.file-list

%changelog
* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 0-0.3.git70dbb86
- Update to 70dbb86

* Sat Oct 14 2017 mosquito <sensor.wen@gmail.com> - 0-0.2.gita10a839
- Update to a10a839

* Sun Aug 27 2017 mosquito <sensor.wen@gmail.com> - 0-0.1.git67aca0b
- Initial package build
