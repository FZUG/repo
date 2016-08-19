%define module mt7601u
%define commit ad5474ecd9fd6efd4a7f03f4a8c71ea4bb57ca73
%define version %(c=%{commit}; echo ${c:0:10})
Name:		dkms-%{module}
Version:	%{version}
Release:	1%{?dist}
Summary:	Linux mac80211-based driver for Mediatek MT7601U USB bgn WiFi dongle

BuildArch:      noarch
License:	GPL
URL:		https://github.com/kuba-moo/mt7601u
Source0:	https://github.com/kuba-moo/mt7601u/archive/%{version}.tar.gz
Source1:        https://github.com/porjo/mt7601/raw/master/src/mcu/bin/MT7601.bin
Requires:	gcc, make, dkms
Requires:       kernel-devel >= 3.19.0

%description
This package contains the dmks kernel modules for Mediatek MT7601U USB WiFi dongle provided by https://github.com/kuba-moo/mt7601u. Be careful since this include binary firmware from vendor, which is also licensed under GPL.

%prep
%setup -n %{module}-%{commit}



%install
mkdir -p %{buildroot}/usr/src/%{module}-%{version}/
cp -rf * %{buildroot}/usr/src/%{module}-%{version}
cat << EOF >>%{buildroot}/usr/src/%{module}-%{version}/dkms.conf
PACKAGE_NAME="%{module}"
PACKAGE_VERSION="%{version}"
BUILT_MODULE_NAME[0]="%{module}"
DEST_MODULE_LOCATION[0]="/kernel/drivers/net/wireless"
AUTOINSTALL="yes"
EOF
mkdir -p %{buildroot}/lib/firmware/
cp -rf %_sourcedir/MT7601.bin %{buildroot}/lib/firmware/mt7601u.bin
%files
%defattr(-,root,root)
/usr/src/%{module}-%{version}
/lib/firmware/mt7601u.bin

%post
for POSTINST in /usr/lib/dkms/common.postinst; do
    if [ -f $POSTINST ]; then
        $POSTINST %{module} %{version}
        exit $?
    fi
    echo "WARNING: $POSTINST does not exist."
done
echo -e "ERROR: DKMS version is too old and %{module} was not"
echo -e "built with legacy DKMS support."
echo -e "You must either rebuild %{module} with legacy postinst"
echo -e "support or upgrade DKMS to a more current version."
exit 1

%preun
# Only remove the modules if they are for this %{version}-%{release}.  A
# package upgrade can replace them if only the %{release} is changed.
RELEASE="/var/lib/dkms/%{module}/%{version}/build/%{module}.release"
#if [ -f $RELEASE ] && [ `cat $RELEASE`%{?dist} = "%{version}-%{release}" ]; then
    echo -e
    echo -e "Uninstall of %{module} module (version %{version}) beginning:"
    dkms remove -m %{module} -v %{version} --all --rpm_safe_upgrade
#fi
exit 0

%changelog
* Tue May 26 2015 Zamir SUN <zsun@fedoraproject.org> - ad5474ecd9
- Switch to github source code.
* Sun Mar 15 2015 Zamir SUN <zsun@fedoraproject.org> - 3.0.0.4-1
- Initial the rpm
