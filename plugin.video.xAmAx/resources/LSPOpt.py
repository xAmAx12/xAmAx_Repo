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
try:
    import json
except:
    import simplejson as json

class cLiveSPOpt():

    LiveStream = None
    CheminLive = ""
    SourceFile = ""
    nomPlugin = 'plugin.video.xAmAx'
    addon = xbmcaddon.Addon(nomPlugin)

    def __init__(self):
        try:
            self.LiveStream  = xbmcaddon.Addon('plugin.video.vstream')
            self.CheminLive=str(xbmc.translatePath(self.vStream.getAddonInfo('profile').decode('utf-8')))
            if not os.path.isdir(self.CheminLive):
                xbmc.log("Chemin LiveStreamPro creer: " + self.CheminLive)
                xbmcvfs.mkdirs(self.CheminLive)
        except:
            pass

    def TryConnectLiveStream(self):
        try:
            xbmc.log("TryConnectLiveStream")
            self.LiveStream  = xbmcaddon.Addon('plugin.video.live.streamspro')
            self.CheminLive = str(xbmc.translatePath(self.LiveStream.getAddonInfo('profile').decode('utf-8')))
            xbmc.log("Chemin LiveStreamPro: " + self.CheminLive)
            self.SourceFile = str(os.path.join(self.CheminLive, 'source_file'))
            return "OK"
        except:
            return "LiveStreamPro non installer!"

    def EffaceFich(self):
        try:
            with open(os.path.join(self.CheminLive,'listeTV.m3u')) as f:
                pass
            f.closed
            os.remove(os.path.join(self.CheminLive,'listeTV.m3u'))
        except IOError:
            pass

    def Crack(self, code):
        zeros = ''
        ones = ''
        for n,letter in enumerate(code):
            if n%2 == 0:
                zeros += code[n]
            else:
                ones =code[n] + ones
        key = zeros + ones
        xbmc.log("Key ADFLY: "+str(key))
        key = base64.b64decode(key.encode("utf-8"))
        return key[2:]

    def ConvNom(self, Nom):
        return Nom.upper().replace(
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
                        "\r", "")
    
        
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
            req = urllib.Request(url)
        else:
            data = urlib.urlencode(Post)
            req = urllib.Request(url,data)
            
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
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
            if response.info().get('Content-Encoding') == 'gzip':
                    from StringIO import StringIO
                    import gzip
                    Tempon = StringIO( response.read())
                    f = gzip.GzipFile(fileobj=Tempon)
                    FichTelecharg = f.read()
            else:
                FichTelecharg=response.read()
            response.close()
            return FichTelecharg;
        except:
            xbmc.log("Erreur téléchargement Page: "+str(url)+"\n Erreur = "+str(sys.exc_info()[0]))
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
        if self.addon.getSetting(id="Majtv1")=="true":
            xbmc.log("Recherche Liste de chaine 1")
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
                                VALUES (?,?,?)''',(IdLP,Nom+" [COLOR gold](1)[/COLOR]",Url))
            else:
                if Erreur!="":
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok("Mise a jour Liste TV 1 Impossible!!!", Erreur)
                    
        if self.addon.getSetting(id="Majtv2")=="true":
            xbmc.log("Recherche Liste de chaine 2")
            dp = xbmcgui.DialogProgress()
            dp.create("Telechargement de la liste de chaine:","Recherche de la liste de chaine 2...")
            Retour, Erreur2 = self.RechercheSources2()
            if Erreur2=="OK":
                for cNom,curl in Retour:
                    j+=1
                    dp.update(j*(100/len(Retour)))
                    if cNom.capitalize().startswith('S1'):
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
                                                               'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER'%(urlib.quote_plus(Url))))
                            dp.update(100,"Liste de chaine tv 2 a jour!")
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok("Mise a jour Liste TV 2 Impossible!!!", Erreur2)
            xbmc.sleep(1000)
            dp.close()
                
        if self.addon.getSetting(id="Majtv3")=="true":
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
                        cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                    VALUES (?,?,?)''',(IdLP,
                                                       Nom+" [COLOR gold](3)[/COLOR]",
                                                       'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER'%(urlib.quote_plus(Url))))
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok("Mise a jour Liste TV 3 Impossible!!!", Erreur3)

        if self.addon.getSetting(id="Majtv4")=="true":
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
                        cUrl.execute('''INSERT INTO ListePrincipale (IDLP,Nom,Url)
                                    VALUES (?,?,?)''',(IdLP,
                                                       self.ConvNom(Nom)+" [COLOR gold](4)[/COLOR]",
                                                       'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER'%(urlib.quote_plus(Url))))
            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok("Mise a jour Liste TV 4 Impossible!!!", Erreur4)

        if 1==2:
            xbmc.log("Recherche Liste de chaine 5")
            Retour5, Erreur5 = self.RechercheSources5()
            if Erreur5=="OK":
                if len(Retour5)>0 and Retour5!=[]:
                    xbmc.log("Liste de chaine 5 a afficher: "+str(len(Retour5)))
                    for Nom,Url in Retour5:
                        IdLP += 1
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
                                                       self.ConvNom(Nom)+" [COLOR gold](5)[/COLOR]",
                                                       'plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER'%(urlib.quote_plus(Url))))

            else:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok("Mise a jour Liste TV 5 Impossible!!!", Erreur5)
            
        try:
            if cUrl:
                cUrl.close()
        except: pass
        try:
            if NewDB:
                NewDB.commit()
                NewDB.close()
        except: pass
        
        return "OK"

    def RechercheSources1(self):
        ListeChaine=[]
        try:
            xbmc.log("Recherche de la liste de chaine...")
            dp = xbmcgui.DialogProgress()
            dp.create("Telechargement de la liste de chaine:","Recherche de la liste de chaine...")
            dp.update(10)
            essai = str(self.TelechargPage(url="http://redeneobux.com/fr/updated-kodi-iptv-m3u-playlist/"))
            essai2 = essai.split("France IPTV")[1].split("location.href=\'")[1].split("\';")[0]
            dp.update(20,"Page Internet France IPTV...")
            
            essai = str(self.TelechargPage(url=essai2))
            essai2 = essai.split("http://adf.ly/")[1].split(" ")[0]
            dp.update(30,"Recherche Adresse ADFLY...")

            url = "http://adf.ly/"+essai2
            xbmc.log(" [+] Connection a ADFLY. . . "+url)
            adfly_data = str(self.TelechargPage(url=url))#str(urllib.urlopen(url).read())#.decode('utf-8'))
            if not('#EXTM3U' in adfly_data):
                dp.update(40,"Décodage de l'adresse . . .")
                
                xbmc.log(" [+] Recherche adresse du téléchargement . . .")
                ysmm = adfly_data.split("ysmm = ")[1].split("'")[1].split("';")[0]
                xbmc.log(" [+] Décodage de l'adresse . . ." + str(ysmm))
                essai2 = str(self.Crack(str(ysmm)))
                dp.update(50,"Adresse du fichier Trouvée..")
                
                xbmc.log("\n ### L'adresse du fichier : " + essai2.replace("b'",'').replace("'",''))
                essai = str(self.TelechargPage(url=essai2.replace("b'",'').replace("'",'')))
            else:
                essai = adfly_data
            
            dp.update(70,"Enregistrement de la liste de chaine...")
            
            ListeChaine=[]
            Chaine = essai.split("#EXTINF:-1,")
            for Ch in Chaine:
                InfoChaine = str(Ch).replace('\r','').split(chr(10))
                if len(InfoChaine) > 1:
                    Nom =InfoChaine[0]
                    if InfoChaine[1]!="" and not Nom.startswith("***")and not Nom.startswith("+++")and not Nom.startswith("---")and not Nom.startswith("==="):
                        ListeChaine.append((self.ConvNom(Nom),InfoChaine[1]))
                        
            dp.update(100,"Fichier télécharger!")
            xbmc.sleep(1000)
            dp.close()
            xbmc.sleep(1000)
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

                print "u= "+ u #)xbmc.log(
                html=self.TelechargPage(url=u).replace(chr(13),"")
                if html!="Erreur...":
                    if Essai:
                        print html
                    TabM3u = re.compile('^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)\n', re.I+re.M+re.U+re.S).findall(html)
                    for Par , Nom , Url in TabM3u :
                        Nom = Nom.replace(' :', ':').replace(' |', ':').replace('\r','').upper()
                        if Nom.startswith('FR:'):
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
        
        url = 'http://www.oneplaylist.space/database/export/'
        SourcesListe = self.TelechargPage(url=url,Post={'kategorija' : '3'})#urllib.urlopen(req).read()

        ListeM3u = SourcesListe.split("#EXTM3U")[1].split("</div>")[0].split("#EXTINF:0, ")
        #print str(ListeM3u)
        ret=[]
        NbAdresse = 0
        for NomAdresse in ListeM3u:
            TabNomAdresse = NomAdresse.split("<br/>")
            Nom = TabNomAdresse[0]
            Adresse = TabNomAdresse[1]
            if Adresse!="" and not Adresse.startswith("rtmp:") and "type=m3u" in Adresse:
                #print str(Nom)+"="+str(Adresse)
                Retour,Erreur = self.RechercheChaines3(Nom=str(Nom), Url=str(Adresse),Essai=Essai)
                if Erreur == "OK" and len(Retour)>0:
                    for Nom,Url in Retour:
                        ret.append((Nom,Url))
                        NbAdresse += 1
        if NbAdresse>0:
            return ret, "OK"
        else:
            return ret, "Pas de Chaines dans la liste 3!"

    def RechercheChaines3(self, Nom, Url, Essai = False):
        ListeM3u=[]
        try:
            #print str(Retour)
            if Nom == "Africa + mix":
                Retour = self.TelechargPage(url=Url)
                ListeM3u = Retour.replace(chr(13),"").split('#EXTINF:-1 group-title="French",')
                
            elif Nom=="FR IT" or Nom=="FR, IT" or Nom=="French, IT":
                Retour = self.TelechargPage(url=Url)
                ListeM3u = Retour.replace(chr(13),"").split('#EXTINF:-1,------IT')[0].split("#EXTINF:-1,")
            elif Nom=="Arab FR, DE, UK":
                Retour = TelechargPage(url=Url)
                ListeM3u = Retour.replace(chr(13),"").split('#EXTINF:-1,FR_')
            else:
                if Essai==True:
                    Retour = self.TelechargPage(url=Url)
                else:
                    Retour = ""
                #print Nom+"="+str(Retour)
                
            if len(ListeM3u)>0:
                ret=[]
                NbAdresse = 0
                for NomAdresse in ListeM3u:
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
                print str(NbAdresse)
                return ret, "OK"
            else:
                return [], Retour
        except:
            return [], "Erreur Mise à jour Liste TV 3: "+"\n Erreur = "+str(sys.exc_info()[0])
        
    def RechercheSources4(self):
        try:
            UserAgent = self.TelechargPage(url=self.TelechargPage(url="https://raw.githubusercontent.com/catoalkodi/repository.catoal/master/plugin.video.catoaliptv/resources/Blue/logo.png"))
            if not UserAgent.startswith('Erreur'):
                ListeM3u = self.TelechargPage(url="https://raw.githubusercontent.com/catoalkodi/repository.catoal/master/plugin.video.catoaliptv/resources/Blue/logo2.png")
                M3u = self.TelechargPage(url=ListeM3u)
                if not M3u.startswith('Erreur'):
                    TabM3u = re.compile('^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)\n', re.I+re.M+re.U+re.S).findall(M3u)
                    ret = []
                    for Par , Nom , Url in TabM3u :
                        Nom = Nom.replace(' :', ':').replace(' |', ':').replace('\r','').upper()
                        if Nom.startswith('FR:'):
                            DicM3u = (self.ConvNom(Nom),Url.replace('\n', '').replace('\r', '')+'|User-Agent='+UserAgent)
                            ret.append(DicM3u)
                    return ret, "OK"
                else:
                    return [], "M3u: "+UserAgent
            else:
                return [], "User agent: "+UserAgent
        except:
            return [], "Erreur Mise à jour Liste TV 4: "+"\n Erreur = "+str(sys.exc_info()[0])

    def RechercheSources5(self):
        #try:
        M3u = self.TelechargPage(url="https://raw.githubusercontent.com/quoc66/IfreemanWeb/master/Fr%20main")
        if not M3u.startswith('Erreur'):
            TabM3u = re.compile('^#.+?:-?[0-9]*(.*?),(.*?)\n(.*?)\n', re.I+re.M+re.U+re.S).findall(M3u)
            ret = []
            for Par, Nom , Url in TabM3u :
                Nom = self.ConvNom(Nom)
                DicM3u = (Nom,Url.split("|")[0].replace(".m3u8",".ts"))
                ret.append(DicM3u)
            return ret, "OK"
        else:
            return [], "M3u: "+M3u
        #except:
            #return [], "Erreur Mise à jour Liste TV 5: "+"\n Erreur = "+str(sys.exc_info()[0])

    def LireM3u(self, CheminxAmAx, F4m=False):
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
                        Nom = self.ConvNom(Nom)
                        if F4m==True:
                            Url='plugin://plugin.video.f4mTester/?url=%s&streamtype=TSDOWNLOADER'%(urlib.quote_plus(Url))
                        DicM3u = (Nom,Url.split("|")[0].replace(".m3u8",".ts").replace("\r", ""))
                        ret.append(DicM3u)
        return ret

    def AdulteSources(self,Url="http://www.mrsexe.com/cat/62/sodomie/"):
        xbmc.log("Recherche de la liste de chaine...")
        essai = str(self.TelechargPage(url=Url))#.decode('utf-8'))
        match = re.compile('thumb-list(.*?)<ul class="right pagination">', re.DOTALL | re.IGNORECASE).findall(essai)
        match1 = re.compile(r'<li class="[^"]*">\s<a class="thumbnail" href="([^"]+)">\n<script.+?</script>\n<figure>\n<img  id=".+?" src="([^"]+)".+?/>\n<figcaption>\n<span class="video-icon"><i class="fa fa-play"></i></span>\n<span class="duration"><i class="fa fa-clock-o"></i>([^<]+)</span>\n(.+?)\n',
                            re.DOTALL | re.IGNORECASE).findall(match[0])
        ret = []
        for url, image, Temp, Descript in match1:
            ret.append((url,image,Descript+" "+Temp))
            xbmc.log("image= "+str(image))
        try:
            nextp=re.compile(r'<li class="arrow"><a href="(.+?)">suivant</li>').findall(essai)
            xbmc.log("next= "+str(nextp))
            ret.append(('http://www.mrsexe.com' + nextp[0],"","Page Suivante..."))
        except: pass
        return ret
