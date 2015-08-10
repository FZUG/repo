# Require 20G+ disk space, download 2.7G source files, build time 3-5 hours.
# https://wiki.unrealengine.com/Building_On_Linux
# https://github.com/EpicGames/UnrealEngine/blob/master/Engine/Build/BatchFiles/Linux/README.md
%global debug_package %{nil}
%global project UnrealEngine
%global repo %{project}

# commit
%global _commit d049f041989d62f6d6d4840d58e084a52f0558a9
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		ue4
Version:	4.8.3
Release:	1.git%{_shortcommit}%{?dist}
Summary:	UnrealEngine 4 are integrated tools for game develop
License:	Custom
URL:		https://www.unrealengine.com
Source0:	https://github.com/EpicGames/UnrealEngine/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

# Note:
# You will also need at least 20 GB of free disk space and a relatively powerful machine.
# The mono-project provides latest mono-* packages.
# dnf config-manager --add-repo http://download.mono-project.com/repo/centos
AutoReqProv: false
BuildRequires:	cmake
BuildRequires:	clang >= 3.5.0
BuildRequires:	mono-core >= 3.0.0
BuildRequires:	mono-devel >= 3.0.0
BuildRequires:	dos2unix
# third-party dependencies
BuildRequires:	gtk3-devel
BuildRequires:	qt-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	zlib-devel
BuildRequires:	jemalloc-devel
BuildRequires:	opus-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libmcpp-devel
BuildRequires:	freetype-devel
BuildRequires:	libicu-devel
BuildRequires:	nvidia-texture-tools-devel
BuildRequires:	SDL2-devel
Provides: %{name} = %{version}
Requires: qt5-qtbase-gui qt-x11
Requires: cairo-gobject SDL2

%description
UnrealEngine 4 is a suite of integrated tools for game developers
to design and build games, simulations, and visualizations.

%package devel
Summary: Source for UnrealEngine 4 to create C++ scripts
Provides: %{name}-devel = %{version}
Requires: %{name} = %{version}

%description devel
Source for UnrealEngine 4 to create C++ scripts.

%package docs
Summary: Documents for UnrealEngine 4
Provides: %{name}-docs = %{version}
Requires: %{name} = %{version}

%description docs
Documents for UnrealEngine 4.

%prep
%setup -q -n %repo-%{_commit}

%build
cp -r Engine/Source Engine/Source.bak
find Engine/Source/Programs/AutomationTool -name "*Automation.csproj" \
  -exec sed -i "s|ToolsVersion=\"11.0\"|ToolsVersion=\"4.0\"|" "{}" \;
pushd Engine/Build/BatchFiles/Linux
# Note: download complete, backup directory
# tar zcf UnrealEngine-%%{_shortcommit}.tar.gz UnrealEngine-%%{_commit}
sh Setup.sh
sh GenerateProjectFiles.sh
popd
# normal build
items="SlateViewer ShaderCompileWorker UnrealLightmass \
       UnrealPak UE4Editor UnrealFrontend CrashReportClient"
# full build
#items="UnrealHeaderTool BlankProgram SlateViewer ShaderCompileWorker \
#      UnrealLightmass UnrealPak UE4Client UE4Game UE4Server UE4Editor " # runs
#items+="UE4EditorServices UnrealFileServer UnrealVersionSelector \
#      UnrealFrontend CrashReportClient" # untested
for item in $items; do
make $item || make $item
done

%install
# You need additionally about 5GB extra space for shaders that will be compiled on the 1st run!
find Engine -name "*.a" -or -name "*.dmg" -or -name "*.msi" -or -name "Intermediate" | xargs rm -rf
find Engine -name "*.py" | xargs sed -i -e 's||\n|g' -e '/^\s*$/d'
rm -rf Engine/Extras/Maya_AnimationRiggingTools
rm -rf Engine/Source/*
mv -T Engine/Source.bak Engine/Source

install -d %{buildroot}%{_bindir}
install -d %{buildroot}/opt/%{name}
cat > %{buildroot}%{_bindir}/%{name} <<EOF
cd /opt/%{name}/Engine/Binaries/Linux
./UE4Editor -SaveToUserDir
EOF
ln -sfv /opt/%{name}/Engine/Binaries/Linux/UnrealFrontend %{buildroot}%{_bindir}
ln -sfv /opt/%{name}/Engine/Binaries/Linux/SlateViewer %{buildroot}%{_bindir}

# editor
cp -r Engine %{buildroot}/opt/%{name}/
cp -r FeaturePacks %{buildroot}/opt/%{name}/
cp -r Templates %{buildroot}/opt/%{name}/
cp -r Samples %{buildroot}/opt/%{name}/
#make install DESTDIR=%%{buildroot}

# permission
install -d -m757 %{buildroot}/opt/%{name}/Engine/Intermediate
install -d -m757 %{buildroot}/opt/%{name}/Engine/DerivedDataCache
install -d -m757 %{buildroot}/opt/%{name}/Engine/Saved
find %{buildroot}/opt/%{name}/Engine/Saved -type d | xargs chmod 757
find %{buildroot}/opt/%{name}/Engine/Saved -type f | xargs chmod 646
find %{buildroot}/opt/%{name} -name "*.dll" -or -name "*.so*" | xargs chmod 755

%post -p /sbin/ldconfig
%postun
if [ $1 -eq 0 ]; then
rm -rf /opt/%{name}
fi

%files
%defattr(-,root,root,-)
%doc README.md LICENSE.pdf
%attr(0755,root,root) %{_bindir}/%{name}
%{_bindir}/UnrealFrontend
%{_bindir}/SlateViewer
/opt/%{name}/
%exclude /opt/%{name}/Engine/Source
%exclude /opt/%{name}/Engine/Documentation

%files devel
%defattr(-,root,root,-)
/opt/%{name}/Engine/Source

%files docs
%defattr(-,root,root,-)
/opt/%{name}/Engine/Documentation

%changelog
* Fri Aug  7 2015 mosquito <sensor.wen@gmail.com> - 4.8.3-1.gitd049f04
- Initial build
