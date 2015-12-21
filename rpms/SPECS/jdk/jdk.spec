%global __provides_exclude_from ^%{jdkhome}/.*
%global __requires_exclude_from ^%{jdkhome}/.*

%global debug_package %{nil}
%global __jar_repack %{nil}
%global tmproot /tmp/%{name}-%{version}

%global arch    %(test $(rpm -E%?_arch) = x86_64 && echo "x64" || echo "i586")
%global appfile jdk-8u66-linux-%{arch}.tar.gz
# http://www.oracle.com/technetwork/java/javase/downloads
%global appurl  http://download.oracle.com/otn-pub/java/jdk/8u66-b17/%{appfile}
# https://www.oracle.com/webfolder/s/digest/8u66checksum.html
%global sha256  %(test %arch = x64 &&
   echo "7e95ad5fa1c75bc65d54aaac9e9986063d0a442f39a53f77909b044cef63dc0a" ||
   echo "21026a8d789f479d3905a4ead0c97fd5190aa9b4d1bfc66413e9136513ca84a2")

%global getopts --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" -O
%global jdkdir  jdk1.8.0_66
%global jdkhome %{_jvmdir}/%{jdkdir}
%global jdkvars %{_sysconfdir}/sysconfig/%{name}

Name:    oracle-jdk
Version: 1.8.0.66
Release: 1.net
Summary: Java Platform Standard Edition Development Kit
Summary(zh_CN): Oracle Java SE 开发套件
Group:   Development/Tools
License: http://java.com/license
URL:     http://www.oracle.com/technetwork/java/javase

BuildRequires: wget tar
Requires: wget tar
Provides: jdk = %{version}-%{release}
Provides: jre = %{version}-%{release}

%description
The Java Platform Standard Edition Development Kit (JDK) includes both
the runtime environment (Java virtual machine, the Java platform classes
and supporting files) and development tools (compilers, debuggers,
tool libraries and other tools).

The JDK is a development environment for building applications, applets
and components that can be deployed with the Java Platform Standard
Edition Runtime Environment.

%description -l zh_CN
Java SE 开发套件 (JDK) 包含运行环境 (Java虚拟机, Java类库, 帮助文件)
和开发工具 (编译器, 调试器, 库和其他工具).

JDK 是一个用于开发可部署到 JRE (Java Platform Standard Edition Runtime
Environment) 的应用程序, applets, 组件的开发环境.

%prep
# Download JDK
Download() {
    SHA=$(test -f %{appfile} && sha256sum %{appfile} ||:)
    if [[ ! -f %{appfile} || "${SHA/ */}" != "%sha256" ]]; then
        wget %getopts %appfile %appurl; Download
    fi
}
Download

# Extract archive
tar -xvf %{appfile}

%build

%install
# Main
install -d %{buildroot}%{jdkhome}
cp -r %{jdkdir}/* %{buildroot}%{jdkhome}

# Link files
ln -sfv %{jdkhome} %{buildroot}%{_jvmdir}/latest
ln -sfv %{_jvmdir}/latest %{buildroot}%{_jvmdir}/default

# Variable file
install -d %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{jdkvars}

%pre
if [ $1 -ge 1 ]; then
# Download JDK
cd /tmp
Download() {
    SHA=$(test -f %{appfile} && sha256sum %{appfile} ||:)
    if [[ ! -f %{appfile} || "${SHA/ */}" != "%sha256" ]]; then
        wget %getopts %appfile %appurl; Download
    fi
}
Download

# Extract archive
mkdir %{tmproot} &>/dev/null ||:
tar -xf %{appfile}

# Main
install -d %{tmproot}%{jdkhome}
cp -r %{jdkdir}/* %{tmproot}%{jdkhome}

# Variable file
install -d %{tmproot}%{_sysconfdir}/sysconfig
cat > %{tmproot}%{jdkvars} <<EOF
# Enable JDK environment variables
Enable_JDK=1

# Java environment variables
JAVA_HOME=%{_jvmdir}/default
JRE_HOME=\$JAVA_HOME/jre
CLASSPATH=.:\$JAVA_HOME/lib/tools.jar:\$JAVA_HOME/lib/dt.jar

# Virtual device save to sdk/.android
ANDROID_SDK_HOME=~/android/sdk
AndroidStudio=~/android/android-studio
Eclipse=~/android/eclipse

# PATH variable
if [ ! \$PATH_BAK ]; then
    declare -r PATH_BAK=\$PATH
fi
PATH=\$JAVA_HOME/bin:\$JRE_HOME/bin:\$ANDROID_SDK_HOME/tools:\$ANDROID_SDK_HOME/platform-tools:\$AndroidStudio/bin:\$Eclipse:\$PATH_BAK

# Environment variables
if [ \$Enable_JDK -eq 1 ]; then
    export JAVA_HOME JRE_HOME CLASSPATH
    export ANDROID_SDK_HOME AndroidStudio Eclipse
    export PATH PATH_BAK
else
    unset JAVA_HOME JRE_HOME CLASSPATH
    unset ANDROID_SDK_HOME AndroidStudio Eclipse
    export PATH=\$PATH_BAK
fi
EOF
fi

%post
if [ $1 -ge 1 ]; then
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} /tmp/%{jdkdir}
    # Link files
    ln -sf %{jdkhome} %{_jvmdir}/latest
    ln -sf %{_jvmdir}/latest %{_jvmdir}/default
    # load variables
    for i in $(ls /home/*/.bashrc); do
        grep -q "JDK" $i || \
        echo -e "\n# JDK variables\ntest -f %{jdkvars} && . %{jdkvars} ||:" >> $i
    done
fi

%files
%defattr(-,root,root,-)
%doc %{jdkdir}/README.html
%license %{jdkdir}/LICENSE
%config(noreplace) %{jdkvars}
%ghost %{_jvmdir}/latest
%ghost %{_jvmdir}/default
%ghost %{jdkhome}

%changelog
* Mon Dec 21 2015 mosquito <sensor.wen@gmail.com> - 1.8.0.66-1
- Initial build
