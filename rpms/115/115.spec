# https://bugzilla.redhat.com/show_bug.cgi?id=1869423
%global __filter_GLIBC_PRIVATE 1
# do not call strip
%global __os_install_post %{nil}
# do not provides/requires for 115 private lib
%global __provides_exclude_from /usr/local/115/(lib/.*|plugins/.*)$
%global __requires_exclude_from /usr/local/115/(lib/.*|plugins/.*)$
%global __requires_exclude ^(libQt5.*|libav.*|libswresample.*)$
%define rel 6

Name: 115
Version: 1.0.1
Release: %{rel}%{?dist}
Summary: 115 PC client for Linux
License: 115 License Agreement
URL: https://pc.115.com/
Source0: https://down.115.com/client/%{name}pc/lin/%{name}pc_%{version}.%{rel}.deb
BuildArch: x86_64
BuildRequires: alien

%description
115 PC client for Linux

%prep
# use our own way to extract the files
cp -p %{SOURCE0} .
rm -rf %{name}pc-%{version}
rm -rf %{name}pc-%{version}.%{rel}
alien -t -g %{name}pc_%{version}.%{rel}.deb
mv %{name}-%{version}.%{rel} %{name}-%{version}
%setup -T -D

%install
mkdir -p %{buildroot}/usr/local/
mkdir -p %{buildroot}/usr/share/applications/
sed -i 's/dpkg -r/rpm -e/' usr/local/115/update.sh
sed -i 's/dpkg -i/rpm -i/' usr/local/115/update.sh
cp -a usr/local/115 %{buildroot}/usr/local/
install -m 644 usr/share/applications/115.desktop %{buildroot}/usr/share/applications/115.desktop

%files
/usr/local/115
/usr/share/applications/115.desktop

%changelog
* Mon Mar 7 2022 Hangbin Liu <liuhangbin@gmail.com> - 1.0.1-6
- Update to 1.0.1-6

* Mon Mar 7 2022 Hangbin Liu <liuhangbin@gmail.com> - 1.0.0-16
- Initial build
