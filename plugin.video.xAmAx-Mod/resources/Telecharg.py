# -*- coding: utf-8 -*-
# Module: Telecharg
# Author: xamax
# Created on: 05.08.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import sys
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
        self.UrlRepo = "https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/"
        
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

        self.Maj=[("xAmAx",".db","resources/"),
                  ("settings",".xml","resources/"),
                  ("vStreamOpt",".py","resources/"),
                  ("LSPOpt",".py","resources/"),
                  ("default",".py",""),
                  ("Samba",".py","resources/"),
                  ("Menu",".py","resources/")]

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
            err="Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0])
            print err
            return err

    def TelechargementZip(self,url,dest,DPAff=True):
        if DPAff:
            dp = xbmcgui.DialogProgress()
            dp.create("Telechargement Mise a jour:","Fichier en téléchargement",url)
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
        
    def RechMajAuto(self,NomMaj,resources=""):
        try:
            AdresseVersion = self.UrlRepo+self.nomPlugin+"/"+resources+NomMaj
            VRech = urllib.urlopen(AdresseVersion).read()
            VLspopt = self.adn.getSetting(id=NomMaj)
            print "Version "+NomMaj+": "+VLspopt+" Version sur internet: "+VRech
            if VLspopt!=str(VRech):
                return str(VRech)
            else:
                return ""
        except:
            print "Erreur mise a jour: "+str(sys.exc_info()[0])
            return ""

    def MajAuto(self, vertionMaj): #,NomMaj,Ext,resources=""
        """self.MajAuto("xAmAx",".db","resources/")
        self.MajAuto("settings",".xml","resources/")
        self.MajAuto("vStreamOpt",".py","resources/")
        self.MajAuto("LSPOpt",".py","resources/")
        ret = self.MajAuto("default",".py")
        if self.adn.getSetting(id="stban")=="true":
            self.MajAuto("Samba",".py","resources/")
        
        if ret == True:
            executebuiltin('XBMC.Container.Update')
            sleep(0.2)
            executebuiltin('XBMC.Container.Refresh')
            sleep(0.2)"""

        for NomMaj,Ext,resources in self.Maj:
            if resources=="":
                AdresseFich = os.path.join(self.AdressePlugin, NomMaj+Ext)
            else:
                AdresseFich = os.path.join(self.AdressePlugin, "resources", NomMaj+Ext)
            try:
                    """AdresseVersion = self.UrlRepo+self.nomPlugin+"/"+resources+NomMaj
                    VRech = urllib.urlopen(AdresseVersion).read()
                    VLspopt = self.adn.getSetting(id=NomMaj)
                    print "Version "+NomMaj+": "+VLspopt+" Version sur internet: "+VRech"""
                ret = self.RechMajAuto(NomMaj,resources)
                if ret != "":
                    DL = urllib.urlopen(self.UrlRepo+self.nomPlugin+"/"+resources+NomMaj+Ext).read()
                    fichier = open(AdresseFich, "w")
                    fichier.write(DL)
                    fichier.close()
                    self.adn.setSetting(id=NomMaj, value=ret)
                    print "Mise a jour de "+NomMaj+" OK"
                except:
                    print "Erreur mise a jour: "+str(sys.exc_info()[0])
                    return "Erreur mise a jour: "+str(sys.exc_info()[0])
        self.adn.setSetting(id="MajV", value=vertionMaj)
        return "OK"

