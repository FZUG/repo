%global project deepin-utils
%global repo %{project}

%global _commit 8aaf2a6f002eeba5506c11c64b25d1404de78744
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           python2-%{repo}
Version:        0.0.2
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Utils library for all project in Linux Deepin

License:        GPLv3
Group:          Development/Libraries
URL:            https://github.com/martyr-deepin/deepin-utils
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(pygobject-2.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk+-2.0)
# webkitgtk-devel
BuildRequires:  pkgconfig(webkit-1.0)
BuildRequires:  libsoup-devel
BuildRequires:  python-devel
BuildRequires:  pygtk2-devel
BuildRequires:  python2-setuptools
Requires:       pywebkitgtk
Requires:       numpy
Provides:       python-%{repo} = %{version}-%{release}
#pygtk2 pycairo freetype webkitgtk python-xlib pywebkitgtk glib2 pygobject2

%description
Utils library for all project in Linux Deepin.

Base code move from utils module of deepin-ui.

%prep
%setup -q -n %{repo}-%{_commit}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitearch}/deepin_utils
%{python_sitearch}/deepin_utils-1.0-py%{python_version}.egg-info
%{python_sitearch}/dtk_cairo_blur.so
%{python_sitearch}/dtk_webkit_cookie.so
%{python_sitearch}/deepin_font_icon.so

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.0.2-1.git8aaf2a6
- Rebuild
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
