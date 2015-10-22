Name:       fzug-release
Version:    %{fedora}
Release:    0.1
Summary:    FZUG package repositories
Summary(zh_CN): FZUG 中文社区源

License:    MIT
Group:      System Environment/Base
URL:        https://github.com/FZUG/repo
Source0:    fzug-free.repo
Source1:    fzug-nonfree.repo
BuildArch:  noarch

%description
FZUG (Fedora Zh User Group) package repository files for yum and dnf.

%prep

%build

%install
install -d -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 %{S:0} %{buildroot}/etc/yum.repos.d
install -m 644 %{S:1} %{buildroot}/etc/yum.repos.d

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fzug-free.repo
%config(noreplace) /etc/yum.repos.d/fzug-nonfree.repo

%changelog
* Fri Oct 23 2015 mosquito <sensor.wen@gmail.com> - 23-0.1
- Initial build
