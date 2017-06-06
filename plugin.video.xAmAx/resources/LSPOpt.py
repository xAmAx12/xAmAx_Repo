# -*- coding: utf-8 -*-
# Module: LSPOpt
# Author: xamax
# Created on: 29.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import os, re, sys
import xbmcvfs
import xbmcaddon
import xbmcgui
import xbmc
import urllib2 as urllib
import urllib as urlib
import base64
import sqlite3 as lite
import httplib
#import resources.utils as utils
try:
    import json
except:
    import simplejson as json

USER_AGENT = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

headers = {'User-Agent': USER_AGENT,
           'Accept': '*/*',
           'Connection': 'keep-alive'}

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

class cLiveSPOpt():
    nomPlugin = 'plugin.video.xAmAx'

    def __init__(self):
        self.addon = xbmcaddon.Addon(self.nomPlugin)

    def UrlADFLY(self, code):
        zero = ''
        un = ''
        for n,letter in enumerate(code):
            if n%2 == 0:
                zero += code[n]
            else:
                un =code[n] + un
        clef = zero + un
        xbmc.log("clef ADFLY: "+str(clef))
        clef = base64.b64decode(clef.encode("utf-8"))
        return clef[2:]

    def ConvNom(self, Nom):
        NomRet = str(Nom).upper().replace(
                        "[ FR ] ","").replace(
                        "[ FR: ] ","").replace(
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
                        "(SERVER 1)","").replace(
                        "*","").replace(
                        "'"," ").replace(
                        "=","").replace(
                        ">","").replace(
                        "/","").replace(
                        ":","").replace(
                        ","," ").replace(
                        "ê",'E').replace(
                        "é",'E').replace(
                        "è",'E').replace(
                        "ï", "I").replace(
                        "Ã",'A').replace(
                        "©","").replace(
                        "В","").replace(
                        "і","").replace(
                        "н","").replace(
                        "т","").replace(
                        "а","").replace(
                        "ж","").replace(
                        "’"," ").replace(
                        chr(160), "").replace(
                        "¨","")
        while 1:
            if NomRet.startswith(' '):
                NomRet = NomRet[1:]
            else:
                break
        return NomRet
    
    def CreerBouquet(self, CheminxAmAx):
        Bouquet=[]
        xbmc.log("CreerBouquet: CheminxAmAx= "+CheminxAmAx)
        dbxAmAx = os.path.join(CheminxAmAx, "resources", "xAmAx.db")
        try:
            xbmc.log("Ouverture de la Base de donnée xAmAx: "+dbxAmAx)
            NewDB = lite.connect(dbxAmAx)
            cBouq = NewDB.cursor()
            cChaine = NewDB.cursor()
            cUrl = NewDB.cursor()
            cListCh = NewDB.cursor()
            cBouq.execute("SELECT IDBouquet, TriDesChaines FROM Bouquet ORDER BY Ordre ASC;")
            xbmc.log("Enregistrement de tous les nouveaux Membres de la table...")
            cChaine.execute("DELETE FROM UrlBouquet;")
            IdUrlChaine = 0
            for IDBouqu, TriDesChaines in cBouq:
                #xbmc.log("SELECT IDChaineB, NomChaine, PasDansChaine FROM ChaineBouquet WHERE IDBouqChaine = "+str(IDBouqu)+" ORDER BY "+str(TriDesChaines)+";")
                cChaine.execute("SELECT IDChaineB, NomChaine, PasDansChaine FROM ChaineBouquet WHERE IDBouqChaine = " + str(IDBouqu)+" ORDER BY "+str(TriDesChaines)+";")
                for IDChaine, NomC, PasC in cChaine:
                    #xbmc.log("SELECT * FROM ListePrincipale WHERE Nom LIKE '%"+str(NomC).upper()+"%' ORDER BY Nom ASC;")
                    cListCh.execute("SELECT * FROM ListePrincipale WHERE Nom LIKE '%"+str(NomC).upper()+"%' ORDER BY Nom ASC;")
                    for IdLP, Nom, Url, Entete in cListCh:
                        EnrOk=True
                        if len(str(PasC))>0 and str(PasC).upper()!="NONE":
                            PasDansChaine = str(PasC).encode('utf-8').upper().split(",")
                            for Pas in PasDansChaine:
                                if Nom.upper().find(Pas)!=-1:
                                    EnrOk=False
                                    break
                        if EnrOk==True:
                            IdUrlChaine += 1
                            #xbmc.log('INSERT INTO UrlBouquet (IDUrlB,IdBouquet,IDChaine,Url,NomAffichChaine) VALUES (%s,%s,%s,%s,%s)'%(str(IdUrlChaine),str(IDBouqu),str(IDChaine),Url,Nom))
                            cUrl.execute('INSERT INTO UrlBouquet (IDUrlB,IdBouquet,IDChaine,Url,NomAffichChaine) VALUES (?,?,?,?,?)',(IdUrlChaine,IDBouqu,IDChaine,Url,Nom))
        except lite.Error as e:
            if NewDB:
                NewDB.rollback()
            xbmc.log("Erreur %s:" % e.args[0])
            return "Erreur de connection à la base xAmAx!"
            xbmc.log("Erreur de connection à la base xAmAx!")
            # raise e
        finally:
            try:
                if cBouq:
                    cBouq.close()
            except: pass
            try:
                if cChaine:
                    cChaine.close()
            except: pass
            try:
                if cUrl:
                    cUrl.close()
            except: pass
            try:
                if cListCh:
                    cListCh.close()
            except: pass
            try:
                if NewDB:
                    NewDB.commit()
                    NewDB.close()
            except: pass
        return "OK"
    
    def TelechargPage(self, url="", Entete=None, Post={}):

        cookie = urllib.HTTPCookieProcessor(None)
        opener = urllib.build_opener(cookie, urllib.HTTPBasicAuthHandler(), urllib.HTTPHandler())
        EnteteDansPage=None

        if '|' in url:
            url,EnteteDansPage=url.split('|')
        if len(Post)==0:
            req = urllib.Request(url,headers=hdr)
        else:
            data = urlib.urlencode(Post)
            req = urllib.Request(url,data,headers=hdr)
            
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
            xbmc.log("Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0]))
            return "Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0])

    def getHtml2(self, url, Post={}):
        if len(Post)>0:
            UrlPost = urlib.urlencode(Post)
            req = urllib.Request(url,data=UrlPost,headers=hdr)
        else:
            req = urllib.Request(url,headers=hdr)

        try:
            response = urllib.urlopen(req,timeout=60)
            page = response.read()
            response.close()
            return page
        except:
            print "Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0])
            return "Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0])

    def getHtml3(self, host, url, Post={}):
        headers = {'User-Agent': 'python',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        conn = httplib.HTTPSConnection(host)
        if len(Post)>0:
            values = Post
            values = urlib.urlencode(values)

            conn.request("POST", url, values, headers)

        try:
            response = conn.getresponse()
            data = response.read()
            print 'Response: ', response.status, response.reason
            print 'Data:'
            return data
        except:
            print "Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0])
            return "Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0])

    
    def RechercheChaine(self, CheminxAmAx):
        i=0
        j=0
        ListeEffacer = False
        dbxAmAx = os.path.join(CheminxAmAx, "resources", "xAmAx.db")
        xbmc.log("Ouverture de la Base de donnée xAmAx: "+dbxAmAx)
        NewDB = lite.connect(dbxAmAx)
        NewDB.text_factory = str
        cUrl = NewDB.cursor()
        IdLP = 0

        Majtv1=self.addon.getSetting(id="Majtv1")=="true"
        Majtv2=self.addon.getSetting(id="Majtv2")=="true"
        Majtv3=self.addon.getSetting(id="Majtv3")=="true"
        Majtv4=self.addon.getSetting(id="Majtv4")=="true"

        NbMaj=Majtv1+Majtv2+Majtv3+Majtv4
        
        if NbMaj>0:
            self.MajDiv = 100/NbMaj
            self.TotMaj = 0
            self.dp = xbmcgui.DialogProgress()
            self.dp.create("Telechargement de la liste de chaine:")
            NbMajEc = 0
            if Majtv1:
                NbMajEc += 1
                xbmc.log("Recherche Liste de chaine 1")
                self.dp.update(self.TotMaj,"Recherche Liste de chaine 1")
                Retour,Erreur = self.RechercheSources1()
                if len(Retour)>0 and Erreur=="":
                    xbmc.log("Liste de chaine 1 a afficher: "+str(len(Retour)))
                    cUrl.execute("DELETE FROM ListePrincipale;")
                    ListeEffacer = True
                    for Nom,Url in Retour:
                        IdLP += 1
                        while 1:
                            if Nom[:1]==" ":
                                Nom = Nom[1:]
                            else:
                                break
                        cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                    VALUES (?,?,?)''',(IdLP,Nom+" [COLOR gold](1)[/COLOR]",Url+"&name="+Nom))
                else:
                    if Erreur!="":
                        xbmc.executebuiltin("XBMC.Notification(Mise a jour Liste TV 1 Impossible!!! ,"+Erreur+",5000,"")")
                        #dialog = xbmcgui.Dialog()
                        #ok = dialog.ok("Mise a jour Liste TV 1 Impossible!!!", Erreur)
                self.TotMaj = self.MajDiv*NbMajEc
            xbmc.log("Telechargement de la liste de chaine:"+str(self.TotMaj)+"%")
            if Majtv2:
                NbMajEc += 1
                xbmc.log("Recherche Liste de chaine 2")
                NbDivSrc = 7
                self.TotMaj += self.MajDiv/NbDivSrc
                self.dp.update(self.TotMaj,"Recherche Liste de chaine 2")
                xbmc.sleep(50)
                Retour, Erreur2 = self.RechercheSources2()
                if Erreur2=="OK" and len(Retour)>0:
                    NbSouDivSrc = ((self.MajDiv-(self.MajDiv/NbDivSrc))/len(Retour))
                    for cNom,curl in Retour:
                        j+=1
                        self.TotMaj += NbSouDivSrc
                        self.dp.update(self.TotMaj)
                        xbmc.sleep(50)
                        if cNom.capitalize().startswith('S4'): #cNom.capitalize().startswith('S1') or cNom.capitalize().startswith('S2') or 
                            i+=1
                            xbmc.log("Adresse chaineTV: "+cNom+" "+curl)
                            Retour2,Erreur2=self.RechercheChaines2(url=[curl])
                            xbmc.log("Liste de chaine 2 a afficher: "+str(len(Retour2)))
                            xbmc.log("Liste de chaine 2 Erreur: "+Erreur2)
                            if len(Retour2)>0 and Retour2!=[]:
                                for Nom,Url,Entete in Retour2:
                                    IdLP += 1
                                    if Entete!="":
                                        Url=Url+"|"+Entete
                                    while 1:
                                        if Nom[:1]==" ":
                                            Nom = Nom[1:]
                                        else:
                                            break
                                    if ListeEffacer == False:
                                        cUrl.execute("DELETE FROM ListePrincipale;")
                                        ListeEffacer = True
                                    cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                                VALUES (?,?,?)''',(IdLP,
                                                                   Nom+" [COLOR gold](2)[/COLOR]",
                                                                   'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER&name=%s'%(urlib.quote_plus(Url),Nom)))
                else:
                    xbmc.executebuiltin("XBMC.Notification(Mise a jour Liste TV 2 Impossible!!! ,"+Erreur2+",5000,"")")
                xbmc.sleep(100)
                self.TotMaj = self.MajDiv*NbMajEc
                xbmc.log("Telechargement de la liste de chaine:"+str(self.TotMaj)+"%")
            if Majtv3:
                self.TotMaj = self.MajDiv*NbMajEc
                self.dp.update(self.TotMaj,"Recherche Liste de chaine 3")
                NbMajEc += 1
                xbmc.log("Recherche Liste de chaine 3")
                Retour3, Erreur3 = self.RechercheSources3()
                if Erreur3=="OK":
                    if len(Retour3)>0 and Retour3!=[]:
                        xbmc.log("Liste de chaine 3 a afficher: "+str(len(Retour3)))
                        for Nom,Url in Retour3:
                            IdLP += 1
                            while 1:
                                if Nom[:1]==" ":
                                    Nom = Nom[1:]
                                else:
                                    break
                            if ListeEffacer == False:
                                cUrl.execute("DELETE FROM ListePrincipale;")
                                ListeEffacer = True
                            if Url.endswith(".ts"):
                                cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                        VALUES (?,?,?)''',(IdLP,
                                                           Nom+" [COLOR gold](3)[/COLOR]",
                                                           'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER&name=%s'%(urlib.quote_plus(Url),Nom)))
                            else:
                                cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                        VALUES (?,?,?)''',(IdLP,
                                                           Nom+" [COLOR gold](3)[/COLOR]",
                                                           'plugin://plugin.video.f4mTester/?url=%s'%(urlib.quote_plus(Url))))
                else:
                    xbmc.executebuiltin("XBMC.Notification(Mise a jour Liste TV 3 Impossible!!! ,"+Erreur3+",5000,"")")
                self.TotMaj = self.MajDiv*NbMajEc
                self.dp.update(self.TotMaj)
                xbmc.sleep(50)
                xbmc.log("Telechargement de la liste de chaine:"+str(self.TotMaj)+"%")
            if Majtv4:
                self.dp.update(self.TotMaj,"Recherche Liste de chaine 4")
                xbmc.sleep(50)
                NbMajEc += 1
                xbmc.log("Recherche Liste de chaine 4")
                Retour4, Erreur4 = self.RechercheSources4()
                if Erreur4=="OK":
                    if len(Retour4)>0 and Retour4!=[]:
                        xbmc.log("Liste de chaine 4 a afficher: "+str(len(Retour4)))
                        for Nom,Url in Retour4:
                            IdLP += 1
                            while 1:
                                if Nom[:1]==" ":
                                    Nom = Nom[1:]
                                else:
                                    break
                            if ListeEffacer == False:
                                cUrl.execute("DELETE FROM ListePrincipale;")
                                ListeEffacer = True
                                Nom=self.ConvNom(Nom)
                            cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                        VALUES (?,?,?)''',(IdLP,
                                                           Nom+" [COLOR gold](4)[/COLOR]",
                                                           'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER&name=%s'%(urlib.quote_plus(Url),Nom)))
                else:
                    xbmc.executebuiltin("XBMC.Notification(Mise a jour Liste TV 4 Impossible!!! ,"+Erreur4+",5000,"")")
                self.TotMaj = self.MajDiv*NbMajEc
                self.dp.update(self.TotMaj)
                xbmc.log("Telechargement de la liste de chaine:"+str(self.TotMaj)+"%")
                xbmc.sleep(50)

        if 1==2:
            xbmc.log("Recherche Liste de chaine 5")
            Retour5, Erreur5 = self.RechercheSources5()
            if Erreur5=="OK":
                if len(Retour5)>0 and Retour5!=[]:
                    xbmc.log("Liste de chaine 5 a afficher: "+str(len(Retour5)))
                    for Nom,Url,icon,cat in Retour5:
                        IdLP += 1
                        while 1:
                            if Nom[:1]==" ":
                                Nom = Nom[1:]
                            else:
                                break
                        if ListeEffacer == False:
                            cUrl.execute("DELETE FROM ListePrincipale;")
                            ListeEffacer = True
                            Nom=self.ConvNom(Nom)
                        cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                    VALUES (?,?,?)''',(IdLP,
                                                       Nom+" [COLOR gold](5)[/COLOR]",
                                                       'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER&name=%s'%(urlib.quote_plus(Url),Nom)))

            else:
                xbmc.executebuiltin("XBMC.Notification(Mise a jour Liste TV 5 Impossible!!! ,"+Erreur5+",5000,"")")
            
        try:
            if cUrl:
                cUrl.close()
        except: pass
        try:
            if NewDB:
                NewDB.commit()
                NewDB.close()
        except: pass
        xbmc.sleep(1000)
        self.dp.close()
        return "OK"

    def RechercheSources1(self):
        ListeChaine=[]
        try:
            xbmc.log("Recherche de la liste de chaine...")
            NbDivSrc = 7
            self.TotMaj += self.MajDiv/NbDivSrc
            self.dp.update(self.TotMaj,"Recherche Liste de chaine 1")
            xbmc.sleep(50)
            essai = str(self.TelechargPage("http://redeneobux.com/fr/updated-kodi-iptv-m3u-playlist/"))
            essai2 = essai.split("France IPTV")[1].split("location.href=\'")[1].split("\';")[0]
            self.TotMaj += self.MajDiv/NbDivSrc
            self.dp.update(self.TotMaj)
            xbmc.sleep(50)
            
            essai = str(self.TelechargPage(essai2))
            essai2 = essai.split("http://adf.ly/")[1].split(" ")[0]
            self.TotMaj += self.MajDiv/NbDivSrc
            self.dp.update(self.TotMaj,"Recherche Liste de chaine 1")
            xbmc.sleep(50)

            url = "http://adf.ly/"+essai2
            xbmc.log(" [+] Connection a ADFLY. . . "+url)
            adfly_data = str(self.TelechargPage(url))#str(urllib.urlopen(url).read())#.decode('utf-8'))
            if not('#EXTM3U' in adfly_data):
                self.TotMaj += self.MajDiv/NbDivSrc
                self.dp.update(self.TotMaj,"Recherche Liste de chaine 1")
                
                xbmc.log(" [+] Recherche adresse du téléchargement . . .")
                ysmm = adfly_data.replace("ysmm =","ysmm=").split("ysmm=")[1].replace('"',"'").split("'")[1]
                xbmc.log(" [+] Décodage de l'adresse . . ." + str(ysmm))
                essai2 = str(self.UrlADFLY(str(ysmm)))
                self.TotMaj += self.MajDiv/NbDivSrc
                self.dp.update(self.TotMaj)
                xbmc.sleep(50)
                
                xbmc.log("\n ### L'adresse du fichier : " + essai2.replace("b'",'').replace("'",''))
                essai = str(self.TelechargPage(essai2.replace("b'",'').replace("'",'')))
            else:
                essai = adfly_data
            
            self.TotMaj += self.MajDiv/NbDivSrc
            self.dp.update(self.TotMaj)
            xbmc.sleep(50)
            
            ListeChaine=[]
            Chaine = essai.split("#EXTINF:-1,")
            for Ch in Chaine:
                InfoChaine = str(Ch).replace('\r','').split(chr(10))
                if len(InfoChaine) > 1:
                    Nom =InfoChaine[0]
                    if InfoChaine[1]!="" and not Nom.startswith("***")and not Nom.startswith("+++")and not Nom.startswith("---")and not Nom.startswith("==="):
                        ListeChaine.append((self.ConvNom(Nom),InfoChaine[1]))
                        
            self.TotMaj += self.MajDiv/NbDivSrc
            self.dp.update(self.TotMaj)
            xbmc.sleep(50)
            return ListeChaine, ""
        except:
            xbmc.log("Erreur téléchargement liste 1: "+str(sys.exc_info()[0]))
            return ListeChaine, "Erreur téléchargement liste 1: "+str(sys.exc_info()[0])
    
    def RechercheSources2(self):
        ret=[]
        Retour=self.TelechargPage(url="http://pastebin.com/raw/GrYKMHrF")
        if not Retour.startswith("Erreur"):
            Retour=Retour.splitlines()
            for R in Retour:
                try:
                    if not R.startswith("---") and len(R)>0:
                        servername,surl=R.split('$')
                        ret.append((servername, surl ))
                except:
                    pass
            return ret, "OK"
        else:
            return ret, Retour

    def RechercheChaines2(self,url,Essai=False):
        ret=[]
        Erreur = "OK"
        try:
            for u in url:
                EnteteFichier,EnteteLecture=None,""
                if '|' in u:
                    u,EnteteFichier,EnteteLecture=u.split('|')
                    u=u+'|'+EnteteFichier
                    EnteteDansPage=EnteteLecture.split('&')
                    Entete=[]
                    for h in EnteteDansPage:
                        if len(h.split('='))==2:
                            n,v=h.split('=')
                        else:
                            vals=h.split('=')
                            n=vals[0]
                            v='='.join(vals[1:])
                            #n,v=h.split('=')
                        print n,v
                        if n=="User-Agent" and v.startswith('http'):
                            v=self.TelechargPage(url=v)
                            print "v= "+ v #)xbmc.log(
                        Entete.append((n,v))
                    EnteteLecture=str(urlib.urlencode(Entete))

                html=self.TelechargPage(url=u.replace("[gettext]","")).replace(chr(13),"")
                if html!="Erreur...":
                    if Essai:
                        print html
                    if "https://pastebin" in html:
                        html=self.TelechargPage(url=html).replace(chr(13),"")
                    if "http://" in html:
                        html=self.TelechargPage(url=html).replace(chr(13),"")
                    if html=="Erreur...":
                        return ret, "Erreur: "+str(sys.exc_info()[0])
                    TabM3u = re.compile('^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)\n', re.I+re.M+re.U+re.S).findall(html)
                    for Par , Nom , Url in TabM3u :
                        Nom = Nom.replace(' :', ':').replace(' |', ':').replace('\r','').upper()
                        if (('FR:'in Nom) or ("[ FR ]" in Nom) or ("[ FR: ]" in Nom)):
                            try:
                                cNom=self.ConvNom(Nom)
                                
                                curl=Url.replace('\r','').replace('.m3u8','.ts')
                                if str(EnteteLecture)!="":
                                    Retour = "ok"
                                else:
                                    EnteteLecture="" #'User-Agent=VLC/2.2.1 LibVLC/2.2.17&Icy-MetaData=1'
                                #print "EnteteLecture= "+str(EnteteLecture) #)xbmc.log(
                                ret.append((cNom, curl, EnteteLecture))
                            except:
                                if Essai:
                                    print '### Erreur '+ str(sys.exc_info()[0])
                    if len(ret)>0:
                        ret=sorted(ret,key=lambda s: s[0].lower())
            return ret, Erreur
        except:
            return ret, "Erreur: "+str(sys.exc_info()[0])
    
    def RechercheSources3(self, Essai = False):
        
        #url = 'https://www.oneplaylist.space/database/export'
        #SourcesListe = self.TelechargPage(url=url,Post={'kategorija' : '3'})#urllib.urlopen(req).read()


        host = 'www.oneplaylist.space'
        url = '/database/export'
        SourcesListe = self.getHtml3(host,url,{'kategorija' : '3'})

        ListeM3u = SourcesListe.split("#EXTM3U")
        ret=[]
        NbAdresse = 0
        NbAdresse2 = 0
        if len(ListeM3u)>1:
            ListeM3u = ListeM3u[1].split("</div>")
            if len(ListeM3u)>0:
                ListeM3u = ListeM3u[0].split("#EXTINF:0, ")
                #print str(ListeM3u)
                for NomAdresse in ListeM3u:
                    TabNomAdresse = NomAdresse.split("<br/>")
                    Nom = TabNomAdresse[0]
                    Adresse = TabNomAdresse[1]
                    if Adresse!="" and not Adresse.startswith("rtmp:") and "type=m3u" in Adresse:
                        #print str(Nom)+"="+str(Adresse)
                        Retour3,Erreur3 = self.RechercheChaines3(Nom=str(Nom), Url=str(Adresse),Essai=Essai)
                        if Erreur3 == "OK" and len(Retour3)>0:
                            for Nom,Url in Retour3:
                                ret.append((Nom,Url))
                                NbAdresse += 1
                    elif Adresse.endswith(".ts") or Adresse.endswith(".m3u8"):
                        ret.append((self.ConvNom(Nom),Adresse.replace(".m3u8",".ts")))
                        NbAdresse2 += 1
                if Essai:
                    print "Liste directe: "+str(NbAdresse2)+" Liste déporté: "+str(NbAdresse)+" Liste complette: "+str(ret)
            if NbAdresse>0 or NbAdresse2>0:
                return ret, "OK"
            else:
                ret.append(("Erreur","Pas de Chaines dans la liste 3!"))
                return ret, "Pas de Chaines dans la liste 3!"
        else:
            return ret, "Pas de Chaines dans la liste 3!"

    def RechercheChaines3(self, Nom, Url, Essai = False):
        ListeM3u2=[]
        Ret3=""
        try:
            xbmc.log("Nom Source 3: "+Nom+" Url: "+Url)
            if Nom=="Arab FR, DE, UK":
                Ret3 = self.TelechargPage(url=Url)
                ListeM3u2 = Ret3.replace(chr(13),"").split('#EXTINF:-1,FR_')
            elif Nom=="France IPTV":
                Retour = self.TelechargPage(url=Url)
                ListeM3u2 = Retour.replace(chr(13),"").split('#EXTINF:-1,')
            elif Nom == "Mix World":
                Retour = self.TelechargPage(url=Url)
                ListeM3u2 = Retour.replace(chr(13),"").split('#EXTINF:-1,FR:')
            elif Nom == "France, World IPTV":
                Retour = self.TelechargPage(url=Url)
                ListeM3u2 = Retour.replace(chr(13),"").split('#EXTINF:-1,=====_Swiss')[0].split('#EXTINF:-1,')
            else:
                if Essai==True:
                    Ret3 = "" #self.TelechargPage(url=Url)
                else:
                    Ret3 = ""
                #print Nom+"="+str(Retour)
            if len(ListeM3u2)>0:
                ret=[]
                NbAdresse = 0
                for NomAdresse in ListeM3u2:
                    TabNomAdresse = NomAdresse.split(chr(10))
                    Nom = TabNomAdresse[0]
                    Adresse = TabNomAdresse[1]
                    if Adresse!="" and not Adresse.startswith("rtmp:")and not(
                        "#EXTM3U" in Nom) and not(
                        Nom.startswith("***"))and not(
                        Nom.startswith("+++"))and not(
                        Nom.startswith("---"))and not(
                        Nom.startswith("===")):
                        #print str(Nom)+"="+str(Adresse)
                        ret.append((self.ConvNom(Nom), str(Adresse)))
                        NbAdresse += 1
                if Essai: print str(NbAdresse)
                return ret, "OK"
            else:
                return [], Ret3
        except:
            return [], "Erreur Mise à jour Liste TV 3: "+"\n Erreur = "+str(sys.exc_info()[0])
        
    def RechercheSources4(self):
        ret = []
        try:
            html = self.TelechargPage(url="https://sourcetv.info/category/europe-iptv/france-iptv/")
            div = html.split('<div class="main-loop-inner">')
            if len(div)>0:
                div2 = div[1].split('<div class="panel-wrapper"><div class="panel">')
                for listTxt in div2:
                        div3 = listTxt.split('</div></div></div><br class="clearer" />')
                        if len(div3)>0:
                            Url0 = div3[0].split('<a href="')
                            if len(Url0)>1:
                                Url1 = Url0[1].split('"')
                                if len(Url1)>0:
                                    Url = Url1[0]
                                    NomAddrss = div3[0].split('title="')[1].split('"')[0]
                                    if "France" in NomAddrss:
                                        html = self.TelechargPage(url=Url)
                                        div3 = html.split('<pre class="alt2"')
                                        if len(div3)>0:
                                            div3 = div3[1].split("> ")
                                            if len(div3)>1:
                                                m3u = div3[1].split("</pre")[0]
                                                TabM3u = re.compile('^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)\n', re.I+re.M+re.U+re.S).findall(m3u)
                                                for Par , Nom2 , Url in TabM3u :
                                                    Nom2 = Nom2.replace(' :', ':').replace(' |', ':').replace('\r','').upper()
                                                    try:
                                                        cNom=self.ConvNom(Nom2)
                                                        curl=Url.replace('\r','').replace('.m3u8','.ts')
                                                        Ret2 = "ok"
                                                        #print "EnteteLecture= "+str(EnteteLecture) #)xbmc.log(
                                                        ret.append((cNom, curl))
                                                    except:
                                                        return ret, "Erreur Mise à jour Liste TV 4: "+"\n Erreur = "+str(sys.exc_info()[0])
                                                if len(ret)>0:
                                                    ret=sorted(ret,key=lambda s: s[0].lower())
                                        if len(ret)>0: break
            return ret, "OK"
        except: return ret, "Erreur Mise à jour Liste TV 4: "+"\n Erreur = "+str(sys.exc_info()[0])
        
    def RechercheSources5(self):
        try:
            ListeM3u = []
            M3u = str(self.TelechargPage(url="https://raw.githubusercontent.com/Jaguar868/cars/master/lists/roku.txt"))
            if not M3u.startswith('Erreur'):
                TabM3u = re.compile('^#.+?:-?[0-9]*(.*?), (.*?)\nlogo=(.*?) stream=(.*?) cat=(.*?)\n', re.I+re.M+re.U+re.S).findall(M3u)
                for Par , Nom , icon, Url, cat in TabM3u :
                    Nom = Nom.replace(' :', ':').replace(' |', ':').replace('\r','').upper()
                    if 'FRENCH' in Nom:
                        DicM3u = (Nom,Url.replace('\n', '').replace('\r', ''),icon,cat)
                        ListeM3u.append(DicM3u)
                return ListeM3u, "OK"
            else:
                return [], M3u
        except:
            return [], "Erreur Mise à jour Liste TV 5: "+"\n Erreur = "+str(sys.exc_info()[0])

    def LireM3u(self, CheminxAmAx, F4m=False, cvNom=True):
        xbmc.log("Liste de chaine M3u")
        dialog = xbmcgui.Dialog()
        fn = dialog.browse(1, 'Ouvrir le fichier M3u', 'files', '.m3u|.m3u8', False, False, 'special://home')
        ret = []
        if fn != False and fn != "":
            if xbmcvfs.exists(fn):
                f = xbmcvfs.File(fn)
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
        xbmc.log("Recherche de la liste de chaine...")
        Page = str(self.TelechargPage(url=Url))
        ret = []
        if not Page.startswith("Erreur"):
            match = re.compile('thumb-list(.*?)<ul class="right pagination">', re.DOTALL | re.IGNORECASE).findall(Page)
            #xbmc.log("Resulta 1 tri: "+str(match))
            match1 = re.compile(r'<li class="[^"]*">\s<a class="thumbnail" href="([^"]+)">\n<script.+?([^;]+);</script>\n<figure>\n<img  id=".+?" src="([^"]+)".+?/>\n<figcaption>\n<span class="video-icon"><i class="fa fa-play"></i></span>\n<span class="duration"><i class="fa fa-clock-o"></i>([^<]+)</span>\n(.+?)\n',
                                re.DOTALL | re.IGNORECASE).findall(match[0])
            for url, Timage, image, Temp, Descript in match1:
                ret.append((url,"https:"+image, Timage.split("(")[1][:-1].replace("'","").split(","),Descript+" "+Temp))
            xbmc.log("Recherche OK...")
            try:
                nextp=re.compile(r'<li class="arrow"><a href="(.+?)">suivant</li>').findall(Page)
                ret.append(('https://www.mrsexe.com' + nextp[0],"",[],"Page Suivante..."))
            except: pass
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok("Telechargement impossible...", Page)
        return ret
