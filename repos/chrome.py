#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
@author: mosquito
@email: sensor.wen@gmail.com
@description: download google chrome browser.
@github: https://github.com/FZUG/repo
@version: 0.4 (2016.1.30)
@history:
    0.4(2016.1.30) - Use python3
    0.3(2015.11.21) - Add DMG version
    0.2(2015.9.8) - Refactoring
    0.1(2015.6.2) - Initial version
'''

import urllib.request, urllib.parse, urllib.error
import os, sys, re, random
import gzip, ssl, json
import argparse
import xml.etree.ElementTree as tree

def get(url, data=None, timeout=200):
    ''' 获取数据
    return str '''
    ualist = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
              'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36',
              'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36']

    header = { 'Accept-Encoding': 'gzip' }
    header['User-Agent'] = ualist[random.randint(0, len(ualist)-1)]

    req  = urllib.request.Request(url=url, data=data, headers=header)
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
             'win_stable':'{4DC8B4CA-1BDA-483E-B5FA-D3C12E15B62D}',
             'win_beta'  :'{4DC8B4CA-1BDA-483E-B5FA-D3C12E15B62D}',
             'win_dev'   :'{4DC8B4CA-1BDA-483E-B5FA-D3C12E15B62D}',
             'win_canary':'{4EA16AC7-FD5A-47C3-875B-DBF4A2008C20}',
             'mac_stable':'com.google.Chrome',
             'mac_beta'  :'com.google.Chrome',
             'mac_dev'   :'com.google.Chrome',
             'mac_canary':'com.google.Chrome.Canary'
            }
    ap = {
          'win_stable':{'x86':'-multi-chrome', 'x64':'x64-stable-multi-chrome'},
          'win_beta'  :{'x86':'1.1-beta',      'x64':'x64-beta-multi-chrome'},
          'win_dev'   :{'x86':'2.0-dev',       'x64':'x64-dev-multi-chrome'},
          'win_canary':{'x86':'',              'x64':'x64-canary'},
          'mac_stable':{'x86':'',              'x64':''},
          'mac_beta'  :{'x86':'betachannel',   'x64':'betachannel'},
          'mac_dev'   :{'x86':'devchannel',    'x64':'devchannel'},
          'mac_canary':{'x86':'',              'x64':''}
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
    return Json '''
    archs = '_'+ arch if os == 'win' else ''

    root = tree.fromstring(xmls)
    manifest_node = root.find('.//manifest')
    manifest_version = manifest_node.get('version')

    pkg_node = root.find('.//package')
    pkg_name = pkg_node.get('name')
    pkg_size = float(pkg_node.get('size'))
    pkg_hash = pkg_node.get('hash_sha256')

    url_nodes = root.findall('.//url')
    urls = []
    for node in url_nodes:
        urls.append(node.get('codebase') + pkg_name)

    return json.dumps({
                        'success': True,
                        'os': os + archs,
                        'branch': branch,
                        'name': pkg_name,
                        'version': manifest_version,
                        'url': urls,
                        'sha256': pkg_hash,
                        'size': '{:0.2f}MB'.format(pkg_size/1024/1024)
                       })

def output(file, obj=None, mode='wb'):
    ''' 输出至文件
    '''
    with open(file, mode) as f:
        if 'r' in mode:
            return f.read()
        else:
            f.write(obj)

def get_rpm():
    repofile = [os.path.join(rootdir, 'google-chrome-mirrors.repo'),
'''[google-chrome-mirrors]
name=Google Chrome mirrors
#baseurl=https://dl.google.com/linux/chrome/rpm/stable/$basearch
#gpgkey=https://dl.google.com/linux/linux_signing_key.pub
baseurl=https://repo.fdzh.org/chrome/rpm/$basearch
gpgkey=https://repo.fdzh.org/chrome/linux_signing_key.pub
gpgcheck=1
enabled=1
skip_if_unavailable=1''']
    output(repofile[0], repofile[1], 'w')
    keyfile = os.path.join(rootdir, 'linux_signing_key.pub')
    urllib.request.urlretrieve('http://dl.google.com/linux/linux_signing_key.pub', filename=keyfile)

    url = 'https://dl.google.com/linux/chrome/rpm/stable/'
    pkgname = ['google-chrome-unstable', 'google-chrome-beta', 'google-chrome-stable']
    archs = ['x86_64']
    metafile = ['repomd.xml', 'primary.xml.gz', 'filelists.xml.gz', 'other.xml.gz']

    for arch in archs:
        for pkg in pkgname:
            try:
                os.makedirs(os.path.join(rootdir, 'rpm', arch, 'repodata'))
            except FileExistsError:
                pass
            for meta in metafile:
                mpath = os.path.join(rootdir, 'rpm', arch, 'repodata', meta)
                urllib.request.urlretrieve(url + arch + '/repodata/' + meta, filename=mpath)
            info_file = os.path.join(rootdir, 'rpm', arch, 'repodata', metafile[1])
            meta_info = gzip.decompress(output(info_file, mode='rb'))
            pkg_full = re.findall(pkg +'.*'+ arch +'.rpm', meta_info.decode())
            try:
                pkg_url = url + arch +'/'+ pkg_full[0]
            except IndexError:
                continue
            pkg_out = os.path.join(rootdir, 'rpm', arch, pkg_full[0])
            if os.path.exists(pkg_out):
                continue
            print('Downloading', pkg_full[0])
            urllib.request.urlretrieve(pkg_url, filename=pkg_out)

def get_deb():
    listfile = [os.path.join(rootdir, 'google-chrome.list'),
'''deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main
deb [arch=amd64] https://repo.fdzh.org/chrome/deb/ stable main''']
    output(listfile[0], listfile[1], 'w')

    url = 'http://dl.google.com/linux/chrome/deb/dists/stable/'
    pkgname = ['google-chrome-unstable', 'google-chrome-beta', 'google-chrome-stable']
    archs = ['amd64']
    metafile = ['Release', 'Packages', 'Packages.gz', 'Packages.bz2']
    dist = os.path.join(rootdir, 'deb')
    metadir = os.path.join(dist, 'dists/stable/main/')
    pooldir = os.path.join(dist, 'pool/main/g/')

    for arch in archs:
        for pkg in pkgname:
            try:
                os.makedirs(os.path.join(metadir, 'binary-'+ arch))
                os.makedirs(os.path.join(pooldir, pkg))
            except FileExistsError:
                pass
            for meta in metafile:
                mpath = os.path.join(metadir, 'binary-'+ arch +'/'+ meta)
                urllib.request.urlretrieve(url +'main/binary-'+ arch +'/'+ meta, filename=mpath)
            info_file = os.path.join(metadir, 'binary-'+ arch, metafile[1])
            meta_info = output(info_file, mode='r')
            pkg_full = re.findall(pkg +'_.*_'+ arch +'.deb', meta_info)
            try:
                pkg_url = url +'../../pool/main/g/'+ pkg +'/'+ pkg_full[0]
            except IndexError:
                continue
            pkg_out = os.path.join(pooldir + pkg +'/'+ pkg_full[0])
            if os.path.exists(pkg_out):
                continue
            print('Downloading', pkg_full[0])
            urllib.request.urlretrieve(pkg_url, filename=pkg_out)

    urllib.request.urlretrieve(url + metafile[0], filename=metadir +'../Release')
    urllib.request.urlretrieve(url + metafile[0] +'.gpg', filename=metadir +'../Release.gpg')

def get_pkg():
    platform = ['win', 'mac']
    branchs = ['stable', 'beta', 'dev', 'canary']
    arch = ['x86', 'x64']

    for i in platform:
        for j in branchs:
            for k in arch:
                if i == 'mac' and k == 'x64':
                    continue
                # Get exe and dmg metadata
                resp = get('https://tools.google.com/service/update2', post(i, j, k))
                json_data = xml_decode(resp, i, j, k)
                output(jsonfile, json_data+'\n', 'a')

                # Download Pkg (exe and dmg)
                item = json.loads(json_data)
                dirname = 'exe' if i == 'win' else 'dmg'
                pkg_out = os.path.join(rootdir, dirname, item.get('name'))
                if os.path.exists(pkg_out):
                    continue
                print('Downloading', item.get('name'))
                f = get(item.get('url')[1])
                output(pkg_out, f)

def helper():
    ''' display help information. '''
    global rootdir
    doclist = []
    for i in __doc__.splitlines():
        if i.startswith("@") and i.find(": ") > -1:
            doclist.append(i.split(': ')[1])
    _author, _email, _description, _github, _version = doclist

    parser = argparse.ArgumentParser(description=_description)
    parser.add_argument('--rootdir', metavar='PATH', type=str,
                        dest='rootdir', action='store',
                        help='root dir to save chrome file')
    parser.add_argument('-v', '--version', dest='version', action='store_true',
                        help='output version information and exit')
    args = parser.parse_args()

    if args.version:
            print('Version {}\nWritten by {} <{}>\nReport bug: <{}>'.format(
                  _version, _author, _email, _github))
            sys.exit()

    if args.rootdir and os.path.exists(args.rootdir):
        rootdir = args.rootdir
    print("Use {} to save Google Chrome.".format(rootdir))

def main():
    global rootdir, jsonfile
    rootdir = '/var/tmp/'
    helper()
    jsonfile = os.path.join(rootdir, 'version.json')
    csvfile = os.path.join(rootdir, 'version.csv')

    if os.path.exists(jsonfile):
        os.remove(jsonfile)
    urllib.request.urlretrieve('http://omahaproxy.appspot.com/all', filename=csvfile)

    # Download exe and dmg
    get_pkg()

    # Download rpm and deb
    get_rpm()
    get_deb()

if __name__ == '__main__':
    main()
