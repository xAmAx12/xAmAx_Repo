# -*- coding: utf-8 -*-
# Module: default
# Author: xamax
# Created on: 29.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import sys
import sqlite3 as lite
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import urllib2 as urllib
import urllib as urlib
from urlparse import parse_qsl

        
from Ressources.vStreamOpt import cvStreamOpt
from Ressources.LSPOpt import cLiveSPOpt
#import Ressources.test as test
    
#Enregistrement des paramètres
Param = {"Chemin":""}

nomPlugin = 'plugin.video.xAmAx'
addon = xbmcaddon.Addon(nomPlugin)

__version__ = addon.getAddonInfo('version')
_vStream = ""
_LiveStream = ""
_ChercheBackgroud = ""
TEXT = ""

# Récupération des info du plugin
_url = sys.argv[0]
AdressePlugin = addon.getAddonInfo('path')
Url_Plugin_Version = "https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/repo/"+nomPlugin+"/README.md"
_handle = int(sys.argv[1])
profile = xbmc.translatePath(addon.getAddonInfo('profile').decode('utf-8'))

_ArtMenu = {'thumb': os.path.join(AdressePlugin,'play.png'),
            'lecture': os.path.join(AdressePlugin,'menu.png'),
            'param': os.path.join(AdressePlugin,'param.png'),
            'fanar': os.path.join(AdressePlugin,'fanart.jpg'),
            'info': os.path.join(AdressePlugin,'info.png')}
_MenuList={"Chaines TV et bouquet":("TV","VisuLiveStream",True),
           "Options de vStream (Film et séries)":("vStream","VisuVstream",True),
           "Options de Kodi":("Kodi","VisuKodi",True),
           "Options de xAmAx":("xAmAx",'VisuxAmAx',True)}
_MenuxAmAx={"Version "+__version__:("xAmAx","InfoVersion",False),
           "Mise a jour de xAmAx":("xAmAx",'MiseAJourxAmAx',True)}#,"test":("xAmAx",'test',False)}
_MenuvStream={"Trier la liste de Recherche vStream":("vStream","RechercheVstream",True),
           "Trier les Marques-Pages vStream":("vStream","MPVstream",True)}
_MenuTV={"Afficher Les chaines Tv":("TV","AffichTV",True),
           "Mise A Jour Liste de chaines":("TV","MajTV",True)}
_MenuKodi={"Afficher le Journal d'erreur":("Kodi","AffichLog",False),
        "Changer le Fond d'écran":("Kodi",'ChangeFonDecran',True),
        "Effacer le fichiers temporaires":("Kodi","SupTemp",True),
        "Effacer les miniatures en mémoire":("Kodi","SupThumb",True)}

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

def AfficheMenu(Menu=_MenuList):
    # creation du menu
    xbmc.log("Menu")
    _vStream = cvStreamOpt().TryConnectvStream() # "vStream non installer!" TryConnectvStream()
    _ChercheBackgroud = TryChercheBackgroud()
    # Création de la liste d'élément.
    xbmc.log(str(Menu.items()))
    for tag, (Titre, Act, is_folder) in Menu.items():
        if ((_vStream == "OK" and Titre == "vStream")or
        (_ChercheBackgroud == "OK" and Titre == "ChangeFonDecran")or
        (Titre != "vStream" and Titre != "ChangeFonDecran")):
            if Titre == "TV":
                icone = _ArtMenu['lecture']
            else:
                icone = _ArtMenu['param']
            addDir(tag,'{0}?action=Menu&ElemMenu={1}&Option={2}'.format(_url, Act, Titre),1,icone,icone,is_folder)
    if Menu==_MenuList:
        # Création de chaque élément
        if _vStream != "OK":
            addDir(_vStream,'{0}?action=Menu&ElemMenu={1}'.format(_url, 'InstallvStream'),1,_ArtMenu['info'],_ArtMenu['fanar'],True)
    xbmcplugin.setPluginCategory( handle=int(sys.argv[1]), category="xAmAx" )
    xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
    

def addDir(name,url,mode,iconimage,fanart,is_Folder,infos={},cat=''):
    u  =url#sys.argv[0]+"?url="+urllib.quote(url)+"&mode="+str(mode)+"&name="+urllib.quote(name)+"&iconimage="+urllib.quote(iconimage)+"&cat="+urllib.quote(cat)
    ok =True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    infos['Title'] = name
    liz.setInfo( type="Video", infoLabels=infos )
    liz.setProperty('Fanart_Image',fanart)
    ok =xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_Folder)
    return ok

def AfichListeTS(ListeChaine=[], Table="ListePrincipale", Colon="Nom, Url", Where="", Ordre="Nom", Bouquet=""):
    if len(ListeChaine)>0:
        for Nom, Url, Entete in ListeChaine:
            addDir(Nom,'{0}?action=Play&Url={1}&ElemMenu={2}'.format(_url, urlib.quote_plus(Url+"|"+Entete), "LireVideo"),1,_ArtMenu['thumb'],_ArtMenu['fanar'],True)
    else:
        dbxAmAx = os.path.join(AdressePlugin, "Ressources", "xAmAx.db")
        xbmc.log("Ouverture Liste TV de: "+dbxAmAx+ "Table: "+Table+" Colon: "+Colon+" Where: "+Where+" Ordre: "+Ordre)
        NewDB = lite.connect(dbxAmAx)
        i = 0
        cUrl = NewDB.cursor()
        if Bouquet!="":
            xbmc.log("Ouverture Bouquet: "+Bouquet)
            cUrl.execute("SELECT IDBouquet, TriDesUrl FROM Bouquet WHERE NomBouq='"+Bouquet+"' ;")
            IdBouq=0
            OrdreB=""
            for IdBouquet,OrdreBouq in cUrl:
                IdBouq=IdBouquet
                OrdreB=OrdreBouq
            Where="IdBouquet="+str(IdBouq)
            Colon="NomAffichChaine, Url"
            Ordre=OrdreB
            Table="UrlBouquet"
        if Where=="":
            cUrl.execute("SELECT "+Colon+" FROM "+Table+" ORDER BY "+Ordre+";")
        else:
            cUrl.execute("SELECT "+Colon+" FROM "+Table+" WHERE "+Where+" ORDER BY "+Ordre+";")
        xbmc.log("Creation Liste de chaine a afficher...")
        for Nom, Url in cUrl:
            #xbmc.log(cname+"\n"+curl)
            i += 1
            addDir(str(i)+"-"+Nom,'{0}?action=Play&Url={1}&ElemMenu={2}'.format(_url, urlib.quote_plus(Url), "LireVideo"),1,_ArtMenu['thumb'],_ArtMenu['fanar'],True)
            #xbmc.log("Affiche Chaine: "+str(i)+" - "+Nom)
        try:
            if cUrl:
                cUrl.close()
        except: pass
        try:
            if NewDB:
                NewDB.commit()
                NewDB.close()
        except: pass
    xbmcplugin.setPluginCategory(handle=int(sys.argv[1]), category="lecture" )
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def TryChercheBackgroud():
    #try:
    NomSkin = xbmc.getSkinDir()
    xbmc.log("skindir: "+NomSkin)
    Defaut = os.path.join(xbmc.translatePath('special://home/addons/'),NomSkin,"backgrounds")
    if ((NomSkin == "skin.confluence")or(NomSkin == "skin.qonfluence")):
        with open(os.path.join(xbmc.translatePath('special://home/'),"userdata","addon_data",NomSkin,"settings.xml")) as f:
            Retour = f.read()
        f.closed
        ModifSkin = Retour.split('<setting id="UseCustomBackground" type="bool">')[1].split("</setting>")[0]
        if ModifSkin == 'true':
            ModifSkin = Retour.split('<setting id="CustomBackgroundPath" type="string">')[1].split("</setting>")[0]
            if xbmcvfs.exists(ModifSkin):
                Param["Chemin"]=ModifSkin
                return "OK"
            elif xbmcvfs.exists(os.path.join(Defaut,"SKINDEFAULT.jpg")):
                Param["Chemin"]=os.path.join(Defaut,"SKINDEFAULT.jpg")
                return "OK"
            else:
                return "Fond d'écran indisponible!"
        else:
            if xbmcvfs.exists(os.path.join(Defaut,"SKINDEFAULT.jpg")):
                Param["Chemin"]=os.path.join(Defaut,"SKINDEFAULT.jpg")
                return "OK"
            else:
                return "Fond d'écran indisponible!"
    elif(NomSkin == "skin.aeon.nox.5"):
        if xbmcvfs.exists(os.path.join(Defaut,"default_bg.jpg")):
            Param["Chemin"]=os.path.join(Defaut,"default_bg.jpg")
            return "OK"
        else:
            return "Fond d'écran indisponible!"
    else:
        return "Fond d'écran indisponible!"
    #except:
    #        return "Fond d'écran indisponible!"

def TelechargementZip(url,dest):
    dp = xbmcgui.DialogProgress()
    dp.create("Telechargement Mise a jour:","Fichier en téléchargement",url)
    try:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
    except:
        xbmc.log("Téléchargement de: " + url)
        xbmc.log("Téléchargement dans le dossier: " + dest)
        req = urllib.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        essai = urllib.urlopen(req)#.decode('utf-8'))
        fichier = open(dest, "wb")
        fichier.write(essai.read())
        fichier.close()

def RechercheMAJ():
    from Ressources.ziptools import ziptools
    xbmc.log('xAmAx Recherche mise a jour...')
    try:
        data = urllib.urlopen(Url_Plugin_Version).read()
        xbmc.log('Lecture de la version du plugin distant: ' + data)
    except:
        data = ""
        xbmc.log('Erreur de la lecture de la version du plugin: ' + Url_Plugin_Version)
        
    version_publique=data
    try:
        numVersionPub = version_publique.split(".")
        xbmc.log('xAmAx version publique:' + version_publique)
        numVersionLoc = __version__.split(".")
        xbmc.log('xAmAx version locale:' + __version__)
    except:
        version_publique = ""
        xbmc.log('xAmAx version locale:' + __version__)
        xbmc.log('Check fail !@*')
    xbmc.log('xAmAx version Publique: ' + str(numVersionPub) +  ' version locale: ' + str(numVersionLoc))
    if version_publique!="" and __version__!="" and len(numVersionPub)==3 and len(numVersionLoc)==3:
        if ((int(numVersionPub[0]) > int(numVersionLoc[0]))or
            ((int(numVersionPub[0]) == int(numVersionLoc[0]))and((int(numVersionPub[1]) > int(numVersionLoc[1]))or
                                                                ((int(numVersionPub[2]) > int(numVersionLoc[2])))))):

            extpath = os.path.join(xbmc.translatePath("special://home/addons/"))
            addon_data_dir = os.path.join(xbmc.translatePath("special://userdata/addon_data" ), nomPlugin)
            try:
                xbmcvfs.mkdir(addon_data_dir)
            except: pass
            dest = os.path.join(addon_data_dir, 'DerMaj.zip')
            MAJ_URL = 'https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/repo/'+nomPlugin+'/'+nomPlugin+'-' +str(int(numVersionPub[0]))+"."+str(int(numVersionPub[1]))+"."+str(int(numVersionPub[2])) + '.zip'
            xbmc.log('Démarrage du téléchargement de:' + MAJ_URL)
                
            TelechargementZip(MAJ_URL,dest)

            unzipper = ziptools()
            unzipper.extract(dest,extpath)
                
            lign1 = 'Nouvelle version installer .....'
            lign2 = 'Version: ' + version_publique 
            xbmcgui.Dialog().ok('xAmAx', lign1, lign2)
                
            if os.remove( dest ):
                xbmc.log('Suppression du fichier télécharger')
            xbmc.executebuiltin("UpdateLocalAddons")
            xbmc.executebuiltin("UpdateAddonRepos")
            xbmc.sleep(1500)
            return "OK"
        else:
            return "Pas de mise à jour disponible! \nVersion Internet: " + version_publique + "Version Actuelle: " + __version__
    else:
        return "Pas de mise à jour disponible!"
    
def Efface_thumb(env):
    if (env == 'fi'):
        try:
            path = xbmc.translatePath('special://temp/')
            filenames = next(os.walk(path))[2]
            for i in filenames:
                if ".fi" in i:
                    os.remove(os.path.join(path, i))
            return "OK"
        except:
            return "Erreur de suppression des fichiers temporaires"

    elif (env == 'thumb'):
        try:
            path = xbmc.translatePath('special://userdata/Thumbnails/')
            path2 = xbmc.translatePath('special://userdata/Database/')
            for i in os.listdir(path):
                folders = os.path.join(path, i)
                if os.path.isdir(folders):
                    p = next(os.walk(folders))[2]
                    for x in p:
                        os.remove(os.path.join(folders, x))

            filenames = next(os.walk(path2))[2]
            for x in filenames:
                if "exture" in x:
                    con = lite.connect(os.path.join(path2, x))
                    cursor = con.cursor()
                    cursor.execute("DELETE FROM texture")
                    con.commit()
                    cursor.close()
                    con.close()
            return "OK"
        except:
            return "Erreur de suppression des miniatures"


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
            if params['action'] == 'Menu':
                
                if params['Option'] =="TV":
                    if params['ElemMenu']=="VisuLiveStream":
                        dbxAmAx = os.path.join(AdressePlugin, "Ressources", "xAmAx.db")
                        xbmc.log("Ouverture Liste Bouquet de: "+dbxAmAx)
                        NewDB = lite.connect(dbxAmAx)
                        cUrl = NewDB.cursor()
                        cUrl.execute("SELECT NomBouq FROM Bouquet ORDER BY Ordre ;")
                        for NomBouq in cUrl:
                            _MenuTV.update({"Bouquet "+str(NomBouq[0]): ("TV","Bouq"+str(NomBouq[0]),True)})
                        cUrl.close()
                        NewDB.close()
                        AfficheMenu(_MenuTV)
                    if params['ElemMenu']=='AffichTV':
                        AfichListeTS()
                    if params['ElemMenu']=='MajTV':
                        Retour2 = cLiveSPOpt().RechercheChaine(AdressePlugin)
                        if Retour2=="OK":
                            cLiveSPOpt().CreerBouquet(AdressePlugin)
                            AfichListeTS()
                        else:
                            dialog = xbmcgui.Dialog()
                            ok = dialog.ok("Erreur chaines TV", Retour2)
                    if params['ElemMenu'][:4]=="Bouq":
                        AfichListeTS(Bouquet=params['ElemMenu'][4:])

                if params['Option']=='vStream':
                    if params['ElemMenu']=="VisuVstream":
                        AfficheMenu(_MenuvStream)
                    if params['ElemMenu']=='MPVstream':
                        Retour = cvStreamOpt().MiseAJourVstream("MarquePage")
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Trier les Marques-Pages vStream", Retour)
                    if params['ElemMenu']=='RechercheVstream':
                        Retour = cvStreamOpt().MiseAJourVstream("Recherche")
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Trier la liste de Recherche vStream", Retour)
                    
                if params['Option']=="Kodi":
                    if params['ElemMenu']=="VisuKodi":
                        AfficheMenu(_MenuKodi)
                    if params['ElemMenu']=="AffichLog":
                        xbmc.log("AffichLog: ")
                        Affich=LogAffich()
                        Affich.Fenetre(Chemin=xbmc.translatePath('special://logpath')+"kodi.log",
                                        line_number=0,Invertion=True,LabTitre="Journal d'erreur")
                    if params['ElemMenu']=='ChangeFonDecran':
                        xbmc.log("ChangeFonDecran")
                        _ChercheBackgroud = TryChercheBackgroud()
                        if _ChercheBackgroud == "OK":
                            CheminSplit = Param["Chemin"][:Param["Chemin"].rfind("/")+1]
                            NomFichier = Param["Chemin"][Param["Chemin"].rfind("/")+1:]
                            Extension = NomFichier[-4:]
                            NomFichier = NomFichier[:-4]
                            xbmc.log(CheminSplit+" "+NomFichier+" "+Extension)
                            Efface_thumb('thumb')
                            dialog = xbmcgui.Dialog()
                            Defaut = CheminSplit
                            fn = dialog.browse(2, "Choisir l'image de fond d'écran", 'files', '.jpg,.png',
                                               True, False, Defaut)
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
                                        ok = dialog.ok("Erreur de recherche du fond d'ecran",
                                                       "Le font d'écran n'a pas pu être modifier!!!",
                                                       "       DESOLE!!!")
                        else:
                            dialog = xbmcgui.Dialog()
                            ok = dialog.ok("Erreur de copy du fichier",_ChercheBackgroud)
                    if params['ElemMenu']=="SupTemp":
                        xbmc.log("SupTemp")
                        dialog = xbmcgui.Dialog()
                        if dialog.yesno('Effacer les fichier temporaires...', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                            Retour = Efface_thumb('fi')
                            if Retour=="OK":
                                xbmc.executebuiltin("XBMC.Notification(Effacement des fichiers temporaires ,OK,2000,"")")
                            else:
                                xbmc.executebuiltin("XBMC.Notification(Effacement des fichiers temporaires ," + Retour + ",2000,"")")
                                
                    if params['ElemMenu']=="SupThumb":
                        xbmc.log("SupThumb")
                        dialog = xbmcgui.Dialog()
                        if dialog.yesno('Effacer les miniatures...', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                            Retour=Efface_thumb('thumb')
                            if Retour=="OK":
                                xbmc.executebuiltin("XBMC.Notification(Effacement Miniatures ,OK,2000,"")")
                            else:
                                xbmc.executebuiltin("XBMC.Notification(Effacement Miniatures ,"+Retour+",2000,"")")
                
                if params['Option']=="xAmAx":
                    if params['ElemMenu']=="VisuxAmAx":
                        xbmc.log("Afficher menu xAmAx")
                        AfficheMenu(_MenuxAmAx)
                    if params['ElemMenu']=="InfoVersion":
                        xbmc.log("InfoVersion: ")
                        Affich=LogAffich()
                        Affich.Fenetre(Chemin=os.path.join(AdressePlugin,"changelog.txt"),line_number=0)
                    if params['ElemMenu']=="MiseAJourxAmAx":
                        Retour = RechercheMAJ()
                        if Retour != "OK":
                            dialog = xbmcgui.Dialog()
                            ok = dialog.ok("Mise à jour xAmAx", Retour)
                    if params['ElemMenu']=="test":
                        xbmc.log("test: ")
                        cLiveSPOpt().CreerBouquet(AdressePlugin)
                
                if params['ElemMenu']=="PluginLSP":
                    xbmc.executebuiltin('XBMC.RunPlugin(plugin://plugin.video.live.streamspro/)')
                    
            if params['action'] == 'Play':
                if params['ElemMenu']=="LireVideo":
                    finalUrl=params['Url']
                    xbmc.log("Lecture de: "+finalUrl) 
                    xbmc.executebuiltin('XBMC.RunPlugin('+finalUrl+')')
        else:
            # Affichage du menu si aucune action
            #xbmc.log("Affichage Menux")
            AfficheMenu()
            #xbmcplugin.endOfDirectory(_handle,succeeded=True)
if __name__ == '__main__':
        
        xbmc.log("Demarrage xAmAx: commande = " + str(sys.argv[2]))
        # Envoi des paramètre du menu
        router(sys.argv[2][1:])
