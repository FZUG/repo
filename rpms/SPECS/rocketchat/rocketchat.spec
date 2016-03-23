%{?nodejs_find_provides_and_requires}
%global debug_package %{nil}
%global _hardened_build 1
%global __requires_exclude (npm)
%global __provides_exclude (npm)

%global project Rocket.Chat.Electron
%global repo %{project}
%global node_ver 0.12

# commit
%global _commit f74b8254b81549ebd39d7176b204e2fc08464093
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    rocketchat
Version: 1.2.0
Release: 2.git%{_shortcommit}%{?dist}
Summary: an open-source chat client

Group:   Applications/System
License: MIT
URL:     https://rocket.chat/
Source0: https://github.com/RocketChat/Rocket.Chat.Electron/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch: noarch
BuildRequires: npm
BuildRequires: git-core
BuildRequires: node-gyp
BuildRequires: nodejs >= 0.10.0
BuildRequires: nodejs-packaging
Requires: electron

%description
From group messages and video calls all the way to helpdesk killer features.
Our goal is to become the number one cross-platform open source chat solution.

%prep
%setup -q -n %repo-%{_commit}
sed -i '/electron-prebuilt/d' package.json
git clone https://github.com/creationix/nvm.git .nvm
source .nvm/nvm.sh
nvm install %{node_ver}
npm config set python=`which python2`

%build
node-gyp -v; node -v; npm -v
source .nvm/nvm.sh
nvm use %{node_ver}
npm install --loglevel error
node_modules/.bin/gulp build --env=production

%install
rm -rf build/images/{osx,windows,_templates}

install -d %{buildroot}%{_datadir}/%{name}
cp -r build/* %{buildroot}%{_datadir}/%{name}
rm -rf %{buildroot}%{_datadir}/%{name}/node_modules

install -d %{buildroot}%{_datadir}/applications
sed -e \
   's|{{productName}}|%{name}|
    s|{{description}}|%{summary}|
    s|/opt/{{name}}/{{name}}|%{name}|
    s|/opt/{{name}}/icon|%{name}|
    /Path/d' \
    resources/linux/app.desktop > \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/bash
ELECTRON="%{_bindir}/electron"
ROOT_PATH="%{_datadir}/%{name}"
"\$ELECTRON" "\$ROOT_PATH" --executed-from="\$(pwd)" --pid=\$\$ "\$@"
EOF

install -Dm644 build/images/icon.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/%{name}.png

# find all *.js files and generate node.file-list
pushd build/node_modules
for ext in js json; do
  find -iname *.${ext} \
    ! -name '.*' \
    ! -name 'bin' \
    ! -path '*test*' \
    ! -path '*example*' \
    ! -path '*benchmark*' \
    -exec install -Dm644 '{}' '%{buildroot}%{_datadir}/%{name}/node_modules/{}' \;
done
popd

pushd %{buildroot}%{_datadir}
find -type f -exec chmod 644 '{}' \;

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
/usr/bin/update-desktop-database &>/dev/null ||:

%postun
if [ $1 -eq 0 ]; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null ||:
    /usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:
fi
/usr/bin/update-desktop-database &>/dev/null ||:

%posttrans
/usr/bin/gtk-update-icon-cache -f -t -q %{_datadir}/icons/hicolor ||:

%files
%defattr(-,root,root,-)
%doc README.md
%attr(755,-,-) %{_bindir}/%{name}
%{_datadir}/%{name}/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Wed Mar 23 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-2.gitf74b825
- Release 1.2.0
* Sat Mar 12 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-1.gitabb7b81
- Initial package
