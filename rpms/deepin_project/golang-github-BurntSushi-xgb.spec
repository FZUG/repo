%global 	debug_package   %{nil}

%global 	provider        github
%global 	provider_tld    com
%global 	project         BurntSushi
%global 	repo            xgb
# https://github.com/BurntSushi/xgb
%global 	provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global 	import_path     %{provider_prefix}
%global 	commit          27f122750802c950b2c869a5b63dafcf590ced95
%global 	shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:       golang-%{provider}-%{project}-%{repo}
Version:    0
Release:    0.1.git%{shortcommit}%{?dist}
Summary:    XGB is the X protocol Go language Binding.

License:    XGB Authors
URL:        https://%{provider_prefix}
Source0:    https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

%package 	devel
Summary:	%{summary}
BuildArch:	noarch

Requires:	golang(golang.org/x/net/context)

Provides:	golang(%{import_path}) = %{version}-%{release}
Provides:	golang(%{import_path}/should) = %{version}-%{release}

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
* Tue Dec 27 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.0.13-1
- Initial package build