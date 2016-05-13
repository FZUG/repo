%global debug_package %{nil}
%global project deepin-utils
%global repo %{project}

# commit
%global _commit 8aaf2a6f002eeba5506c11c64b25d1404de78744
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		deepin-utils
Version:	0.0.2
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Utils library for all project in Linux Deepin

License:	GPLv3
Group:		Development/Libraries
URL:		https://github.com/linuxdeepin/deepin-utils
Source0:	https://github.com/linuxdeepin/deepin-utils/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(pygobject-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
# webkitgtk-devel
BuildRequires:	pkgconfig(webkit-1.0)
BuildRequires:	libsoup-devel
BuildRequires:	python-devel
BuildRequires:	pygtk2-devel
BuildRequires:	python-setuptools
Requires:	pywebkitgtk
Requires:	numpy

%description
Utils library for all project in Linux Deepin.

Base code move from utils module of deepin-ui.

%prep
%setup -q -n %repo-%{_commit}

%build

%install
export CFLAGS="$RPM_OPT_FLAGS"
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitearch}/deepin_utils
%{python_sitearch}/deepin_utils-1.0-py%{python_version}.egg-info
%{python_sitearch}/dtk_cairo_blur.so
%{python_sitearch}/dtk_webkit_cookie.so
%{python_sitearch}/deepin_font_icon.so

%changelog
* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 0.0.2-1.git8aaf2a6
- Update version to 0.0.2-1.git8aaf2a6
* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 0.0.2-2
- Rebuild
* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 0.0.2-1
- Rebuild for Fedora
* Mon Jan 13 2014 Huaren Zhong <huaren.zhong@gmail.com> - 0.0.1
- Rebuild for Fedora
* Wed Aug 14 2013 hillwood@linuxfans.org
- update to git20130724
  upsteam did not provide changlog.
* Sun Apr 28 2013 hillwood@linuxfans.org
- update to git20130314
  fix bugs
* Wed Feb  6 2013 hillwood@linuxfans.org
- Initial package
