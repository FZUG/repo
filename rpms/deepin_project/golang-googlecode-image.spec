%global debug_package   %{nil}

%global provider_tld    com
%global provider        github
%global project         golang
%global repo            image
# https://github.com/golang/image
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     code.google.com/p/go.image
%global commit          426cfd8eeb6e08ab1932954e09e3c2cb2bc6e36d
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

%global x_provider      golang
%global x_provider_tld  org
%global x_repo          image
%global x_import_path   %{x_provider}.%{x_provider_tld}/x/%{x_repo}
%global x_name          golang-%{x_provider}%{x_provider_tld}-%{repo}

%global devel_main      %{x_name}-devel
%global devel_prefix    x

Name:       golang-googlecode-image
Version:    0
Release:    0.1%{?dist}
Summary:    Supplementary Go image libraries
License:    BSD
URL:        https://%{provider_prefix}
Source0:    %{url}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 aarch64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%description
%{summary}.

%package devel
Summary:    Supplementary Go image libraries for code.google.com/p/ imports
BuildArch:  noarch

Provides:   golang(%{import_path}) = %{version}-%{release}
Provides:   golang(%{import_path}/bmp) = %{version}-%{release}
Provides:   golang(%{import_path}/colornames) = %{version}-%{release}
Provides:   golang(%{import_path}/draw) = %{version}-%{release}
Provides:   golang(%{import_path}/font) = %{version}-%{release}
Provides:   golang(%{import_path}/font/basicfont) = %{version}-%{release}
Provides:   golang(%{import_path}/font/gofont) = %{version}-%{release}
Provides:   golang(%{import_path}/font/inconsolata) = %{version}-%{release}
Provides:   golang(%{import_path}/font/plan9font) = %{version}-%{release}
Provides:   golang(%{import_path}/font/sfnt) = %{version}-%{release}
Provides:   golang(%{import_path}/math) = %{version}-%{release}
Provides:   golang(%{import_path}/riff) = %{version}-%{release}
Provides:   golang(%{import_path}/tiff) = %{version}-%{release}
Provides:   golang(%{import_path}/tiff/lzf) = %{version}-%{release}
Provides:   golang(%{import_path}/vector) = %{version}-%{release}
Provides:   golang(%{import_path}/vp8) = %{version}-%{release}
Provides:   golang(%{import_path}/vp8l) = %{version}-%{release}
Provides:   golang(%{import_path}/webp) = %{version}-%{release}
Provides:   golang(%{import_path}/webp/nycbcra) = %{version}-%{release}

%package -n %{x_name}-devel
Summary:    Supplementary Go image libraries for golang.org/x/ imports
BuildArch:  noarch

Provides:   golang(%{x_import_path}) = %{version}-%{release}
Provides:   golang(%{x_import_path}/bmp) = %{version}-%{release}
Provides:   golang(%{x_import_path}/colornames) = %{version}-%{release}
Provides:   golang(%{x_import_path}/draw) = %{version}-%{release}
Provides:   golang(%{x_import_path}/font) = %{version}-%{release}
Provides:   golang(%{x_import_path}/font/basicfont) = %{version}-%{release}
Provides:   golang(%{x_import_path}/font/gofont) = %{version}-%{release}
Provides:   golang(%{x_import_path}/font/inconsolata) = %{version}-%{release}
Provides:   golang(%{x_import_path}/font/plan9font) = %{version}-%{release}
Provides:   golang(%{x_import_path}/font/sfnt) = %{version}-%{release}
Provides:   golang(%{x_import_path}/math) = %{version}-%{release}
Provides:   golang(%{x_import_path}/riff) = %{version}-%{release}
Provides:   golang(%{x_import_path}/tiff) = %{version}-%{release}
Provides:   golang(%{x_import_path}/tiff/lzf) = %{version}-%{release}
Provides:   golang(%{x_import_path}/vector) = %{version}-%{release}
Provides:   golang(%{x_import_path}/vp8) = %{version}-%{release}
Provides:   golang(%{x_import_path}/vp8l) = %{version}-%{release}
Provides:   golang(%{x_import_path}/webp) = %{version}-%{release}
Provides:   golang(%{x_import_path}/webp/nycbcra) = %{version}-%{release}

%description devel
%{summary}.

This package contains library source intended for building other packages
which use the supplementary Go text libraries with code.google.com/p/ imports.

%description -n %{x_name}-devel

This package contains library source intended for building other packages
which use the supplementary Go text libraries with golang.org/x/ imports.

%prep
%setup -q -n %{repo}-%{commit}

%build

%install
# source codes for building projects
install -d -p %{buildroot}%{gopath}/src/%{import_path}/
install -d -p %{buildroot}%{gopath}/src/%{x_import_path}
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . -iname "*.go" \! -iname "*_test.go") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list
    install -d -p %{buildroot}%{gopath}/src/%{x_import_path}/$dirprefix
    cp -pav $file %{buildroot}%{gopath}/src/%{x_import_path}/$file
    echo "%%{gopath}/src/%%{x_import_path}/$file" >> x_devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        echo "%%dir %%{gopath}/src/%%{x_import_path}/$dirprefix" >> x_devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
pushd %{buildroot}/%{gopath}/src/%{import_path}
# from https://groups.google.com/forum/#!topic/golang-nuts/eD8dh3T9yyA, first post
sed -i 's|"golang\.org\/x\/|"code\.google\.com\/p\/go\.|g' \
        $(find . -name '*.go')
popd

sort -u -o devel.file-list devel.file-list
sort -u -o x_devel.file-list x_devel.file-list

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files devel -f devel.file-list
%license LICENSE
%doc AUTHORS CONTRIBUTORS PATENTS README

%files -n %{x_name}-devel -f x_devel.file-list
%license LICENSE
%doc AUTHORS CONTRIBUTORS PATENTS README

%changelog
* Mon Aug  7 2017 mosquito <sensor.wen@gmail.com> - 0-0.1
- Initial package
