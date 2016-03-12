%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global debug_package %{nil}
%global _hardened_build 1
%global __provides_exclude (npm)
%global __requires_exclude (npm)

%global project vscode
%global repo %{project}
%global electron_ver 0.36.11
%global node_ver 0.12

# commit
%global _commit 5b5f4db87c10345b9d5c8d0bed745bcad4533135
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    vscode
Version: 0.10.10
Release: 3%{?dist}
Summary: Visual Studio Code - An open source code editor

Group:   Development/Tools
License: MIT
URL:     https://github.com/Microsoft/vscode
Source0: https://github.com/Microsoft/vscode/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
# https://github.com/Microsoft/vscode/blob/master/src/vs/workbench/electron-main/env.ts
Source1: about.json

BuildRequires: npm, node-gyp
BuildRequires: python, make, libX11-devel
BuildRequires: desktop-file-utils, git
Requires: electron

%description
 VS Code is a new type of tool that combines the simplicity of a code editor
 with what developers need for their core edit-build-debug cycle. Code provides
 comprehensive editing and debugging support, an extensibility model, and
 lightweight integration with existing tools.

%prep
%setup -q -n %{repo}-%{_commit}
# https://github.com/Microsoft/vscode/pull/2559
sed -i '/electronVer/s|:.*,$|: "%{electron_ver}",|' package.json
sed -i '/pipe.electron/s|^|//|' build/gulpfile.vscode.js
git clone https://github.com/creationix/nvm.git .nvm
source .nvm/nvm.sh
nvm install %{node_ver}
npm config set python=`which python2`

%build
export CFLAGS="%{optflags} -fPIC -pie"
export CXXFLAGS="%{optflags} -fPIC -pie"
source .nvm/nvm.sh
nvm use %{node_ver}
scripts/npm.sh install --loglevel info
node_modules/.bin/gulp vscode-linux-%{arch}
npm dedupe

%install
# Data files
mkdir --parents %{buildroot}%{_libdir}/%{name}
cp -a ../VSCode-linux-*/. %{buildroot}%{_libdir}/%{name}
rm -rf %{buildroot}%{_libdir}/%{name}/node_modules

# Bin file
mkdir --parents %{buildroot}%{_bindir}
cat <<EOT >> %{buildroot}%{_bindir}/%{name}
#!/usr/bin/env bash
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root
# for license information.

NAME="%{name}"
VSCODE_PATH="%{_libdir}/\$NAME"
ELECTRON="%{_bindir}/electron"
CLI="\$VSCODE_PATH/out/cli.js"
ATOM_SHELL_INTERNAL_RUN_AS_NODE=1 "\$ELECTRON" "\$CLI" "\$VSCODE_PATH" "\$@"
exit \$?
EOT

# Icon files
install -Dm 0644 resources/linux/code.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# Desktop file
mkdir --parents %{buildroot}%{_datadir}/applications
cat <<EOT >> %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Type=Application
Name=Visual Studio Code
GenericName=VS Code
Comment=Code Editing. Redefined.
Exec=%{name}
Icon=%{name}
Terminal=false
Categories=GTK;Development;IDE;
MimeType=text/plain;text/x-chdr;text/x-csrc;text/x-c++hdr;text/x-c++src;text/x-java;text/x-dsrc;text/x-pascal;text/x-perl;text/x-python;application/x-php;application/x-httpd-php3;application/x-httpd-php4;application/x-httpd-php5;application/xml;text/html;text/css;text/x-sql;text/x-diff;
StartupNotify=true
EOT

desktop-file-install --mode 0644 %{buildroot}%{_datadir}/applications/%{name}.desktop

# Change appName
install -m 0644 %{S:1} %{buildroot}%{_libdir}/%{name}/product.json
sed -i -e \
   '/Short/s|:.*,$|: "VSCode",|
    /Long/s|:.*,$|: "Visual Studio Code",|' \
    %{buildroot}%{_libdir}/%{name}/product.json

# About.json
sed -i '$a\\t"commit": "%{_commit}",\n\t"date": "'`date -u +%FT%T.%3NZ`'"\n}' \
    %{buildroot}%{_libdir}/%{name}/product.json
sed -i '2s|:.*,$|: "VSCode",|' \
    %{buildroot}%{_libdir}/%{name}/package.json

# find all *.js files and generate node.file-list
pushd ../VSCode-linux-*/node_modules
for ext in js json node; do
    find -iname "*.${ext}" \
    ! -path '*doc*' \
    ! -path '*test*' \
    ! -path '*tools*' \
    ! -path '*example*' \
    ! -path '*obj.target*' \
    -exec sh -c "strip '{}' &>/dev/null ||:" \; \
    -exec install -Dm644 '{}' '%{buildroot}%{_libdir}/%{name}/node_modules/{}' \; \
    -exec echo '%%{_libdir}/%{name}/node_modules/{}' >> \
    %{_builddir}/%{repo}-%{_commit}/node.file-list \;
done
popd
sort -u -o node.file-list node.file-list

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

%files -f node.file-list
%defattr(-,root,root,-)
%doc README.md ThirdPartyNotices.txt
%license LICENSE.txt
%attr(755,-,-) %{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/applications/%{name}.desktop

%changelog
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
