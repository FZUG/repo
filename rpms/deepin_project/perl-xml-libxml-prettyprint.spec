Name:           perl-XML-LibXML-PrettyPrint
Version:        0.006
Release:        1%{?dist}
Summary:        Add pleasant whitespace to a DOM tree
Group:          Development/Libraries
License:        GPL+
URL:            https://metacpan.org/release/XML-LibXML-PrettyPrint/
Source0:        http://search.cpan.org/CPAN/authors/id/T/TO/TOBYINK/XML-LibXML-PrettyPrint-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl-devel
# Tests
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Warnings)
# Run-time
BuildRequires:  perl(XML::LibXML)
BuildRequires:  perl(Exporter::Tiny)
Provides:       perl(XML::LibXML::PrettyPrint) == %{version}
%{?perl_default_filter}

%description
%{summary}

%prep
%setup -q -n XML-LibXML-PrettyPrint-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
%make_build

%install
%make_install

%check
make test

%files
%{_bindir}/xml-pretty
%{perl_archlib}/perllocal.pod
%{perl_vendorarch}/auto/XML
%{perl_vendorlib}/XML
%{_mandir}/man*/*.gz

%changelog
* Fri Jul 14 2017 mosquito <sensor.wen@gmail.com> - 0.006-1
- Initial build
