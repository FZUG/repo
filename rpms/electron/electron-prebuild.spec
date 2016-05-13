# build Atom and Electron packages: https://github.com/tensor5/arch-atom
# RPM spec: https://github.com/helber/fedora-specs
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global debug_package %{nil}
%global _hardened_build 1
%global __provides_exclude (libnode)
%global __requires_exclude (libnode|ffmpeg)
%global project electron
%global repo %{project}

# commit
%global _commit c04d43ca132bea2bbd048c2bf3d347b920089438
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    electron
Version: 0.37.7
Release: 1.prebuilt%{?dist}
Summary: Framework for build cross-platform desktop applications

Group:   Applications/Editors
License: MIT
URL:     https://github.com/electron/electron
#Source0: https://github.com/electron/electron/archive/%%{_commit}/%%{repo}-%%{_shortcommit}.tar.gz

BuildRequires: wget

%description
The Electron framework lets you write cross-platform desktop applications
using JavaScript, HTML and CSS. It is based on Node.js and Chromium.

Visit http://electron.atom.io/ to learn more.

%prep
mkdir %{name}_build
pushd %{name}_build

wget https://github.com/electron/electron/releases/download/v%{version}/%{name}-v%{version}-linux-%{arch}.zip
unzip %{name}-v%{version}-linux-%{arch}.zip

wget https://atom.io/download/atom-shell/v%{version}/node-v%{version}.tar.gz
tar xf node-v%{version}.tar.gz

%build

%install
pushd %{name}_build

# Install electron
Files="content_shell.pak electron icudtl.dat libffmpeg.so libnode.so locales \
       natives_blob.bin resources snapshot_blob.bin version"
install -d %{buildroot}%{_libdir}/%{name}
cp -a $Files %{buildroot}%{_libdir}/%{name}

install -d %{buildroot}%{_bindir}
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}

# Install node headers
install -d %{buildroot}%{_libdir}/%{name}/node
cp -r node-v%{version}/* %{buildroot}%{_libdir}/%{name}/node

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}/

%changelog
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
