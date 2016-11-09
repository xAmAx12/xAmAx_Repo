# -*- coding: utf-8 -*-
# Module: default
# Author: xamax
# Created on: 02.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import re
import sys
import sqlite3 as lite
import urllib2 as urllib
from urlparse import parse_qsl
import base64
import datetime
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs

try:
        import json
except:
        import simplejson as json
    
#Enregistrement des paramètres
Param = {"Chemin":"",
         "Table":"",
         "SQL":'SELECT * FROM ',
         "Ordre":' ORDER BY `title2` ',
         "CreerTbl":"",
         "InserTbl":"",
         "InserTbl2":"",
         "FinAffich":"",
         "SourceFile":"",
         "vStream":""}

addon = xbmcaddon.Addon('plugin.video.xAmAx')

__version__ = addon.getAddonInfo('version')
_vStream = ""
_LiveStream = ""
_ChercheBackgroud = ""
TEXT = ""
LiveStream  = None
vStream = None

# Récupération des info du plugin
_url = sys.argv[0]
nomPlugin = _url.replace("plugin://","")
AdressePlugin = xbmc.translatePath('special://home/')+"addons/"+nomPlugin
_handle = int(sys.argv[1])
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))

_ArtMenu = {'thumb': AdressePlugin+'play.png',
            'fanar': AdressePlugin+'fanart.jpg',
            'info': AdressePlugin+'info.png'}
_MenuList={"Version "+__version__:("V","InfoVersion"),
           "Afficher le Journal d'erreur":("log","AffichLog"),
           "Trier la liste de Recherche vStream":("vStream","RechercheVstream"),
           "Trier les Marques-Pages vStream":("vStream","MPVstream"),
           "Mise A Jour Liste de chaines":("LiveStream","MajTV"),
           "Creer des listes TV par Bouquet":("LiveStream","Bouquet"),
           "Changer le Fond d'écran":("ecran",'ChangeFonDecran')}

class LogAffich():
    def Fenetre(self,Chemin="",line_number=0,Invertion=False,LabTitre="xAmAx "+__version__):
        try:
            xbmc.executebuiltin("ActivateWindow(10147)")
            window = xbmcgui.Window(10147)
            xbmc.sleep(100)
            window.getControl(1).setLabel(LabTitre)
            window.getControl(5).setText(self.getcontent(Chemin,line_number,Invertion))
        except:
            pass
    def getcontent(self,Chemin="",line_number=0,Invertion=False):
        if Chemin!="":
            if ((Chemin[:8]=="https://")or(Chemin[:7]=="http://")):
                xbmc.log("Ouverture du Fichier des modifications")
                req = urllib.Request(Chemin)
                req.add_header('User-Agent',
                    'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
                contents = urllib.urlopen(req).read()#.decode('utf-8'))
            else:
                fh = open(Chemin, 'rb')
                contents=fh.read()
                fh.close()
        else:
            contents="Aucun Fichier Selectionner"

        if Invertion==True:
            contents='\n'.join(contents.splitlines()[::-1])

        if line_number>0:
            try: contents=contents[0:line_number]
            except: contents='\n%s' % (contents)

        return contents.replace(
            ' ERROR: ',' [COLOR red]ERREUR[/COLOR]: ').replace(
            ' WARNING: ',' [COLOR gold]AVERTISSEMENT[/COLOR]: ').replace(
            ' NOTICE: ',' [COLOR green]INFO[/COLOR]: ').replace(
            '- Version ',' [COLOR green]- Version[/COLOR]: ').replace(
            '=======================================================================================',
            '[COLOR green]=======================================================================================[/COLOR]')

def AfficheMenu():
    # creation du menu
    #xbmc.log("Menu")
    _vStream = TryConnectvStream() # "vStream non installer!" TryConnectvStream()
    _LiveStream = TryConnectLiveStream() # "LiveStream non installer!" TryConnectLiveStream()
    _ChercheBackgroud = TryChercheBackgroud()
    # Création de la liste d'élément.
    listing = []
    # Création de chaque élément
    if _vStream != "OK":
        list_item = xbmcgui.ListItem(label=_vStream)
        list_item.setArt({'thumb': _ArtMenu['info'],
                        'icon': _ArtMenu['info'],
                        'fanart': _ArtMenu['fanar']})
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        #list_item.setInfo('video', {'title': Titre})
        # Exemple: plugin://plugin.video.example/?action=listing&ElemMenu=Animals
        url = '{0}?action=play&ElemMenu={1}'.format(_url, 'InstallvStream')
        is_folder = True
        listing.append((url, list_item, is_folder))
    if _LiveStream != "OK":
        list_item = xbmcgui.ListItem(label=_LiveStream)
        list_item.setArt({'thumb': _ArtMenu['info'],
                        'icon': _ArtMenu['info'],
                        'fanart': _ArtMenu['fanar']})
        # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        #list_item.setInfo('video', {'title': Titre})
        # Exemple: plugin://plugin.video.example/?action=listing&ElemMenu=Animals
        url = '{0}?action=play&ElemMenu={1}'.format(_url, 'InstallLiveStream')
        is_folder = True
        listing.append((url, list_item, is_folder))
    for tag, (Titre, Act) in _MenuList.items():
        if ((_vStream == "OK" and Titre == "vStream")or
            (_LiveStream == "OK" and Titre == "LiveStream")or
            (_ChercheBackgroud == "OK" and Titre == "ChangeFonDecran")or
            (Titre != "LiveStream" and Titre != "vStream" and Titre != "ChangeFonDecran")):
                list_item = xbmcgui.ListItem(label=tag)
                list_item.setArt({'thumb': _ArtMenu['thumb'],
                                'icon': _ArtMenu['thumb'],
                                'fanart': _ArtMenu['fanar']})
                # http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
                #list_item.setInfo('video', {'title': Titre})
                # Exemple: plugin://plugin.video.example/?action=listing&ElemMenu=Animals
                url = '{0}?action=play&ElemMenu={1}'.format(_url, Act)
                is_folder = False
                listing.append((url, list_item, is_folder))
    #Affichage du Menu
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def TryConnectvStream():
    try:
        vStream  = xbmcaddon.Addon('plugin.video.vstream')
        Param["vStream"]=str(xbmc.translatePath(vStream.getAddonInfo('profile').decode('utf-8')))
        if xbmcvfs.exists(os.path.join(Param["vStream"],'Vstream2.db')):
            os.remove(os.path.join(Param["vStream"],'Vstream2.db'))
        return "OK"
    except:
        return "vStream non installer!"

def TryConnectLiveStream():
    try:
        LiveStream  = xbmcaddon.Addon('plugin.video.live.streamspro')
        Param['SourceFile'] = str(os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('profile').decode('utf-8')), 'source_file'))
        return "OK"
    except:
        return "LiveStreamPro non installer!"

def TryChercheBackgroud():
    try:
        NomSkin = xbmc.getSkinDir()
        xbmc.log("skindir: "+NomSkin)
        Defaut = xbmc.translatePath('special://home/')+'addons/'+NomSkin+"/backgrounds/"
        if ((NomSkin == "skin.confluence")or(NomSkin == "skin.qonfluence")):
            with open(xbmc.translatePath('special://home/')+"userdata/addon_data/"+NomSkin+"/settings.xml") as f:
                Retour = f.read()
            f.closed
            ModifSkin = Retour.split('<setting id="UseCustomBackground" type="bool">')[1].split("</setting>")[0]
            if ModifSkin == 'true':
                ModifSkin = Retour.split('<setting id="CustomBackgroundPath" type="string">')[1].split("</setting>")[0]
                if xbmcvfs.exists(ModifSkin):
                    Param["Chemin"]=ModifSkin
                    return "OK"
                elif xbmcvfs.exists(Defaut+"SKINDEFAULT.jpg"):
                    Param["Chemin"]=Defaut+"SKINDEFAULT.jpg"
                    return "OK"
                else:
                    return "Fond d'écran indisponible!"
            else:
                if xbmcvfs.exists(Defaut+"SKINDEFAULT.jpg"):
                    Param["Chemin"]=Defaut+"SKINDEFAULT.jpg"
                    return "OK"
                else:
                    return "Fond d'écran indisponible!"
        elif(NomSkin == "skin.aeon.nox.5"):
            if xbmcvfs.exists(Defaut+"default_bg.jpg"):
                Param["Chemin"]=Defaut+"default_bg.jpg"
                return "OK"
            else:
                return "Fond d'écran indisponible!"
        else:
            return "Fond d'écran indisponible!"
    except:
            return "Fond d'écran indisponible!"
                
def MiseAJourVstream():
    try:
        xbmc.log("Création de la nouvelle Base de donnée...")
        NewDB = lite.connect(Param["Chemin"]+'Vstream2.db')
        Curs = NewDB.cursor()
        xbmc.log("Création de la nouvelle Table...")
        Curs.execute(Param["CreerTbl"])
        xbmc.log("Connection à la Base de donnée existante\n("+Param["Chemin"]+'vstream.db'+")...")
        conn = lite.connect(Param["Chemin"]+'vstream.db')
        c = conn.cursor()
        xbmc.log(Param["SQL"]+Param["Table"])
        c.execute(Param["SQL"]+Param["Table"])
        xbmc.log("Enregistrement de tous les nouveaux Membres de la table...")
        for row in c:
            tittre=str(row[1]).split("[")
            Nom = str(tittre[0])
            for titi in tittre:
                toto=str(titi).split("]")
                if len(toto) > 1:
                    if len(toto[1])>0:
                        if len(Nom)>0:
                            Nom+=" " + str(toto[1])
                        else:
                            Nom+=str(toto[1])
            Nom=Nom.replace("   ", "")
            Nom=Nom.replace("  ", " ")
            Nom=Nom.replace(" - " + row[3], "")
            if Param["Table"]=="favorite":
                Nom2 = row[1]
                site = " - [COLOR yellow]" + row[3] + "[/COLOR]"
                if len(Nom2)>len(site):
                    if Nom2[len(Nom2)-len(site):]!=site:
                        Nom2=Nom2 + site
                else:
                    Nom2=Nom2 + site
                Curs.execute(Param["InserTbl2"],(row[0],Nom2,Nom,row[2],row[3],row[4],row[5],row[6],row[7]))
            else:
                Curs.execute(Param["InserTbl2"],(row[0],row[1],Nom,row[2],row[3],row[4],row[5],row[6]))
    except lite.Error as e:
        if conn:
            conn.rollback()
        xbmc.log("Error %s:" % e.args[0])
        return "Erreur de connection à la base vstream!"
        xbmc.log("Erreur de connection à la base vstream!")
        # raise e
    finally:
        if Curs:
            Curs.close()
        if c:
            c.close()
        if NewDB:
            NewDB.commit()
            NewDB.close()
        if conn:
            conn.close()

    xbmc.log("Sauv: "+Param["SQL"]+Param["Table"]+Param["Ordre"])
    try:
        conn = lite.connect(Param["Chemin"]+'vstream.db')
        c = conn.cursor()
        c.execute("DELETE FROM "+Param["Table"])
        NewDB = lite.connect(Param["Chemin"]+'Vstream2.db')
        Curs = NewDB.cursor()
        Curs.execute(Param["SQL"]+Param["Table"]+Param["Ordre"])
        i = 0
        if Param["Table"]=="favorite":
            for row in Curs:
                i+=1
                c.execute(Param["InserTbl"],(i,row[1],row[3],row[4],row[5],row[6],row[7],row[8]))
        else:
            for row in Curs:
                i+=1
                c.execute(Param["InserTbl"],(i,row[1],row[3],row[4],row[5],row[6],row[7]))
    except lite.Error as e:
        if conn:
            conn.rollback()
        xbmc.log("Error %s:" % e.args[0])
        return "Erreur de connection à la base vstream!"
        xbmc.log("Erreur de connection à la base vstream!")
        # raise e
    finally:
        if c:
            c.close()
        if Curs:
            Curs.close()
        if NewDB:
            NewDB.close()
        if conn:
            conn.commit()
            conn.close()

    os.remove(Param["Chemin"]+'Vstream2.db')
    xbmc.log(Param["FinAffich"])
    return Param["FinAffich"]

def EffaceFich():
    try:
        with open(Param["Chemin"]+'listeTV.m3u') as f:
            pass
        f.closed
        os.remove(Param["Chemin"]+'listeTV.m3u')
    except IOError:
        pass

def Crack(code):
    zeros = ''
    ones = ''
    for n,letter in enumerate(code):
        if n%2 == 0:
            zeros += code[n]
        else:
            ones =code[n] + ones
    key = zeros + ones
    key = base64.b64decode(key.encode("utf-8"))
    return key[2:]

def Telecharge():
    try:
        xbmc.log("Recherche de la liste de chaine...")
        req = urllib.Request("http://redeneobux.com/fr/updated-kodi-iptv-m3u-playlist/")
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        essai = str(urllib.urlopen(req).read())#.decode('utf-8'))
        essai2 = essai.split("France IPTV")[1].split("location.href=\'")[1].split("\';")[0]

        req = urllib.Request(essai2)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        essai = str(urllib.urlopen(req).read())#.decode('utf-8'))
        essai2 = essai.split("http://adf.ly/")[1].split(" ")[0]

        url = "http://adf.ly/"+essai2
        xbmc.log(" [+] Connection a ADFLY. . .")
        adfly_data = str(urllib.urlopen(url).read())#.decode('utf-8'))
        xbmc.log(" [+] Recherche adresse du téléchargement . . .")
        ysmm = adfly_data.split("ysmm = ")[1].split("\'")[1].split("'\;")[0]
        xbmc.log(" [+] Décodage de l'adresse . . .")
        essai2 = str(Crack(str(ysmm)))
        xbmc.log("\n ### L'adresse du fichier : " + essai2.replace("b'",'').replace("'",''))
        req = urllib.Request(essai2.replace("b'",'').replace("'",''))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')

        essai = str(urllib.urlopen(req).read())#.decode('utf-8'))

        LiveStream  = xbmcaddon.Addon('plugin.video.live.streamspro')
        ListeM3u = os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('profile').decode('utf-8')), "listeTV.m3u")
        fichier = open(ListeM3u, "w")
        fichier.write(essai)
        fichier.close()

        xbmc.log ("\n ### Fichier télécharger dans le dossier: " + ListeM3u)
        return "OK"
    except:
        return "Erreur de Téléchargement"

def SauveMajLivestream(NomFichierM3u="listeTV.m3u", TitreListe="List_A_Jour-"+datetime.datetime.now().strftime("%d/%m/%y")):
    try:
        if TryConnectLiveStream() == "OK":
            xbmc.log("SauveMajLivestream "+Param["SourceFile"])
            LiveStream  = xbmcaddon.Addon('plugin.video.live.streamspro')
            Fanart = os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('path').decode('utf-8')), 'fanart.jpg')
            icon = os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('path').decode('utf-8')), 'icon.png')
            ListeM3u = os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('profile').decode('utf-8')), NomFichierM3u)
            source_list = []
            source_media = {}
            source_media['title'] = TitreListe
            source_media['url'] = ListeM3u.decode('utf-8')
            source_media['fanart'] = Fanart
            source_list.append(source_media)
            sources = None
            if xbmcvfs.exists(Param["SourceFile"])==True:
                xbmc.log("Fichier source OK")
                while 1:
                    sources = json.loads(open(Param["SourceFile"],"r").read())
                    xbmc.log("Fichier source Ouvert")
                    Modif = False
                    if len(sources) > 0:
                        for index in range(len(sources)):
                            if isinstance(sources[index], list):
                                if (sources[index][1] == ListeM3u):
                                    del sources[index]
                                    b = open(Param["SourceFile"],"w")
                                    b.write(json.dumps(sources))
                                    b.close()
                                    Modif = True
                                    break
                            else:
                                if (sources[index]['url'] == ListeM3u):
                                    del sources[index]
                                    b = open(Param["SourceFile"],"w")
                                    b.write(json.dumps(sources))
                                    b.close()
                                    Modif = True
                                    break
                    xbmc.log("modif = " + str(Modif))
                    if Modif == False:
                        break
            if sources!=None:
                if len(sources) > 0:
                    sources = json.loads(open(Param["SourceFile"],"r").read())
                    sources.append(source_media)
                    b = open(Param["SourceFile"],"w")
                    b.write(json.dumps(sources))
                    b.close()
                else:
                    xbmc.log("Ecriture du fichier source_file")
                    b = open(Param["SourceFile"],"w")
                    b.write(json.dumps(source_list))
                    b.close()
                    xbmc.log("Mise a jour Paramettres LiveStream")
            else:
                xbmc.log("Ecriture du fichier source_file")
                b = open(Param["SourceFile"],"w")
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

def Lire_m3u():
    xAmAxPath = xbmc.translatePath(addon.getAddonInfo('path').decode('utf-8'))
    dbxAmAx = os.path.join(xAmAxPath, "Ressources/xAmAx.db")
    LiveStream  = xbmcaddon.Addon('plugin.video.live.streamspro')
    ListeM3u = os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('profile').decode('utf-8')), "listeTV.m3u")
    
    data = open(ListeM3u, 'r').read()
    content = data.rstrip()
    match = re.compile(r'#EXTINF:(.+?),(.*?)[\n\r]+([^\r\n]+)').findall(content)
    total = len(match)
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
            
            xbmc.log("Ecriture du fichier BouqChaine = " + os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('profile').decode('utf-8')), "Bouquet-"+row[1]+".m3u"))
            b = open(os.path.join(xbmc.translatePath(LiveStream.getAddonInfo('profile').decode('utf-8')), "Bouquet-"+row[1]+".m3u"),"w")
            b.write(Bouquet.encode('utf-8'))
            b.close()
            SauveMajLivestream(NomFichierM3u="Bouquet-"+row[1]+".m3u", TitreListe="Bouquet-"+row[1])
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


def router(paramstring):
        #xbmc.log("dans router")
        # reception des paramètres du menu
        if len(paramstring)>=2:
            params = dict(parse_qsl(paramstring))
        else:
            params = None
        # Si aucun paramètre on ouvre le menu
        if params:
            xbmc.log(str(params))
            if params['action'] == 'play':
                # Lance l'action demander dans le menu
                if params['ElemMenu']=='MPVstream':
                    Param["Chemin"]=xbmc.translatePath('special://home/')+"userdata/addon_data/plugin.video.vstream/"
                    Param["Table"]="favorite"
                    Param["CreerTbl"]='''CREATE TABLE favorite
                            (`addon_id` integer PRIMARY KEY AUTOINCREMENT,
                            `title` TEXT,
                            `title2` TEXT,
                            `siteurl` TEXT,
                            `site` TEXT,
                            `fav` TEXT,
                            `cat` TEXT,
                            `icon` TEXT,
                            `fanart` TEXT);'''
                    Param["InserTbl"]='''INSERT INTO favorite (addon_id,title,siteurl,site,fav,cat,icon,fanart)
                                    VALUES (?,?,?,?,?,?,?,?)'''
                    Param["InserTbl2"]='''INSERT INTO favorite (addon_id,title,title2,siteurl,site,fav,cat,icon,fanart)
                                    VALUES (?,?,?,?,?,?,?,?,?)'''
                    Param["FinAffich"]='''
***********************************************************
* Fin de la sauvegarde des Marques-Pages classés par nom! *
***********************************************************'''
                    Retour = TryConnectvStream()
                    if Retour == "OK":
                        Retour = MiseAJourVstream()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Trier les Marques-Pages vStream", Retour)
                    else:
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok('Erreur:', Retour)
                if params['ElemMenu']=='RechercheVstream':
                    Param["Chemin"]=xbmc.translatePath('special://home/')+"userdata/addon_data/plugin.video.vstream/"
                    Param["Table"]="history"
                    Param["CreerTbl"]='''CREATE TABLE `history`
                        (`addon_id` integer PRIMARY KEY AUTOINCREMENT,
                        `title` TEXT,
                        `title2` TEXT,
                        `disp` TEXT,
                        `icone` TEXT,
                        `isfolder` TEXT,
                        `level` TEXT,
                        `lastwatched` TIMESTAMP);'''
                    Param["InserTbl"]='''INSERT INTO history (addon_id,title,disp,icone,isfolder,level,lastwatched)
                            VALUES (?,?,?,?,?,?,?)'''
                    Param["InserTbl2"]='''INSERT INTO history (addon_id,title,title2,disp,icone,isfolder,level,lastwatched)
                            VALUES (?,?,?,?,?,?,?,?)'''
                    Param["FinAffich"]='''
********************************************************
* Fin de la sauvegarde des Recherches classés par nom! *
********************************************************'''
                    Retour = TryConnectvStream()
                    if Retour == "OK":
                        Retour = MiseAJourVstream()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Trier la liste de Recherche vStream", Retour)
                    else:
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok('Erreur:', Retour)
                if params['ElemMenu']=='MajTV':
                    Retour = Telecharge()
                    if Retour == "OK":
                        Retour = SauveMajLivestream()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Mise A Jour Liste de chaines TV", Retour)
                    else:
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Mise A Jour Liste de chaines TV", Retour)
                if params['ElemMenu']=="AffichLog":
                    xbmc.log("AffichLog: ")
                    Affich=LogAffich()
                    Affich.Fenetre(Chemin=xbmc.translatePath('special://logpath')+"kodi.log",
                                    line_number=0,Invertion=True,LabTitre="Journal d'erreur")
                if params['ElemMenu']=="InfoVersion":
                    xbmc.log("InfoVersion: ")
                    Affich=LogAffich()
                    Affich.Fenetre(Chemin=AdressePlugin+"changelog.txt",line_number=0)
                if params['ElemMenu']=="Bouquet":
                    xbmc.log("Bouquet: ")
                    Lire_m3u()
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok("Bouquet TV", "Bouquet TV ajouter a liveStream")
                if params['ElemMenu']=='ChangeFonDecran':
                    xbmc.log("ChangeFonDecran")
                    _ChercheBackgroud = TryChercheBackgroud()
                    if _ChercheBackgroud == "OK":
                        CheminSplit = Param["Chemin"][:Param["Chemin"].rfind("/")+1]
                        NomFichier = Param["Chemin"][Param["Chemin"].rfind("/")+1:]
                        Extension = NomFichier[-4:]
                        NomFichier = NomFichier[:-4]
                        xbmc.log(CheminSplit+" "+NomFichier+" "+Extension)
                        dialog = xbmcgui.Dialog()
                        Defaut = CheminSplit
                        fn = dialog.browse(2, "Choisir l'image de fond d'écran", 'files', '.jpg,.png',
                                           False, False, Defaut)
                        if fn != Defaut and fn != "":
                            if xbmcvfs.exists(fn):
                                if not xbmcvfs.exists(Defaut+NomFichier+"_Sauve"+Extension):
                                    xbmcvfs.rename(Defaut+NomFichier+Extension,
                                                   Defaut+NomFichier+"_Sauve"+Extension)
                                success = xbmcvfs.copy(fn, Defaut+NomFichier+Extension)
                                dialog = xbmcgui.Dialog()
                                if success:
                                    ok = dialog.ok("Le fond d'écran a était modifier!!!",
                                                   "Le fond d'écran a bien était modifier!!!",
                                                   "Si le fond ne s'affiche pas veuillez redémarrer Kodi")
                                else:
                                    ok = dialog.ok("Erreur de copy du fichier",
                                                   "Le font d'écran n'a pas pu être modifier!!!",
                                                   "       DESOLE!!!")
        else:
            # Affichage du menu si aucune action
            # Recherche si la Base vStream est présente
            #xbmc.log("Affichage Menux")
            AfficheMenu()

if __name__ == '__main__':
        
        xbmc.log("Demarrage xAmAx: commande = " + str(sys.argv[2]))
        # Envoi des paramètre du menu
        router(sys.argv[2][1:])
