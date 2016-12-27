%global debug_package %{nil}

Name:    elvish
Version: 0.5
Release: 1%{?dist}
Summary: Elvish - A friendly and expressive Unix shell

Group:   System Environment/Shells
License: BSD 2-Clause
URL:     https://github.com/elves/elvish
Source0: https://github.com/elves/elvish/archive/%{version}/elvish-%{version}.tar.gz
BuildRequires: golang-bin
BuildRequires: golang-googlecode-tools-stringer
Obsoletes: golang-github-elves-elvish

%description
Elvish aims to explore the potentials of the Unix shell. It is a work in progress; things will change without warning. 

%prep
%setup -q -n %{name}-%{version}

%build
mkdir -p ./_build/src/github.com/elves
ln -s $(pwd) ./_build/src/github.com/elves/elvish
export GOPATH=$(pwd)/_build:%{gopath}
go build -o elvish
#make generate

%install
install -Dm 0755 elvish %{buildroot}%{_bindir}/elvish

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/elvish

%changelog
* Tue Dec 27 2016 Zamir SUN <zsun@fedoraproject.org> - 0.5-2
- Rename tp elvish
* Tue Dec 20 2016 Zamir SUN <zsun@fedoraproject.org> - 0.5-1
- Initial with elvish-0.5
