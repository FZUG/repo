# http://pkgs.fedoraproject.org/cgit/rpms/java-1.8.0-openjdk.git
%global debug_package %{nil}
%global __jar_repack %{nil}

Name:    leiningen
Version: 2.6.1
Release: 1%{?dist}
Summary: Clojure projects manager with bundled clojure
Group:   Development/Tools
License: EPL-1.0
URL:     http://leiningen.org/

Source0: https://github.com/technomancy/leiningen/releases/download/%{version}/%{name}-%{version}-standalone.zip
Source1: https://raw.github.com/technomancy/leiningen/stable/bin/lein-pkg
Source2: https://raw.github.com/technomancy/leiningen/master/bash_completion.bash
Source3: https://raw.github.com/technomancy/leiningen/master/zsh_completion.zsh

BuildArch: noarch
Requires: java-1.8.0-openjdk-devel
#Requires: oracle-jdk8

%description
Leiningen is a build and project management tool written in Clojure
and used pervasively throughout the Clojure community.

See more http://clojure.org/community/resources

%description -l zh_CN
Leiningen 是使用 Clojure 编写的 Clojure 项目管理工具, 该工具
在 Clojure 社区中相当普及.

更多信息 http://clojure.org/community/resources

%package zsh-completion
Summary: zsh completion files for leiningen
BuildArch: noarch
Requires: %{name} = %{version}-%{release}
Requires: zsh

%description zsh-completion
This package installs %{summary}.

%prep

%build

%install
# install lein.jar
install -d %{buildroot}%{_javadir}
install -p -m 644 %{S:0} %{buildroot}%{_javadir}/%{name}-%{version}-standalone.jar

# install lein script
install -d %{buildroot}%{_bindir}
install -p -m 755 %{S:1} %{buildroot}%{_bindir}/lein

# install bash completion
install -d %{buildroot}%{_datadir}/bash-completion/completions
install -p -m 644 %{S:2} %{buildroot}%{_datadir}/bash-completion/completions/%{name}

# install zsh completion
install -d %{buildroot}%{_datadir}/zsh/site-functions
install -p -m 644 %{S:3} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}

%files
%defattr(-,root,root,-)
%{_bindir}/lein
%{_javadir}/%{name}-%{version}-standalone.jar
%{_datadir}/bash-completion/completions/%{name}

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{name}

%changelog
* Mon Mar 28 2016 mosquito <sensor.wen@gmail.com> - 2.6.1-1
- Initial build
