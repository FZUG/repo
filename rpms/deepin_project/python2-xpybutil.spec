%global project xpybutil
%global repo %{project}

%global _commit c2d438d4ac246b60e25e1f04da2db0eab40acda5
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           python2-%{repo}
Version:        0.0.1
Release:        1.git%{_shortcommit}%{?dist}
Summary:        An incomplete xcb-util port plus some extras

Group:          Development/Libraries
License:        WTFPL
URL:            https://github.com/BurntSushi/xpybutil
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
BuildRequires:  python-xpyb-devel
Requires:       python-xpyb
Provides:       python-%{repo} = %{version}-%{release}

%description
xpybutil exists because xpyb is a very low level library that communicates
with X. The most mature portions of xpybutil are the ICCCM and EWMH modules.
Each implement their respective specifications of the same name. The EWMH
module also implements the '_NET_WM_WINDOW_OPACITY' and '_NET_VISIBLE_DESKTOPS'
non-standard features. The former is widely used by compositing managers and
other utilities (i.e., xcompmgr and transset-df) while the latter is used by my
fork of Openbox called Openbox Multihead.

%prep
%setup -q -n %{repo}-%{_commit}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root=%{buildroot} --prefix=%{_prefix}
rm -rf %{buildroot}%{_datadir}/doc

%files
%defattr(-,root,root,-)
%doc README COPYING
%{python_sitelib}/*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.0.1-1.git8ee7dc4
- Rebuild for Fedora 25
* Fri Jul  3 2015 mosquito <sensor.wen@gmail.com> - 0.0.1-1.git8ee7dc4
- Rebuild for Fedora
* Sun May 12 2013 Huaren Zhong <huaren.zhong@gmail.com> - 0.0.1
- Rebuild for Fedora
