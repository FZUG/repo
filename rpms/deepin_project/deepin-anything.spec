%global module  deepin-anything

Name:           deepin-anything
Version:        0.0.2
Release:        1%{?dist}
Summary:        Deepin Anything file search tool
License:        GPLv3
Url:            https://github.com/linuxdeepin/deepin-anything
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  qt5-linguist
BuildRequires:  pkgconfig(Qt5Gui)

%description
%{summary}.

%package dkms
Summary:        %{name} dkms package
BuildArch:      noarch
Requires(post): dkms
Requires(post): kernel-devel

%description dkms
This package contains %{name} module wrapped for
the DKMS framework.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files and libraries for %{name}.

%prep
%setup -q
sed -i 's|/lib/systemd/system|%{_unitdir}|' server/src/src.pro
sed -i '/CONFIG +=/s|$| debug|' server/{src/src,lib/lib}.pro
sed -i 's|/usr/lib/$(DEB_HOST_MULTIARCH)|$(LIBDIR)|
        s|^DEB.*|LIBDIR =\nQMAKE_BIN=|
        s|qmake|$(QMAKE_BIN)|
        s|library all|library debug|
        s|release|debug|' Makefile

%build
%make_build VERSION=%{version} LIBDIR=%{_libdir} QMAKE_BIN=%{qmake_qt5}

%install
%make_install VERSION=%{version} LIBDIR=%{_libdir}
install -m644 debian/%{name}-dkms.dkms %{buildroot}%{_usrsrc}/%{name}-%{version}/dkms.conf

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post dkms
dkms add -m %{module} -v %{version} --rpm_safe_upgrade

# Try building it for the current kernel
if [ `uname -r | grep -c "BOOT"` -eq 0 ] && [ -e /lib/modules/`uname -r`/build/include ]; then
    dkms build -m %{module} -v %{version}
    dkms install -m %{module} -v %{version}
elif [ `uname -r | grep -c "BOOT"` -gt 0 ]; then
    echo -e ""
    echo -e "Module build for the currently running kernel was skipped since you"
    echo -e "are running a BOOT variant of the kernel."
else
    echo -e ""
    echo -e "Module build for the currently running kernel was skipped since the"
    echo -e "kernel headers for this kernel do not seem to be installed."
fi

%preun dkms
dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}-server
%{_libdir}/%{name}-server-lib/plugins/handlers/README.txt
%{_libdir}/lib*.so.*
%{_unitdir}/%{name}-server.service

%files dkms
%{_prefix}/lib/modules-load.d/anything.conf
%{_usrsrc}/%{name}-%{version}/

%files devel
%{_includedir}/%{name}/
%{_includedir}/%{name}-server/
%{_libdir}/pkgconfig/*.pc
%{_libdir}/lib*.so

%changelog
* Fri Jul 27 2018 mosquito <sensor.wen@gmail.com> - 0.0.2-1
- Initial package build
