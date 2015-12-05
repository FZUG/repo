#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import json
from utils import convert_to_utf8, list_links
import moonplayer

## hosts
hosts = ('tv.sohu.com', 'my.tv.sohu.com')
    
##--------##
## search ##
##--------##
def search(kw, page):
    kw = kw.replace(' ', '+')
    url = 'http://so.tv.sohu.com/mts?c=0&v=0&length=0&limit=0&o=0&st=&wd=' + kw + '&p=' + str(page) 
    moonplayer.get_url(url, search_cb, kw)
    
def search_cb(page, kw):
    page = convert_to_utf8(page)
    #tv series
    links = list_links(page, 'http://so.tv.sohu.com/show/')
    links += list_links(page, 'http://tv.sohu.com/item/')
    n_series = len(links) / 2
    #movies
    links += list_links(page, 'http://tv.sohu.com/2')
    n = len(links) / 2
    #others
    links += list_links(page, 'http://my.tv.sohu.com/us/')
    links += list_links(page, 'http://my.tv.sohu.com/pl/')
    #show
    moonplayer.show_list(links)
    for i in xrange(n_series):
        moonplayer.set_list_item_color(i, '#0000ff')
    for i in xrange(n_series, n):
	moonplayer.set_list_item_color(i, '#6a4100')
    
##-------##
## parse ##
##-------##
pp_re = re.compile(r'&\\#(\d+);')
def json_pre_process(page):
    match = pp_re.search(page)
    while match:
        i = int(match.group(1))
        s = chr(i).decode('utf-8').encode('unicode-escape')
        page = page.replace(match.group(0), s)
        match = pp_re.search(page)
    return page


def parse(url, options):
    if url.startswith('http://so.tv.sohu.com/show/') or \
        url.startswith('http://tv.sohu.com/item/'): #tv series
        moonplayer.get_url(url, parse_tv_cb, None)
    elif url.startswith('http://tv.sohu.com/2'): #videos
        moonplayer.get_url(url, parse_cb, options)
    elif url.startswith('http://my.tv.sohu.com/us/'):
        vid = url.split('/')[-1].split('.')[0]
        url = 'http://my.tv.sohu.com/play/videonew.do?af=1&out=0&g=8&vid=' + vid
        moonplayer.get_url(url, parse_my_cb, [vid, options])
    else:
        moonplayer.warn('Wrong url')
        
## parse videos
vid_re = re.compile(r'vid\s?=\s?"(\d+)"')
plid_re = re.compile(r'playlistId="(\d*)"')
def parse_cb(page, options):
    vid_match = vid_re.search(page)
    plid_match = plid_re.search(page)
    if vid_match and plid_match:
        vid = vid_match.group(1)
        plid = plid_match.group(1)
        msg = [vid, plid, options]
        url = 'http://hot.vrs.sohu.com/vrs_flash.action?out=0&g=8&r=1&vid=%s&plid=%s' % (msg[0], msg[1])
        moonplayer.get_url(url, parse_cb2, msg)
    else:
        moonplayer.warn('Fail')

def parse_cb2(page, msg):
    page = json_pre_process(page)
    page = json.loads(page)
    data = page[u'data']
    #try other quality
    try:
        if not data:
            moonplayer.warn('解析失败！换个清晰度试试？')
            return
        elif msg[2] & moonplayer.OPT_QL_SUPER and u'superVid' in data:
            newvid = str(data[u'superVid'])
        elif msg[2] & (moonplayer.OPT_QL_HIGH | moonplayer.OPT_QL_SUPER):
            newvid = str(data[u'highVid'])
        else:
            newvid = str(data[u'norVid'])
        if len(newvid) > 0 and newvid != msg[0] and newvid != '0':
            msg[0] = newvid
            url = 'http://hot.vrs.sohu.com/vrs_flash.action?out=0&g=8&r=1&vid=%s&plid=%s' % (msg[0],msg[1])
            moonplayer.get_url(url, parse_cb2, msg)
            return
    except KeyError:
        pass
    #parse
    vid = msg[0]
    su = data[u'su']
    ip = page[u'allot']
    name = data[u'tvName'].encode('UTF-8')
    tvid = page[u'tvid']
    files = [s.replace('http://data.vod.itc.cn', '') for s in data[u'clipsURL']]
    result = []
    i = 0
    #make cdnlist
    cdnlist = []
    for i in xrange(len(su)):
        cdnlist.append('http://%s/yp2p?prot=9&prod=flash&pt=1&file=%s&new=%s&vid=%s&tvid=%s' % (ip, files[i], su[i], vid, tvid))
    data = {'result': [], 'cdnlist': cdnlist, 'name': name, 'options': msg[2]}
    moonplayer.get_url(cdnlist[0], parse_cdnlist, data)
    
# parse personal videos
def parse_my_cb(page, msg):
    page = json_pre_process(page)
    page = json.loads(page)
    data = page[u'data']
    #try other quality
    try:
        if not data:
            moonplayer.warn('解析失败！换个清晰度试试？')
            return
        elif msg[1] & moonplayer.OPT_QL_SUPER and u'superVid' in data:
            newvid = str(data[u'superVid'])
        elif msg[1] & (moonplayer.OPT_QL_HIGH | moonplayer.OPT_QL_SUPER):
            newvid = str(data[u'highVid'])
        else:
            newvid = str(data[u'norVid'])
        if len(newvid) > 0 and newvid != msg[0] and newvid != '0':
            msg[0] = newvid
            url = 'http://my.tv.sohu.com/play/videonew.do?af=1&out=0&g=8&vid=' + newvid
            moonplayer.get_url(url, parse_my_cb, msg)
            return
    except KeyError:
        pass
    #parse
    vid = msg[0]
    su = data[u'su']
    ip = page[u'allot']
    tvid = page[u'tvid']
    name = data[u'tvName'].encode('UTF-8')
    files = [s.replace('http://data.vod.itc.cn', '') for s in data[u'clipsURL']]
    result = []
    i = 0
    #make cdnlist
    cdnlist = []
    for i in xrange(len(su)):
        cdnlist.append('http://%s/yp2p?prot=9&prod=flash&pt=1&file=%s&new=%s&vid=%s&tvid=%s' % (ip, files[i], su[i], vid, tvid))
    data = {'result': [], 'cdnlist': cdnlist, 'name': name, 'options': msg[1]}
    moonplayer.get_url(cdnlist[0], parse_cdnlist, data)
    
def parse_cdnlist(page, data):
    result = data['result']
    cdnlist = data['cdnlist']
    url = str(json.loads(page)[u'url'])
    i = len(result) / 2
    result.append(data['name'] + '_' + str(i) + '.mp4') 
    result.append(url)
    i += 1
    if i < len(cdnlist):
        moonplayer.get_url(cdnlist[i], parse_cdnlist, data)
    elif data['options'] & moonplayer.OPT_DOWNLOAD:
        moonplayer.download(result, data['name'] + '.mp4')
    else:
        moonplayer.play(result)
    
# parse tv series
link_re = re.compile(r'<a target=_blank href=\s*["\'](http://tv[^"\']+?)["\']\s*>([^<>]+?)</a>')
def parse_tv_cb(page, options):
    links = list_links(page, 'http://tv.sohu.com/2')
    moonplayer.show_album(links)
    
