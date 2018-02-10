# -*- coding: UTF-8 -*-
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
        clef = base64.b64decode(clef.encode("latin1"))
        return clef[2:]

    def ConvNom(self, Nom):
        NomRet=str(Nom) #.decode("latin1").encode("latin1","replace")
        NomRet=NomRet.replace(
                        "L-FR: ","").replace(
                        "FR: ","").replace(
                        "FR : ","").replace(
                        "FR:", "").replace(
                        "FR|", "").replace(
                        "FR-", "").replace(
                        " FR ", "").replace(
                        " FR_", "").replace(
                        " (FR)", "").replace(
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
                        "\R", "").replace(
                        "(SERVER 1)","").replace(
                        "\xc3\xa9","e").replace(
                        "\xc3\x89","E").replace(
                        "\xc3\xa8","e").replace(
                        "\xc3\x94","O").replace(
                        "&amp;","&")
        
        if NomRet.startswith("FR "): NomRet = NomRet[3:]
        while 1:
            if NomRet.startswith(' '):
                NomRet = NomRet[1:]
            else:
                break
        return NomRet
    
    def CreerBouquet(self, CheminxAmAx):
        Bouquet=[]
        print "CreerBouquet: CheminxAmAx= "+CheminxAmAx
        dbxAmAx = os.path.join(CheminxAmAx, "xAmAx.db")
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
    
    def RechercheChaine(self, CheminxAmAx):
        i=0
        j=0
        ListeEffacer = False
        dbxAmAx = os.path.join(CheminxAmAx, "xAmAx.db")
        print "Ouverture de la Base de donnée xAmAx: "+dbxAmAx
        DBxAmAx = db(dbxAmAx)
        IdLP = 0
        NbMaj=1
        
        if NbMaj>0:
            self.MajDiv = 100/NbMaj
            self.TotMaj = 0
            self.dp = DialogProgress()
            sleep(0.5)
            self.dp.create("Telechargement de la liste de chaine:")
            sleep(0.5)
            NbMajEc = 1
            

            Retour, Erreur = self.MenuTV()
            NbRecherche = len(Retour)+1
            if len(Retour)>0 and Erreur == "OK":
                print "Liste de chaine 1 a afficher: "+str(len(Retour))
                self.TotMaj = self.MajDiv/25
                self.dp.update(self.TotMaj)
                sleep(0.5)
                ListeEffacer = True
                DivisionRech = ((self.MajDiv-self.TotMaj)/len(Retour))
                
                for Nom,Url in Retour:
                    NbRecherche -= 1
                    print "Recherche Liste de chaine "+str(Nom)
                    self.dp.update(self.TotMaj,"Recherche Liste de chaine "+str(NbRecherche))
                    sleep(0.5)
                    if not "SERVIDOR 1" in Nom:
                        Retour2,Erreur2 = self.ListTv(Url)
                        print "Nombre de résultat de la Liste de chaine "+str(len(Retour2))
                        if len(Retour2)>0 and Erreur2 == "OK":
                            try:
                                DBxAmAx.Delete(Table="List"+str(NbRecherche))
                            except:
                                pass
                            DBxAmAx.CreerTable(Table="List"+str(NbRecherche), colonnes="`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT")
                            for NomTv,UrlTV,IconTV in Retour2:
                                IdLP += 1
                                DBxAmAx.Insert(Table="List"+str(NbRecherche),
                                               Colonnes="IDLP,Nom,Url",
                                               Valeurs=(IdLP,NomTv+" [COLOR gold]("+str(NbRecherche)+")[/COLOR]",UrlTV)) #+"&name="+NomTv))
                        elif Erreur2!="OK":
                            executebuiltin("XBMC.Notification(Mise à jour Liste TV "+str(NbRecherche)+" Impossible!!! ,"+Erreur2+",5000,"")")
                    else:
                        DBxAmAx.Delete(Table="List"+str(NbRecherche))
                    self.TotMaj += DivisionRech
                    self.dp.update(self.TotMaj)
                    sleep(0.3)
                DBxAmAx.FinEnregistrement()
            else:
                if Erreur!="OK":
                    executebuiltin("XBMC.Notification(Mise à jour Liste TV Impossible!!! ,"+Erreur+",5000,"")")
            self.TotMaj = self.MajDiv*NbMajEc
            print "Telechargement de la liste de chaine:"+str(self.TotMaj)+"%"
            sleep(0.5)
        self.dp.close()
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

    def MenuTV(self):
        urlBase = 'aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL2xvZ2FuMTk4My9BRERPTlMtTUVOVVMvbWFzdGVyL0ZSQU5DQSUyME1FTlUueG1s'
        ListeRet = []
        try:
            ret = cDL().TelechargPage(url=b64decode(urlBase))
            if ret.startswith("Erreur"):
                print ret
            else:
                TabXml = re.compile("<name?[^>]*>(.*?)</name>.*?<externallink?[^>]*>(.*?)</externallink>", re.I+re.M+re.S).findall(ret)
                for NomLien,ExtUrl in TabXml:
                    print "   Adresse Ext: "+ExtUrl
                    FichList = (NomLien,ExtUrl)
                    ListeRet.append(FichList)
        except:
            return ListeRet,"Erreur de Recherche des listes de chaines!"
                
        return ListeRet,"OK"

    def ListTv(self,Adress):
        Cmp=0
        ListeRet = []
        try:
            ret2 = cDL().TelechargPage(url=Adress)
            TabLien = re.compile("<title?[^>]*>(.*?)</title>.*?<link?[^>]*>(.*?)</link>", re.I+re.M+re.S).findall(ret2)
            for Nom,Url in TabLien:
                Icon = ""
                if "tvg-name=" in Nom:
                    ConvTitre = Nom.split(chr(34))
                    if len(ConvTitre) > 5:
                        Nom = ConvTitre[3]
                        Icon = ConvTitre[5]
                NomAff=self.ConvNom(Nom)
                if Url!="http://Ignoreme":
                    FichList = (NomAff,Url,Icon)
                    ListeRet.append(FichList)
        except:
            return ListeRet,"Erreur de Recherche des chaines de la liste!"
        return ListeRet,"OK"

    def AdulteSources(self,Url='aHR0cHM6Ly93d3cubXJzZXhlLmNvbS9jYXQvNjIvc29kb21pZS8='):
        print "Recherche de la liste de chaine..."
        Page = str(cDL().TelechargPage(url=b64decode(Url)))
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
