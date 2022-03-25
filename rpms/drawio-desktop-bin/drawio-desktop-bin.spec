Name:           drawio-desktop-bin
Version:        17.2.1
Release:        1%{?dist}
Summary:        Diagram drawing application built on web technology

License:        ASL 2.0
URL:            https://github.com/jgraph/drawio-desktop
Source0:        %{url}/releases/download/v%{version}/drawio-amd64-%{version}.deb
Source1:        https://raw.githubusercontent.com/jgraph/drawio-desktop/release/LICENSE
Source2:        drawio-launcher.sh

Requires:       electron16

%description
%{summary}.

%prep
ar x %{S:0}
tar -xf data.tar.xz

%build
sed -i "s|/opt/drawio/drawio|drawio|g" usr/share/applications/drawio.desktop
cp %{S:1} .

%install
%{__install} -Dm644 opt/drawio/resources/app.asar -t %{buildroot}/%{_prefix}/lib/drawio-desktop
%{__install} -d %{buildroot}%{_datadir}
%{__cp} -a usr/share/{applications,icons,mime} -t %{buildroot}%{_datadir}
%{__install} -Dm755 %{S:2} %{buildroot}%{_bindir}/drawio


%files
%license LICENSE
%{_bindir}/drawio
%{_prefix}/lib/drawio-desktop/app.asar
%{_datadir}/applications/drawio.desktop
%{_datadir}/icons/hicolor/*/apps/drawio.png
%{_datadir}/mime/packages/drawio.xml

%changelog
* Fri Mar 25 2022 zhullyb <zhullyb@outlook.com> - 17.2.1-1
- First build.
