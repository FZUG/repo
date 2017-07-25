# Please use golang-github-go-fsnotify-fsnotify-devel
# https://github.com/fsnotify/fsnotify
%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         howeyc
%global   repo            fsnotify
# https://github.com/howeyc/fsnotify
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          441bbc86b167f3c1f4786afae9931403b99fdacf
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:       golang-%{provider}-%{project}-%{repo}
Version:    0.9.0
Release:    0.1%{?dist}
Summary:    File change notification Go language Binding.

License:    fsnotify Authors
URL:        https://%{provider_prefix}
Source0:    https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%package devel
Summary:    %{summary}
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

sort -u -o devel.file-list devel.file-list

%clean
rm -rf %{buildroot}

%files devel -f devel.file-list
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}

%changelog
* Wed Dec 28 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.9.0.1.git441bbc8
- Initial package build
