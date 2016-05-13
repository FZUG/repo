%global debug_package %{nil}

Name:       ccal
Version:    2.5.3
Release:    1%{?dist}
Summary:    Display a calendar together with Chinese calendar
Summary(zh_CN): Chinese calendar 命令行农历

Group:      Applications/Text
License:    GPL, portions LGPL
URL:        http://ccal.chinesebay.com/ccal
Source0:    http://ccal.chinesebay.com/ccal/%{name}-%{version}.tar.gz

%description
The ccal utility writes a Gregorian calendar together with
Chinese calendar to standard output.

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
%make_install    BINDIR=%{buildroot}%{_bindir}
make install-man MANDIR=%{buildroot}%{_mandir}

%files
%defattr(-,root,root,-)
%doc ChangeLog README
%license COPYING COPYING.LESSER
%{_mandir}/man1/ccal*.1.gz
%attr(0755,root,root) %{_bindir}/ccal*

%changelog
* Wed Sep 30 2015 mosquito <sensor.wen@gmail.com> - 2.5.3-1
- Rebuild for Fedora 23
* Sat Aug 03 2013 Huaren Zhong <huaren.zhong@gmail.com> - 2.5.3
- Rebuild for Fedora
* Sun Mar 04 2012 - Zhuo Meng <zxm8@case.edu>
- Updated for version 2.5.3
* Mon Oct 05 2009 - Zhuo Meng <zxm8@case.edu>
- Updated for version 2.5.2
* Sat Aug 15 2009 - Zhuo Meng <zxm8@case.edu>
- Updated for version 2.5.1
* Fri Jul 25 2008 - Zhuo Meng <zxm8@case.edu>
- Updated for version 2.5
* Sun Mar 26 2006 - Zhuo Meng <zhuo@thunder.cwru.edu>
- Updated for version 2.4
* Tue Jul 06 2004 - Zhuo Meng <zhuo@thunder.cwru.edu>
- Updated for version 2.3.3
* Sat Jun 12 2004 - Zhuo Meng <zhuo@thunder.cwru.edu>
- Updated for version 2.3.2
* Mon Oct 20 2003 - Zhuo Meng <zhuo@thunder.cwru.edu>
- Updated for version 2.3.1
* Sun Sep 28 2003 - Zhuo Meng <zhuo@thunder.cwru.edu>
- Updated for version 2.3
* Mon Jun 30 2003 - Wei He <hewei@ied.org.cn>
- Packaged into a RPM
