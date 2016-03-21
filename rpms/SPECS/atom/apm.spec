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

# commit
%global _commit 955326e9361d7b03499e21b7c06905864ef616c9
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    nodejs-atom-package-manager
Version: 1.7.1
Release: 3.git%{_shortcommit}%{?dist}
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
BuildRequires: git-core
Requires: libgnome-keyring
Requires: git-core
Requires: python2

%description
apm - Atom Package Manager
Discover and install Atom packages powered by https://atom.io

%prep
%setup -q -n %repo-%{_commit}
sed -i 's|<lib>|%{_lib}|' %{P:1}
%patch0 -p1
%patch1 -p1

# Fix location of Atom app
sed -i 's|share/atom/resources/app.asar|%{_lib}/atom|g' src/apm.coffee

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
npm install --loglevel info
npm install --loglevel info -g --prefix build/usr

%install
cp -pr build/. %{buildroot}
rm -rf %{buildroot}%{nodejs_sitelib}/atom-package-manager/node_modules

pushd build/%{nodejs_sitelib}/atom-package-manager/node_modules
npm dedupe
for ext in js json node gypi; do
    find -regextype posix-extended \
      -iname "*.${ext}" \
    ! -name '.*' \
    ! -name 'config.gypi' \
    ! -path '*deps' \
    ! -path '*test*' \
    ! -path '*obj.target*' \
    ! -path '*html*' \
    ! -path '*example*' \
    ! -path '*sample*' \
    ! -path '*benchmark*' \
    ! -regex '.*(oniguruma|git-utils|keytar)/node.*' \
      -exec install -Dm644 '{}' '%{buildroot}%{nodejs_sitelib}/atom-package-manager/node_modules/{}' \;
done

# Remove some files
find %{buildroot} -regextype posix-extended -type f \
    -regex '.*js$' -exec sh -c "sed -i '/^#\!\/usr\/bin\/env/d' '{}'" \; -or \
    -regex '.*node' -exec strip '{}' \; -or \
    -name '.*' -exec rm -rf '{}' \; -or \
    -name '*.md' -delete -or \
    -name 'apm.cmd' -delete

%files
%defattr(-,root,root,-)
%doc README.md
%license LICENSE.md
%{_bindir}/apm
%{nodejs_sitelib}/atom-package-manager/

%changelog
* Mon Mar 21 2016 mosquito <sensor.wen@gmail.com> - 1.7.1-3.git955326e
- Fixed fc24 build error
- Rewrite install script
* Sat Mar 12 2016 mosquito <sensor.wen@gmail.com> - 1.7.1-2.git955326e
- Add requires python2, git-core, libgnome-keyring
* Sat Mar  5 2016 mosquito <sensor.wen@gmail.com> - 1.7.1-1.git955326e
- Release 1.7.1
* Sun Feb 14 2016 mosquito <sensor.wen@gmail.com> - 1.7.0-1.git829b81a
- Initial package
