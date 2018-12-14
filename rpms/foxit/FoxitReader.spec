%global debug_package %{nil}
%define  _foxitrevision r057d814

Name:     FoxitReader
Version:  2.4.4.0911
Release:  1%{?dist}
Summary:  Foxit Reader is a free PDF document viewer
Summary(zh_CN): 福昕 PDF 阅读器

Group:    Applications/Text
License:  EULA
URL:      http://www.foxitsoftware.com
Source0:  http://cdn09.foxitsoftware.com/pub/foxit/reader/desktop/linux/2.x/2.4/en_us/FoxitReader.enu.setup.%{version}.x64.run.tar.gz
Source1:  https://www.foxitsoftware.com/products/pdf-reader/eula.html
Source2:  FoxitReader-excluded_files

Patch1:   FoxitReader.patch

BuildRequires: p7zip, chrpath, p7zip-plugins
Requires: gstreamer,gstreamer-tools
Requires: /usr/bin/gtk-update-icon-cache
Requires: desktop-file-utils
Provides: foxitreader = %{version}-%{release}

%description
Foxit Reader is a free PDF document viewer for the Linux platform, with
a new streamlined interface, user-customized toolbar, incredibly small
size, breezing-fast launch speed and rich features. This empowers PDF
document users with Zoom function, Navigation function, Bookmarks,
Thumbnails, Text Selection Tool, Snapshot, and Full Screen capabilities.
Foxit Reader for Desktop Linux is provided by Foxit Corporation free for
non-commercial use.

%prep
mkdir -p %{name}.%{version}
tar -xzf FoxitReader.enu.setup.%{version}.x64.run.tar.gz -C %{name}.%{version}/.
cp %{SOURCE1} %{name}.%{version}/.
cp %{SOURCE2} %{name}.%{version}/.
cp %{PATCH1} %{name}.%{version}/.

%build

build(){
local _file
local _line
local _position
export srcdir=$(pwd)
# Clean installer dir
if [ -d "%{name}-installer" ]
then
rm -rf "%{name}-installer"
fi
mkdir "%{name}-installer"
# Decompress .run installer
_file="FoxitReader.enu.setup.%{version}(%{_foxitrevision}).x64.run"
LANG=C grep --only-matching --byte-offset --binary \
          --text $'7z\xBC\xAF\x27\x1C' "${_file}" | cut -f1 -d: | 
     while read _position
     do
       dd if="${_file}" \
          bs=1M iflag=skip_bytes status=none skip=${_position} \
          of="%{name}-installer/bin-${_position}.7z"
     done
# Clean build dir
if [ -d "%{name}-build" ]
then
rm -rf "%{name}-build"
fi
# Decompress 7z files (some files are damaged during the extraction)
cd "%{name}-installer"
install -m 755 -d "${srcdir}/%{name}-build"
for _file in *.7z
do
echo ${_file}
7z -bd -bb0 -y x -o"${srcdir}/%{name}-build" ${_file} 1>/dev/null 2>&1 || true
done
# Apply final patches
cd "${srcdir}/%{name}-build"
patch -p1 --no-backup-if-mismatch -i %{PATCH1}
# Remove insecure RPATH
for _file in "lib/libFcitxQt5DBusAddons.so.1.0" \
           "lib/libQt5PrintSupport.so.5.3.2" \
           "platforminputcontexts/libfcitxplatforminputcontextplugin.so" \
           "printsupport/libcupsprintersupport.so"
do
echo "  -> Removing insecure RPATH from ${_file}"
chrpath --delete "${_file}"
done
# Remove unneeded files
rm "Activation" "Activation.desktop" "Activation.sh" \
 "countinstalltion" "countinstalltion.sh" \
 "installUpdate" "ldlibrarypath.sh" \
 "maintenancetool.sh" "Uninstall.desktop" \
 "Update.desktop" "updater" "updater.sh"
find -type d -name ".svn" -exec rm -rf {} +
find -type f -name ".directory" -exec rm -rf {} +
find -type f -name "*~" -exec rm {} +
# Remove excluded files
while IFS='' read -r _line
do
if [ "${_line::2}" = "# " ]
then
  echo "  -> Removing excluded files from ${_line:2}..."
elif [ -n "${_line}" -a "${_line::1}" != "#" ]
then
  rm "${srcdir}/%{name}-build/${_line}"
fi
done < "${srcdir}/%{name}-excluded_files"
}

pushd %{name}.%{version}
build
popd

%install
rm -rf %{buildroot}
pushd %{name}.%{version}
install -m 755 -d "%{buildroot}%{_libdir}/%{name}"
cd "%{name}-build"
cp -r * "%{buildroot}%{_libdir}/%{name}"
# Install icon and desktop files
install -m 755 -d "%{buildroot}%{_datadir}/pixmaps"
install -m 644 "images/FoxitReader.png" \
"%{buildroot}%{_datadir}/pixmaps/%{name}.png"
install -m 755 -d "%{buildroot}%{_datadir}/applications"
install -m 755 "FoxitReader.desktop" \
"%{buildroot}%{_datadir}/applications/%{name}.desktop"
rm FoxitReader.desktop
# Install license file
install -m 755 -d "%{buildroot}%{_datadir}/licenses/%{name}"
install -m 644 -t "%{buildroot}%{_datadir}/licenses/%{name}" %{SOURCE1}
# Install launcher script
cd "%{buildroot}"
install -m 755 -d "%{buildroot}%{_bindir}"
ln -s "%{_libdir}/%{name}/%{name}.sh" "%{buildroot}%{_bindir}/%{name}"
popd
%post

%postun

%posttrans

%files
%license %{_datadir}/licenses/%{name}/eula.html
%{_bindir}/%{name}
%{_libdir}/%{name}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.png

%changelog
* Fri Dec 14 2018 Bangjie Deng <dengbangjie@foxmail.com> - 2.4.4.0911
- Bump version to 2.4.4.0911. The spec was converted from archlinuxcn repo.
* Mon Dec 14 2015 mosquito <sensor.wen@gmail.com> - 1.1.0-1
- Initial build
