%global debug_package %{nil}
Name: antigen
Version: 2.2.3
Release: 1%{?dist}
Summary: A plugin manager for zsh, inspired by oh-my-zsh and vundle.

License: MIT
URL: https://github.com/zsh-users/antigen
Source0: https://github.com/zsh-users/antigen/releases/download/v%{version}/v%{version}.tar.gz
BuildRequires: make
Requires: zsh
Requires: git

%description
Antigen is a small set of functions that help you easily manage your shell (zsh) plugins,
called bundles. The concept is pretty much the same as bundles in a typical vim+pathogen setup.
Antigen is to zsh, what Vundle is to vim.

%prep
%setup -q

%build
make build

%install
make PREFIX=%{buildroot}/%{_prefix} install

%files
%license LICENSE
%{_datadir}/antigen.zsh

%doc README.mkd

%changelog
* Fri Mar 26 2021 justforlxz <justforlxz@gmail.com> - 2.2.3-1
- Initial build
