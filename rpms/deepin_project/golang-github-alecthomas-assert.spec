%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         alecthomas
%global   repo            assert
# https://github.com/alecthomas/assert
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          561411bbb7e98b005e520f4c0f491c2d23782048
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Units - Helpful unit multipliers and functions for Go
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
BuildRequires:  golang(github.com/alecthomas/colour)
BuildRequires:  golang(github.com/alecthomas/repr)
BuildRequires:  golang(github.com/sergi/go-diff/diffmatchpatch)
Requires:       golang(github.com/alecthomas/colour)
Requires:       golang(github.com/alecthomas/repr)
Requires:       golang(github.com/sergi/go-diff/diffmatchpatch)
Provides:       golang(%{import_path}) = %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.


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

sort -u -o devel.file-list devel.file-list

%check
export GOPATH=%{buildroot}%{gopath}:%{gopath}

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}

%files devel -f devel.file-list
%doc README.md
%license LICENCE.txt
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}

%changelog
* Fri Aug 11 2017 mosquito <sensor.wen@gmail.com> - 0-0.1
- Initial package build
