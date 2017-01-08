# https://aur.archlinux.org/packages/grumpy-git
%global debug_package %{nil}
%global project grumpy
%global repo %{project}

%global _commit 47e0e02297d6a43f8e9cb062e041802f93e4b09b
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

%global goarch %(go env GOHOSTARCH)
%global goroot %(go env GOROOT)
%global gopkgdir %{goroot}/pkg/linux_%{goarch}

Name:    grumpy
Version: 0.0.1
Release: 1.git%{_shortcommit}%{?dist}
Summary: a Python to Go source code transcompiler and runtime
License: Apache 2.0
URL:     https://github.com/google/grumpy
Source0: %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: python-devel
BuildRequires: golang-bin
Requires: golang

%description
Grumpy is a Python to Go source code transcompiler and runtime.

%prep
%setup -q -n %{repo}-%{_commit}

sed -i 's|@python|@python2|; s|@pip|@pip2|' Makefile
sed -i '1s|python|python2|' tools/*

%build
make
find . -name "*.d" -delete

%install
pushd build
install -d %{buildroot}%{goroot}
cp -rv bin lib %{buildroot}%{_prefix}/
cp -rv pkg src %{buildroot}%{goroot}/
popd

cp -rv tools/* %{buildroot}%{_bindir}/

%check
make test

%files
%defattr(-,root,root,-)
%doc README.md
%{_bindir}/benchcmp
%{_bindir}/coverparse
%{_bindir}/diffrange
%{_bindir}/grumpc
%{_bindir}/grumprun
%{python_sitelib}/%{name}/
%{gopkgdir}/%{name}/
%{gopkgdir}/%{name}.a
%{goroot}/src/%{name}/

%changelog
* Sun Jan  8 2017 mosquito <sensor.wen@gmail.com> - 0.0.1-1.git47e0e02
- Initial build
