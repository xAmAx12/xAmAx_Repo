# -*- coding: utf-8 -*-
# Module: Telecharg
# Author: xamax
# Created on: 05.08.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys,os
import urllib2 as urllib
import urllib as urlib
from urllib import FancyURLopener
from httplib import HTTPSConnection
import xbmcgui
from xbmcaddon import Addon
import time

class MonTelecharg(FancyURLopener):
    version = 'xAmAx-Mod'

MonDL = MonTelecharg()
urlretrieve = MonTelecharg().retrieve
urlopen = MonTelecharg().open

def _pbhook(numblocks, blocksize, filesize, dp, start_time):
    try: 
        percent = min(numblocks * blocksize * 100 / filesize, 100) 
        currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
        kbps_speed = numblocks * blocksize / (time.time() - start_time) 
        if kbps_speed > 0: 
            eta = (filesize - numblocks * blocksize) / kbps_speed 
        else: 
            eta = 0 
        kbps_speed = kbps_speed / 1024 
        mbps_speed = kbps_speed / 1024 
        total = float(filesize) / (1024 * 1024) 
        mbs = '[COLOR white]%.02f MB[/COLOR] sur %.02f MB' % (currently_downloaded, total)
        e = 'Vitesse: [COLOR lime]%.02f Mb/s ' % mbps_speed  + '[/COLOR]'
        e += 'ETA: [COLOR yellow]%02d:%02d' % divmod(eta, 60) + '[/COLOR]'
    except: 
        percent = 100 

class cDL():

    def __init__(self):
        self.nomPlugin = 'plugin.video.xAmAx-Mod'
        self.adn = Addon(self.nomPlugin)
        self.AdressePlugin = self.adn.getAddonInfo('path')
        
        self.USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

        self.headers = {'User-Agent': self.USER_AGENT,
                       'Accept': '*/*',
                       'Connection': 'keep-alive'}

        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}

    def TelechargPage2(self,url="", Entete=None, Post={}):
        try:
            import requests
            headers = {}
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
            link = requests.session().get(url, headers=headers, verify=False).text
            link = link.encode('utf-8', 'ignore')
            return link
        except:
            return self.TelechargPage(url=url, Entete=Entete, Post=Post)

    def TelechargPage(self, url="", Entete=None, Post={}):

        cookie = urllib.HTTPCookieProcessor(None)
        opener = urllib.build_opener(cookie, urllib.HTTPBasicAuthHandler(), urllib.HTTPHandler())
        EnteteDansPage=None

        if '|' in url:
            url,EnteteDansPage=url.split('|')
        if len(Post)==0:
            req = urllib.Request(url,headers=self.hdr)
        else:
            data = urlib.urlencode(Post)
            req = urllib.Request(url,data,headers=self.hdr)
            
        #req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
        if Entete:
            for h,hv in Entete:
                req.add_header(h,hv)
        if EnteteDansPage:
            EnteteDansPage=EnteteDansPage.split('&')
            for h in EnteteDansPage:
                if len(h.split('='))==2:
                    n,v=h.split('=')
                else:
                    vals=h.split('=')
                    n=vals[0]
                    v='='.join(vals[1:])
                req.add_header(n,v)
                
        try:
            response = opener.open(req,None,timeout=20)
            FichTelecharg=response.read()
            response.close()
            return FichTelecharg;
        except:
            sysErr = sys.exc_info()
            err="Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sysErr[0])+"\n"+str(sysErr[1])
            print err
            return err

    def TelechargementZip(self,url,dest,DPAff=True,Nom="Mise a jour"):
        if DPAff:
            dp = xbmcgui.DialogProgress()
            dp.create("Telechargement "+Nom+":","Fichier en téléchargement",url)
        try:
            Demar=time.time()
            urlretrieve(url,dest,lambda nb, bs, fs: _pbhook(nb,bs,fs,dp,Demar))
        except:
            print "Téléchargement de: " + url
            print "Téléchargement dans le dossier: " + dest
            req = urllib.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
            essai = urllib.urlopen(req)
            fichier = open(dest, "wb")
            fichier.write(essai.read())
            fichier.close()
        if os.path.exists(dest):
            statinfo = os.stat(dest)
            if statinfo.st_size > 0:
                return True
        return False
    

    def DLFich(self,url,dest, DPView=True):
        if DPView:
            dp = xbmcgui.DialogProgressBG()
            dp.create("Telechargement du fichier...",url)
        try:
            Demar=time.time()
            urllib.urlretrieve(url,dest,lambda nb, bs, fs: _pbhook(nb,bs,fs,dp,Demar))
        except:
            req = urllib.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
            essai = urllib.urlopen(req)
            fichier = open(dest, "wb")
            fichier.write(essai.read())
            fichier.close()

    def EnvoiLogKodi(self, CheminLog, ListeFichier ):
        headers = { 'User-Agent' : self.USER_AGENT }
        for i in ListeFichier:
            if 'kodi.log' in i:
                post_data = {}
                cUrl = 'http://slexy.org/index.php/submit'
                logop = open(CheminLog + i,'rb')
                result = logop.read()
                logop.close()
                post_data['raw_paste'] = result
                post_data['author'] = 'kodi.log'
                post_data['language'] = 'text'
                post_data['permissions'] = 1 #private
                post_data['expire'] = 259200 #3j
                post_data['submit'] = 'Submit+Paste'
                request = urllib.Request(cUrl,urlib.urlencode(post_data),headers)
                reponse = urllib.urlopen(request)
                code = reponse.geturl().replace('http://slexy.org/view/','')
                reponse.close()
                return code
        return "Erreur d'envoi du ficher Log! \n Le fichier est introuvable... \n Désolé!"
    

    

