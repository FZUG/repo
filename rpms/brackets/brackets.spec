# https://github.com/jgillich/brackets-rpm
%global debug_package %{nil}
%global _hardened_build 1
%global __provides_exclude (npm)
%global __requires_exclude (npm|0.12)
%global project brackets
%global repo %{project}

# commit
%global _commit0 3af64fae4b8430318770375c0125fcc9eeda1e85
%global _scommit0 %(c=%{_commit0}; echo ${c:0:7})
%global _commit1 0ad2696e4e34880385c710addab1554d1476315c
%global _scommit1 %(c=%{_commit1}; echo ${c:0:7})

Name:    brackets
Version: 1.8
Release: 1%{?dist}
Summary: An open source code editor for the web

Group:   Development/Tools
License: MIT
URL:     http://brackets.io
Source0: http://rpm-ostree.cloud.fedoraproject.org/repo/pkgs/mosquito/brackets/brackets/adobe.brackets.extract.0.8.0-1749-release.zip/200eb47ad53f74e57caa13a6ae16ef5a/adobe.brackets.extract.0.8.0-1749-release.zip
Source1: GettingStarted-zhcn.html

BuildRequires: alsa-lib, GConf2
BuildRequires: gtk2-devel, git
BuildRequires: /usr/bin/npm, node-gyp
BuildRequires: desktop-file-utils
Requires: desktop-file-utils
%if 0%{?fedora}
# enable Live Preview
Recommends: google-chrome
# enable LiveDevelopment Inspector
Recommends: ruby
%endif
Obsoletes: %{name} <= 1.5.0

# libcef.so require libgcrypt.so.11, libudev.so.0
# https://github.com/adobe/brackets/issues/10255
# http://red.fedorapeople.org/SRPMS/compat-libgcrypt-1.5.3-4.fc21.src.rpm
%if 0%{?fedora} >= 21
BuildRequires: compat-libgcrypt
Requires: compat-libgcrypt
%else
BuildRequires: libgcrypt
Requires: libgcrypt
%endif

%description
 Brackets is an open-source editor for web design and development
 built on top of web technologies such as HTML, CSS and JavaScript.
 The project was created and is maintained by Adobe, and is released
 under an MIT License.

%prep
git clone https://github.com/adobe/brackets
git clone https://github.com/adobe/brackets-shell
pushd %{name} && git checkout %{_commit0} && git submodule update --init && popd
pushd %{name}-shell && git checkout %{_commit1} && popd

%build
ln -sfv %{_libdir}/libudev.so.1 %{_builddir}/libudev.so.0
export LD_LIBRARY_PATH="$LD_LIBRARY_PATH:%{_builddir}"
export CFLAGS="%{optflags} -fPIC -pie"
export CXXFLAGS="%{optflags} -fPIC -pie"

pushd %{_builddir}/%{name}
npm install && npm install grunt-cli
./node_modules/.bin/grunt clean less targethtml useminPrepare htmlmin requirejs concat copy usemin
cp -a src/config.json dist/config.json

pushd %{_builddir}/%{name}-shell
npm install && npm install grunt-cli
./node_modules/.bin/grunt setup full-build

%install
mkdir --parents %{buildroot}%{_libdir}/%{name} %{buildroot}%{_datadir}
pushd %{_builddir}/%{name}-shell
cp -a installer/linux/debian/package-root/opt/%{name}/. %{buildroot}%{_libdir}/%{name}
cp -a installer/linux/debian/package-root/usr/share/icons %{buildroot}%{_datadir}/
popd

mkdir --parents %{buildroot}%{_bindir}
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}/
ln -sfv %{_libdir}/%{name}/Brackets %{buildroot}%{_bindir}/%{name}-bin

mkdir --parents %{buildroot}%{_datadir}/applications
cat <<EOT >> %{buildroot}%{_datadir}/applications/%{name}.desktop
[Desktop Entry]
Name=Brackets
Type=Application
Categories=Development
Exec=brackets %U
Icon=brackets
MimeType=text/html;
Keywords=Text;Editor;Write;Web;Development;
EOT

desktop-file-install --mode 0644 %{buildroot}%{_datadir}/applications/%{name}.desktop
rm -rf %{buildroot}%{_libdir}/%{name}/*.desktop

ln -sfv %{_libdir}/libudev.so.1 %{buildroot}%{_libdir}/%{name}/lib/libudev.so.0

# strip symbol information
strip %{buildroot}%{_libdir}/%{name}/{Brackets{,-node},lib/libcef.so}

# extensions
mkdir --parents %{buildroot}%{_libdir}/%{name}/auto-install-extensions
install -m 0644 %{S:0} %{buildroot}%{_libdir}/%{name}/auto-install-extensions/

# Getting Started zh_cn
cp -a %{buildroot}%{_libdir}/%{name}/samples/zh-{tw,cn}
install -m 0644 %{S:1} %{buildroot}%{_libdir}/%{name}/samples/zh-cn/Get*/index.html

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
%doc %{name}/README.md
%license %{name}/LICENSE
%{_bindir}/%{name}*
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/*
%{_datadir}/icons/*
%{_datadir}/applications/%{name}.desktop
%attr(755,root,root) %{_libdir}/%{name}/%{name}
%attr(755,root,root) %{_libdir}/%{name}/Brackets
%attr(755,root,root) %{_libdir}/%{name}/Brackets-node

%changelog
* Thu Dec  1 2016 mosquito <sensor.wen@gmail.com> - 1.8-1
- Release 1.8
* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 1.7-1
- Release 1.7
* Mon Jan 25 2016 mosquito <sensor.wen@gmail.com> - 1.6-1
- Release 1.6
* Sun Nov 22 2015 mosquito <sensor.wen@gmail.com> - 1.5-1
- Initial build
