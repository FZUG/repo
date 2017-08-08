%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         disintegration
%global   repo            imaging
# https://github.com/disintegration/imaging
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          a5858022df0e1734a59f973fffe3f87b51c087ed
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:       golang-%{provider}-%{project}-%{repo}
Version:    1.2.1
Release:    1%{?dist}
Summary:    Simple Go image processing package
License:    MIT
URL:        https://%{provider_prefix}
Source0:    %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%package devel
Summary:    %{summary}
BuildArch:  noarch
Provides:   golang(%{import_path}) = %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%description
%{summary}.

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

%files devel -f devel.file-list
%doc README.md
%license LICENSE
%dir %{gopath}/src/%{import_path}

%changelog
* Tue Aug  8 2017 mosquito <sensor.wen@gmail.com> - 1.2.1-1
- Initial package build
