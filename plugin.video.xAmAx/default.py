# -*- coding: utf-8 -*-
# Module: default
# Author: xamax
# Created on: 02.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
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

#Enregistrement des paramètres
Param = {"Chemin":"", "Table":"", "SQL":'SELECT * FROM ', "Ordre":' ORDER BY `title2` ', "CreerTbl":"", "InserTbl":"", "InserTbl2":"", "FinAffich":""}

_vStream = ""
_LiveStream = ""
_ChercheBackgroud = ""

# Récupération des info du plugin
_url = sys.argv[0]
nomPlugin = _url.replace("plugin://","")
AdressePlugin = xbmc.translatePath('special://home/')+"/addons/"+nomPlugin+'/'
_handle = int(sys.argv[1])
_ArtMenu = {'thumb': AdressePlugin+'play.png',
            'fanar': AdressePlugin+'fanart.jpg',
            'info': AdressePlugin+'info.png'}
_MenuList={"Vertion 1.1.3":("V","InfoVersion"),
           "Trier la liste de Recherche vStream":("vStream","RechercheVstream"),
           "Trier les Marques-Pages vStream":("vStream","MPVstream"),
           "Mise A Jour Liste de chaines":("LiveStream","MajTV"),
           "Changer le Fond d'écran":("ecran",'ChangeFonDecran')}

def AfficheMenu():
        # creation du menu
        #xbmc.log("Menu")
        Param["Chemin"]=xbmc.translatePath('special://home/')+"/userdata/addon_data/plugin.video.vstream/"
        _vStream = TryConnectvStream() # "vStream non installer!" TryConnectvStream()
        Param["Chemin"]=xbmc.translatePath('special://home/')+"/userdata/addon_data/plugin.video.live.streamspro/"
        _LiveStream = TryConnectLiveStream() # "LiveStream non installer!" TryConnectLiveStream()
        _ChercheBackgroud = TryChercheBackgroud()
        #xbmc.log( _vStream + " " + _LiveStream)
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
                            is_folder = True
                            listing.append((url, list_item, is_folder))
        #Affichage du Menu
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
        xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(_handle)

def TryConnectvStream():
        try:
                with open(Param["Chemin"]+'Vstream2.db') as f:
                        pass
                f.closed
                os.remove(Param["Chemin"]+'Vstream2.db')
        except IOError:
                pass
        try:
                with open(Param["Chemin"]+'vstream.db') as v:
                        pass
                v.closed
                return "OK"
        except IOError:
                return "vStream non installer!"

def TryConnectLiveStream():
        try:
                with open(Param["Chemin"]+'/source_file', 'r') as l:
                        pass
                l.closed
                return "OK"
        except IOError:
                return "LiveStream non installer!"

def TryChercheBackgroud():
        try:
                with open(xbmc.translatePath('special://home/')+"/userdata/guisettings.xml") as f:
                        Retour = f.read()
                        NomSkin = Retour.split("<skin")[1].split("</skin>")[0]
                        NomSkin = NomSkin.replace(' default="true">','').replace('>','')
                f.closed
                Defaut = xbmc.translatePath('special://home/')+'/addons/'+NomSkin+"/backgrounds/"
                if ((NomSkin == "skin.confluence")or(NomSkin == "skin.qonfluence")):
                        with open(xbmc.translatePath('special://home/')+"/userdata/addon_data/"+NomSkin+"/settings.xml") as f:
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
        except IOError:
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

                fichier = open(Param["Chemin"]+"listeTV.m3u", "w")
                fichier.write(essai)
                fichier.close()

                xbmc.log ("\n ### Fichier télécharger dans le dossier: " + Param["Chemin"]+"listeTV.m3u")
                return "OK"
        except:
                return "Erreur de Téléchargement"

def SauveMajLivestream():
        Date=datetime.datetime.now().strftime("%d/%m/%y")
        fichASauv = '[{"url": "'+Param["Chemin"]+"listeTV.m3u"+'", "fanart": "/home/max/.kodi/addons/plugin.video.live.streamspro/fanart.jpg", "title": "List_A_Jour'+Date+'"},'

        try:
                with open(Param["Chemin"]+'/source_file', 'r') as f:
                        essai = f.read()
                f.closed
                essai2 = essai.replace("[","").replace("]","").split("{")
                a=len(Param["Chemin"])+len("listeTV.m3u")
                for liste in essai2:
                        if len(liste) > 10:
                                if liste[:a+8] != '"url": "'+Param["Chemin"]+"listeTV.m3u":
                                        fichASauv = fichASauv + "{" + liste
        except:
                pass

        if fichASauv[-1] == ",":
                fichASauv=fichASauv[:-1] + "]"
        else:
                fichASauv=fichASauv + "]"

        xbmc.log(fichASauv)

        with open(Param["Chemin"]+'/source_file', 'w') as f:
                a = f.write(fichASauv)
                xbmc.log("******Liste de chaine LiveStreamPro a jour******")
                return "******Liste de chaine LiveStreamPro a jour******"

def router(paramstring):
        #xbmc.log("dans router")
        # reception des paramètres du menu
        params = dict(parse_qsl(paramstring))
        # Si aucun paramètre on ouvre le menu
        if params:
                xbmc.log(str(params))
                if params['action'] == 'play':
                        # Lance l'action demander dans le menu
                        if params['ElemMenu']=='MPVstream':
                                Param["Chemin"]=xbmc.translatePath('special://home/')+"/userdata/addon_data/plugin.video.vstream/"
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
                                Param["Chemin"]=xbmc.translatePath('special://home/')+"/userdata/addon_data/plugin.video.vstream/"
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
                                Param["Chemin"]=xbmc.translatePath('special://home/')+"/userdata/addon_data/plugin.video.live.streamspro/"
                                Retour = Telecharge()
                                if Retour == "OK":
                                        Retour = SauveMajLivestream()
                                        dialog = xbmcgui.Dialog()
                                        ok = dialog.ok("Mise A Jour Liste de chaines TV", Retour)
                                else:
                                        dialog = xbmcgui.Dialog()
                                        ok = dialog.ok("Mise A Jour Liste de chaines TV", Retour)
                        if params['ElemMenu']=='InstallvStream':
                                xbmc.log("InstallvStream")
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
                                        fn = dialog.browse(2, "Choisir l'image de fond d'écran", 'files', '.jpg,.png', False, False, Defaut)
                                        if fn != Defaut and fn != "":
                                                if xbmcvfs.exists(fn):
                                                        if not xbmcvfs.exists(Defaut+NomFichier+"_Sauve"+Extension):
                                                                xbmcvfs.rename(Defaut+NomFichier+Extension, Defaut+NomFichier+"_Sauve"+Extension)
                                                        success = xbmcvfs.copy(fn, Defaut+NomFichier+Extension)
                                                        dialog = xbmcgui.Dialog()
                                                        if success:
                                                                ok = dialog.ok("Le fond d'écran a était modifier!!!", "Le fond d'écran a bien était modifier!!!","Si le fond ne s'affiche pas veuillez redémarrer Kodi")
                                                        else:
                                                                ok = dialog.ok("Erreur de copy du fichier", "Le font d'écran n'a pas pu être modifier!!!","       DESOLE!!!")
        else:
                # Affichage du menu si aucune action
                # Recherche si la Base vStream est présente
                #xbmc.log("Affichage Menux")
                AfficheMenu()

if __name__ == '__main__':
        #xbmc.log("Demarrage xAmAx")
        # Envoi des paramètre du menu
        router(sys.argv[2][1:])
