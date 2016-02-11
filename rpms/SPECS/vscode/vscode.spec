%global debug_package %{nil}
%global _hardened_build 1
%global __provides_exclude (libnode)
%global __requires_exclude (libnode)
%global project vscode
%global repo %{project}

# commit
%global _commit 149e7a0debf3e32f95978a606e00d3c09bcac3d6
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    vscode
Version: 0.10.8
Release: 1%{?dist}
Summary: Visual Studio Code - An open source code editor

Group:   Development/Tools
License: MIT
URL:     https://github.com/Microsoft/vscode
Source0: https://github.com/Microsoft/vscode/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Source1: about.json

BuildRequires: npm, node-gyp
BuildRequires: python, make, libX11-devel
BuildRequires: desktop-file-utils, git

%description
 VS Code is a new type of tool that combines the simplicity of a code editor
 with what developers need for their core edit-build-debug cycle. Code provides
 comprehensive editing and debugging support, an extensibility model, and
 lightweight integration with existing tools.

%prep
%setup -q -n %{repo}-%{_commit}
git clone https://github.com/creationix/nvm.git .nvm
source .nvm/nvm.sh
nvm install 0.12
nvm use 0.12
npm config set python `which python`
npm install -g gulp

%build
export CFLAGS="%{optflags} -fPIC -pie"
export CXXFLAGS="%{optflags} -fPIC -pie"

source .nvm/nvm.sh
nvm use 0.12
scripts/npm.sh install
%ifarch x86_64
gulp vscode-linux-x64
%else
gulp vscode-linux-ia32
%endif

%install
# Data files
mkdir --parents %{buildroot}%{_datadir}/%{name}
cp -a ../VSCode-linux-*/. %{buildroot}%{_datadir}/%{name}
mv %{buildroot}%{_datadir}/%{name}/{Code*,%{name}}

# Bin file
mkdir --parents %{buildroot}%{_bindir}
ln -sfv %{_datadir}/%{name}/%{name} %{buildroot}%{_bindir}/

# Icon files
install -Dm 0644 resources/linux/code.png %{buildroot}%{_datadir}/pixmaps/%{name}.png
mv %{buildroot}%{_datadir}/%{name}/resources/app/resources/linux/{code,%{name}}.png

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
install -m 0644 %{S:1} %{buildroot}%{_datadir}/%{name}/resources/app/product.json
sed -i -e \
   '/Short/s|:.*,$|: "VSCode",|
    /Long/s|:.*,$|: "Visual Studio Code",|' \
    %{buildroot}%{_datadir}/%{name}/resources/app/product.json

# About.json
sed -i '$a\\t"commit": "%{_commit}",\n\t"date": "'`date -u +%FT%T.%3NZ`'"\n}' \
    %{buildroot}%{_datadir}/%{name}/resources/app/product.json
sed -i '2s|:.*,$|: "VSCode",|' \
    %{buildroot}%{_datadir}/%{name}/resources/app/package.json

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
%doc README.md ThirdPartyNotices.txt
%license LICENSE.txt
%{_bindir}/%{name}
%dir %{_datadir}/%{name}/
%{_datadir}/%{name}/*
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/applications/%{name}.desktop
%attr(755,root,root) %{_datadir}/%{name}/%{name}
%attr(755,root,root) %{_datadir}/%{name}/libnode.so
%exclude %{_datadir}/%{name}/libgcrypt.so.*
%exclude %{_datadir}/%{name}/libnotify.so.*

%changelog
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
