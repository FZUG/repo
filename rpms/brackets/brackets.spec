%global debug_package %{nil}
%global __provides_exclude (npm)
%global __requires_exclude (npm)

%define subm() %{lua:
printf, sub = function(...) print(string.format(...)) end, string.sub
for argv in string.gmatch(rpm.expand('%*'), '%w+%.%a+') do
  key, typ = string.match(argv, '(%w+)%.(%a+)')
  me = loadstring('return '..rpm.expand('%{meta_data}'))()
  proj, comm, outdir = string.match(me[key][1], '/(%w.*)'), me[key][2], me[key][3]
  tgzurl = 'https://github.com/%s/archive/%s/%s-%s.tar.gz'
  if typ == 'tgz' then printf(tgzurl, me[key][1], sub(comm,1,7), proj, sub(comm,1,7)) end
  if typ == 'src' then print(proj ..'-'.. comm) end
  if typ == 'out' then print(outdir) end
  if typ == 'com' then print(comm) end
  if typ == 'md'  then printf('mv -T ../%s-%s %s\\n', proj, comm, outdir) end
end}

%define meta_data %(echo "{
  %{name} = {'adobe/%{name}', '49d29a8bc3ac373c881152c4088bf3b3212b8393', '%{name} '},
  %{name}shell = {'adobe/%{name}-shell', 'b858d450cf34cf3cbae7bcfd6da1525d958c8426', '%{name}-shell '},
  jslint = {'peterflynn/JSLint', '5a09b359873fe98ddd4ec88b7beed3a4171fd8e0', 'src/extensions/default/JSLint/thirdparty/jslint '},
  i18n   = {'requirejs/i18n',    'ca7d048cbd365acdb1e25f64d86378976d8a029b', 'src/thirdparty/i18n '},
  text   = {'requirejs/text',    '35c3ead097a9ede09469172666cc96349d2ce3e4', 'src/thirdparty/text '},
  must   = {'janl/mustache.js',  '0be4e2b9446ccac052a8e74e57fe6d7444dcc231', 'src/thirdparty/mustache '},
  path   = {'jblas/path-utils',  'cc7f66e8e213e798f7504d64eaa3d1ae6860c636', 'src/thirdparty/path-utils '},
  reqjs  = {'jrburke/requirejs', 'a5f5750896bd06a21c2a96e4678cf47e03d80a1a', 'src/thirdparty/requirejs '}
}")

Name:    brackets
Version: 1.13
Release: 1%{?dist}
Summary: An open source code editor for the web
License: MIT
URL:     https://brackets.io
Source0: %subm %{name}shell.tgz
Source1: %subm %{name}.tgz
Source2: %subm jslint.tgz
Source3: %subm i18n.tgz
Source4: %subm text.tgz
Source5: %subm must.tgz
Source6: %subm path.tgz
Source7: %subm reqjs.tgz
Patch0:  %{name}-fix-config.patch

BuildRequires: git
BuildRequires: gcc-c++
BuildRequires: python2
BuildRequires: npm(npm)
BuildRequires: npm(node-gyp)
BuildRequires: npm(grunt-cli)
BuildRequires: pkgconfig(gtk+-2.0)
BuildRequires: desktop-file-utils
# ld link for libcef.so
BuildRequires: alsa-lib
BuildRequires: GConf2
BuildRequires: libXtst
BuildRequires: libXScrnSaver
BuildRequires: nspr
BuildRequires: nss

Requires:      npm(arrify)
Requires:      npm(async)
Requires:      npm(async-each)
Requires:      npm(chainsaw)
Requires:      npm(fs-extra)
Requires:      npm(micromatch)
Requires:      npm(glob-parent)
Requires:      npm(lodash)
Requires:      npm(opn)
Requires:      npm(readdirp)
Requires:      npm(request)
Requires:      npm(semver)
Requires:      npm(temp)
Requires:      npm(touch)
Requires:      npm(ws)
# enable Live Preview
Recommends:    google-chrome
# enable LiveDevelopment Inspector
Recommends:    ruby

%description
 Brackets is an open-source editor for web design and development
 built on top of web technologies such as HTML, CSS and JavaScript.
 The project was created and is maintained by Adobe, and is released
 under an MIT License.

%prep
%setup -q -a1 -a2 -a3 -a4 -a5 -a6 -a7 -n %{subm %{name}shell.src}
mv %{subm %{name}.src} %{name}; pushd %{name}
install -d %subm jslint.out i18n.out text.out must.out path.out reqjs.out
%subm jslint.md i18n.md text.md must.md path.md reqjs.md
%patch0 -p1 -b .fix-config

sed -E '/(eslint:src|jasmine|npm-install).,$/d' -i Gruntfile.js
sed 's|python|python2|' -i ../gyp/gyp
sed 's|<commit>|%{subm %{name}.com}|
     s|<branch>|release-%{version}|' -i tasks/write-config.js

%build
npm install
grunt cef icu node create-project
make

pushd %{name}
npm install
grunt build

%install
install -d %{buildroot}%{_bindir}
install -Dm755 installer/linux/debian/%{name} %{buildroot}%{_libdir}/%{name}/%{name}
ln -sv ../%{_lib}/%{name}/%{name} %{buildroot}%{_bindir}/%{name}
ln -sv ../libudev.so.1 %{buildroot}%{_libdir}/%{name}/libudev.so.0

install -Dm644 installer/linux/debian/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
cp -r installer/linux/debian/package-root/usr/share/icons %{buildroot}%{_datadir}/
for px in 32 48 128 256; do
  install -Dm644 out/Release/files/appshell${px}.png \
    %{buildroot}%{_datadir}/icons/hicolor/${px}x${px}/apps/%{name}.png
done

pushd out/Release
cp -r {files,locales,node-core} %{buildroot}%{_libdir}/%{name}/
find -maxdepth 1 -type f -exec cp {} %{buildroot}%{_libdir}/%{name}/{} \;
chmod 4755 %{buildroot}%{_libdir}/%{name}/chrome-sandbox
popd

pushd %{name}
cp -r samples %{buildroot}%{_libdir}/%{name}/samples
cp -r dist    %{buildroot}%{_libdir}/%{name}/www

install -d %{buildroot}%{_libdir}/%{name}/www/node_modules
cp -r node_modules/{anymatch,buffers,is-binary-path,binary{,-ext*},chokidar,decompress-zip,mkpath} \
  %{buildroot}%{_libdir}/%{name}/www/node_modules/
ln -sv ../../lib/node_modules %{buildroot}%{_libdir}/%{name}/node_modules

%files
%doc README.md
%license LICENSE
%{_bindir}/%{name}
%{_libdir}/%{name}/
%{_datadir}/icons/hicolor/*/apps/%{name}*
%{_datadir}/applications/%{name}.desktop

%changelog
* Fri Dec 21 2018 mosquito <sensor.wen@gmail.com> - 1.13-1
- Release 1.13

* Sun Dec 25 2016 mosquito <sensor.wen@gmail.com> - 1.8-2
- Back to linux-1547 branch
- Set config.json for check version

* Thu Dec  1 2016 mosquito <sensor.wen@gmail.com> - 1.8-1
- Release 1.8

* Fri Jun 17 2016 mosquito <sensor.wen@gmail.com> - 1.7-1
- Release 1.7

* Mon Jan 25 2016 mosquito <sensor.wen@gmail.com> - 1.6-1
- Release 1.6

* Sun Nov 22 2015 mosquito <sensor.wen@gmail.com> - 1.5-1
- Initial build
