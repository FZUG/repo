# build Atom and Electron packages: https://github.com/tensor5/arch-atom
# RPM spec: http://pkgs.fedoraproject.org/cgit/rpms/?q=nodejs
%{?nodejs_find_provides_and_requires}
%global debug_package %{nil}
%global _hardened_build 1
%global __provides_exclude_from %{nodejs_sitelib}/.*/node_modules
%global __requires_exclude_from %{nodejs_sitelib}/.*/node_modules
%global __requires_exclude (npm)

%global project apm
%global repo %{project}
%global npm_ver 2.13.3

# commit
%global _commit 829b81a1f7c55e882ea0523d4f325b5c1b8b283f
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    nodejs-atom-package-manager
Version: 1.7.0
Release: 1.git%{_shortcommit}%{?dist}
Summary: Atom package manager

Group:   Applications/System
License: MIT
URL:     https://github.com/atom/apm/
Source0: https://github.com/atom/apm/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
Patch0:  use-system-nodejs.patch
Patch1:  get-electron-version.patch

BuildRequires: npm
BuildRequires: node-gyp
BuildRequires: nodejs-packaging
BuildRequires: libgnome-keyring-devel
BuildRequires: python2-devel
BuildRequires: git-core

%description
apm - Atom Package Manager
Discover and install Atom packages powered by https://atom.io

%prep
%setup -q -n %repo-%{_commit}
sed -i 's|<lib>|%{_lib}|' %{P:1}
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"

# Upgrade npm
## Install new npm to INSTALL_PREFIX for build package
npm config set registry="http://registry.npmjs.org/"
npm config set ca ""
npm config set strict-ssl false
npm config set python `which python2`
npm install -g --ca=null --prefix %{buildroot}%{_prefix} npm@%{npm_ver}
## Export PATH to new npm version
export PATH="%{buildroot}%{_bindir}:$PATH"
node-gyp -v; node -v; npm -v

# Build package
npm install --loglevel info

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/atom-package-manager
cp -pr deprecated-packages.json package.json bin lib native-module script templates \
    %{buildroot}%{nodejs_sitelib}/atom-package-manager

mkdir -p %{buildroot}%{_bindir}
ln -sfv %{nodejs_sitelib}/atom-package-manager/bin/apm %{buildroot}%{_bindir}

pushd node_modules
Mods="asar-require async colors exit first-mate fs-plus git-utils keytar mv ncp \
      npm open plist q read season temp underscore-plus wordwrap wrench yargs"

# Find all *.js files and generate node.file-list
for mod in `echo $Mods`; do
  for ext in js json py gypi; do
    find $mod -regextype posix-extended -type f \
      \( -iname "*.${ext}" -or -perm 755 \) \
      ! -regex '.*\.(bat|cmd|sh)$' \
      ! -name '.*' \
      ! -name 'cibuild' \
      ! -name 'LICENSE*' \
      ! -name 'README*' \
      ! -name 'Makefile*' \
      ! -path '*deps*' \
      ! -path '*test*' \
      ! -path '*obj.target*' \
      ! -regex '.*(oniguruma|git-utils|keytar)/node.*' -prune \
      ! -name 'config.gypi' \
      ! -path '*html*' \
      ! -path '*sample*' \
      ! -path '*example*' \
      ! -path '*benchmark*' \
      -exec install -D '{}' '%{buildroot}%{nodejs_sitelib}/atom-package-manager/node_modules/{}' \; \
      -exec echo '%%{nodejs_sitelib}/atom-package-manager/node_modules/{}' >> ../node.file-list \;
  done
done
popd
sort -u -o node.file-list node.file-list
sed -i 's|py$|py\*|' node.file-list

# Fix location of Atom app
sed -e 's|share/atom/resources/app.asar|%{_lib}/atom|g' \
    -i %{buildroot}%{nodejs_sitelib}/atom-package-manager/lib/apm.js

# Remove the executable bits
find %{buildroot} -type f -regextype posix-extended \( \
    -regex '.*(js|py)$' -exec sh -c "head -n2 '{}'|grep -q '^#\!/usr/bin/env' && chmod a+x '{}' || chmod 644 '{}'" \; -or \
    -regex '.*(json|conf|gypi)$' -exec chmod 644 '{}' \; -or \
    -regex '.*node' -perm 755 -exec strip '{}' \; -or \
    -regex '.*(.gitignore.*|apm.cmd|binding.gyp$)' -exec rm -f '{}' \; \)

%files -f node.file-list
%defattr(-,root,root,-)
%doc README.md
%license LICENSE.md
%{_bindir}/apm
%dir %{nodejs_sitelib}/atom*
%{nodejs_sitelib}/atom*/bin/
%{nodejs_sitelib}/atom*/lib/
%{nodejs_sitelib}/atom*/native-module/
%{nodejs_sitelib}/atom*/script/
%{nodejs_sitelib}/atom*/templates/
%{nodejs_sitelib}/atom*/package.json
%{nodejs_sitelib}/atom*/deprecated-packages.json

%changelog
* Sun Feb 14 2016 mosquito <sensor.wen@gmail.com> - 1.7.0-1.git829b81a
- Initial package
