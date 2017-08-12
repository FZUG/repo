%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         alecthomas
%global   repo            kingpin
# https://github.com/alecthomas/kingpin
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   import_path2    gopkg.in/%{project}/%{repo}.v2
%global   commit          1087e65c9441605df944fb12c33f0fe7072d18ca
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        2.2.5
Release:        1%{?dist}
Summary:        A Go command line and flag parser
License:        MIT
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
BuildRequires:  golang(github.com/alecthomas/template)
BuildRequires:  golang(github.com/alecthomas/units)
BuildRequires:  golang(github.com/alecthomas/assert)
Requires:       golang(github.com/alecthomas/template)
Requires:       golang(github.com/alecthomas/units)
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path2}) = %{version}-%{release}

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
install -d -p %{buildroot}%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done

# Add symlink to older name
install -d -p %{buildroot}%{gopath}/src/gopkg.in/alecthomas/
echo "%%dir %%{gopath}/src/gopkg.in/alecthomas/." >> devel.file-list
ln -s %{gopath}/src/%{import_path}/ %{buildroot}%{gopath}/src/%{import_path2}
echo "%%{gopath}/src/%{import_path2}" >> devel.file-list

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
%doc README.md
%license COPYING
%dir %{gopath}/src/%{import_path}
%{gopath}/src/%{import_path2}

%files unit-test-devel -f unit-test-devel.file-list
%doc README.md
%license COPYING

%changelog
* Mon Aug  7 2017 mosquito <sensor.wen@gmail.com> - 2.2.5-1
- Release 2.2.5

* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 2.2.3-1.gite9044be
- Initial package build
