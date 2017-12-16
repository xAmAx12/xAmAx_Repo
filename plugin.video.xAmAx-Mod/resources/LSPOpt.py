# -*- coding: utf-8 -*-
# Module: LSPOpt
# Author: xamax
# Created on: 29.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import os, re, sys
from xbmcvfs import exists,File
from xbmcaddon import Addon
from xbmcgui import DialogProgress,Dialog
from xbmc import executebuiltin
import urllib as urlib
from base64 import b64decode
from resources.DB import db
from time import sleep
from resources.Telecharg import cDL

class cLiveSPOpt():

    def __init__(self):
        self.adn = Addon('plugin.video.xAmAx-Mod')

    def UrlADFLY(self, code):
        zero = ''
        un = ''
        for n,letter in enumerate(code):
            if n%2 == 0:
                zero += code[n]
            else:
                un =code[n] + un
        clef = zero + un
        print "clef ADFLY: "+str(clef)
        clef = base64.b64decode(clef.encode("utf-8"))
        return clef[2:]

    def ConvNom(self, Nom):
        ret = ''
        for l in Nom:
            if (ord(l) > 0 and ord(l)!=13 and ord(l) < 126):
                ret += l
            elif (ord(l) > 191  and ord(l) < 198):
                ret += "A" #chr(65)
            elif (ord(l) > 199  and ord(l) < 204):
                ret += "E" #chr(69)
            elif (ord(l) > 203  and ord(l) < 208):
                ret += "I" #chr(73)
            elif (ord(l) > 209  and ord(l) < 215):
                ret += "O" #chr(79)
            elif (ord(l) > 216  and ord(l) < 221):
                ret += "U" #chr(85)
            elif (ord(l) > 223  and ord(l) < 230):
                ret += "a" #chr(97)
            elif (ord(l) > 231  and ord(l) < 236):
                ret += "e" #chr(101)
            elif (ord(l) > 235  and ord(l) < 240):
                ret += "i" #chr(105)
            elif (ord(l) > 241  and ord(l) < 247):
                ret += "o" #chr(111)
            elif (ord(l) > 248  and ord(l) < 253):
                ret += "u" #chr(117)
            elif ord(l) > 125:
                ret += "?"
                print "+++++++++ chr= "+str(ord(l))
        NomRet = ret.upper().replace(
                        "[ FR ] ","").replace(
                        "[ FR: ] ","").replace(
                        "| FR | ","").replace(
                        "FR: ","").replace(
                        "FR : ","").replace(
                        "FR:", "").replace(
                        "FR|", "").replace(
                        "FR-", "").replace(
                        "FR ", "").replace(
                        "ENF-", "").replace(
                        "FRENCH", "FRANCE").replace(
                        "FRANCE", "FRANCE ").replace(
                        "FRANCE  ", "FRANCE ").replace(
                        "+", " +").replace(
                        "  +", " +").replace(
                        "-", " ").replace(
                        ".", " ").replace(
                        "_", " ").replace(
                        "FRANCE |", "").replace(
                        "\r", "").replace(
                        "(SERVER 1)","")
                       
        
        while 1:
            if NomRet.startswith(' '):
                NomRet = NomRet[1:]
            else:
                break
        return NomRet
    
    def CreerBouquet(self, CheminxAmAx):
        Bouquet=[]
        print "CreerBouquet: CheminxAmAx= "+CheminxAmAx
        dbxAmAx = os.path.join(CheminxAmAx, "resources", "xAmAx.db")
        try:
            DBxAmAx = db(dbxAmAx)
            DBxAmAx.Delete("UrlBouquet")
        
            IdUrlChaine = 0
            for numTab in range(1,5):
                if DBxAmAx.TableExist("List"+str(numTab)):
                    #print "------List"+str(numTab)
                    cBouq = DBxAmAx.Select(Table="Bouquet", Colonnes="IDBouquet, TriDesChaines", Where="", Order="Ordre ASC")
                    for IDBouqu, TriDesChaines in cBouq:
                        cChaine = DBxAmAx.Select(Table="ChaineBouquet",
                                            Colonnes="IDChaineB, NomChaine, PasDansChaine",
                                            Where="IDBouqChaine = " + str(IDBouqu),
                                            Order=str(TriDesChaines))
                        #print "-----cChaine: "+str(cChaine)
                        for IDChaine, NomC, PasNom in cChaine:
                            if PasNom != None and PasNom != "":
                                ANDWHERE = "AND Nom NOT LIKE '%"+PasNom+"%' "
                            else:
                                ANDWHERE = ""
                            cListCh = DBxAmAx.Select(Table="List"+str(numTab),
                                            Colonnes="*",
                                            Where="Nom LIKE '%"+str(NomC).upper()+"%' "+ANDWHERE,
                                            Order="Nom ASC")
                            #print "-----cListCh: "+str(cListCh)
                            for IdLP, Nom, Url, Entete in cListCh:
                                IdUrlChaine += 1
                                DBxAmAx.Insert(Table="UrlBouquet",
                                               Colonnes="IDUrlB,IdBouquet,IDChaine,Url,NomAffichChaine",
                                               Valeurs=(IdUrlChaine,IDBouqu,IDChaine,Url,Nom))
                            DBxAmAx.FinEnregistrement()
        except:
            print "Erreur de connection à la base xAmAx!"
            return "Erreur de connection à la base xAmAx!"
            
        return "OK"

    def LireM3u(self, CheminxAmAx, F4m=False, cvNom=True):
        print "Liste de chaine M3u"
        dialog = Dialog()
        fn = dialog.browse(1, 'Ouvrir le fichier M3u', 'files', '.m3u|.m3u8', False, False, 'special://home')
        ret = []
        if fn != False and fn != "":
            if exists(fn):
                f = File(fn)
                M3u = f.read()
                f.close()
                if M3u!="":
                    TabM3u = re.compile('^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)\n', re.I+re.M+re.U+re.S).findall(M3u)
                    for Par, Nom , Url in TabM3u :
                        if cvNom==True:
                            Nom = self.ConvNom(Nom)
                        Url=Url.split("|")[0].replace(".m3u8",".ts").replace("\r", "")
                        if F4m==True:
                            Url='plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER'%(urlib.quote_plus(Url))
                        DicM3u = (Nom,Url)
                        ret.append(DicM3u)
        return ret

    def AdulteSources(self,Url='https://www.mrsexe.com/cat/62/sodomie/'):
        print "Recherche de la liste de chaine..."
        Page = str(cDL().TelechargPage(url=Url))
        ret = []
        if not Page.startswith("Erreur"):
            match = re.compile('thumb-list(.*?)<ul class="right pagination">', re.DOTALL | re.IGNORECASE).findall(Page)
            #xbmc.log("Resulta 1 tri: "+str(match))
            match1 = re.compile(r'<li class="[^"]*">\s<a class="thumbnail" href="([^"]+)">\n<script.+?([^;]+);</script>\n<figure>\n<img  id=".+?" src="([^"]+)".+?/>\n<figcaption>\n<span class="video-icon"><i class="fa fa-play"></i></span>\n<span class="duration"><i class="fa fa-clock-o"></i>([^<]+)</span>\n(.+?)\n',
                                re.DOTALL | re.IGNORECASE).findall(match[0])
            for url, Timage, image, Temp, Descript in match1:
                ret.append((url,"https:"+image, Timage.split("(")[1][:-1].replace("'","").split(","),Descript+" "+Temp))
            print "Recherche OK..."
            try:
                nextp=re.compile(r'<li class="arrow"><a href="(.+?)">suivant</li>').findall(Page)
                ret.append(('https://www.mrsexe.com' + nextp[0],"",[],"Page Suivante..."))
            except: pass
        else:
            dialog = Dialog()
            ok = dialog.ok("Telechargement impossible...", Page)
        return ret
