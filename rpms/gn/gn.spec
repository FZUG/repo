%global debug_package %{nil}

%global commit 78db9de5aed44f03763176ac6067fb1a73798684
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           gn
Version:        1559
Release:        1.git%{shortcommit}%{?dist}
Summary:        A meta-build system that generates build files for Ninja.

License:        MIT
URL:            https://gn.googlesource.com/gn
Source0:        https://gn.googlesource.com/gn/+archive/%{commit}.tar.gz
Patch0:         fix-version.patch

BuildRequires: gcc gcc-c++
BuildRequires: libstdc++-static
BuildRequires: ninja-build python

%description
GN is a meta-build system that generates build files for Ninja.

%prep
%autosetup -p1 -n gn-%{commit}


%build

export CC=/usr/bin/gcc
export CXX=/usr/bin/g++
export AR=/usr/bin/ar

python build/gen.py
ninja -C out

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_bindir}/gn
install -m644 out/gn %{buildroot}%{_bindir}/gn

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%license LICENSE 
%{_bindir}/gn


%changelog
* Thu Apr 18 2019 Bangjie Deng <dengbangjie@foxmail.com> - 234-2
- Package init.


