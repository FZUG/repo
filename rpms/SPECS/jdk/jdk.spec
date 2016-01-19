# http://pkgs.fedoraproject.org/cgit/rpms/java-1.8.0-openjdk.git
%global __provides_exclude_from ^%{jdkhome}/.*
%global __requires_exclude_from ^%{jdkhome}/.*

%global debug_package %{nil}
%global __jar_repack %{nil}
%global _tmppath /var/tmp
%global tmproot %{_tmppath}/%{name}-%{version}_tmproot

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
%global jdkbindir %{_jvmdir}/%{jdkdir}/bin
%global jredir  %{jdkdir}/jre
%global jrebindir %{_jvmdir}/%{jredir}/bin
%global jdkvars %{_sysconfdir}/sysconfig/%{name}

# Usage: DownloadPkg appfile appurl
%global DownloadPkg() %{expand:
Download() {
    SHA=$(test -f %1 && sha256sum %1 ||:)
    if [[ ! -f %1 || "${SHA/ */}" != "%sha256" ]]; then
        wget %getopts %1 %2; Download
    fi
}
Download
}

%global priority 20000
%global family_option %(test $(rpm -E%?fedora) -ge 22 && echo "--family java-1.8.0-openjdk")
%global req_vers %(test $(rpm -E%?fedora) -ge 22 && echo ">= 1.7")
%global post_script() %{expand:
PRIORITY=%{priority}

alternatives \\
    --install %{_bindir}/java java %{jrebindir}/java $PRIORITY %{family_option} \\
    --slave %{_jvmdir}/jre jre %{_jvmdir}/%{jredir} \\
    --slave %{_bindir}/javaws javaws %{jrebindir}/javaws \\
    --slave %{_bindir}/jcontrol jcontrol %{jrebindir}/jcontrol \\
    --slave %{_bindir}/jjs jjs %{jrebindir}/jjs \\
    --slave %{_bindir}/keytool keytool %{jrebindir}/keytool \\
    --slave %{_bindir}/orbd orbd %{jrebindir}/orbd \\
    --slave %{_bindir}/pack200 pack200 %{jrebindir}/pack200 \\
    --slave %{_bindir}/policytool policytool %{jrebindir}/policytool \\
    --slave %{_bindir}/rmid rmid %{jrebindir}/rmid \\
    --slave %{_bindir}/rmiregistry rmiregistry %{jrebindir}/rmiregistry \\
    --slave %{_bindir}/servertool servertool %{jrebindir}/servertool \\
    --slave %{_bindir}/tnameserv tnameserv %{jrebindir}/tnameserv \\
    --slave %{_bindir}/unpack200 unpack200 %{jrebindir}/unpack200

alternatives \\
    --install %{_bindir}/javac javac %{jdkbindir}/javac $PRIORITY %{family_option} \\
    --slave %{_jvmdir}/java java_sdk %{_jvmdir}/%{jdkdir} \\
    --slave %{_bindir}/appletviewer appletviewer %{jdkbindir}/appletviewer \\
    --slave %{_bindir}/extcheck extcheck %{jdkbindir}/extcheck \\
    --slave %{_bindir}/idlj idlj %{jdkbindir}/idlj \\
    --slave %{_bindir}/jar jar %{jdkbindir}/jar \\
    --slave %{_bindir}/jarsigner jarsigner %{jdkbindir}/jarsigner \\
    --slave %{_bindir}/javadoc javadoc %{jdkbindir}/javadoc \\
    --slave %{_bindir}/javafxpackager javafxpackager %{jdkbindir}/javafxpackager \\
    --slave %{_bindir}/javah javah %{jdkbindir}/javah \\
    --slave %{_bindir}/javap javap %{jdkbindir}/javap \\
    --slave %{_bindir}/javapackager javapackager %{jdkbindir}/javapackager \\
    --slave %{_bindir}/java-rmi.cgi java-rmi.cgi %{jdkbindir}/java-rmi.cgi \\
    --slave %{_bindir}/jcmd jcmd %{jdkbindir}/jcmd \\
    --slave %{_bindir}/jconsole jconsole %{jdkbindir}/jconsole \\
    --slave %{_bindir}/jdb jdb %{jdkbindir}/jdb \\
    --slave %{_bindir}/jdeps jdeps %{jdkbindir}/jdeps \\
    --slave %{_bindir}/jhat jhat %{jdkbindir}/jhat \\
    --slave %{_bindir}/jinfo jinfo %{jdkbindir}/jinfo \\
    --slave %{_bindir}/jmap jmap %{jdkbindir}/jmap \\
    --slave %{_bindir}/jmc jmc %{jdkbindir}/jmc \\
    --slave %{_bindir}/jps jps %{jdkbindir}/jps \\
    --slave %{_bindir}/jrunscript jrunscript %{jdkbindir}/jrunscript \\
    --slave %{_bindir}/jsadebugd jsadebugd %{jdkbindir}/jsadebugd \\
    --slave %{_bindir}/jstack jstack %{jdkbindir}/jstack \\
    --slave %{_bindir}/jstat jstat %{jdkbindir}/jstat \\
    --slave %{_bindir}/jstatd jstatd %{jdkbindir}/jstatd \\
    --slave %{_bindir}/jvisualvm jvisualvm %{jdkbindir}/jvisualvm \\
    --slave %{_bindir}/native2ascii native2ascii %{jdkbindir}/native2ascii \\
    --slave %{_bindir}/rmic rmic %{jdkbindir}/rmic \\
    --slave %{_bindir}/schemagen schemagen %{jdkbindir}/schemagen \\
    --slave %{_bindir}/serialver serialver %{jdkbindir}/serialver \\
    --slave %{_bindir}/wsgen wsgen %{jdkbindir}/wsgen \\
    --slave %{_bindir}/wsimport wsimport %{jdkbindir}/wsimport \\
    --slave %{_bindir}/xjc xjc %{jdkbindir}/xjc
}

%global postun_script() %{expand:
alternatives --remove java %{jrebindir}/java
alternatives --remove javac %{jdkbindir}/javac
}

Name:    oracle-jdk8
Version: 1.8.0.66
Release: 3.net
Summary: Java Platform Standard Edition Development Kit
Summary(zh_CN): Oracle Java SE 开发套件
Group:   Development/Tools
License: http://java.com/license
URL:     http://www.oracle.com/technetwork/java/javase

BuildRequires: wget tar
Requires: wget tar
Requires: chkconfig %{req_vers}
Provides: jdk = %{version}-%{release}
Provides: jre = %{version}-%{release}
Provides: oracle-jdk = %{version}-%{release}
Obsoletes: oracle-jdk = 1.8.0.66-1.net

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
%DownloadPkg %{appfile} %{appurl}

# Extract archive
tar -xvf %{appfile}

%build

%install
# Main
install -d %{buildroot}%{jdkhome}
cp -r %{jdkdir}/* %{buildroot}%{jdkhome}
rm -rf %{buildroot}%{jdkhome}/{README.html,COPYRIGHT,LICENSE,THIRDPARTYLICENSE*}

# Variable file
install -d %{buildroot}%{_sysconfdir}/sysconfig
touch %{buildroot}%{jdkvars}

%pre
if [ $1 -ge 1 ]; then
# Download JDK
cd %{_tmppath}
%DownloadPkg %{appfile} %{appurl}

# Extract archive
mkdir %{tmproot} &>/dev/null ||:
tar -xf %{appfile}

# Main
install -d %{tmproot}%{jdkhome}
rm -rf %{jdkdir}/{README.html,COPYRIGHT,LICENSE,THIRDPARTYLICENSE*}
cp -r %{jdkdir}/* %{tmproot}%{jdkhome}

# Variable file
install -d %{tmproot}%{_sysconfdir}/sysconfig
cat > %{tmproot}%{jdkvars} <<EOF
# Please add follow command to ~/.bash_profile file for load variables.
#  # JDK variables
#  test -f %{jdkvars} && . %{jdkvars} ||:

# Enable JDK environment variables
Enable_JDK=1

# Java environment variables
JAVA_HOME=%{_jvmdir}/%{jdkdir}
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
    cp -rf %{tmproot}/* /; rm -rf %{tmproot} %{_tmppath}/%{jdkdir}
    %{post_script}
fi

%postun
if [ $1 -eq 0 ]; then
    %{postun_script}
fi

%files
%defattr(-,root,root,-)
%doc %{jdkdir}/README.html
%license %{jdkdir}/{COPYRIGHT,LICENSE,THIRDPARTYLICENSE*}
%config(noreplace) %{jdkvars}
%ghost %{jdkhome}

%changelog
* Tue Jan 19 2016 mosquito <sensor.wen@gmail.com> - 1.8.0.66-3
- Fix https://github.com/FZUG/repo/issues/58
* Tue Jan 19 2016 mosquito <sensor.wen@gmail.com> - 1.8.0.66-2
- Add alternatives support
* Mon Dec 21 2015 mosquito <sensor.wen@gmail.com> - 1.8.0.66-1
- Initial build
