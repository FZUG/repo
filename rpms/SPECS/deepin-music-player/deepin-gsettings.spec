%global debug_package %{nil}
%global project deepin-gsettings
%global repo %{project}

# commit
%global _commit a64de3ac195fe8d5878a07f2e862a058d49ce16d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		deepin-gsettings
Version:	0.1
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Deepin gsettings python bindings

License:	GPLv3
Group:		Development/Libraries
Url:		https://github.com/linuxdeepin/deepin-gsettings
Source:		https://github.com/linuxdeepin/deepin-gsettings/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	libsoup-devel
BuildRequires:	python-devel
#BuildRequires:	python-gtk-devel
BuildRequires:	python-setuptools
BuildRequires:	pkgconfig(cairo)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(pygobject-2.0)
# webkitgtk-devel
BuildRequires:	pkgconfig(webkit-1.0)
Requires:	numpy
Requires:	pywebkitgtk

%description
A python2 bindings in Linux Deepin

This package contains a module to get this working on
Deepin Desktop which requires GSettings in their own
XSETTINGS daemons.

%prep
%setup -q -n %repo-%{_commit}

%build

%install
export CFLAGS="$RPM_OPT_FLAGS"
%{__python} setup.py install --prefix=%{_prefix} --root=%{buildroot}

%files
%defattr(-,root,root,-)
%{python_sitearch}/deepin_gsettings-0.1-py%{python_version}.egg-info
%{python_sitearch}/deepin_gsettings.so

%changelog
* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 0.1-1.gita64de3a
- Rebuild for fedora 22
* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 0.1-1
- Rebuild for fedora
* Wed Aug 14 2013 hillwood@linuxfans.org
- Initial package
