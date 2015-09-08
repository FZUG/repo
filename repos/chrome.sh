#!/bin/bash
# Description: download google chrome browser.
# Author: mosquito <sensor.wen@gmail.com>
# Date: 2015.9.8
# Changelog:
#   0.1(2015.6.2) - Initial version
#   0.2(2015.9.8) - Refactoring

# Download rpm
echo "-> download rpm"
Prefix="/path/to/chrome/"
Dist="${Prefix}rpm/"

URL="https://dl.google.com/linux/chrome/rpm/stable/"
Name="google-chrome-unstable google-chrome-beta google-chrome-stable"
Platform="x86_64 i386"
MetaFile="repomd.xml primary.xml.gz filelists.xml.gz other.xml.gz"

key="linux_signing_key.pub"
keyURL="https://dl-ssl.google.com/linux/$key"

for Pkg in $Name; do
    for Arch in $Platform; do
        mkdir -p "$Dist$Arch/repodata"
        cd "$Dist$Arch/repodata"
        for item in $MetaFile; do
            curl -Os "$URL$Arch/repodata/$item"
        done
        Chrome=`gzip -cd primary.xml.gz|awk -F"\"" '/'$Pkg'/ && /'$Arch'.rpm/{print $12}'`
        ChromeURL="$URL$Arch/$Chrome"
        Output="$Dist$Arch/$Chrome"
        if [ ! -f $Output ]; then
            rm -f $Dist$Arch/${Pkg}*; axel -q -n4 "$ChromeURL" -o "$Output"
        fi
    done
done
curl -s $keyURL -o ${Prefix}$key

cat > ${Prefix}google-chrome-mirrors.repo <<EOF
[google-chrome-mirrors]
name=Google Chrome mirrors
#baseurl=http://dl.google.com/linux/chrome/rpm/stable/\$basearch
baseurl=http://repo.fdzh.org/chrome/rpm/\$basearch
enabled=1
gpgcheck=0
EOF

# Download deb
echo "-> download deb"
URL="http://dl.google.com/linux/chrome/deb/dists/stable/"
Platform="amd64 i386"
MetaFile="Release Packages Packages.gz Packages.bz2"
Dist="${Prefix}deb/"
MetaDir="${Dist}dists/stable/main/"
PoolDir="${Dist}pool/main/g/"

for Pkg in $Name; do
    for Arch in $Platform; do
        mkdir -p "$PoolDir$Pkg/" "${MetaDir}binary-$Arch/"
        cd "${MetaDir}binary-$Arch"
        for item in $MetaFile; do
            curl -Os "${URL}main/binary-$Arch/$item"
        done
        Chrome=`awk '/'$Pkg'/&&/File/{print $2}' Packages`
        ChromeURL="${URL}../../$Chrome"
        Output="$Dist$Chrome"
        if [ ! -f "$Output" ]; then
            rm -f $PoolDir$Pkg/${Pkg}*${Arch}.deb; axel -q -n4 "$ChromeURL" -o "$Output"
        fi
    done
done
curl -s "${URL}Release" -o "${MetaDir}../Release"; curl -s "${URL}Release.gpg" -o "${MetaDir}../Release.gpg"

cat > ${Prefix}google-chrome.list <<EOF
deb http://dl.google.com/linux/chrome/deb/ stable main
deb http://repo.fdzh.org/chrome/deb/ stable main
EOF

# Download dmg
echo "-> download dmg"
URL="https://dl.google.com/chrome/mac/"
Name="stable beta dev canary"
PkgName="googlechrome"
Dist="${Prefix}dmg/"

mkdir -p $Dist
for Pkg in $Name; do
    if [ "$Pkg" == "canary" ]; then
        ChromeURL="https://storage.googleapis.com/chrome-canary/GoogleChromeCanary.dmg"
    else
        ChromeURL="$URL$Pkg/${PkgName}.dmg"
    fi
    Output="${Dist}google-chrome-${Pkg}.dmg"
    rm -f $Output; axel -q -n4 "$ChromeURL" -o "$Output"
done

# Download 32bit exe
echo "-> download exe"
UUID="8a69d345-d564-463c-aff1-a69d9e530f96"
URL="http://clients2.google.com/service/update2/crx?x=id={$UUID}%26uc"
Dist="${Prefix}exe/"

mkdir -p $Dist
for Pkg in $Name; do
    if [ "$Pkg" == "canary" ]; then
        UUID="4ea16ac7-fd5a-47c3-875b-dbf4a2008c20"
        URL_canary="http://clients2.google.com/service/update2/crx?x=id={$UUID}%26uc"
        ChromeURL=`wget -qO - "$URL_canary"|awk -F\" '{print $30}'`
        Vers=`wget -qO - "$URL_canary"|awk -F\" '{print $24}'`
        Vers_canary="$Vers"
    elif [ "$Pkg" == "dev" ]; then
        URL_dev="${URL}&ap=2.0-${Pkg}"
        ChromeURL=`wget -qO - "$URL_dev"|awk -F\" '{print $28}'`
        Vers=`wget -qO - "$URL_dev"|awk -F\" '{print $24}'`
        Vers_dev="$Vers"
    elif [ "$Pkg" == "beta" ]; then
        URL_beta="${URL}&ap=1.1-${Pkg}"
        ChromeURL=`wget -qO - "$URL_beta"|awk -F\" '{print $28}'`
        Vers=`wget -qO - "$URL_beta"|awk -F\" '{print $24}'`
        Vers_beta="$Vers"
    else
        ChromeURL=`wget -qO - "$URL"|awk -F\" '{print $28}'`
        Vers=`wget -qO - "$URL"|awk -F\" '{print $24}'`
        Vers_stable="$Vers"
    fi
    Output="${Dist}chrome_${Pkg}_${Vers}.exe"
    if [ ! -f "$Output" ]; then
        rm -f ${Dist}chrome_${Pkg}*; axel -q -n4 "$ChromeURL" -o "$Output"
    fi
done

# Download 64bit exe with protocol v3
URL="http://tools.google.com/service/update2"

for Pkg in $Name; do
    UUID="4DC8B4CA-1BDA-483E-B5FA-D3C12E15B62D"

    if [ "$Pkg" == "canary" ]; then
        UUID="4EA16AC7-FD5A-47C3-875B-DBF4A2008C20"
        AP="x64-canary"
        Vers="$Vers_canary"
    elif [ "$Pkg" == "dev" ]; then
        AP="x64-dev-multi-chrome"  # 2.0-dev
        Vers="$Vers_dev"
    elif [ "$Pkg" == "beta" ]; then
        AP="x64-beta-multi-chrome"  # 1.1-beta
        Vers="$Vers_beta"
    else
        AP="x64-stable-multi-chrome"
        Vers="$Vers_stable"
    fi

    Data="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
        <request protocol=\"3.0\" ismachine=\"0\">\
        <os platform=\"win\" version=\"$Vers\" arch=\"x64\"/>\
        <app appid=\"{$UUID}\" ap=\"$AP\"><updatecheck/></app></request>"
    Chrome=`curl -s -d "$Data" "$URL"|awk -F\" '{print $24}'`
    if [ "$Pkg" == "canary" ]; then
        ChromeURL="${Chrome}${Vers}_chrome_installer_win64.exe"
    else
        ChromeURL="${Chrome}${Vers}_chrome64_installer.exe"
    fi
    Output="${Dist}chrome64_${Pkg}_${Vers}.exe"
    if [ ! -f "$Output" ]; then
        rm -f ${Dist}chrome64_${Pkg}*; axel -q -n4 "$ChromeURL" -o "$Output"
    fi
done
