%global debug_package %{nil}
%global project fcitx-sunpinyin
%global repo %{project}

# commit
%global _commit 188ef63237401b4a511d6b9633c45a73f427b170
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		fcitx-sunpinyin
Version:	0.4.1
Release:	6.git%{_shortcommit}%{?dist}
Summary:	Sunpinyin Wrapper for Fcitx
Summary(zh_CN):	Sunpinyin Fcitx 前端
Group:		System Environment/Libraries
License:	GPLv2+
URL:		http://fcitx-im.org/wiki/Fcitx
Source0:	https://github.com/fcitx/fcitx-sunpinyin/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	cmake
BuildRequires:	gettext
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	dbus-devel
BuildRequires:	fcitx-devel
BuildRequires:	sunpinyin-devel
BuildRequires:	sunpinyin
BuildRequires:	fcitx
Requires:	fcitx
Requires:	fcitx-data
Requires:	sunpinyin

%description
Fcitx-sunpinyin is a Sunpinyin Wrapper for Fcitx.

SunPinyin is an SLM (Statistical Language Model) based input method
engine. To model the Chinese language, it use a backoff bigram and
trigram language model.

%description -l zh_CN
Fcitx-sunpinyin 是一个 Sunpinyin 的 Fcitx 前端.

SunPinyin 是一个基于 SLM (Statistical Language Model) 的输入法引擎.
为中文语言建模, 它使用 bigram 和 trigram 语言模型.

%prep
%setup -q -n %repo-%{_commit}

%build
mkdir -pv build
pushd build
%cmake ..
make %{?_smp_mflags}
popd

%install
rm -rf $RPM_BUILD_ROOT
pushd build
make install DESTDIR=$RPM_BUILD_ROOT
popd

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS README COPYING 
%{_libdir}/fcitx/%{name}.so
%{_datadir}/fcitx/addon/%{name}.conf
%{_datadir}/fcitx/inputmethod/sunpinyin.conf
%{_datadir}/fcitx/configdesc/%{name}.desc
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/22x22/apps/%{name}.png
%{_datadir}/icons/hicolor/24x24/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_datadir}/icons/hicolor/128x128/apps/%{name}.png
%{_datadir}/fcitx/skin/classic/sunpinyin.png
%{_datadir}/fcitx/skin/dark/sunpinyin.png
%{_datadir}/fcitx/skin/default/sunpinyin.png
%{_datadir}/fcitx/imicon/sunpinyin.png

%changelog
* Wed May 06 2015 mosquito <sensor.wen@gmail.com> - 0.4.1-6
- Rename version name

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.4.1-5
- Rebuilt for GCC 5 C++11 ABI change

* Tue Sep 16 2014 mosquito <sensor.wen@gmail.com> - 0.4.1git20131031-1
- Rebuild for rhel/centos 7

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 14 2013 Liang Suilong <liangsuilong@gmail.com> - 0.4.1-1
- Upstream to fcitx-sunpinyin-0.4.1

* Sun Feb 24 2013 Liang Suilong <liangsuilong@gmail.com> - 0.4.0-1
- Upstream to fcitx-sunpinyin-0.4.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 29 2012 Liang Suilong <liangsuilong@gmail.com> - 0.3.8-1
- Upstream to fcitx-sunpinyin-0.3.8

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun May 13 2012 Liang Suilong <liangsuilong@gmail.com> - 0.3.6-1
- Upstream to fcitx-sunpinyin-0.3.6

* Wed Feb 08 2012 Liang Suilong <liangsuilong@gmail.com> - 0.3.3-1
- Initial Package
