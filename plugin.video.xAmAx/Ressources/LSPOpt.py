# -*- coding: utf-8 -*-
# Module: LSPOpt
# Author: xamax
# Created on: 20.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import os
import xbmcvfs
import xbmcaddon
import xbmcgui
import xbmc
import urllib2 as urllib
from urlparse import parse_qsl
import base64
import datetime
import sqlite3 as lite
try:
    import json
except:
    import simplejson as json

class cLiveSPOpt():

    LiveStream = None
    CheminLive = ""
    SourceFile = ""

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

    def Telecharge(self):
        self.TryConnectLiveStream()
        try:
            xbmc.log("Recherche de la liste de chaine...")
            dp = xbmcgui.DialogProgress()
            dp.create("Telechargement de la liste de chaine:","Recherche de la liste de chaine...")
            req = urllib.Request("http://redeneobux.com/fr/updated-kodi-iptv-m3u-playlist/")
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
            dp.update(10)
            essai = str(urllib.urlopen(req).read())#.decode('utf-8'))
            essai2 = essai.split("France IPTV")[1].split("location.href=\'")[1].split("\';")[0]
            dp.update(20,"Page Internet France IPTV...")
            
            req = urllib.Request(essai2)
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
            essai = str(urllib.urlopen(req).read())#.decode('utf-8'))
            essai2 = essai.split("http://adf.ly/")[1].split(" ")[0]
            dp.update(30,"Recherche Adresse ADFLY...")

            url = "http://adf.ly/"+essai2
            xbmc.log(" [+] Connection a ADFLY. . . "+url)
            adfly_data = str(urllib.urlopen(url).read())#.decode('utf-8'))
            if not('#EXTM3U' in adfly_data):
                dp.update(40,"Décodage de l'adresse . . .")
                
                xbmc.log(" [+] Recherche adresse du téléchargement . . ."+adfly_data)
                ysmm = adfly_data.split("ysmm = ")[1].split("'")[1].split("';")[0]
                xbmc.log(" [+] Décodage de l'adresse . . ." + str(ysmm))
                essai2 = str(self.Crack(str(ysmm)))
                dp.update(50,"Adresse du fichier Trouvée..")
                
                xbmc.log("\n ### L'adresse du fichier : " + essai2.replace("b'",'').replace("'",''))
                req = urllib.Request(essai2.replace("b'",'').replace("'",''))
                req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
                essai = str(urllib.urlopen(req).read())#.decode('utf-8'))
            else:
                essai = adfly_data
            
            dp.update(70,"Enregistrement de la liste de chaine...")

            ListeM3u = os.path.join(self.CheminLive, "listeTV.m3u")
            fichier = open(ListeM3u, "w")
            fichier.write(essai)
            fichier.close()
            dp.update(100,"Fichier télécharger!")
            xbmc.sleep(1000)
            dp.close()
            xbmc.sleep(1000)
            xbmc.log ("\n ### Fichier télécharger dans le dossier: " + ListeM3u)
            return "OK"
        except:
            dp.update(100)
            xbmc.sleep(1000)
            dp.close()
            xbmc.sleep(1000)
            return "Erreur de Téléchargement"

    def SauveMajLivestream(self, CheminxAmAx, NomFichierM3u="listeTV.m3u", TitreListe="List_A_Jour-"+datetime.datetime.now().strftime("%d/%m/%y")):
        try:
            if self.TryConnectLiveStream() == "OK":
                xbmc.log("SauveMajLivestream "+self.SourceFile)
                Fanart = os.path.join(CheminxAmAx, 'fanart.jpg')
                icon = os.path.join(CheminxAmAx, 'icon.png')
                ListeM3u = os.path.join(self.CheminLive, NomFichierM3u)
                source_list = []
                source_media = {}
                source_media['title'] = TitreListe
                source_media['url'] = ListeM3u.decode('utf-8')
                source_media['fanart'] = Fanart
                source_list.append(source_media)
                sources = None
                if xbmcvfs.exists(self.SourceFile)==True:
                    xbmc.log("Fichier source OK")
                    while 1:
                        sources = json.loads(open(self.SourceFile,"r").read())
                        xbmc.log("Fichier source Ouvert")
                        Modif = False
                        if len(sources) > 0:
                            for index in range(len(sources)):
                                if isinstance(sources[index], list):
                                    if (sources[index][1] == ListeM3u):
                                        del sources[index]
                                        b = open(self.SourceFile,"w")
                                        b.write(json.dumps(sources))
                                        b.close()
                                        Modif = True
                                        break
                                else:
                                    if (sources[index]['url'] == ListeM3u):
                                        del sources[index]
                                        b = open(self.SourceFile,"w")
                                        b.write(json.dumps(sources))
                                        b.close()
                                        Modif = True
                                        break
                        xbmc.log("modif = " + str(Modif))
                        if Modif == False:
                            break
                if sources!=None:
                    if len(sources) > 0:
                        sources = json.loads(open(self.SourceFile,"r").read())
                        sources.append(source_media)
                        b = open(self.SourceFile,"w")
                        b.write(json.dumps(sources))
                        b.close()
                    else:
                        xbmc.log("Ecriture du fichier source_file")
                        b = open(self.SourceFile,"w")
                        b.write(json.dumps(source_list))
                        b.close()
                        xbmc.log("Mise a jour Paramettres LiveStream")
                else:
                    xbmc.log("Ecriture du fichier source_file")
                    b = open(self.SourceFile,"w")
                    b.write(json.dumps(source_list))
                    b.close()
                    xbmc.log("Mise a jour Paramettres LiveStream")
                
                #xbmc.executebuiltin("XBMC.Notification(LiveStreamsPro,Nouvelle source ajouter.,5000,"+icon+")")
                #xbmc.executebuiltin("XBMC.Container.Refresh")
                xbmc.log("******Liste de chaine LiveStreamPro a jour******")
                return "******Liste de chaine LiveStreamPro a jour******"
            else:
                xbmc.log("**Erreur de mise a jour de liste LiveStreamPro a jour 1***")
                return "**Erreur de mise a jour de liste LiveStreamPro a jour**"
        except:
            xbmc.log("**Erreur de mise a jour de liste LiveStreamPro a jour 2**")
            return "**Erreur de mise a jour de liste LiveStreamPro a jour**"

    def Lire_m3u(self, CheminxAmAx):
        xbmc.log("Lire_M3u: CheminxAmAx= "+CheminxAmAx)
        dbxAmAx = os.path.join(CheminxAmAx, "Ressources", "xAmAx.db")
        ListeM3u = os.path.join(self.CheminLive, "listeTV.m3u")
        
        data = open(ListeM3u, 'r').read()
        #content = data.rstrip()
        #match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
        #total = len(match)
        try:
            xbmc.log("Ouverture de la Base de donnée xAmAx...")
            NewDB = lite.connect(dbxAmAx)
            cBouq = NewDB.cursor()
            xbmc.log("SELECT * FROM Bouquet ORDER BY Ordre ASC;")
            cBouq.execute("SELECT * FROM Bouquet ORDER BY Ordre ASC;")
            xbmc.log("Enregistrement de tous les nouveaux Membres de la table...")
            for row in cBouq:
                cChaine = NewDB.cursor()
                cChaine.execute("DELETE FROM UrlBouquet;")
                IdUrlChaine = 0
                xbmc.log("SELECT * FROM ChaineBouquet ORDER BY Ordre WHERE IDBouqChaine = " + str(row[0])+" ORDER BY "+str(row[3])+";")
                cChaine.execute("SELECT * FROM ChaineBouquet WHERE IDBouqChaine = " + str(row[0])+" ORDER BY "+str(row[3])+";")
        
                for row2 in cChaine:
                    numLignSuiv = 0
                    while 1:
                        num = data.upper().find(str(row2[2]).upper(),numLignSuiv)
                        if num > 0:
                            num = data.upper().rfind(",",0,num)+1
                            numLignSuiv = num + data[num:].upper().find("#EXTINF")
                            if numLignSuiv == -1:
                                numLignSuiv = len(data)
                            data2 = data[num:numLignSuiv].decode('utf-8').split(chr(10))
                            if len(data2) > 0:
                                #try:
                                EnrOk=True
                                xbmc.log("**** Pas dans chaine:"+str(row2[3])+" len:"+str(len(str(row2[3]))))
                                if len(str(row2[3]))>0 and str(row2[3]).upper()!="NONE":
                                    PasDansChaine = str(row2[3]).encode('utf-8').upper().split(",")
                                    for Pas in PasDansChaine:
                                        if data2[0].upper().find(Pas)!=-1:
                                            xbmc.log("**** Pas dans chaine:"+Pas+" Find:"+str(data2[0].find(Pas)))
                                            EnrOk=False
                                            break
                                if EnrOk==True:
                                    IdUrlChaine += 1
                                    cUrl = NewDB.cursor()
                                    cUrl.execute('''INSERT INTO UrlBouquet (IDUrlB,IDChaine,Url,NomAffichChaine)
                                    VALUES (?,?,?,?)''',(IdUrlChaine,row2[0],data2[1],data2[0].replace("FR: ",'').replace("|FR| ",'')))
                                    #xbmc.log("**** "+data2[0]+" url:"+data2[1])
                                    #
                                #except:
                                    #xbmc.log("**** Erreur: "+data[num:numLignSuiv])
                        else:
                            break
                #try:
                xbmc.log("Ecriture du fichier BouqChaine = SELECT * FROM UrlBouquet ORDER BY "+row[4]+";")
                cUrl.execute("SELECT * FROM UrlBouquet ORDER BY "+row[4]+";")
                Bouquet="#EXTM3U"
                for row3 in cUrl:
                    Bouquet+="\n#EXTINF:-1,"+row3[3]+"\n"+row3[2]
                
                xbmc.log("Ecriture du fichier BouqChaine = " + os.path.join(self.CheminLive, "Bouquet-"+row[1]+".m3u"))
                b = open(os.path.join(self.CheminLive, "Bouquet-"+row[1]+".m3u"),"w")
                b.write(Bouquet.encode('utf-8'))
                b.close()
                self.SauveMajLivestream(CheminxAmAx, NomFichierM3u="Bouquet-"+row[1]+".m3u", TitreListe="Bouquet-"+row[1])
                #except: pass
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
                if NewDB:
                    NewDB.commit()
                    NewDB.close()
            except: pass
    #    print 'total m3u links',total
