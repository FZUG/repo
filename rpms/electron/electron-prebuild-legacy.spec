# build Atom and Electron packages: https://github.com/tensor5/arch-atom
# RPM spec: https://github.com/helber/fedora-specs
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global debug_package %{nil}
%global _hardened_build 1
%global __provides_exclude (libnode)
%global __requires_exclude (libnode|ffmpeg)
%global project electron
%global repo %{project}
%global electrondir %{_libdir}/%{repo}/%{version}

# commit
%global _commit 553341db87fc095b25aaea180ebf90966c96611b
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    electron-legacy
Version: 0.37.8
Release: 2.prebuilt%{?dist}
Summary: Framework for build cross-platform desktop applications
Group:   Applications/Editors
License: MIT
URL:     https://github.com/electron/electron
#Source0: https://github.com/electron/electron/archive/%%{_commit}/%%{repo}-%%{_shortcommit}.tar.gz

BuildRequires: wget
Requires(post): chkconfig
Requires(postun): chkconfig
Provides:  %{repo} = %{version}-%{release}
Provides:  %{repo}%{?_isa} = %{version}-%{release}
Obsoletes: %{repo} < %{version}-%{release}

%description
The Electron framework lets you write cross-platform desktop applications
using JavaScript, HTML and CSS. It is based on Node.js and Chromium.

Visit http://electron.atom.io/ to learn more.

%prep
mkdir %{name}_build
pushd %{name}_build

wget %{url}/releases/download/v%{version}/%{repo}-v%{version}-linux-%{arch}.zip
unzip %{repo}-v%{version}-linux-%{arch}.zip

wget https://atom.io/download/atom-shell/v%{version}/node-v%{version}.tar.gz
tar xf node-v%{version}.tar.gz

%build

%install
pushd %{name}_build

# Install electron
Files="content_shell.pak electron icudtl.dat libffmpeg.so libnode.so locales \
       natives_blob.bin resources snapshot_blob.bin version"
install -d %{buildroot}%{electrondir}
cp -a $Files %{buildroot}%{electrondir}

install -d %{buildroot}%{_bindir}
ln -sfv %{electrondir}/%{repo} %{buildroot}%{_bindir}/%{repo}-%{version}

# Install node headers
install -d %{buildroot}%{electrondir}/node
cp -r node-v%{version}/* %{buildroot}%{electrondir}/node

%post
if [ $1 -ge 1 ]; then
PRIORITY=100
/sbin/alternatives --install %{_bindir}/%{repo} %{repo} %{electrondir}/%{repo} $PRIORITY
fi

%postun
if [ $1 -eq 0 ]; then
/sbin/alternatives --remove %{repo} %{electrondir}/%{repo}
fi

%files
%defattr(-,root,root,-)
%{_bindir}/%{repo}-%{version}
%{_libdir}/%{repo}/%{version}/

%changelog
* Wed Jun 29 2016 mosquito <sensor.wen@gmail.com> - 0.37.8-2.gitedb73fb
- Rename to electron-legacy
* Sun Jun 19 2016 mosquito <sensor.wen@gmail.com> - 1.2.3-2.git553341d
- Rewrite post script for rhel7
* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 1.2.3-1.git553341d
- Release 1.2.3
- Set priority 90
* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 0.37.8-1.gitedb73fb
- Revert to 0.37.8
- Use multiversion config
* Fri Jun 10 2016 mosquito <sensor.wen@gmail.com> - 1.2.2-1.gitb2bea57
- Release 1.2.2
* Fri Jun  3 2016 mosquito <sensor.wen@gmail.com> - 1.2.1-1.git97dd71d
- Release 1.2.1
* Thu May 26 2016 mosquito <sensor.wen@gmail.com> - 1.2.0-1.gitc127274
- Release 1.2.0
* Mon Apr 25 2016 mosquito <sensor.wen@gmail.com> - 0.37.7-1.gitc04d43c
- Release 0.37.7
- Add node headers
* Wed Apr 13 2016 mosquito <sensor.wen@gmail.com> - 0.37.5-1.git55b8e9a
- Release 0.37.5
* Sat Mar 12 2016 mosquito <sensor.wen@gmail.com> - 0.36.11-1.gitead94b7
- Release 0.36.11
* Sat Mar  5 2016 mosquito <sensor.wen@gmail.com> - 0.36.10-1.git3397845
- Release 0.36.10
* Sat Feb 20 2016 mosquito <sensor.wen@gmail.com> - 0.36.8-1.git4b18317
- Release 0.36.8
* Sun Feb 14 2016 mosquito <sensor.wen@gmail.com> - 0.36.7-1.git9d8e23c
- Initial package
