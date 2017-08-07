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

Name:       golang-%{provider}-%{project}-%{repo}
Version:    2.2.5
Release:    1%{?dist}
Summary:    A Go command line and flag parser
License:    MIT
URL:        https://%{provider_prefix}
Source0:    %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%package devel
Summary:    %{summary}
BuildArch:  noarch

Requires:   golang(golang.org/x/net/context)

Provides:   golang(%{import_path}) = %{version}-%{release}
Provides:   golang(%{import_path}/should) = %{version}-%{release}
Provides:   golang(%{import_path2}) = %{version}-%{release}
Provides:   golang(%{import_path2}/should) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%description
%{summary}


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

install -d -p %{buildroot}%{gopath}/src/%{import_path2}/
echo "%%dir %%{gopath}/src/%%{import_path2}/." >> devel.file-list
cp -r %{buildroot}%{gopath}/src/%{import_path}/* %{buildroot}/%{gopath}/src/%{import_path2}/
find %{buildroot}%{gopath}/src/%{import_path2}/ | sed 's|%{buildroot}||' >> devel.file-list

sort -u -o devel.file-list devel.file-list

%files devel -f devel.file-list
%doc README.md
%license COPYING
%dir %{gopath}/src/%{import_path}
%dir %{gopath}/src/%{import_path2}

%changelog
* Mon Aug  7 2017 mosquito <sensor.wen@gmail.com> - 2.2.5-1
- Release 2.2.5

* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 2.2.3-1.gite9044be
- Initial package build
