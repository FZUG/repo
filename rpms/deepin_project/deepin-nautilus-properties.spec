%global debug_package %{nil}
%global commit 859b1134ff1a1bbf06ce5a03a616fe9fe192f1a9
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:           deepin-nautilus-properties
Version:        3.14.3
Release:        1.git%{shortcommit}%{?dist}
Summary:        Provide file property dialog for Deepin desktop environment
License:        GPL
URL:            https://github.com/linuxdeepin/deepin-nautilus-properties
Source0:        %{url}/archive/%{commit}/%{name}-%{shortcommit}.tar.gz

BuildRequires:  intltool
BuildRequires:  libnotify-devel
BuildRequires:  libexif-devel
BuildRequires:  libxml2-devel
BuildRequires:  libX11-devel
BuildRequires:  exempi-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk3-devel
BuildRequires:  gnome-desktop3-devel
BuildRequires:  gobject-introspection-devel

%description
Provide file property dialog for Deepin desktop environment

%prep
%setup -q -n %{name}-%{commit}

%build
libtoolize && aclocal && autoheader && \
  automake --add-missing && autoconf

%configure \
    --libexecdir=%{_libdir}/nautilus \
    --disable-nst-extension \
    --disable-update-mimedb \
    --disable-packagekit \
    --disable-introspection \
    --disable-tracker
%make_build

%install
cd src
install -d %{buildroot}%{_bindir}
libtool --mode=install /bin/install -c %{name} deepin-open-chooser %{buildroot}%{_bindir}/

%files
%doc README
%license COPYING
%{_bindir}/%{name}
%{_bindir}/deepin-open-chooser

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 3.14.3-1.git859b113
- Update to 3.14.3
* Sun Oct 02 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 3.14.3-1
- Initial package build
