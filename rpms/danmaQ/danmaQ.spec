%global _icondir %{_datadir}/icons/hicolor
%global _commit 9fe006265ab3e7b796cdbb3a5c3993e76cbc8e68
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		danmaQ
Version:	0
Release:	1.git%{_shortcommit}%{?dist}
Summary:	DanmaQ is a small QT program to play danmaku on any screen

Group:		Applications/Internet
License:	GPLv3
URL:		https://github.com/tuna/danmaQ
#Source0:	%{url}/%{_commit}/%{name}-%{_shortcommit}.tar.gz
Source0:	%{url}/archive/%{_commit}.tar.gz

BuildRequires:	qt5-qtx11extras-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	cmake
BuildRequires:  desktop-file-utils

%description
DanmaQ, pronounced as /danmakju:/ is a small QT program to play danmaku on any screen.

%prep
%setup -q -n %{name}-%{_commit}

%build
mkdir build && cd build
cmake .. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release
%make_build


%install
# install 
install -Dm 0755 build/src/%{name} %{buildroot}%{_bindir}/%{name}

# icon files
install -Dm0644 src/icons/statusicon.ico    %{buildroot}%{_datadir}/pixmaps/statusicon.ico
install -Dm0644 src/icons/statusicon.png    %{buildroot}%{_datadir}/pixmaps/statusicon.png
install -Dm0644 src/icons/statusicon_disabled.png    %{buildroot}%{_datadir}/pixmaps/statusicon_disabled.png
install -Dm0644 src/icons/statusicon.svg %{buildroot}%{_icondir}/scalable/apps/statusicon.svg


# desktop file
install -d %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/%{name}.desktop <<EOF
[Desktop Entry]
Type=Application
Name=%{name}
Exec=%{name}
Icon=%{name}
EOF
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null ||:

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/
%{_datadir}/applications/%{name}.desktop

%changelog
* Tue Dec 20 2016 Zamir SUN <zsun@fedoraproject.org> - 0-1.git9fe0062
- Initial with danmaQ git 9fe006265ab3e7b796cdbb3a5c3993e76cbc8e68
