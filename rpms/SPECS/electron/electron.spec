# https://github.com/atom/electron/blob/master/docs/development/build-instructions-linux.md
# build Atom and Electron packages: https://github.com/tensor5/arch-atom
#
# https://github.com/atom/electron/issues/4377
# You can find the list of libraries used by Electron in:
# https://github.com/atom/brightray/blob/master/brightray.gyp#L4
# Copying what Chromium uses should be a very safe choice:
# http://copr-dist-git.fedorainfracloud.org/cgit/spot/chromium/chromium.git/tree/chromium.spec
%global arch %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "ia32")
%global debug_package %{nil}
%global _hardened_build 1
%global __requires_exclude (libnode)

# 0: don't rebuild libchromiumcontent
%global with_buildcc 1

%global chromium_url https://github.com/zcbenz/chromium-source-tarball/releases/download/%{chromium_ver}/chromium-%{chromium_ver}.tar.xz
%global chromium_ver 49.0.2623.75
%global project electron
%global repo %{project}

# commit
%global _commit c04d43ca132bea2bbd048c2bf3d347b920089438
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:    electron
Version: 0.37.7
Release: 1.git%{_shortcommit}%{?dist}
Summary: Framework for build cross-platform desktop applications

Group:   Applications/System
License: MIT
URL:     http://electron.atom.io/
#Source0: https://github.com/electron/electron/archive/%%{_commit}/%%{repo}-%%{_shortcommit}.tar.gz

Patch0:  dont-use-sysroot.patch
Patch1:  use-system-clang.patch
Patch2:  use-system-ninja.patch
Patch3:  use-system-ffmpeg.patch
Patch4:  brightray-use-system-ffmpeg.patch
Patch5:  libchromiumcontent-dont-create-zip.patch
Patch6:  libchromiumcontent-use-system-tools.patch
Patch7:  libchromiumcontent-use-system-ffmpeg.patch
Patch8:  unbundle-libvpx_new-fix.patch
Patch9:  https://raw.githubusercontent.com/gentoo/gentoo/master/www-client/chromium/files/chromium-system-ffmpeg-r2.patch

BuildRequires: clang python npm
BuildRequires: gperf bison
BuildRequires: node-gyp
BuildRequires: nodejs-packaging
BuildRequires: atk-devel
BuildRequires: cups-devel
BuildRequires: fontconfig-devel
BuildRequires: freetype-devel
#BuildRequires: ffmpeg-devel
BuildRequires: flac-devel
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: expat-devel
BuildRequires: jsoncpp-devel
BuildRequires: harfbuzz-icu
BuildRequires: gtk2-devel
BuildRequires: glib2-devel
BuildRequires: GConf2-devel
BuildRequires: libnotify-devel
BuildRequires: libgnome-keyring-devel
BuildRequires: libicu-devel
BuildRequires: libcap-devel
BuildRequires: libexif-devel
BuildRequires: libevent-devel
BuildRequires: libffi-devel
BuildRequires: libjpeg-turbo-devel
#BuildRequires: libvpx-devel
BuildRequires: libpng-devel
BuildRequires: libwebp-devel
BuildRequires: libxslt-devel
BuildRequires: libXtst-devel
BuildRequires: libxml2-devel
BuildRequires: libX11-devel
BuildRequires: libXi-devel
BuildRequires: libXrandr-devel
BuildRequires: libXScrnSaver-devel
BuildRequires: pciutils-devel
BuildRequires: dbus-devel
BuildRequires: nss-devel
BuildRequires: re2-devel
BuildRequires: snappy-devel
BuildRequires: minizip-devel
BuildRequires: ninja-build
BuildRequires: yasm-devel
BuildRequires: zlib-devel
BuildRequires: wget git

%description
The Electron framework lets you write cross-platform desktop applications
using JavaScript, HTML and CSS. It is based on Node.js and Chromium.

Visit http://electron.atom.io/ to learn more.

%prep
export srcdir="%{_builddir}"

git clone https://github.com/electron/electron
git clone https://github.com/boto/boto
git clone https://github.com/electron/brightray
git clone https://github.com/electron/chromium-breakpad breakpad
git clone https://github.com/electron/crashpad
git clone https://github.com/svn2github/gyp
git clone https://github.com/electron/libchromiumcontent
git clone https://github.com/zcbenz/native-mate native_mate
git clone https://github.com/electron/node
git clone https://github.com/kennethreitz/requests
git clone https://chromium.googlesource.com/external/google-breakpad/src google-breakpad
#git clone https://chromium.googlesource.com/chromium/tools/depot_tools

cd ${srcdir}/%{name}
git checkout %{_commit}
%patch0 -p1
%patch1 -p1
%patch2 -p1
#%patch3 -p1

sed -i '/update_submodules()/d' script/bootstrap.py
sed -i "s|'lib',|'%{_lib}',|" toolchain.gypi

# Get dependence code
for m in boto breakpad brightray crashpad native_mate node requests; do
    git submodule init vendor/${m}
    git config submodule.vendor/${m}.url ${srcdir}/${m}
done
git submodule update

#git submodule init
#git submodule update --recursive
#git submodule foreach --recursive git submodule init
#git submodule foreach --recursive git submodule update

cd ${srcdir}/%{name}/vendor/breakpad
git submodule init src
git config submodule.src.url ${srcdir}/google-breakpad
git submodule update

cd ${srcdir}/%{name}/vendor/brightray
#patch -Np1 -i %{P:4}
sed -i '/update_submodules()/d' script/bootstrap
for m in libchromiumcontent gyp; do
    git submodule init vendor/${m}
    git config submodule.vendor/${m}.url ${srcdir}/${m}
done
git submodule update

# Remove unused shared library and add extra libraries for unbundling
sed -e "/-lcups/d" \
    -e "s|'-lexpat',|'-lexpat', '<\!@(pkg-config --libs-only-l libevent flac harfbuzz-icu jsoncpp libpng libwebpdemux libxml-2.0 libxslt)', '-ljpeg', '-lre2', '-lsnappy',|" \
    -i brightray.gyp

%if 0%{?with_buildcc}
cd ${srcdir}/libchromiumcontent
_cc_commit=$(awk -F\' '/LIBCHROMIUMCONTENT_COMMIT/{print $2}' ${srcdir}/%{name}/script/lib/config.py)
git checkout ${_cc_commit:0:40}
git submodule update --init vendor/python-patch
patch -Np1 -i %{P:5}
patch -Np1 -i %{P:6}
#patch -Np1 -i %{P:7}
#rm patches/third_party/ffmpeg/ffmpeg.patch  # Use system ffmpeg

_chromium_flags=(
    'clang=1'
    'clang_use_chrome_plugins=0'
    'fastbuild=2'
    'host_clang=0'
    'release_extra_cflags="-O3 -Wno-error"'  # -Wno-error required by bundled ICU
    'remove_webcore_debug_symbols=1'
    'use_sysroot=0'
    'use_system_expat=1'
    'use_system_ffmpeg=0'
    'use_system_flac=1'
    'use_system_harfbuzz=1'
    'use_system_jsoncpp=1'
    'use_system_libevent=1'
    'use_system_libjpeg=1'
    'use_system_libpng=1'
    'use_system_libvpx=0'
    'use_system_libwebp=1'
    'use_system_libxml=1'
    'use_system_libxslt=1'
    'use_system_re2=1'
    'use_system_snappy=1'
    'use_system_yasm=1'
)

cd ${srcdir}/libchromiumcontent/vendor/chromium
cat > chromium.gyp_env <<EOF
{
  'CC': 'clang -Qunused-arguments',
  'CXX': 'clang++ -Qunused-arguments',
  'GYP_DEFINES': '${_chromium_flags[*]}'
}
EOF

echo '-> Extracting chromium source...'
wget %{chromium_url} -P "${srcdir}"
tar -xf "${srcdir}/chromium-%{chromium_ver}.tar.xz"
mv chromium-%{chromium_ver} src
cd src
if [ ! -e .version ]; then
    echo "%{chromium_ver}" > .version
fi
#patch -Np1 -i %{P:9}  # Use system ffmpeg
#patch -Np1 -i %{P:8}  # Use system libvpx
build/linux/unbundle/replace_gyp_files.py "${_chromium_flags[@]/#/-D}"
%endif

%build
export srcdir="%{_builddir}"
#export CFLAGS="%{optflags}"
#export CXXFLAGS="%{optflags}"

%if 0%{?with_buildcc}
echo '-> Building libchromiumcontent...'
cd ${srcdir}/libchromiumcontent
export -n CFLAGS CXXFLAGS
script/update --target_arch=%{arch}
script/build --target_arch=%{arch} --component=static_library
script/create-dist --target_arch=%{arch} --component=static_library

# Necessary for electron build scripts
mkdir -p dist/main/shared_library
echo '-> Stripping static libraries (saves space and linking time)...'
find dist/main/static_library -name *.a -exec strip --strip-debug '{}' \;
%endif

echo '-> Building electron...'
cd ${srcdir}/%{name}
_cc="${srcdir}/libchromiumcontent/dist/main"
LDFLAGS="%{__global_ldflags} -Wl,-z,noexecstack"
script/bootstrap.py \
    --target_arch=%{arch} \
    --libcc_source_path=${_cc}/src \
    --libcc_shared_library_path=${_cc}/shared_library \
    --libcc_static_library_path=${_cc}/static_library
script/build.py -c Release

%install
export srcdir="%{_builddir}"

# Install electron
cd ${srcdir}/%{name}/out/R
strip %{name} *.so
install -d %{buildroot}%{_libdir}/%{name}
# namcap warning: Referenced library 'libnode.so' is an uninstalled dependency
# Fixable by moving libnode.so to /usr/lib
install -m644 content_shell.pak icudtl.dat natives_blob.bin snapshot_blob.bin \
    libffmpeg.so libnode.so %{buildroot}%{_libdir}/%{name}
install -m755 %{name} %{buildroot}%{_libdir}/%{name}
install -d %{buildroot}%{_bindir}
ln -sfv %{_libdir}/%{name}/%{name} %{buildroot}%{_bindir}
cp -r locales resources %{buildroot}%{_libdir}/%{name}
echo -n "v%{version}" > %{buildroot}%{_libdir}/%{name}/version

# Install Node headers
_headers_dest="%{buildroot}%{_libdir}/%{name}/node"
install -d -m755 ${_headers_dest}

cd ${srcdir}/%{name}/vendor/node
find src deps/http_parser deps/zlib deps/uv deps/npm \
  -name "*.gypi" \
    -exec install -D -m644 '{}' "${_headers_dest}/{}" \; -or \
  -name "*.h" \
    -exec install -D -m644 '{}' "${_headers_dest}/{}" \;
install -m644 {common,config}.gypi "${_headers_dest}"

cd ${srcdir}/libchromiumcontent/dist/main/src
find v8 -name "*.h" \
    -exec install -D -m644 '{}' "${_headers_dest}/deps/{}" \;
echo '9' > "${_headers_dest}/installVersion"

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_libdir}/%{name}/

%changelog
* Mon Apr 25 2016 mosquito <sensor.wen@gmail.com> - 0.37.7-1.gitc04d43c
- Release 0.37.7
* Wed Apr 20 2016 mosquito <sensor.wen@gmail.com> - 0.37.6-1.gitaefb672
- Initial package
