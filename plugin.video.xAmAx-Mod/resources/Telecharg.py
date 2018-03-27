# -*- coding: utf-8 -*-
# Module: Telecharg
# Author: xamax
# Created on: 05.08.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import sys,os
import urllib2 as urllib
import urllib as urlib
from httplib import HTTPSConnection
import xbmcgui
from xbmcaddon import Addon

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
            urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
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
            urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
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
    

    

