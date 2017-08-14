%global         debug_package   %{nil}

%global         provider        github
%global         provider_tld    com
%global         project         BurntSushi
%global         repo            xgb
# https://github.com/BurntSushi/xgb
%global         provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global         import_path     %{provider_prefix}
%global         commit          27f122750802c950b2c869a5b63dafcf590ced95
%global         shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        XGB is the X protocol Go language Binding
License:        WTFPL
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
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/bigreq) = %{version}-%{release}
Provides:       golang(%{import_path}/composite) = %{version}-%{release}
Provides:       golang(%{import_path}/damage) = %{version}-%{release}
Provides:       golang(%{import_path}/dpms) = %{version}-%{release}
Provides:       golang(%{import_path}/dri2) = %{version}-%{release}
Provides:       golang(%{import_path}/ge) = %{version}-%{release}
Provides:       golang(%{import_path}/glx) = %{version}-%{release}
Provides:       golang(%{import_path}/randr) = %{version}-%{release}
Provides:       golang(%{import_path}/record) = %{version}-%{release}
Provides:       golang(%{import_path}/render) = %{version}-%{release}
Provides:       golang(%{import_path}/res) = %{version}-%{release}
Provides:       golang(%{import_path}/screensaver) = %{version}-%{release}
Provides:       golang(%{import_path}/shape) = %{version}-%{release}
Provides:       golang(%{import_path}/shm) = %{version}-%{release}
Provides:       golang(%{import_path}/xcmisc) = %{version}-%{release}
Provides:       golang(%{import_path}/xevie) = %{version}-%{release}
Provides:       golang(%{import_path}/xf86dri) = %{version}-%{release}
Provides:       golang(%{import_path}/xf86vidmode) = %{version}-%{release}
Provides:       golang(%{import_path}/xfixes) = %{version}-%{release}
Provides:       golang(%{import_path}/xinerama) = %{version}-%{release}
Provides:       golang(%{import_path}/xprint) = %{version}-%{release}
Provides:       golang(%{import_path}/xproto) = %{version}-%{release}
Provides:       golang(%{import_path}/xselinux) = %{version}-%{release}
Provides:       golang(%{import_path}/xtest) = %{version}-%{release}
Provides:       golang(%{import_path}/xv) = %{version}-%{release}
Provides:       golang(%{import_path}/xvmc) = %{version}-%{release}

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

install xproto/xproto_test.go %{buildroot}%{gopath}/src/%{import_path}/xproto/

sort -u -o devel.file-list devel.file-list

%check
export GOPATH=%{buildroot}%{gopath}:%{gopath}

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}
%gotest %{import_path}/bigreq
%gotest %{import_path}/composite
%gotest %{import_path}/damage
%gotest %{import_path}/dpms
%gotest %{import_path}/dri2
%gotest %{import_path}/ge
%gotest %{import_path}/glx
%gotest %{import_path}/randr
%gotest %{import_path}/record
%gotest %{import_path}/render
%gotest %{import_path}/res
%gotest %{import_path}/screensaver
%gotest %{import_path}/shape
%gotest %{import_path}/shm
%gotest %{import_path}/xcmisc
%gotest %{import_path}/xevie
%gotest %{import_path}/xf86dri
%gotest %{import_path}/xf86vidmode
%gotest %{import_path}/xfixes
%gotest %{import_path}/xinerama
%gotest %{import_path}/xprint
#%%gotest %%{import_path}/xproto
%gotest %{import_path}/xselinux
%gotest %{import_path}/xtest
%gotest %{import_path}/xv
%gotest %{import_path}/xvmc

%files devel -f devel.file-list
%doc README
%license LICENSE
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}

%files unit-test-devel
%{gopath}/src/%{import_path}/xproto/xproto_test.go 

%changelog
* Fri Aug 11 2017 mosquito <sensor.wen@gmail.com> - 0-0.1.git27f1227
- Initial package
