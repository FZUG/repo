#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import moonplayer
import json
from utils import list_links

hosts = ('www.fun.tv',)

def search(keyword, page):
    keyword = keyword.replace(' ', '+')
    url = 'http://www.fun.tv/search/pg-%i.word-%s' % (page, keyword)
    moonplayer.get_url(url, search_cb, None)
    
sub_re = re.compile(r'<a[^>]+title=[\'"](.+?)[\'"][^>]+href=[\'"]/subject/(\d+).+?[\'"]')
m_re = re.compile(r'<a[^>]+title=[\'"](.+?)[\'"][^>]+href=[\'"]/vplay/m-(\d+).+?[\'"]')
def search_cb(page, data):
    # Movie
    result = list_links(page, '/subject/')
    result += list_links(page, '/vplay/m-')
    result += list_links(page, '/vplay/g-')
    result += list_links(page, '/vplay/v-')
    moonplayer.show_list(result)

tv_re = re.compile(r'[mg]-(\d+)\.e-(\d+)')
tv_re2 = re.compile(r'[mg]-(\d+)')
v_re = re.compile(r'v-(\d+)')
v_re2 = re.compile(r'[mg]-\d+\.v-(\d+)/')
def parse(url, options):
    if url.startswith('http://www.fun.tv'):
        url = url.replace('http://www.fun.tv', '')
        
    if url.startswith('/subject/'):
        vid = url.split('/')[2]
        url = 'http://api.fun.tv/ajax/get_web_fsp/' + vid + '/mp4'
        moonplayer.get_url(url, parse_subject, vid)
        return
    
    match = tv_re.search(url)
    if match:
        (vid, num) = match.group(1, 2)
        url = 'http://api.fun.tv/ajax/get_web_fsp/' + vid + '/mp4'
        moonplayer.get_url(url, parse_m_vid, (options, int(num)))
        return
            
    match = v_re2.search(url)
    if match:
        vid = match.group(1)
        url = 'http://api1.fun.tv/ajax/playinfo/video/' + vid
        moonplayer.get_url(url, parse_v_vid, options)
        return
    
    match = tv_re2.search(url)
    if match:
        vid = match.group(1)
        url = 'http://api.fun.tv/ajax/get_web_fsp/' + vid + '/mp4'
        moonplayer.get_url(url, parse_subject, vid)
        return
    
    match = v_re.search(url)
    if match:
        vid = match.group(1)
        url = 'http://api.fun.tv/ajax/get_media_data/video/' + vid
        moonplayer.get_url(url, parse_v_vid, options)
        return
    
    moonplayer.warn('Wrong url.')
    

# Parse TV series list
def parse_subject(page, vid):
    result = []
    try:
        mults = json.loads(page)[u'data'][u'fsps'][u'mult']
    except KeyError:
        url = 'http://www.fun.tv/vplay/g-' + vid
        moonplayer.get_url(url, parse_subject2, vid)
        return
    for mult in mults:
        name = 'unknown'
        try:
            name = mult[u'name'].encode('UTF-8')
            name = mult[u'full'].encode('UTF-8')
        except KeyError:
            pass
        url = 'http://www.fun.tv' + str(mult[u'url'])
        result.append(name)
        result.append(url)
    moonplayer.show_album(result)
    
vinfo_re = re.compile(r'''window\.vplayInfo\s*=\s*({.+?});''')
def parse_subject2(page, vid):
    match = vinfo_re.search(page)
    if match:
        result = []
        data = json.loads(match.group(1))[u'dvideos'][0][u'videos']
        for item in data:
            name = item[u'title'].encode('utf-8')
            url = 'http://www.fun.tv' + str(item[u'url'])
            result.append(name)
            result.append(url)
        moonplayer.show_album(result)
    else:
        moonplayer.warn('Parse fail!')
    
# Parse 'http://www.fun.tv/vplay/m-...'
def parse_m_vid(page, data):
    options = data[0]
    mults = json.loads(page)[u'data'][u'fsps'][u'mult']
    for mult in mults:
        if mult[u'number'] == data[1]:
            name = 'unknown'
            try:
                name = mult[u'name'].encode('UTF-8')
                name = mult[u'full'].encode('UTF-8')
            except KeyError:
                pass
            name += '.mp4'
            cid = str(mult[u'cid'])
            if options & moonplayer.OPT_QL_SUPER:
                p = 737280  # 720p
            elif options & moonplayer.OPT_QL_HIGH:
                p = 491520  # 480p
            else:
                p = 327680  # 320p
            url = 'http://jobsfe.funshion.com/query/v1/mp4/%s.json?bits=%i' % (cid, p)
            moonplayer.get_url(url, parse_m_cb, (options, name))
            
def parse_m_cb(page, data):
    url = json.loads(page)[u'playlist'][0][u'urls'][0]
    name = data[1]
    options = data[0]
    if options & moonplayer.OPT_DOWNLOAD:
        moonplayer.download([name, str(url)])
    else:
        moonplayer.play([name, str(url)])
        
# Parse 'http://www.fun.tv/.../play/v-.../'
def parse_v_vid(page, options):
    data = json.loads(page)[u'data']
    name = data[u'name_cn'].encode('UTF-8') + '.mp4'
    hashid = str(data[u'hashid'])
    if options & moonplayer.OPT_QL_SUPER:
        p = 737280  # 720p
    elif options & moonplayer.OPT_QL_HIGH:
        p = 491520  # 480p
    else:
        p = 327680  # 320p
    url = 'http://jobsfe.funshion.com/query/v1/mp4/%s.json?bits=%i' % (hashid, p)
    moonplayer.get_url(url, parse_m_cb, (options, name))
