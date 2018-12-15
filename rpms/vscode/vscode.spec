%global debug_package %{nil}
%global __provides_exclude (npm)
%global __requires_exclude (npm|nodejs.abi)

%global arch       %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global strip()    find %1 -name "*.node" -exec strip {} \\;
%global yarn       node --max-old-space-size=%{mem_limit} %{_bindir}/npx yarn
%global mem_limit  4095

%global nodesqlurl https://github.com/mapbox/node-sqlite3
%global nodesqltgz %{nodesqlurl}/archive/%{nodesqlver}/%{nodesqlver}.tar.gz
%global nodesqlver 5bb0dc0e7511cf42cfda72f02e1354c4962c192b

%global commit     a684fe7ee136f89d92fa25ee0b8f9bdeacd104b6
%global scommit    %(c=%{commit}; echo ${c:0:7})
%global target     3.0.10

Name:    vscode
Version: 1.30.0
Release: 2%{?dist}
Summary: Visual Studio Code - An open source code editor
License: MIT
URL:     https://github.com/Microsoft/vscode
Source0: %{url}/archive/%{scommit}/%{name}-%{scommit}.tar.gz
Source1: product-release.json

BuildRequires: openssl
BuildRequires: python2, git
BuildRequires: npm, node-gyp
BuildRequires: pkgconfig(x11)
BuildRequires: pkgconfig(xkbfile)
BuildRequires: pkgconfig(libsecret-1)
BuildRequires: desktop-file-utils
BuildRequires: libappstream-glib
# sysctl_apply macro
BuildRequires: systemd
# /usr/lib/systemd/systemd-sysctl
Requires:      systemd
Requires:      electron >= %{target}

%description
 VS Code is a new type of tool that combines the simplicity of a code editor
 with what developers need for their core edit-build-debug cycle. Code provides
 comprehensive editing and debugging support, an extensibility model, and
 lightweight integration with existing tools.

%prep
%setup -q -n %{name}-%{commit}

# Skip preinstall check
sed -i '/preinstall/d' package.json

# Use system python2
# https://github.com/mapbox/node-sqlite3/issues/1044
sed -i '/sqlite/s|:.*"|: "%{nodesqltgz}"|' package.json

# Skip smoke test
sed -i '/smoketest/d' build/npm/postinstall.js

# Do not download electron
sed -i '/pipe.electron/d' build/gulpfile.vscode.js

# Set output directory
sed -i "/destin/s|=.*|='%{name}';|; /destin/s|result|all|
        /Asar/s|app|%{name}|" build/gulpfile.vscode.js

# Build native modules for system electron
sed -i '/target/s|".*"|"%{target}"|' .yarnrc

# Patch appdata and desktop file
sed -i resources/linux/code.{appdata.xml,desktop} \
 -e 's|%{_datadir}.*@@|%{name}|
     s|@@NAME_SHORT@@|VSCode|
     s|@@NAME_LONG@@|Visual Studio Code|
     s|@@NAME@@|%{name}|
     s|@@ICON@@|%{name}|
     s|@@LICENSE@@|MIT|
     s|inode/directory;||'

# Output release product.json
cp %{SOURCE1} product.json

# Disable crash reporter and telemetry service by default
sed -i '/default/s|:.*,|:false,|' src/vs/platform/telemetry/common/telemetryService.ts \
    src/vs/workbench/services/crashReporter/electron-browser/crashReporterService.ts

%build
export BUILD_SOURCEVERSION="%{commit}"
export NODE_OPTIONS="--max-old-space-size=%{mem_limit}"
npm config set python="/usr/bin/python2"
%yarn install
%strip node_modules
%yarn gulp %{name}-linux-%{arch}-min
rm -rf %{name}/*min

# Set application name
sed -i '/Code/s|:.*"|: "Code"|' %{name}/package.json

%install
# Install data files
install -d %{buildroot}%{_libdir}
cp -r %{name} %{buildroot}%{_libdir}

# Install binary
install -d %{buildroot}%{_bindir}
cat <<EOT > %{buildroot}%{_bindir}/%{name}
#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root
# for license information.

VSCODE_PATH="%{_libdir}/%{name}"
ELECTRON="%{_bindir}/electron"
CLI="\$VSCODE_PATH/out/cli.js"
ELECTRON_RUN_AS_NODE=1 "\$ELECTRON" "\$CLI" --app="\$VSCODE_PATH" "\$@"
exit \$?
EOT

# Install appdata and desktop file
pushd resources/linux
install -Dm644 code.appdata.xml %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
install -Dm644 code.desktop     %{buildroot}%{_datadir}/applications/%{name}.desktop
install -Dm644 code.png         %{buildroot}%{_datadir}/pixmaps/%{name}.png

# Set user watch files
#https://github.com/FZUG/repo/issues/210
install -d %{buildroot}%{_sysconfdir}/sysctl.d
cat > %{buildroot}%{_sysconfdir}/sysctl.d/50-%{name}.conf <<EOF
fs.inotify.max_user_watches=$((8192*64))
EOF

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/%{name}.appdata.xml
%yarn monaco-compile-check
%yarn strict-null-check

%posttrans
%sysctl_apply %{_sysconfdir}/sysctl.d/50-%{name}.conf

%files
%doc README.md ThirdPartyNotices.txt
%license LICENSE.txt
%{_sysconfdir}/sysctl.d/50-%{name}.conf
%attr(755,-,-) %{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%{_datadir}/metainfo/%{name}.appdata.xml

%changelog
* Fri Dec 14 2018 mosquito <sensor.wen@gmail.com> - 1.30.0-2
- Fix save file for electron-3
- Disable crash reporter and telemetry service by default
- Set max memory size via NODE_OPTIONS

* Wed Dec 12 2018 mosquito <sensor.wen@gmail.com> - 1.30.0-1
- Release 1.30.0

* Fri Dec  7 2018 mosquito <sensor.wen@gmail.com> - 1.29.1-1
- Release 1.29.1

* Sun Sep 24 2017 mosquito <sensor.wen@gmail.com> - 1.16.1-1
- Release 1.16.1

* Wed May 24 2017 mosquito <sensor.wen@gmail.com> - 1.12.2-1
- Release 1.12.2

* Sat Feb 11 2017 mosquito <sensor.wen@gmail.com> - 1.9.1-1
- Release 1.9.1

* Sat Jan  7 2017 mosquito <sensor.wen@gmail.com> - 1.8.1-2
- Fix watch files limit

* Tue Jan  3 2017 mosquito <sensor.wen@gmail.com> - 1.8.1-1
- Release 1.8.1

* Sat Dec  3 2016 mosquito <sensor.wen@gmail.com> - 1.7.2-2
- Fix reopen /usr/lib64/vscode/ directory every time

* Thu Dec  1 2016 mosquito <sensor.wen@gmail.com> - 1.7.2-1
- Release 1.7.2

* Sun Oct 16 2016 mosquito <sensor.wen@gmail.com> - 1.6.1-2
- Compute checksum

* Sat Oct 15 2016 mosquito <sensor.wen@gmail.com> - 1.6.1-1
- Release 1.6.1

* Thu Oct  6 2016 mosquito <sensor.wen@gmail.com> - 1.5.3-1
- Release 1.5.3

* Wed Jul 13 2016 mosquito <sensor.wen@gmail.com> - 1.3.1-1
- Release 1.3.1
- Build for electron 1.2.7

* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 1.2.1-1
- Release 1.2.1
- Build for electron 1.2.3

* Tue May 31 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-2
- Use ELECTRON_RUN_AS_NODE for Electron 1.2.0

* Mon May 30 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-1
- Release 1.2.0
- Build for electron 1.2.0
- Use ELECTRON_RUN_AS_NODE environment variable

* Fri May  6 2016 mosquito <sensor.wen@gmail.com> - 1.1.0-1
- Release 1.1.0 (insiders)
- Build for electron 0.37.8
- fsevents dont support linux
- Fix postinstall.js script

* Thu Apr 14 2016 mosquito <sensor.wen@gmail.com> - 1.0.0-1
- Release 1.0.0
- Improve i18n

* Wed Apr 13 2016 mosquito <sensor.wen@gmail.com> - 0.10.15-1
- Release 0.10.15 (insiders)
- Use gulp-tsb 1.10.3 for node 0.12

* Tue Apr 12 2016 mosquito <sensor.wen@gmail.com> - 0.10.14-2
- Build test for electron 0.37.5
- Use node 0.12 to build native module

* Wed Apr  6 2016 mosquito <sensor.wen@gmail.com> - 0.10.14-1
- Release 0.10.14 (insiders)
- Build test for electron 0.37.4, but running crash
- Use node 4.x to build native module
- Update nan 2.2.0, fixes oniguruma native module build error
- Fix crash by remove value of aiConfig
  https://github.com/electron/electron/issues/4299

* Sat Mar 12 2016 mosquito <sensor.wen@gmail.com> - 0.10.10-3
- Rebuild for electron 0.36.11

* Tue Mar  8 2016 mosquito <sensor.wen@gmail.com> - 0.10.10-2
- Fixed extensionsGallery url

* Tue Mar  8 2016 mosquito <sensor.wen@gmail.com> - 0.10.10-1
- Release 0.10.10
- Spilt package
- Update electron to 0.36.10

* Thu Feb 11 2016 mosquito <sensor.wen@gmail.com> - 0.10.8-1
- Release 0.10.8
- Remove welcome.md

* Thu Dec 24 2015 mosquito <sensor.wen@gmail.com> - 0.10.6-1
- Release 0.10.6

* Sun Dec 20 2015 mosquito <sensor.wen@gmail.com> - 0.10.5-1
- Release 0.10.5

* Fri Dec 04 2015 mosquito <sensor.wen@gmail.com> - 0.10.3-1
- Release 0.10.3

* Thu Nov 26 2015 mosquito <sensor.wen@gmail.com> - 0.10.2-1
- Release 0.10.2
- Add about information

* Wed Nov 25 2015 mosquito <sensor.wen@gmail.com> - 0.10.1-1
- Initial build
