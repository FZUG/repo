%global   debug_package   %{nil}

%global   provider        github
%global   provider_tld    com
%global   project         BurntSushi
%global   repo            xgbutil
# https://github.com/BurntSushi/xgbutil
%global   provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global   import_path     %{provider_prefix}
%global   commit          f7c97cef3b4e6c88280a5a7091c3314e815ca243
%global   shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           golang-%{provider}-%{project}-%{repo}
Version:        0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        XGB is the X protocol Go language Binding.
License:        XGB Authors
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
BuildRequires:  golang(github.com/BurntSushi/freetype-go/freetype)
BuildRequires:  golang(github.com/BurntSushi/freetype-go/freetype/truetype)
BuildRequires:  golang(github.com/BurntSushi/graphics-go/graphics)
BuildRequires:  golang(github.com/BurntSushi/xgb)
BuildRequires:  golang(github.com/BurntSushi/xgb/shape)
BuildRequires:  golang(github.com/BurntSushi/xgb/xinerama)
BuildRequires:  golang(github.com/BurntSushi/xgb/xproto)
Requires:       golang(github.com/BurntSushi/freetype-go/freetype)
Requires:       golang(github.com/BurntSushi/freetype-go/freetype/truetype)
Requires:       golang(github.com/BurntSushi/graphics-go/graphics)
Requires:       golang(github.com/BurntSushi/xgb)
Requires:       golang(github.com/BurntSushi/xgb/shape)
Requires:       golang(github.com/BurntSushi/xgb/xinerama)
Requires:       golang(github.com/BurntSushi/xgb/xproto)
Provides:       golang(%{import_path}) = %{version}-%{release}
Provides:       golang(%{import_path}/ewmh) = %{version}-%{release}
Provides:       golang(%{import_path}/gopher) = %{version}-%{release}
Provides:       golang(%{import_path}/icccm) = %{version}-%{release}
Provides:       golang(%{import_path}/keybind) = %{version}-%{release}
Provides:       golang(%{import_path}/motif) = %{version}-%{release}
Provides:       golang(%{import_path}/mousebind) = %{version}-%{release}
Provides:       golang(%{import_path}/xcursor) = %{version}-%{release}
Provides:       golang(%{import_path}/xevent) = %{version}-%{release}
Provides:       golang(%{import_path}/xgraphics) = %{version}-%{release}
Provides:       golang(%{import_path}/xinerama) = %{version}-%{release}
Provides:       golang(%{import_path}/xprop) = %{version}-%{release}
Provides:       golang(%{import_path}/xrect) = %{version}-%{release}
Provides:       golang(%{import_path}/xwindow) = %{version}-%{release}

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

%files devel -f devel.file-list
%doc README
%license COPYING
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}

%changelog
* Wed Dec 28 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.0.1.gitf7c97ce
- Initial package build
