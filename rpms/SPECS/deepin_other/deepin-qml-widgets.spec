%global debug_package %{nil}
%global project deepin-qml-widgets
%global repo %{project}

# commit
%global _commit a864d6ff58d8d185bd98b5ad4408da154da275d2
%global _shortcommit %(c=%{_commit}; echo ${c:0:7})

Name:		deepin-qml-widgets
Version:	2.3.0
Release:	1.git%{_shortcommit}%{?dist}
Summary:	Deepin QML widgets
Summary(zh_CN):	深度 QML 部件库

Group:		Development/Libraries
License:	GPLv3
URL:		https://github.com/linuxdeepin/deepin-qml-widgets
Source:		https://github.com/linuxdeepin/deepin-qml-widgets/archive/%{_commit}/%{repo}-%{_shortcommit}.tar.gz

BuildRequires:	pkgconfig
BuildRequires:	gettext
BuildRequires:	desktop-file-utils
BuildRequires:	gtk2-devel
BuildRequires:	qt5-qtbase-devel
BuildRequires:	qt5-qtdeclarative-devel >= 5.3.1
BuildRequires:	qt5-qtwebkit-devel >= 5.3.1
BuildRequires:	qt5-qtx11extras-devel
#BuildRequires:	qt5-qtmultimedia-devel
#BuildRequires:	qt5-qtgraphicaleffects
#BuildRequires:	qt5-qtquickcontrols
BuildRequires:	libXcomposite-devel
BuildRequires:	libxcb-devel

%description
Deepin QML widgets

%description -l zh_CN
深度 QML 部件库, deepin 应用需要此程序库.

%prep
%setup -q -n %repo-%{_commit}

%build
%{_qt5_qmake}
make %{?_smp_mflags}

%install
make install INSTALL_ROOT=%{buildroot}

pushd locale
for i in `ls *.po`
 do
    install -d %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/
    msgfmt $i -o %{buildroot}%{_datadir}/locale/${i%.*}/LC_MESSAGES/%{name}.mo
 done
popd

%find_lang %{name}

%files -f %{name}.lang
%defattr(-,root,root,-)
%{_bindir}/deepin-dialog
%{_qt5_archdatadir}/qml/Deepin/Locale
%{_qt5_archdatadir}/qml/Deepin/StyleResources
%{_qt5_archdatadir}/qml/Deepin/Widgets
%{_datadir}/dbus-1/services/com.deepin.dialog.service

%changelog
* Wed Jul 01 2015 mosquito <sensor.wen@gmail.com> - 2.3.0-1.gita864d6f
- Update version to 2.3.0-1.gita864d6f
* Wed Dec 31 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141231-1
- Update version to 0.0.2git20141231
* Tue Dec 23 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141216-1
- Update version to 0.0.2git20141216
* Mon Dec 15 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141214-1
- Update version to 0.0.2git20141214
* Mon Dec 08 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141205-1
- Update version to 0.0.2git20141205
* Thu Dec 04 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141204-1
- Update version to 0.0.2git20141204
* Wed Dec 03 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141202-1
- Update version to 0.0.2git20141202
* Tue Dec 02 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141201-1
- Update version to 0.0.2git20141201
* Tue Nov 18 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141117-1
- Update version to 0.0.2git20141117
* Wed Nov 12 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141112-1
- Update version to 0.0.2git20141112
* Tue Nov 4 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20141104-1
- Update version to 0.0.2git20141104
* Mon Sep 29 2014 mosquito <sensor.wen@gmail.com> - 0.0.2git20140925-1
- Initial build
