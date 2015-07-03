%global debug_package %{nil}
%global project xpybutil
%global repo %{project}

# commit
%global _commit 8ee7dc406aabb3d54f38e692bf068b1b61131d83
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:       python-xpybutil
Version:    0.0.1
Release:    1.git%{_shortcommit}%{?dist}
Summary:    An abstraction over the X Python Binding

Group:      Development/Libraries
License:    MIT
URL:        https://github.com/BurntSushi/xpybutil
Source0:    https://github.com/BurntSushi/xpybutil/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: python-devel
BuildRequires: python-xpyb

%description
xpybutil exists because xpyb is a very low level library that communicates
with X. The most mature portions of xpybutil are the ICCCM and EWMH modules.
Each implement their respective specifications of the same name. The EWMH
module also implements the '_NET_WM_WINDOW_OPACITY' and '_NET_VISIBLE_DESKTOPS'
non-standard features. The former is widely used by compositing managers and
other utilities (i.e., xcompmgr and transset-df) while the latter is used by my
fork of Openbox called Openbox Multihead.

%prep
%setup -q -n %repo-%{_commit}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --skip-build --root=%{buildroot} --prefix=%{_prefix}
rm -rf %{buildroot}%{_datadir}/doc

%files
%defattr(-,root,root,-)
%doc README COPYING
%{python_sitelib}/*

%changelog
* Fri Jul  3 2015 mosquito <sensor.wen@gmail.com> - 0.0.1-1.git8ee7dc4
- Rebuild for Fedora
* Sun May 12 2013 Huaren Zhong <huaren.zhong@gmail.com> - 0.0.1
- Rebuild for Fedora
