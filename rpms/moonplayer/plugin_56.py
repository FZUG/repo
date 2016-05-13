#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import moonplayer
import json
from moonplayer_utils import list_links

hosts = ('www.56.com',)

# Search videos
def search(keyword, page):
    keyword = keyword.replace(' ', '%20')
    url = 'http://so.56.com/video/' + keyword + '/?s=3&t=&c=&page=' + str(page)
    moonplayer.get_url(url, search_cb, None)
    
def search_cb(page, data):
    result = list_links(page, 'http://www.56.com/u')
    moonplayer.show_list(result)
    
# Search albums
def search_album(keyword, page):
    keyword = keyword.replace(' ', '%20')
    url = 'http://so.56.com/album/' + keyword + '/?page=' + str(page)
    moonplayer.get_url(url, search_album_cb, None)
    
def search_album_cb(page, data):
    result = list_links(page, 'http://www.56.com/w')
    moonplayer.show_list(result)

# Parse video
enid_re = re.compile(r'v_(\w+?).html')
album_re = re.compile(r'http://www.56.com/w(\d+)/play_album-aid-(\d+)')
def parse(url, options):
    match = album_re.search(url) # albums
    if match:
        (wid, aid) = match.group(1, 2)
        AlbumParser(wid, aid)
        return
    match = enid_re.search(url) # videos
    if match and '56.com' in url:
        enid = match.group(1)
        url = 'http://vxml.56.com/json/' + enid + '/?src=site'
        moonplayer.get_url(url, parse_cb, options)
        return
    moonplayer.warn('Wrong url.')
    
def parse_cb(page, options):
    data = json.loads(page)
    if data[u'msg'] != u'ok':
        moonplayer.warn(data[u'msg'].encode('utf-8'))
        return
    info = data[u'info']
    name = info[u'Subject'].encode('utf-8')
    urls = [None] * 3
    for rfile in info[u'rfiles']:
        if rfile[u'type'] == u'super':
            urls[2] = rfile[u'url'].encode('utf-8')
        elif rfile[u'type'] == u'clear':
            urls[1] = rfile[u'url'].encode('utf-8')
        elif rfile[u'type'] == u'normal':
            urls[0] = rfile[u'url'].encode('utf-8')
    if options & moonplayer.OPT_QL_SUPER:
        q = 2
    elif options & moonplayer.OPT_QL_HIGH:
        q = 1
    else:
        q = 0
    for i in xrange(q, -1, -1):
        if urls[i]:
            if options & moonplayer.OPT_DOWNLOAD:
                moonplayer.download([name, urls[i]])
            else:
                moonplayer.play([name, urls[i]])
            return
            
# Parse album
album_url_fmt = r'http://www.56.com/w%s/album_v3/album_videolist_2011.phtml?row=100&aid=%s&page=%i'
class AlbumParser(object):
    def __init__(self, wid, aid):
        self.wid = wid
        self.aid = aid
        self.page = 1
        self.result = []
        url = album_url_fmt % (wid, aid, 1)
        moonplayer.get_url(url, self.parse_album_cb, None)
        
    def parse_album_cb(self, content, data):
        if content[-1] == ';':
            content = content[0:-1]
        inf = json.loads(content)
        try:
            items = inf[u'data']
        except KeyError: # last page
            moonplayer.show_album(self.result)
            return
            
        for item in items:
            enid = item[u'video_id'].encode('utf-8')
            name = item[u'video_title'].encode('utf-8')
            url = 'http://www.56.com/u30/v_%s.html' % (enid,)
            self.result.append(name)
            self.result.append(url)
        self.page += 1
        url = album_url_fmt % (self.wid, self.aid, self.page)
        moonplayer.get_url(url, self.parse_album_cb, None)
        
