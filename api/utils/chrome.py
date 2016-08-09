#!/bin/python3
# coding: utf-8
import urllib.request, urllib.error
import xml.etree.ElementTree as tree
import random
import time
import gzip
import ssl
import re

def get(url, data=None, timeout=200):
    ''' 获取数据
    return str '''
    ualist = [
        'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'
    ]
    header = {'Accept-Encoding': 'gzip'}
    header['User-Agent'] = random.choice(ualist)

    req = urllib.request.Request(url=url, data=data, headers=header)
    #req.set_proxy('127.0.0.1:8118', 'https')
    #context = ssl._create_unverified_context()
    page = urllib.request.urlopen(req, timeout=timeout).read()

    try:
        return gzip.decompress(page).decode()
    except OSError:
        return page

def post(os, branch, arch):
    ''' 返回 POST 数据
    return bytes '''
    vers = '6.3' if os == 'win' else '46.0.2490.86'
    key = os +'_'+ branch

    # Windows - {GUID}; Mac - bundle ID (com.google.appname)
    appid = {
        'win_stable': '{4DC8B4CA-1BDA-483E-B5FA-D3C12E15B62D}',
        'win_beta'  : '{4DC8B4CA-1BDA-483E-B5FA-D3C12E15B62D}',
        'win_dev'   : '{4DC8B4CA-1BDA-483E-B5FA-D3C12E15B62D}',
        'win_canary': '{4EA16AC7-FD5A-47C3-875B-DBF4A2008C20}',
        'mac_stable': 'com.google.Chrome',
        'mac_beta'  : 'com.google.Chrome',
        'mac_dev'   : 'com.google.Chrome',
        'mac_canary': 'com.google.Chrome.Canary'
    }
    ap = {
        'win_stable': {'x86':'-multi-chrome', 'x64':'x64-stable-multi-chrome'},
        'win_beta'  : {'x86':'1.1-beta',      'x64':'x64-beta-multi-chrome'},
        'win_dev'   : {'x86':'2.0-dev',       'x64':'x64-dev-multi-chrome'},
        'win_canary': {'x86':'',              'x64':'x64-canary'},
        'mac_stable': {'x86':'',              'x64':''},
        'mac_beta'  : {'x86':'betachannel',   'x64':'betachannel'},
        'mac_dev'   : {'x86':'devchannel',    'x64':'devchannel'},
        'mac_canary': {'x86':'',              'x64':''}
    }
    data = '''<?xml version='1.0' encoding='UTF-8'?>
<request protocol='3.0' version='1.3.23.0' ismachine='0'>
    <hw sse='1' sse2='1' sse3='1' ssse3='1' sse41='1' sse42='1' avx='1' physmemory='12582912' />
    <os platform='{0}' version='{1}' arch='x64'/>
    <app appid='{2}' ap='{3}'>
        <updatecheck/>
        <ping r='1'/>
    </app>
</request>'''.format(os, vers, appid[key], ap[key][arch])
    return data.encode()

def xml_decode(xmls, os=None, branch=None, arch=None):
    ''' 解析 XML
    return Dict '''
    os_type = {'win': 'exe', 'mac': 'dmg'}
    fzug_url = 'https://repo.fdzh.org/chrome/%s/' % os_type[os]

    root = tree.fromstring(xmls)
    manifest_node = root.find('.//manifest')
    manifest_version = manifest_node.get('version')

    pkg_node = root.find('.//package')
    pkg_name = pkg_node.get('name')
    pkg_size = pkg_node.get('size')
    pkg_hash = pkg_node.get('hash_sha256')

    url_nodes = root.findall('.//url')
    urls = []
    for node in url_nodes:
        urls.append(node.get('codebase') + pkg_name)
    if arch == 'x64' and os == 'win':
        pkg_name = pkg_name.replace('.exe', '_win64.exe')
    urls.append(fzug_url + pkg_name)

    return {
        'timestamp': str(time.time()).split('.')[0],
        'os': os,
        'arch': arch,
        'channel': branch,
        'name': pkg_name,
        'version': manifest_version,
        'size': pkg_size,
        'sha256': pkg_hash,
        'urls': urls
    }

def get_rpm_info(branch):
    arch = 'x86_64'
    url = 'https://dl.google.com/linux/chrome/rpm/stable/'
    fzug_url = 'https://repo.fdzh.org/chrome/rpm/'
    pkgname = {
        'stable': 'google-chrome-stable',
        'beta': 'google-chrome-beta',
        'dev': 'google-chrome-unstable'
    }
    metafile = ['repomd.xml', 'primary.xml.gz', 'filelists.xml.gz', 'other.xml.gz']

    meta_xml = get(url + arch +'/repodata/'+ metafile[1])
    metas = re.findall('<name.*?<format>', meta_xml, re.S)
    pattern = '.*ver="(.+?)".*>(.{40})<.*file="(.+?)".*package="(.+?)".*href="(.+)"'
    for meta in metas:
        pkg_info = re.match('.*'+ pkgname[branch] + pattern, meta, re.S)
        if pkg_info:
            break
    pkg_uri = arch +'/'+ pkg_info.group(5)

    return {
        'timestamp': pkg_info.group(3),
        'os': 'linux',
        'arch': arch,
        'channel': branch,
        'name': pkg_info.group(5),
        'version': pkg_info.group(1),
        'size': pkg_info.group(4),
        'sha256': pkg_info.group(2),
        'urls': [url + pkg_uri, fzug_url + pkg_uri]
    }

def get_pkg_info(platform, branch, arch):
    api_url = 'https://tools.google.com/service/update2'
    result = []
    for i in platform:
        for j in branch:
            if i == 'linux' and j == 'canary':
                continue
            for k in arch:
                if i in ['mac', 'linux'] and k == 'x64':
                    continue
                if i == 'linux':
                    # Get rpm metadata
                    data = get_rpm_info(j)
                else:
                    # Get exe and dmg metadata
                    resp = get(api_url, post(i, j, k))
                    data = xml_decode(resp, i, j, k)
                result.append(data)
    return result
