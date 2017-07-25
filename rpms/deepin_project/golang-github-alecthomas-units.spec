%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         alecthomas
%global   repo            units
# https://github.com/alecthomas/units
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          2efee857e7cfd4f3d0138cc3cbb1b4966962b93a
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:       golang-%{provider}-%{project}-%{repo}
Version:    0
Release:    0.1%{?dist}
Summary:    Units - Helpful unit multipliers and functions for Go

License:    MIT
URL:        https://%{provider_prefix}
Source0:    https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%package  devel
Summary:  %{summary}
BuildArch:  noarch

Requires: golang(golang.org/x/net/context)

Provides: golang(%{import_path}) = %{version}-%{release}
Provides: golang(%{import_path}/should) = %{version}-%{release}

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
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    echo "%%dir %%{gopath}/src/%%{import_path}/$(dirname $file)" >> devel.file-list
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$(dirname $file)
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
done

# Add symlink to older name
install -d -p %{buildroot}/%{gopath}/src/gopkg.in/alecthomas/
echo "%%dir %%{gopath}/src/gopkg.in/alecthomas/." >> devel.file-list

ln -s %{gopath}/src/%{import_path}/ %{buildroot}/%{gopath}/src/gopkg.in/alecthomas/kingpin.v2
echo "%%{gopath}/src/gopkg.in/alecthomas/kingpin.v2" >> devel.file-list

sort -u -o devel.file-list devel.file-list

%clean
rm -rf %{buildroot}

%files devel -f devel.file-list
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}

%changelog
* Mon Jan 16 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 0-0.1.git2efee85
- Initial package build