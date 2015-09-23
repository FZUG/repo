%global debug_package %{nil}
%global project brise
%global repo %{project}

# commit
%global _commit d6ad1644161fd250b1be82efc2c75802f9025dd0
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           brise
Version:        0.35
Release:        2.git%{_shortcommit}%{?dist}
Summary:        The official Rime schema repository
Summary(zh_CN): Rime 输入法规则库

License:        GPLv3
URL:            https://github.com/rime/brise
Source0:        https://github.com/rime/brise/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:  kyotocabinet
BuildRequires:  librime-tools

%description
La brise: The official Rime schema repository.

%description -l zh_CN
brise: Rime 输入法规则库.

%prep
%setup -q -n %{repo}-%{_commit}

%build
make %{?_smp_mflags}

%install
%make_install

%files
%defattr(-,root,root,-)
%doc README.md ChangeLog AUTHORS
%license LICENSE
%{_datadir}/rime-data

%changelog
* Wed Sep 23 2015 mosquito <sensor.wen@gmail.com> - 0.35-2.gitd6ad164
- Update to 0.35-2.gitd6ad164

* Wed Feb 04 2015 mosquito <sensor.wen@gmail.com> - 0.35git20150203-1
- Update version to 0.35git20150203

* Sun Jan 25 2015 mosquito <sensor.wen@gmail.com> - 0.35git20150125-1
- Update version to 0.35git20150125

* Tue Jan  6 2015 Peng Wu <pwu@redhat.com> - 0.35-1
- Update to 0.35

* Sun Dec 28 2014 mosquito <sensor.wen@gmail.com> - 0.35git20141225-1
- Update version to 0.35git20141225

* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 0.35git20141201-1
- Update version to 0.35git20141201

* Wed Nov 19 2014 mosquito <sensor.wen@gmail.com> - 0.35git20141119-1
- Update version to 0.35git20141119

* Wed Nov 5 2014 mosquito <sensor.wen@gmail.com> - 0.35git20141015-1
- Update version to 0.35git20141015

* Mon Sep 15 2014 mosquito <sensor.wen@gmail.com> - 0.35git20140905-1
- Build for rhel/centos 7
- Update to 0.35git20140905

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Dec 27 2013 Peng Wu <pwu@redhat.com> - 0.32-1
- Update to 0.32

* Mon Dec  9 2013 Peng Wu <pwu@redhat.com> - 0.30-1
- Update to 0.30

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 22 2013 Peng Wu <pwu@redhat.com> - 0.22-2
- Fixes the spec

* Thu May  9 2013 Peng Wu <pwu@redhat.com> - 0.22-1
- The Initial Version
