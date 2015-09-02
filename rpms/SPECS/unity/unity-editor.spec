# http://forum.unity3d.com/threads/fedora-22.350432
# http://forum.unity3d.com/threads/unity-on-linux-release-notes-and-known-issues.350256
# chrome-sandbox requires this: https://code.google.com/p/chromium/wiki/LinuxSUIDSandbox
%global debug_package %{nil}
%global repo Unity
%global _build f3
%global _buildtag 2015082501

Name: unity-editor
Version: 5.1.0%{_build}
Release: 1%{?dist}
Summary: Editor for the Unity Game Engine
License: Proprietary
URL: http://unity3d.com
Source0: http://download.unity3d.com/download_unity/%{name}-%{version}+%{_buildtag}_amd64.deb

BuildRequires: dpkg
BuildRequires: desktop-file-utils
Requires: alsa-lib expat libpng12
%filter_provides_in -P ^/opt/%{repo}/(MonoDevelop/.*|Editor/Data/.*)$
%filter_requires_in -P ^/opt/%{repo}/(MonoDevelop/.*|Editor/Data/.*)$
%filter_from_requires /mono/d; /local/d; /Geometry/d; /crypto/d; /element/d;
%filter_from_requires /Texture/d; /Unwrap/d; /libcapi/d; /libcef/d;
%filter_from_requires /libdlog/d; /libefl/d; /libumbra/d; /libdl.*2.4/d;
%filter_from_requires /GCC_3.5/d; /libpq/d; /ARM/d; /libCg/d; /ecore/d;
%filter_setup

# If you need to export players to certain targets, there are other dependencies:
# For WebGL: ffmpeg nodejs java6-runtime gzip
# For Android and Tizen: java7-jdk Android-jdk

%description
 Unity is a flexible and powerful development platform for creating
 multiplatform 3D and 2D games and interactive experiences. It's a
 complete ecosystem for anyone who aims to build a business on creating
 high-end content and connecting to their most loyal and enthusiastic
 players and customers.

%prep
%build

%install
dpkg-deb -X %{SOURCE0} %{buildroot}

# unity and monodevelop start script
install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/bash
/opt/%{repo}/Editor/%{repo}
EOF
cat > %{buildroot}%{_bindir}/unity-monodevelop <<EOF
#!/bin/bash
/opt/%{repo}/MonoDevelop/bin/monodevelop
EOF

%post
update-desktop-database -q ||:
touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
/sbin/ldconfig

%postun
if [ $1 -eq 0 ]; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
update-desktop-database -q ||:
/sbin/ldconfig

%files
%defattr(-,root,root,-)
%attr(0755,root,root) %{_bindir}/%{name}
%attr(0755,root,root) %{_bindir}/unity-monodevelop
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*
%{_defaultdocdir}/%{name}
/opt/%{repo}/
%attr(4755,root,root) /opt/%{repo}/Editor/chrome-sandbox

%changelog
* Tue Sep  1 2015 mosquito <sensor.wen@gmail.com> - 5.1.0f3-1
- Initial build
