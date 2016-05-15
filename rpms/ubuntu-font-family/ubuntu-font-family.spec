Name:           ubuntu-font-family
Version:        0.83
Release:        2%{?dist}
Summary:        This is the Ubuntu Font Family

License:        Ubuntu Font License 1.0
URL:            http://font.ubuntu.com/
Source0:        http://font.ubuntu.com/download/%{name}-%{version}.zip

BuildArch:      noarch

%description
Ubuntu is an OpenType-based font family, designed to be a modern, 
humanist-style typeface by London-based type foundry Dalton Maag, 
with funding by Canonical Ltd.

%prep
%autosetup
mv LICENCE.txt LICENSE.txt
mv LICENCE-FAQ.txt LICENSE-FAQ.txt

%build

%install
for font in `ls | grep ttf`; do
    %{__install} -D -m 0644 $font %{buildroot}%{_datadir}/fonts/%{name}/$font
done

%post
if [ -x /usr/bin/fc-cache ]; then
    /usr/bin/fc-cache /usr/share/fonts || :
fi

%postun
if [ $1 -eq 0 -a -x /usr/bin/fc-cache ] ; then
    /usr/bin/fc-cache /usr/share/fonts || :
fi

%files
%doc CONTRIBUTING.txt FONTLOG.txt README.txt TRADEMARKS.txt
%license copyright.txt LICENSE.txt LICENSE-FAQ.txt
%{_datadir}/fonts/%{name}

%changelog
* Sun May 15 2016 nrechn <neil@gyz.io> - 0.83-2
- update spec and rebuild for F24

* Wed Nov 04 2015 Maxim Orlov <murmansksity@gmail.com> - 0.83-1.R
- Update to 0.83

* Fri Nov 11 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 0.69-2.R
- Revert to 0.69

* Fri Sep 30 2011 Vasiliy N. Glazov <vascom2@gmail.com> - 0.80-1.R
- Update to 0.80

* Tue Oct 12 2010 Arkady L. Shane <ashejn@yandex-team.ru> 0.69-1
- initial build for Fedora
