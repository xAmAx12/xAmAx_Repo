# -*- coding: UTF-8 -*-
# Module: LSPOpt
# Author: xamax
# Created on: 29.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import os, re, sys
from xbmcvfs import exists,File
from xbmcaddon import Addon
from xbmcgui import DialogProgress,Dialog
from xbmc import executebuiltin,log,LOGNOTICE
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
                        b64decode("SXB0djRzYXQuY29t"),"").replace(
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
                        "FRANCE |", "").replace(
                        "\R", "").replace(
                        "(SERVER 1)","").replace(
                        "\xe2\x80\x99","").replace(
                        "\xc2\xa0"," ").replace(
                        "\xc3\xa9","e").replace(
                        "\xc3\x89","E").replace(
                        "\xc3\xa8","e").replace(
                        "\xc3\xa7","c").replace(
                        "\xc3\x94","O").replace(
                        "¯", "-").replace(
                        ".", " ").replace(
                        "_", " ").replace(
                        "|", " ").replace(
                        "ALACART", "A LA CARTE").replace(
                        "ALACARTE", "A LA CARTE").replace(
                        "A-LA-CARTE", "A LA CARTE").replace(
                        "&amp;","&").replace(
                        b64decode("W0NPTE9SIHJlZF0gTE9HQU4gVFZbL0NPTE9SXQ=="),"").replace(
                        "\r","")
        
        if NomRet.startswith("FR "): NomRet = NomRet[3:]
        while 1:
            if NomRet.startswith(' '):
                NomRet = NomRet[1:]
            else:
                break
        return NomRet.upper()

    def ConvText(self, Text):
        return Text.replace(
                        '\\/','/').replace(
                        '&amp;','&').replace(
                        '\xc9','E').replace(
                        '&#8211;', '-').replace(
                        '&#038;', '&').replace(
                        '&rsquo;','\'').replace(
                        '\r','').replace(
                        '\n','').replace(
                        '\t','').replace(
                        '&#039;',"'").replace(
                        '&quot;','"').replace(
                        '&gt;','>').replace(
                        '&lt;','<').replace(
                        '&nbsp;','')
    
    def CreerBouquet(self, CheminxAmAx):
        Bouquet=[]
        print "CreerBouquet: CheminxAmAx= "+CheminxAmAx
        dbxAmAx = os.path.join(CheminxAmAx, "xAmAx.db")
        try:
            DBxAmAx = db(dbxAmAx)
            DBxAmAx.Delete("UrlBouquet")
            DBxAmAx.CreerTable(Table="UrlBouquet", colonnes="`IDUrlB` INTEGER PRIMARY KEY AUTOINCREMENT,`IdBouquet` INTEGER,`IDChaine` INTEGER,`Url` TEXT,`NomAffichChaine` TEXT")
        
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
        M3uxAmAx = os.path.join(CheminxAmAx, "M3uTV.m3u")
        print "Ouverture de la Base de donnée xAmAx: "+dbxAmAx
        DBxAmAx = db(dbxAmAx)
        IdLP = 0

        liste = []
        """liste.append( ['Iptv4Sat',
                       "https://www.iptv4sat.com/category/france-m3u-iptv/",
                       '"https://www.iptv4sat.com/download-attachment/([^"]+)".+?class="attachment-caption">([^<]+)<',
                       '',
                       0,
                       False])"""
        
        liste.append( ['Iptv Gratuit',
                       'https://iptvgratuit.com/france/',
                       '<h2 class="entry-title"><a href="(.+?)" rel="bookmark">(.+?)</a>',
                       '<a class="more-link" title="(.+?)".+?href="(.+?)"',
                       1,
                       True])
        
        NbMaj=len(liste)

        self.MajDiv = 100/NbMaj
        self.TotMaj = 0
        self.dp = DialogProgress()
        sleep(0.5)
        self.dp.create("Telechargement de la liste de chaine:")
        sleep(0.5)
        NbMajEc = 1

        NbRecherche = 0
        print "Liste de chaine 1 a afficher"
        ListeEffacer = True
        DivisionRech = (self.MajDiv-self.TotMaj)
        TxtFinal = ""
        
        for Nom,Url,Re1,Re2,NumM3u,TelLien in liste:
            NbRecherche += 1
            if self.adn.getSetting(id="MajList"+str(NbRecherche))=="true":
                #log('\t[PLUGIN] xAmAx-Mod: Recherche Liste de chaine '+str(Nom), LOGNOTICE)
                print "Recherche Liste de chaine "+str(Nom)
                self.dp.update(self.TotMaj,"Recherche Liste de chaine "+str(NbRecherche))
                sleep(0.5)
                if Nom != "Iptv4Sat":
                    
                    Retour2,Erreur2 = self.ListTv(Url,Re1,Re2,NumM3u,TelLien,CheminxAmAx)
                    #log('\t[PLUGIN] xAmAx-Mod: Nombre de résultat de la Liste de chaine '+str(len(Retour2)), LOGNOTICE)
                    print "Nombre de résultat de la Liste de chaine "+str(len(Retour2))
                    if len(Retour2)>0 and Erreur2 == "OK":
                        log('\t[PLUGIN] xAmAx-Mod: Liste de chaine '+str(Retour2), LOGNOTICE)
                        try:
                            DBxAmAx.Delete(Table="List"+str(NbRecherche))
                        except:
                            pass
                        DBxAmAx.CreerTable(Table="List"+str(NbRecherche), colonnes="`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT")
                        for NomTv,UrlTV in Retour2:
                            IdLP += 1
                            DBxAmAx.Insert(Table="List"+str(NbRecherche),
                                           Colonnes="IDLP,Nom,Url",
                                           Valeurs=(IdLP,NomTv+" [COLOR gold]("+str(NbRecherche)+")[/COLOR]",UrlTV)) #+"&name="+NomTv))
                    elif Erreur2!="OK":
                        executebuiltin("XBMC.Notification(Mise à jour Liste TV "+str(NbRecherche)+" Impossible!!! ,"+Erreur2+",5000,'')")
                else:
                    Page = cDL().TelechargPage2(url=Url)
                    #print Page
                    try: part = re.compile(Re1, re.I+re.M+re.S).findall(self.ConvText(Page))
                    except: part = ''
                    #log('\t[PLUGIN] xAmAx-Mod: part = '+str(part), LOGNOTICE)
                    try: zip = 'https://www.iptv4sat.com/download-attachment/' + str(part[0][0][:-1]) #).group(1)
                    except: zip = ''
                    #Page = cDL().TelechargPage2(url=Url)
                    #log('\t[PLUGIN] xAmAx-Mod: page = '+self.ConvText(Page), LOGNOTICE)
                    try:
                        udata= os.path.join(CheminxAmAx, "Telecharg")
                        dest = os.path.join(udata, 'iptv4sat.zip')
                        if not os.path.exists(udata):
                            os.makedirs(udata)
                        cDL().TelechargementZip(zip,dest,DPAff=False,Nom="Téléchargement Liste 1")
                        #Page = cDL().TelechargPage2(url=Url)
                        #log('\t[PLUGIN] xAmAx-Mod: page = '+self.ConvText(Page), LOGNOTICE)
                        from resources.ziptools import ziptools
                        unzipper = ziptools()
                        unzipper.extract(dest,udata)
                    
                        os.remove(dest)
                        
                        dir = os.listdir(udata)
                    
                        for a in dir:
                            if a.endswith('.m3u'):
                                print "Ouverture de :"+os.path.join(udata, a)
                                with open(os.path.join(udata, a),'r') as fm3u:
                                    ListM3u = fm3u.read()
                                Retour3 = self.TabM3u(ListM3u, True, True)
                                os.remove(os.path.join(udata, a))
                                log('\t[PLUGIN] xAmAx-Mod: Nombre de résultat de la Liste de chaine '+str(len(Retour3)), LOGNOTICE)
                                #print "Nombre de résultat de la Liste de chaine "+str(len(Retour3))
                                if len(Retour3)>0:
                                    try:
                                        DBxAmAx.Delete(Table="List"+str(NbRecherche))
                                    except:
                                        pass
                                    DBxAmAx.CreerTable(Table="List"+str(NbRecherche), colonnes="`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT")
                                    for NomTv,UrlTV in Retour3:
                                        IdLP += 1
                                        DBxAmAx.Insert(Table="List"+str(NbRecherche),
                                                       Colonnes="IDLP,Nom,Url",
                                                       Valeurs=(IdLP,NomTv+" [COLOR gold]("+str(NbRecherche)+")[/COLOR]",UrlTV)) #+"&name="+NomTv))
                                else:
                                    executebuiltin("XBMC.Notification(Mise à jour Liste TV "+str(NbRecherche)+" Impossible!!! ,"+"Pas fichier dans la liste!"+",5000,'')")
                            else:
                                os.remove(os.path.join(udata, a))
                        
                    except:
                        executebuiltin("XBMC.Notification(Mise à jour Liste TV "+str(NbRecherche)+" Impossible!!! ,"+"Pas fichier dans la liste!"+", ,5000,'')")
            else:
                DBxAmAx.Delete(Table="List"+str(NbRecherche))
                DBxAmAx.CreerTable(Table="List"+str(NbRecherche), colonnes="`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT")
            DBxAmAx.FinEnregistrement()
            self.TotMaj = self.MajDiv*NbRecherche
            print "Telechargement de la liste de chaine:"+str(self.TotMaj)+"%"
        if NbRecherche<4:
            for i in range(NbRecherche+1,5):
                DBxAmAx.Delete(Table="List"+str(i))
                DBxAmAx.CreerTable(Table="List"+str(i), colonnes="`IDLP` INTEGER PRIMARY KEY AUTOINCREMENT, `Nom` TEXT, `Url` TEXT, `Entete` TEXT")
            DBxAmAx.FinEnregistrement()
        self.dp.update(100, "Nombre de résultat sur les "+str(NbRecherche)+" listes de chaines: "+str(IdLP))
        sleep(1)
        self.dp.close()
        executebuiltin("XBMC.Notification("+str(IdLP)+" Chaînes à jour,,,5000,'')")
        return "OK"

    def TabM3u(self,FichierTxt, F4m=False, cvNom=True,reComp='^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)\n',AjoutHttp="",AjoutFin=""):
        ret = []
        FichierTxt = FichierTxt.replace("\r","").replace("\t","").replace("\n\n\n\n","\n").replace("\n\n\n","\n").replace("\n\n","\n")
        #log('\t[PLUGIN] xAmAx-Mod: FichierTxt: '+FichierTxt, LOGNOTICE)
        TabM3u = re.compile(reComp, re.I+re.M+re.U+re.S).findall(FichierTxt)
        for Par, Nom , Url in TabM3u :
            if cvNom==True:
                Nom = self.ConvNom(Nom)
            if Url != "":
                Url=Url.split("|")[0].replace("\r", "")
                if F4m==True:
                    if (not ".m3u8" in Url):
                        Url='plugin://plugin.video.f4mTester/?url=%s&amp;streamtype=TSDOWNLOADER&name=%s'%(urlib.quote_plus(AjoutHttp+Url+AjoutFin),urlib.quote(Nom)) #&name=%s ,Nom
                    else:
                        Url='plugin://plugin.video.f4mTester/?url=%s&amp;streamtype=HLSRETRY&name=%s'%(urlib.quote_plus(AjoutHttp+Url+AjoutFin),urlib.quote(Nom)) #&name=%s ,Nom
                        
                DicM3u = (Nom,Url)
                ret.append(DicM3u)
        return ret

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
                    ret = self.TabM3u(M3u, F4m, cvNom)
        return ret

    def ListTv(self,Adress,Re1,Re2,NumM3u,TelLien,CheminxAmAx=""):
        Cmp=0
        ListeRet = []
        try:
            #print Adress
            ret2 = cDL().TelechargPage(url=Adress)
            #print ret2
            TabLien = re.compile(Re1, re.I+re.M+re.S).findall(self.ConvText(ret2))
            #log('\t[PLUGIN] xAmAx-Mod: TabLien '+str(len(TabLien)), LOGNOTICE)
            print TabLien
            TabLien2 = []
            for Url, Nom in TabLien:
                if (("France" in Nom)): # or ("French" in Nom)):
                    ret2 = cDL().TelechargPage(url=Url)
                    #print ret2
                    TabLien2 = re.compile(Re2, re.I+re.M+re.S).findall(self.ConvText(ret2))
                    break
            #log('\t[PLUGIN] xAmAx-Mod: TabLien2 '+str(TabLien2), LOGNOTICE)
            if len(TabLien2)>0:
                print str(TabLien2)
                if TelLien:
                    udata= os.path.join(CheminxAmAx, "Telecharg")
                    dest = os.path.join(udata, 'm3u.zip')
                    if not os.path.exists(udata):
                        os.makedirs(udata)
                    cDL().TelechargementZip(TabLien2[0][1],dest,DPAff=False,Nom="Téléchargement Liste")

                    from resources.ziptools import ziptools
                    unzipper = ziptools()
                    unzipper.extract(dest,udata)
                
                    os.remove(dest)
                    
                    dir = os.listdir(udata)
                
                    for a in dir:
                        if a.endswith('.m3u'):
                            log('\t[PLUGIN] xAmAx-Mod: Ouverture de :'+os.path.join(udata, a), LOGNOTICE)
                            print "Ouverture de :"+os.path.join(udata, a)
                            with open(os.path.join(udata, a),'r') as fm3u:
                                ListM3u = fm3u.read()
                            ListeRet = ListeRet + self.TabM3u(ListM3u, True, True)
                            #log('\t[PLUGIN] xAmAx-Mod: liste M3U '+str(ListeRet), LOGNOTICE)
                            os.remove(os.path.join(udata, a))
                    """else:
                        ret2 = cDL().TelechargPage(url=TabLien2[0][NumM3u])
                        print ret2
                        log('\t[PLUGIN] xAmAx-Mod: liste '+str(ret2), LOGNOTICE)
                        ListeRet = self.TabM3u(ret2, F4m=True, cvNom=True)"""
                else:
                    #print TabLien2[0]
                    ret2 = TabLien2[0].replace('<br />','')
                    ListeRet = self.TabM3u(ret2,
                                           F4m=True,
                                           cvNom=True,
                                           reComp='EXTINF.+?:-?[0-9]*(.*?),FR(.*?)http:(.*?).ts',
                                           AjoutHttp="http:",
                                           AjoutFin=".ts")
            #print str(TabLien2[0][1])
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
