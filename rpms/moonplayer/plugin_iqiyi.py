#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import moonplayer
import json
import hashlib
from uuid import uuid4
from random import random, randint
from math import floor
from moonplayer_utils import list_links

## hosts
hosts = ('www.iqiyi.com',)
    
## parse
def parse(url, options):
    if url.startswith('http://www.iqiyi.com/a_'):
        moonplayer.get_url(url, parse_a_cb, None)
    elif url.startswith('http://www.iqiyi.com/lib/m_'):
        moonplayer.get_url(url, parse_tv_cb, None)
    elif url.startswith('http://www.iqiyi.com/v_') or \
    url.startswith('http://www.iqiyi.com/w_') or \
    url.startswith('http://www.iqiyi.com/dianshiju/') or \
    url.startswith('http://www.iqiyi.com/dianying/'):
        parser.feed(url, options)
    else:
        moonplayer.warn('Wrong URL!')

vid_re = re.compile(r'data-player-videoid="(.+?)"')
tvid_re = re.compile(r'tvId:\s?(\d+),')
name_re = re.compile(r'data-sharethirdparty-videoname="(.+?)"')

class Parser(object):
    def __init__(self):
        pass
        
    def mix(self, tvid):
        enc = ['97596c0abee04ab49ba25564161ad225']
        tm = str(randint(2000,4000))
        src = 'eknas'
        enc.append(str(tm))
        enc.append(tvid)
        sc = hashlib.new('md5', "".join(enc)).hexdigest()
        return tm,sc,src
        
    def getVRSXORCode(self, arg1, arg2):
        loc3 = arg2 % 3
        if loc3 == 1:
            return arg1 ^ 121
        if loc3 == 2:
            return arg1 ^ 72
        return arg1 ^ 103
        
    def getVrsEncodeCode(self, vlink):
        loc6 = 0
        loc2 = ''
        loc3 = vlink.split("-")
        loc4 = len(loc3)
        for i in range(loc4-1,-1,-1):
            loc6 = self.getVRSXORCode(int(loc3[loc4-i-1],16),i)
            loc2 += chr(loc6)
        return loc2[::-1]
    
    def feed(self, url, options):
        self.origin_url = url
        moonplayer.get_url(url, self.parse_vid, options)
        
    def parse_vid(self, content, options):
        name_match = name_re.search(content)
        if name_match:
            self.name = name_match.group(1)
        else:
            self.name = '未知视频名称'
        tvid_match = tvid_re.search(content)
        vid_match = vid_re.search(content)
        if tvid_match and vid_match:
            self.uid = uuid4().hex
            tvid = tvid_match.group(1)
            vid = vid_match.group(1)
            tm,sc,src = self.mix(tvid)
            url = 'http://cache.video.qiyi.com/vms?key=fvip&src=1702633101b340d8917a69cf8a4b8c7' +\
                "&tvId="+tvid+"&vid="+vid+"&vinfo=1&tm="+tm+\
                "&enc="+sc+\
                "&qyid="+self.uid+"&tn="+str(random()) +"&um=1" +\
                "&authkey="+hashlib.new('md5', hashlib.new('md5', '').hexdigest()+str(tm)+tvid).hexdigest()
            moonplayer.get_url(url, self.parse_vms, options)
        else:
            moonplayer.warn('Fail!')
            
    def parse_vms(self, content, options):
        info = json.loads(content)
        if info['code'] != 'A000000':
            moonplayer.warn('Code Error')
            return
        if info["data"]['vp']["tkl"]=='':
            moonplayer.warn('Error: empty data.')
            return
        # Read urls of all qualities
        vs = info["data"]["vp"]["tkl"][0]["vs"]
        bids = [None] * 5
        for v in vs:
            bid = int(v[u'bid']) - 1
            if bid < 5 and bid >= 0:
                bids[bid] = v['fs']
                if not v["fs"][0]["l"].startswith("/"):
                    tmp = self.getVrsEncodeCode(v["fs"][0]["l"])
                    if tmp.endswith('mp4'):
                        bids[bid] = v["flvs"]
        # Select quality
        if options & moonplayer.OPT_QL_SUPER:
            q = 3
        elif options & moonplayer.OPT_QL_HIGH:
            q = 1
        else:
            q = 0
        for i in xrange(q, -1, -1):
            if bids[i]:
                self.video_links = bids[i]
                break
        if options & moonplayer.OPT_DOWNLOAD and bids[4]:
            if moonplayer.question('是否下载1080P版本？'):
                self.video_links = bids[4]
        
        # Get video's key
        self.urls = []
        self.vlinks = []
        self.key_roots = []
        self.info = info
        for i in self.video_links:
            vlink = i['l']
            if not vlink.startswith('/'):
                vlink = self.getVrsEncodeCode(vlink)
            self.vlinks.append(vlink)
            self.key_roots.append(vlink.split("/")[-1].split(".")[0])
        url = "http://data.video.qiyi.com/t?tn=" + str(random())
        moonplayer.get_url(url, self.parse_key, options)
    
    def parse_key(self, content, options):
        time = json.loads(content)["t"]
        t = str(int(floor(int(time)/(10*60.0))))
        tp = ")(*&^flash@#$%a"  #magic from swf
        for i in xrange(len(self.key_roots)):
            key = hashlib.new("md5", t+tp+self.key_roots[i]).hexdigest()
            baseurl = self.info["data"]["vp"]["du"].split("/")
            baseurl.insert(-1, key)
            url = "/".join(baseurl) + self.vlinks[i] + \
                '?su=' + self.uid + \
                '&qyid=' + uuid4().hex + \
                '&client=&z=&bt=&ct=&tn=' + str(randint(10000,20000))
            self.urls.append(url)
            
        # Get final urls
        self.result = []
        moonplayer.get_url(self.urls[0], self.parse_final_url, options)
        
    def parse_final_url(self, content, options):
        i = len(self.result) / 2
        self.result.append('%s_%i.mp4' % (self.name, i))
        self.result.append(str(json.loads(content)['l']))
        i += 1
        if i < len(self.urls):  # Parse next final url
            moonplayer.get_url(self.urls[i], self.parse_final_url, options)
        elif options & moonplayer.OPT_DOWNLOAD:
            moonplayer.download(self.result, self.name + '.mp4')
        else:
            if len(self.urls) > 2:
                moonplayer.warn('本视频较长，爱奇艺视频地址10分钟变化一次，建议下载后播放，避免播放到一半时下载地址失效！')
            moonplayer.play(self.result)

parser = Parser()
