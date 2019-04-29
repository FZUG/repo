%global debug_package %{nil}

Name:           netease-cloud-music
Version:        1.2.0.2
Release:        1%{?dist}
Summary:        Netease Cloud Music, converted from .deb package
License:        EULA
URL:            https://music.163.com/
Source0:        https://packages.deepin.com/deepin/pool/main/n/%{name}/%{name}_%{version}-1_amd64.deb
Source1:        %{name}.appdata.xml
BuildRequires:  dpkg
BuildRequires:  desktop-file-utils
Requires:       desktop-file-utils
Requires:       gstreamer1-plugins-ugly

%description
%{summary}.

%prep
dpkg -X %{S:0} .
find usr -type f -exec mv {} . \;

%install
install -Dm755 %{name} %{buildroot}%{_bindir}/%{name}
install -Dm644 %{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm644 %{name}.svg %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
install -Dm644 %{S:1} %{buildroot}%{_metainfodir}/%{name}.appdata.xml

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%files
%doc README.md
%license copyright
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_metainfodir}/%{name}.appdata.xml

%changelog
* Mon Apr 29 2019 Bangjie Deng <dengbangjie@foxmail.com> - 1.2.0.2-1
- Update to 1.2.0.2

* Mon Dec 31 2018 mosquito <sensor.wen@gmail.com> - 1.1.3.1-1
- Update to 1.1.3.1

* Sun Mar 25 2018 robberphex <robberphex@gmail.com> - 1.1.0-1
- Update to 1.1.0
- Add appdata.xml

* Mon Oct 03 2016 nrechn <nrechn@gmail.com> - 1.0.0-2
- Fix source libssl not found
- Update source libssl package

* Sun Jul 31 2016 mosquito <sensor.wen@gmail.com> - 1.0.0-1
- Update to 1.0.0

* Tue May 31 2016 mosquito <sensor.wen@gmail.com> - 0.9.0-2
- Add Req gstreamer1-plugins-ugly

* Wed May 25 2016 mosquito <sensor.wen@gmail.com> - 0.9.0-1
- Initial build
