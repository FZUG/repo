%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global debug_package %{nil}
%global __provides_exclude (libnode)
%global __requires_exclude (libnode|ffmpeg)

Name:    electron
Version: 3.0.10
Release: 1.prebuilt%{?dist}
Summary: Framework for build cross-platform desktop applications
License: MIT
URL:     https://github.com/electron/electron

BuildRequires: wget
Requires(post): chkconfig
Requires(postun): chkconfig
Obsoletes: %{name} < %{version}-%{release}

%description
The Electron framework lets you write cross-platform desktop applications
using JavaScript, HTML and CSS. It is based on Node.js and Chromium.

Visit https://electronjs.org/ to learn more.

%prep
mkdir %{name}_build
pushd %{name}_build

wget %{url}/releases/download/v%{version}/%{name}-v%{version}-linux-%{arch}.zip
unzip %{name}-v%{version}-linux-%{arch}.zip

wget https://atom.io/download/atom-shell/v%{version}/node-v%{version}.tar.gz
tar xf node-v%{version}.tar.gz

%install
pushd %{name}_build

# Install electron
rpak="resources_200_percent.pak"
Files="blink_image_$rpak content_$rpak ui_$rpak views_$rpak content_shell.pak \
       icudtl.dat natives_blob.bin v8_context_snapshot.bin \
       %{name} libffmpeg.so libnode.so locales resources version"
install -d %{buildroot}%{_libdir}/%{name}
cp -a $Files %{buildroot}%{_libdir}/%{name}

install -d %{buildroot}%{_bindir}
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}

# Install node headers
cp -r node-v%{version} %{buildroot}%{_libdir}/%{name}/node

%files
%{_bindir}/%{name}
%{_libdir}/%{name}/

%changelog
* Thu Dec  6 2018 mosquito <sensor.wen@gmail.com> - 3.0.10-1
- Release 3.0.10

* Sat Sep 23 2017 mosquito <sensor.wen@gmail.com> - 1.6.9-1.gitf0c38b7
- Release 1.6.9

* Wed May 24 2017 mosquito <sensor.wen@gmail.com> - 1.3.15-1.git39d33df
- Release 1.3.15

* Tue Jan  3 2017 mosquito <sensor.wen@gmail.com> - 1.3.13-1.git93c4f90
- Release 1.3.13

* Thu Dec  1 2016 mosquito <sensor.wen@gmail.com> - 1.3.9-1.gitcb9fdc4
- Release 1.3.9

* Sat Oct 15 2016 mosquito <sensor.wen@gmail.com> - 1.3.7-1.gite3688a8
- Release 1.3.7

* Wed Jul 13 2016 mosquito <sensor.wen@gmail.com> - 1.2.7-1.git13e1818
- Release 1.2.7

* Wed Jun 29 2016 mosquito <sensor.wen@gmail.com> - 1.2.3-3.git553341d
- Dont edit the global config file in postscript

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
