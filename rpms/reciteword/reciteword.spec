%global project reciteword

Name:    reciteword
Version: 0.8.6
Release: 1%{?dist}
Summary:  Recite word easily

License: GPLv2+
URL:     https://sourceforge.net/projects/%{project}
Source0: %{url}/files/%{name}/%{version}/%{name}-%{version}.tar.bz2

BuildRequires: esound-devel
BuildRequires: automake
BuildRequires: espeak-devel

%description
Recite word easily.

%prep
%setup -q 

%build
%configure
make %{?_smp_mflags}

%install
%make_install

%preun

%postun

%files
%doc README* Readme.mac readme.txt AUTHORS ChangeLog NEWS
%license COPYING
%{_bindir}/%{name}
%{_datadir}/locale/zh_CN/LC_MESSAGES/%{name}.mo
%{_datadir}/pixmaps/*.png
%dir %{_datadir}/%{name}
%{_datadir}/%{name}
%{_datadir}/applications/*.desktop

%changelog
* Sun Apr 15 2018 Zamir SUN <sztsian@gmail.com> 0.8.6-1
- Initial RPM package
