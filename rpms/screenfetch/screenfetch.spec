%global debug_package %{nil}
%global project screenFetch
%global repo %{project}

%global _commit 36518ac06dc5cef4ab5fcf998bf5e09e3f570722
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           screenfetch
Version:        3.8.0
Release:        1.git%{_shortcommit}%{?dist}
Summary:        Fetches system/theme information in terminal
Summary(zh_CN): 终端查询系统/主题信息

License:        GPLv3
URL:            https://github.com/KittyKatt/screenFetch
Source:         %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz
BuildArch:      noarch

%description
Fetches system/theme information in terminal for Linux desktop screenshots.

%description -l zh_CN
终端查询系统/主题信息.

%prep
%setup -q -n %{repo}-%{_commit}

%build

%install
install -Dm 0755 %{name}-dev %{buildroot}%{_bindir}/%{name}
install -Dm 0644 %{name}.1   %{buildroot}%{_mandir}/man1/%{name}.1

%files
%doc CHANGELOG README.mkdn TODO
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

%changelog
* Sat Mar 11 2017 mosquito <sensor.wen@gmail.com> - 3.8.0-1.git36518ac
- Update to 3.8.0
* Sat Dec 12 2015 mosquito <sensor.wen@gmail.com> - 3.7.0-3.git22e5bee
- Update version to 3.7.0-3.git22e5bee
* Thu Sep 24 2015 mosquito <sensor.wen@gmail.com> - 3.7.0-2.gita86ce5e
- Update version to 3.7.0-2.gita86ce5e
* Fri Aug 14 2015 mosquito <sensor.wen@gmail.com> - 3.7.0-1.gitd3a0f2b
- Update version to 3.7.0-1.gitd3a0f2b
* Tue Jun 30 2015 mosquito <sensor.wen@gmail.com> - 3.6.5-1.gite73c7af
- Update version to 3.6.5-1.gite73c7af
* Wed May  6 2015 mosquito <sensor.wen@gmail.com> - 3.6.5-1.git53e1c0c
- Rename version name
* Fri Dec 12 2014 mosquito <sensor.wen@gmail.com> - 3.6.5git20141211-1
- Update version to 3.6.5git20141211
* Wed Nov 12 2014 mosquito <sensor.wen@gmail.com> - 3.6.5git20141112-1
- Update version to 3.6.5git20141112
* Fri Nov  7 2014 mosquito <sensor.wen@gmail.com> - 3.6.5git20141105-1
- Update version to 3.6.5git20141105
* Tue Nov  4 2014 mosquito <sensor.wen@gmail.com> - 3.6.5git20141031-1
- Update version to 3.6.5git20141031
* Sun Oct 19 2014 mosquito <sensor.wen@gmail.com> - 3.6.5-1
- Initial build
