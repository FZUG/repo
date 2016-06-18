%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%{?nodejs_find_provides_and_requires}
%global debug_package %{nil}
%global _hardened_build 1
%global __requires_exclude (npm|0.12)
%global __provides_exclude (npm)

%global project N1
%global repo %{project}
%global electron_ver 1.2.3
%global node_ver 0.12

# commit
%global _commit 76372654dc9f3d363636541ddefadbe08e63b918
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    n1
Version: 0.4.45
Release: 2.git%{_shortcommit}%{?dist}
Summary: an open-source mail client

Group:   Applications/System
License: MIT
URL:     https://nylas.com/N1/
Source0: https://github.com/nylas/N1/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Patch0:  n1-use-system-apm.patch
# https://github.com/nylas/N1/issues/107, https://github.com/atom/electron/issues/4778
Patch1:  n1-fix-renderer-path.patch
# fix protocol for Electron 1.2.3
Patch2:  n1-fix-protocol.patch

BuildRequires: node-gyp
BuildRequires: /usr/bin/npm
BuildRequires: nodejs-packaging
BuildRequires: libgnome-keyring-devel
BuildRequires: nodejs-atom-package-manager
Requires: nodejs-atom-package-manager
Requires: electron = %{electron_ver}

%description
N1 is an open-source mail client built on the modern web with Electron,
React, and Flux. It is designed to be extensible, so it's easy to create
new experiences and work-flows around email.
N1 is built on the Nylas Sync Engine which is also open source free software.

Visit https://nylas.com/N1/ to learn more.

%prep
%setup -q -n %repo-%{_commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1

# apm with system (updated) nodejs cannot 'require' modules inside asar
sed -e "s|, 'generate-asar'||" -i build/Gruntfile.coffee

%build
export CFLAGS="%{optflags} -fPIC -pie"
export CXXFLAGS="%{optflags} -fPIC -pie"

# Update node for fedora 23
%if 0%{?fedora} < 24
git clone https://github.com/creationix/nvm.git .nvm
source .nvm/nvm.sh
nvm install %{node_ver}
nvm use %{node_ver}
%endif

# Build package
node-gyp -v; node -v; npm -v; apm -v
## https://github.com/nylas/N1/blob/master/script/bootstrap
# If unset, ~/.atom/.node-gyp/.atom/.npm is used
## https://github.com/atom/electron/blob/master/docs/tutorial/using-native-node-modules.md
npm_config_cache="${HOME}/.nylas"
npm_config_disturl="https://atom.io/download/atom-shell"
npm_config_target="%{electron_ver}"
#npm_config_target_arch="x64|ia32"
npm_config_runtime="electron"
# The npm_config_target is no effect, set ATOM_NODE_VERSION
## https://github.com/atom/apm/blob/master/src/command.coffee
ATOM_ELECTRON_VERSION="%{electron_ver}"
ATOM_ELECTRON_URL="$npm_config_disturl"
ATOM_RESOURCE_PATH="`pwd`"
ATOM_HOME="$npm_config_cache"

_packagesToDedupe=(
    'fs-plus'
    'humanize-plus'
    'roaster'
    'season'
    'grim'
)

# 1. Installing N1 build tools (like Grunt)
pushd build; npm install --loglevel error; popd
script/grunt add-nylas-build-resources

# 2. Installing apm
# NPM=`pwd`/build/node_modules/.bin/npm
# cd apm; $NPM --target=0.10.40 install
# 2.1 Flattening apm package tree
# cd node_modules/npm; $NPM --target=0.10.40 dedupe
# 2.2 Cleaning apm
# ../atom-package-manager/bin/apm clean

export ATOM_ELECTRON_VERSION ATOM_ELECTRON_URL \
       ATOM_RESOURCE_PATH ATOM_HOME

# 3. build internal package
pushd internal_packages
for dir in `ls`; do
    Pkg="$dir/package.json"
    Num=`awk '/depend/{print FNR}' $Pkg`
    Str=`sed -n "$(($Num+1))s| *||p" $Pkg`
    if [ "$Str" != "}" ]; then
        echo "Installing dependencies for $dir"
        pushd "$dir"; /bin/apm install --verbose; popd
    fi
done
popd

# 4. Installing N1 dependencies
/bin/apm install --verbose
# 4.1 De-duping packages
/bin/apm dedupe ${_packagesToDedupe[@]}

# 5. Installing integration test modules
#pushd spec_integration
#$NPM install --loglevel error
#popd

# 6. Building sqlite3
npm install https://github.com/bengotow/node-sqlite3/archive/bengotow/fts5.tar.gz \
  --ignore-scripts --loglevel error && pushd node_modules/sqlite3 && \
node-gyp configure rebuild --target="%{electron_ver}" --target_platform=linux \
  --arch="%{arch}" --dist-url="$npm_config_disturl" --module_name=node_sqlite3 \
  --module_path="../lib/binding/electron-v1.2-linux-%{arch}" && popd

# 7. Packaging files
script/grunt --build-dir='n1-build'

%install
install -d %{buildroot}%{_libdir}/nylas
cp -r n1-build/Nylas/resources/app/* %{buildroot}%{_libdir}/nylas
rm -rf %{buildroot}%{_libdir}/nylas/node_modules

install -d %{buildroot}%{_datadir}/applications
sed -e \
   's|<%= description %>|%{summary}|
    s|<%= linuxShareDir %>/<%= appFileName %>|%{name}|
    s|<%= iconName %>|%{name}|' \
    build/resources/linux/nylas.desktop.in > \
    %{buildroot}%{_datadir}/applications/%{name}.desktop

install -d %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
#!/bin/bash
ELECTRON="%{_bindir}/electron-%{electron_ver}"
NYLAS_PATH="%{_libdir}/nylas"
NYLAS_HOME="\${NYLAS_HOME:-\$HOME/.nylas}"
mkdir -p "\$NYLAS_HOME"

(
  nohup "\$ELECTRON" "\$NYLAS_PATH" --executed-from="\$(pwd)" --pid=\$\$ "\$@" > "\$NYLAS_HOME/nohup.out" 2>&1
  if [ \$? -ne 0 ]; then
    cat "\$NYLAS_HOME/nohup.out"
    exit \$?
  fi
) &
EOF

# copy over icons in sizes that most desktop environments like
for i in 512 256 128 64 32; do
    install -D -m 0644 n1-build/icons/${i}.png \
      %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# find all *.js files and generate node.file-list
pushd n1-build/Nylas/resources/app
for ext in js json node types less png; do
  find node_modules -iname \*.${ext} \
    ! -name '.*' \
    ! -path '*/test*' \
    ! -path '*tests*' \
    ! -path '*example*' \
    ! -path '*benchmark*' \
    -exec sh -c "strip '{}' &>/dev/null ||:" \; \
    -exec install -Dm644 '{}' '%{buildroot}%{_libdir}/nylas/{}' \;
done
popd

pushd %{buildroot}%{_libdir}
find -type f -exec chmod 644 '{}' \;
find -name '*.js' -exec sh -c "head -n2 '{}'|grep -q '^#\!/usr/bin/env'&&rm -rf '{}'" \;
find nylas \
    -name '.*' -or \
    -name 'bin' -or \
    -name 'man' -or \
    -name 'CHANGE*' -or \
    -name 'CONTRIBUT*' -or \
    -name 'LICENSE' -or \
    -name 'README*' -or \
    -name 'test*' -or \
    -name 'example*' -or \
    -name 'benchmark' -or \
    -name 'dashdash.bash*' -or \
    -size 0 | xargs rm -rf

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
%license LICENSE.md
%attr(755,-,-) %{_bindir}/%{name}
%{_libdir}/nylas/
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png

%changelog
* Sat Jun 18 2016 mosquito <sensor.wen@gmail.com> - 0.4.45-2.git7637265
- Fix double windows
* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 0.4.45-1.git7637265
- Release 0.4.45
- Build for electron 1.2.3
- Fix protocol for Electron 1.2.3
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 0.4.40-1.git85cf726
- Release 0.4.40
- Build for electron 1.2.0
- Update node 0.12 for fedora 23
* Fri May  6 2016 mosquito <sensor.wen@gmail.com> - 0.4.33-1.gite8f137e
- Release 0.4.33
- Build for electron 0.37.8
* Wed Apr 13 2016 mosquito <sensor.wen@gmail.com> - 0.4.25-1.gita22631a
- Release 0.4.25
* Tue Apr 12 2016 mosquito <sensor.wen@gmail.com> - 0.4.19-3.gitd41e72c
- Rebuild for electron 0.37.5
- Remove BReq git-core nodejs
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 0.4.19-2.gitd41e72c
- Fixes keytar build error, require libgnome-keyring-devel
- Fixes no found mime.types file
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 0.4.19-1.gitd41e72c
- Release 0.4.19
* Mon Mar 21 2016 mosquito <sensor.wen@gmail.com> - 0.4.16-1.git8cb7748
- Release 0.4.16
* Sun Mar 13 2016 mosquito <sensor.wen@gmail.com> - 0.4.14-2.git53cd69b
- Fixes renderer path
* Sat Mar 12 2016 mosquito <sensor.wen@gmail.com> - 0.4.14-1.git53cd69b
- Initial package
