# build Atom and Electron packages: https://github.com/tensor5/arch-atom
# RPM spec: http://pkgs.fedoraproject.org/cgit/rpms/?q=nodejs
# https://fedoraproject.org/wiki/Packaging:Node.js
%{?nodejs_find_provides_and_requires}
%global _cpln %(test $(rpm -E%?fedora) -gt 23 && echo "ln -s" || echo "cp -p")
%global debug_package %{nil}
%global _hardened_build 1
%global __provides_exclude_from %{nodejs_sitelib}/.*/node_modules
%global __requires_exclude_from %{nodejs_sitelib}/.*/node_modules
%global __requires_exclude (npm)

%global project apm
%global repo %{project}

# commit
%global _commit 87b4bcb678682ff9e64f8aa1e11dd8d51c1ab2c5
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    nodejs-atom-package-manager
Version: 1.10.0
Release: 2.git%{_shortcommit}%{?dist}
Summary: Atom package manager

Group:   Applications/System
License: MIT
URL:     https://github.com/atom/apm/
Source0: https://github.com/atom/apm/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

Patch0:  use-system-nodejs.patch
Patch1:  get-electron-version.patch
Patch2:  use-system-npm.patch
Patch3:  fetch-local-pkgs.patch
Patch4:  use-local-node-devel.patch

BuildRequires: npm, git
BuildRequires: nodejs-packaging
BuildRequires: libgnome-keyring-devel
Requires: /usr/bin/npm, git, python2
# In fc25, the nodejs contains /bin/npm, and it do not depend node-gyp
Requires: node-gyp

%description
apm - Atom Package Manager
Discover and install Atom packages powered by https://atom.io

%prep
%setup -q -n %repo-%{_commit}
sed -i 's|<lib>|%{_lib}|' %{P:1} %{P:4}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

# Fix location of Atom app
sed -i 's|share/atom/resources/app.asar|%{_lib}/atom|g' src/apm.coffee

# Fix system arch of dedupe
sed -i "/ia32/s|ia32'|' + process.arch|" src/dedupe.coffee

# Do not download node 0.10
sed -i '/download-node/d' package.json

%build
export CFLAGS="%{optflags}"
export CXXFLAGS="%{optflags}"
npm install --loglevel info
npm install --loglevel info -g --prefix build/usr

# Copy system node binary
%{_cpln} %{_bindir}/node build%{nodejs_sitelib}/atom-package-manager/bin

%install
cp -pr build/. %{buildroot}
rm -rf %{buildroot}%{nodejs_sitelib}/atom-package-manager/{node_modules,script,src}

pushd build%{nodejs_sitelib}/atom-package-manager
for ext in js json node gypi; do
    find node_modules -regextype posix-extended \
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
      -exec install -Dm644 '{}' '%{buildroot}%{nodejs_sitelib}/atom-package-manager/{}' \;
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
* Wed May 18 2016 mosquito <sensor.wen@gmail.com> - 1.10.0-2.git87b4bcb
- Fix #105 by rebuild apm
  https://github.com/FZUG/repo/issues/105
* Mon May  2 2016 mosquito <sensor.wen@gmail.com> - 1.10.0-1.git87b4bcb
- Release 1.10.0
* Fri Apr 29 2016 mosquito <sensor.wen@gmail.com> - 1.9.3-2.git38ff5b5
- Fix arguments to path.join must be strings
* Fri Apr 29 2016 mosquito <sensor.wen@gmail.com> - 1.9.3-1.git38ff5b5
- Release 1.9.3
* Sun Apr 24 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-10.gitdef66c9
- Use npm path instead of package name
  https://github.com/FZUG/repo/issues/91
* Thu Apr 21 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-9.gitdef66c9
- Use local node devel files
* Sat Apr 16 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-8.gitdef66c9
- Fix system arch of dedupe for fc24+
* Sat Apr 16 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-7.gitdef66c9
- Fix fetch local packages failed for fc25
  https://github.com/FZUG/repo/issues/88
* Fri Apr 15 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-6.gitdef66c9
- Fix only be one child in node_modules
  https://github.com/FZUG/repo/issues/88
* Tue Apr 12 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-5.gitdef66c9
- Use system node for electron 0.37.5
- Link system node for fc24+
* Wed Apr  6 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-4.gitdef66c9
- Use node 4.x to build native modules for electron 0.37.4
* Tue Apr  5 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-3.gitdef66c9
- Add Req npm
- Use system npm
* Tue Apr  5 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-2.gitdef66c9
- Add Req node-gyp
* Wed Mar 30 2016 mosquito <sensor.wen@gmail.com> - 1.9.2-1.gitdef66c9
- Release 1.9.2
- Remove BReq node-gyp, Req libgnome-keyring
- Replace BReq git-core to git
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 1.9.1-2.git24807ff
- Fixed fc24 running error: undefined symbol node_module_register
  https://github.com/atom/atom/issues/3385
- Copy system node binary
* Tue Mar 29 2016 mosquito <sensor.wen@gmail.com> - 1.9.1-1.git24807ff
- Release 1.9.1
* Mon Mar 21 2016 mosquito <sensor.wen@gmail.com> - 1.7.1-3.git955326e
- Fixed fc24 build error
- Rewrite install script
* Sat Mar 12 2016 mosquito <sensor.wen@gmail.com> - 1.7.1-2.git955326e
- Add requires python2, git-core, libgnome-keyring
* Sat Mar  5 2016 mosquito <sensor.wen@gmail.com> - 1.7.1-1.git955326e
- Release 1.7.1
* Sun Feb 14 2016 mosquito <sensor.wen@gmail.com> - 1.7.0-1.git829b81a
- Initial package
