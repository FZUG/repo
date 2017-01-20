%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%global project deepin-storm
%global repo %{project}

%global _commit e6fe6aab1cadca5ed2ed6f086fb2db9699e00416
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:           python2-%{repo}
Version:        0.3
Release:        1.git%{_shortcommit}%{?dist}
Summary:        A download library and powerful download manager

License:        GPL
URL:            https://github.com/martyr-deepin/deepin-storm
Source0:        %{url}/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildArch:      noarch
BuildRequires:  python2-devel
Provides:       python-%{repo} = %{version}-%{release}

%description
A download library and powerful download manager

%prep
%setup -q -n %{repo}-%{_commit}

%build
%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --root="%{buildroot}"

%files
%{python2_sitelib}/*

%changelog
* Tue Jan 17 2017 mosquito <sensor.wen@gmail.com> - 0.3-1.gite6fe6aa
- Update to 0.3
* Tue Jan 03 2017 Jaroslav <cz.guardian@gmail.com> Stepanek 0.4.gite6fe6aa-1
- Major rewrite of SPEC file
* Wed Oct 12 2016 Jaroslav <cz.guardian@gmail.com> Stepanek 0.3.20140625
- Initial package build
