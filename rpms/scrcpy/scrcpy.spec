Name:       scrcpy

Version:    1.13

Release:    1

Summary:    scrcpy

License:    Apache License, Version 2.0

Source0:	https://github.com/Genymobile/scrcpy/archive/v1.13.tar.gz
Source1:	https://github.com/Genymobile/scrcpy/releases/download/v1.13/scrcpy-server-v1.13
BuildRequires:	meson
BuildRequires:	SDL2-devel
BuildRequires:	ffms2-devel
BuildRequires:	gcc
BuildRequires:	make

Requires:	android-tools
%global debug_package %{nil}

%description
This application provides display and control of Android devices connected on USB (or over TCP/IP). It does not require any root access. It works on GNU/Linux, Windows and macOS.

%prep
%setup -q

%build
meson x --buildtype release --strip -Db_lto=true -Dprebuilt_server=%{SOURCE1}
ninja -Cx

%install
strip x/app/%{name}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/usr/local/share/%{name}
mkdir -p %{buildroot}/usr/local/share/man/man1
install -m 0755 x/app/%{name} %{buildroot}%{_bindir}/%{name}
install -m 0755 x/server/%{name}-server %{buildroot}/usr/local/share/%{name}/%{name}-server
install -m 0644 app/scrcpy.1 %{buildroot}/usr/local/share/man/man1

%files
%{_bindir}/%{name}
/usr/local/share/%{name}/%{name}-server
/usr/local/share/man/man1/%{name}.1

%changelog

# let's skip this for now
