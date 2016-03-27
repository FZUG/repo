%global debug_package %{nil}
%global project fcitx-cloudpinyin
%global repo %{project}

%global _commit 45277f6bce6f93056d091a11be3fe44d90b6ffe4
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    fcitx-cloudpinyin
Version: 0.3.4
Release: 3.git%{_shortcommit}%{?dist}
Summary: Cloudpinyin module for fcitx
Group:   System Environment/Libraries
License: GPLv2+
URL:     https://fcitx-im.org/wiki/Cloudpinyin
Source0: https://github.com/fcitx/fcitx-cloudpinyin/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires: cmake, gettext, pkgconfig, intltool, fcitx-devel, libcurl-devel
Requires: fcitx, fcitx-pinyin

%description
Cloudpinyin is Fcitx addon that will add one candidate word to your pinyin
list. It current support four provider, Sogou, QQ, Baidu, Google.

%prep
%setup -q -n %{repo}-%{_commit}

# Fix google url
sed -i '/google/s|com|com.cn|' src/cloudpinyin.c

%build
%{cmake}
make %{?_smp_mflags} VERBOSE=1

%install
make install DESTDIR=%{buildroot} INSTALL='install -p'

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc README COPYING
%{_datadir}/fcitx/configdesc/*.desc
%{_datadir}/fcitx/addon/*.conf
%{_libdir}/fcitx/*.so

%changelog
* Mon Mar 28 2016 mosquito <sensor.wen@gmail.com> - 0.3.4-3
- Fix google url

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct  1 2015 Robin Lee <cheeselee@fedoraproject.org> - 0.3.4-1
- Update to 0.3.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Sep 15 2014 mosquito <sensor.wen@gmail.com> - 0.3.4-1
- Upstream to 0.3.4

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 23 2013 Robin Lee <cheeselee@fedoraproject.org> - 0.3.2-1
- Update to 0.3.2
- Remove fcitx-0.3.0-logging.patch
- Requires fcitx-pinyin
- Update URL and Source0 URL
- Revise description following upstream wiki

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> - 0.3.0-3
- fix FTBFS with fcitx >= 4.2.7

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Liang Suilong <liangsuilong@gmail.com> - 0.3.0-1
- Upstream to fcitx-cloudpinyin-0.3.0

* Sun Jul 29 2012  Liang Suilong <liangsuilong@gmail.com> - 0.2.3-1
- Upstream to fcitx-cloudpinyin-0.2.3

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 22 2012  Liang Suilong <liangsuilong@gmail.com> - 0.2.1-1
- Upstream to fcitx-cloudpinyin-0.2.1

* Sun Feb 26 2012 Liang Suilong <liangsuilong@gmail.com> - 0.2.0-1
- Initial Package
