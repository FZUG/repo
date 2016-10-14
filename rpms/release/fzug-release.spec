Name:       fzug-release
Version:    %{fedora}
Release:    0.2
Summary:    FZUG package repositories
Summary(zh_CN): FZUG 中文社区源
License:    MIT
Group:      System Environment/Base
URL:        https://github.com/FZUG/repo
BuildArch:  noarch

%description
FZUG (Fedora Zh User Group) package repository files for yum and dnf.

%prep

%build

%install
Branch=(free nonfree testing pr)
install -d -m 755 %{buildroot}/etc/yum.repos.d

for i in ${Branch[@]}; do
cat > %{buildroot}/etc/yum.repos.d/fzug-${i}.repo <<EOF
[fzug-${i}]
name=FZUG fc\$releasever - ${i^}
baseurl=https://repo.fdzh.org/FZUG/${i}/\$releasever/\$basearch/
skip_if_unavailable=True
metadata_expire=1d
gpgcheck=0
enabled=1

[fzug-${i}-source]
name=FZUG fc\$releasever - ${i^} - Source
baseurl=https://repo.fdzh.org/FZUG/${i}/\$releasever/source/SRPMS/
skip_if_unavailable=True
metadata_expire=1d
gpgcheck=0
enabled=0
EOF
done

%files
%defattr(-,root,root,-)
%dir /etc/yum.repos.d
%config(noreplace) /etc/yum.repos.d/fzug*.repo

%changelog
* Sat Oct 15 2016 mosquito <sensor.wen@gmail.com> - 25-0.2
- Add testing, pr repository
* Fri Oct 23 2015 mosquito <sensor.wen@gmail.com> - 23-0.1
- Initial build
