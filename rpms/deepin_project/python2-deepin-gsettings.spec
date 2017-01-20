%global project deepin-gsettings
%global repo %{project}

%global _commit a64de3ac195fe8d5878a07f2e862a058d49ce16d
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           python2-%{repo}
Version:        0.1
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Deepin gsettings python bindings

License:        GPLv3
Group:          Development/Libraries
Url:            https://github.com/linuxdeepin/deepin-gsettings
Source:         %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  python-devel
BuildRequires:  python2-setuptools
BuildRequires:  pkgconfig(glib-2.0)
Provides:       python-%{repo} = %{version}-%{release}
Provides:       %{repo} = %{version}-%{release}

%description
A python2 bindings in Linux Deepin

This package contains a module to get this working on
Deepin Desktop which requires GSettings in their own
XSETTINGS daemons.

%prep
%setup -q -n %{repo}-%{_commit}

# fix tests by using another key to test, since the old one was deprecated
sed -e 's|motion-threshold|drag-threshold|' \
    -e 's|idle-dim-battery|idle-dim|g' \
    -i example.py

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --prefix="%{_prefix}" --root="%{buildroot}"

%files
%defattr(-,root,root,-)
%{python_sitearch}/deepin_gsettings-0.1-py%{python_version}.egg-info
%{python_sitearch}/deepin_gsettings.so

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.1-1.gita64de3a
- Rebuild for fedora 25
* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 0.1-1.gita64de3a
- Rebuild for fedora 22
* Fri Sep 19 2014 mosquito <sensor.wen@gmail.com> - 0.1-1
- Rebuild for fedora
* Wed Aug 14 2013 hillwood@linuxfans.org
- Initial package
