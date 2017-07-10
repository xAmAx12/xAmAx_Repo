# -*- coding: utf-8 -*-
# Module: default
# Author: xamax
# Created on: 29.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import re
import sys
import sqlite3 as lite
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import urllib2 as urllib
import urllib as urlib
import base64
from random import randint
from urlparse import parse_qsl
from time import gmtime, strftime
from resources.vStreamOpt import cvStreamOpt
from resources.LSPOpt import cLiveSPOpt
#import resources.test as test
    
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
            "Ouvrir fichier m3u avec le lecteur de kodi":("xAmAx","LireUrl",True),
            "Ouvrir fichier m3u avec le lecteur F4m":("xAmAx","LireF4m",True),
           "Options de vStream (Film et séries)":("vStream","VisuVstream",True),
           "Options de Kodi":("Kodi","VisuKodi",True),
           "Options de xAmAx":("xAmAx",'VisuxAmAx',True)}
_MenuxAmAx={"Version "+__version__:("xAmAx","InfoVersion",False),
           "Mise a jour de xAmAx":("xAmAx",'MiseAJourxAmAx',True),
            "Paramètres de xAmAx":("xAmAx","ParamxAmAx",False)}#,"test":("xAmAx",'test',True)}
_MenuvStream={"Trier la liste de Recherche vStream":("vStream","RechercheVstream",True),
           "Trier les Marques-Pages vStream":("vStream","MPVstream",True)}
_MenuTV={"Afficher Les chaines Tv":("TV","AffichTV",True),
           "Mise A Jour Liste de chaines":("TV","MajTV",True)}
_MenuKodi={"Afficher le Journal d'erreur":("Kodi","AffichLog",False),
           "Changer le Fond d'écran":("Kodi",'ChangeFonDecran',True),
           "Effacer le fichiers temporaires":("Kodi","SupTemp",True),
           "Effacer les miniatures en mémoire":("Kodi","SupThumb",True)}
_MenuPC={"Afficher l'historique":("PC","AffichLog",True),
         "Réaliser une action":("PC","ActPC",True)}
_MenuActPC={"Changer heure d'arrêt":("PC","ActHArret",True),
            "Arrêter le pc":("PC","ActArretDirect",True),
            "Arrêt de l'arrêt automatique":("PC","ActArretAuto",True),
            "Re-démarrage de l'arrêt automatique":("PC","ActDemarArret",True),
            "Interrogation Heure d'arrêt":("PC","ActIHArret",True),
            "Interrogation Heure du pc":("PC","ActHeurePC",True)}

class LogAffich():
    def Fenetre(self,Chemin="",line_number=0,Invertion=False,LabTitre="xAmAx "+__version__,Texte=''):
        #try:
        xbmc.log("Fenetre de lecture de texte")
        xbmc.executebuiltin("ActivateWindow(10147)") #10147
        window = xbmcgui.Window(10147)
        #window.getControl(1).setLabel(LabTitre)
        
        if Texte=='':
            Texte = self.getcontent(Chemin,line_number,Invertion)
        xbmc.sleep(500)
        window.getControl(5).setText(Texte)
        xbmc.sleep(200)
        #except:
        #    pass
    def getcontent(self,Chemin="",line_number=0,Invertion=False):
        xbmc.log("Récupération fichier texte")
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
        xbmc.log("Affichage du texte")
        return contents.replace(
            ' ERROR: ',' [COLOR red]ERREUR[/COLOR]: ').replace(
            ' WARNING: ',' [COLOR gold]AVERTISSEMENT[/COLOR]: ').replace(
            ' NOTICE: ',' [COLOR green]INFO[/COLOR]: ').replace(
            '- Version ',' [COLOR green]- Version[/COLOR]: ').replace(
            '=======================================================================================',
            '[COLOR green]=======================================================================================[/COLOR]')
    

def AfficheMenu(Menu=_MenuList, Icone=False):
    # creation du menu
    xbmc.log("Menu")
    # Création de la liste d'élément.
    if not Icone:
        _vStream = cvStreamOpt().TryConnectvStream() # "vStream non installer!" TryConnectvStream()
        _ChercheBackgroud = TryChercheBackgroud()
        for tag, (Titre, Act, is_folder) in Menu.items():
            if ((_vStream == "OK" and Titre == "vStream")or
            (_ChercheBackgroud == "OK" and Titre == "ChangeFonDecran")or
            (Titre != "vStream" and Titre != "ChangeFonDecran")):
                if Titre == "TV":
                    icone = _ArtMenu['lecture']
                else:
                    icone = _ArtMenu['param']
                addDir(tag,
                       '{0}?action=Menu&ElemMenu={1}&Option={2}'.format(_url, Act, Titre),
                       1,
                       icone,
                       icone,
                       is_folder)
    else:
        for tag, (Titre, Url, is_folder, icone, Tmage) in Menu.items():
            if icone != "":
                text = base64.b64decode(str(Titre)).replace('&#8211;','-')
                text = text.replace('&ndash;','-')
                text = text.replace('&#038;','&')
                text = text.replace('&#8217;','\'')
                text = text.replace('&#8216;','\'')
                text = text.replace('&#8230;','...')
                text = text.replace('&quot;','"')
                text = text.replace('&#039;','`')
                text = text.replace('&amp;','&')
                text = text.replace('&ntilde;','ñ')
                Titre = text.replace('&rsquo;','\'')   
                #xbmc.log("list m3u: "+Titre+' {0}?action=Play&Url={1}&ElemMenu={2}&Tmage={3}'.format(_url,Url,"LireVideo2",Tmage)+" Icone= "+base64.b64decode(icone))
                if base64.b64decode(icone)==_ArtMenu['lecture']:
                    addDir(Titre,
                           '{0}?action=Play&Url={1}&ElemMenu={2}&Adult=0'.format(_url,Url,"LireVideo2"),
                           1,
                           _ArtMenu['lecture'],
                           _ArtMenu['lecture'],
                           is_folder)
                elif base64.b64decode(icone)==_ArtMenu['info']:
                    URL=base64.b64decode(str(Url))
                    cCommands=[]
                    cCommands.append(("Lire le Fichier",
                                      'XBMC.RunPlugin({0}?action=OuvTxt&Url={1}&ElemMenu={2})'.format(_url,base64.b64encode(URL[3:]),"LogSamba")))
                    cCommands.append(("Supprimer le fichier",
                                      'XBMC.RunPlugin({0}?action=SupFich&Url={1}&ElemMenu={2})'.format(_url,
                                                                                                        base64.b64encode(URL[3:]),
                                                                                                        "LogSamba")))
                    if URL.startswith("LOG"):
                        addDir(Titre,
                           '{0}?action=OuvTxt&Url={1}&ElemMenu={2}'.format(_url,base64.b64encode(URL[3:]),"LogSamba"),
                           1,
                           _ArtMenu['lecture'],
                           _ArtMenu['lecture'],
                           is_folder,
                           contextCommands=cCommands)
                else:
                    cCommands=[]
                    cCommands.append(("Telecharger vidéo",
                                      'XBMC.RunPlugin({0}?action=Play&Url={1}&ElemMenu={2}&Adult=1)'.format(_url,Url,"DL")))
                    cCommands.append(("Afficher les photos",
                                      'XBMC.RunPlugin({0}?action=FichierEnCour&ElemMenu={1}&Adult=1&Icone={2}&timage={3})'.format(_url,
                                                                                                                                  "Photo",
                                                                                                                                  base64.b64decode(icone),
                                                                                                                                  Tmage)))
                    RetAdd = addDir(Titre,
                                    '{0}?action=Play&Url={1}&ElemMenu={2}&Adult=1'.format(_url,Url,"LireVideo2"),
                                    1,
                                    base64.b64decode(icone),
                                    _ArtMenu['lecture'],
                                    is_folder,
                                    contextCommands=cCommands)
            else:
                addDir(base64.b64decode(Titre),
                       '{0}?action=Menu&ElemMenu={1}&Option={2}&Url={3}'.format(_url,"Adult","TV",Url),
                       1,
                       _ArtMenu['lecture'],
                       _ArtMenu['lecture'],
                       True)
    if Menu==_MenuList:
        # Création de chaque élément
        if _vStream != "OK":
            addDir(_vStream,
                   '{0}?action=Menu&ElemMenu={1}'.format(_url, 'InstallvStream'),
                   1,
                   _ArtMenu['info'],
                   _ArtMenu['fanar'],
                   True)
        if addon.getSetting(id="Adult")=="true":
            addDir("Plus",
                   '{0}?action=Menu&ElemMenu={1}&Option={2}'.format(_url, "Adult", 'TV'),
                   1,
                   _ArtMenu['lecture'],
                   _ArtMenu['fanar'],
                   True)
        if addon.getSetting(id="stban")=="true":
            addDir("PC distant",
                   '{0}?action=Menu&ElemMenu={1}&Option={2}'.format(_url, "stBan", 'PC'),
                   1,
                   _ArtMenu['lecture'],
                   _ArtMenu['fanar'],
                   True)
            
    xbmcplugin.setPluginCategory( handle=int(sys.argv[1]), category="xAmAx" )
    xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
        

def MajMenuRegroup():
    _MenuRegroup={}
    dbxAmAx = os.path.join(AdressePlugin, "resources", "xAmAx.db")
    xbmc.log("Ouverture Liste Regroup de: "+dbxAmAx)
    NewDB = lite.connect(dbxAmAx)
    cUrl = NewDB.cursor()
    cUrl2 = NewDB.cursor()
    AffichAutre = False
    listID=[]
    for numTab in range(1,5):
        cUrl.execute("SELECT NomAffiche,NomRegroup, PasDansNom FROM RegroupChaine ORDER BY NomAffiche ;")
        cUrl2.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='List"+str(numTab)+"';")
        Retour = cUrl2.fetchall()
        if len(Retour)==1:
            for Affich, Nom, PasNom in cUrl:
                if PasNom != None and PasNom != "":
                    ANDWHERE = "AND Nom NOT LIKE '%"+PasNom+"%' "
                else:
                    ANDWHERE = ""
                cUrl2.execute("SELECT IDLP FROM List"+str(numTab)+" WHERE Nom LIKE '"+str(Nom)+"%' "+ANDWHERE+"ORDER BY Nom;") # 
                Retour = cUrl2.fetchall()
                if len(Retour)> 0:
                    for IDLP in Retour:
                        listID.append(str(IDLP[0]))
                    _MenuRegroup.update({str(Affich).replace("_"," "): ("TV","ChaineRegroup"+base64.b64encode(str(Nom)),True)})
            addon.setSetting(id="ListAutre", value=str(listID).replace("[","(").replace("]",")").replace("'",""))
            cUrl2.execute("SELECT IDLP FROM List"+str(numTab)+" WHERE IDLP NOT IN "+str(listID).replace("[","(").replace("]",")").replace("'","")+" ;")
            if len(cUrl2.fetchall())>0:
                AffichAutre = True
    if AffichAutre:
        _MenuRegroup.update({"ZZZ Les autres chaines": ("TV","ChaineRegroupLesAutres",True)})
    cUrl.close()
    cUrl2.close()
    NewDB.close()
    return _MenuRegroup
    
def AffichMenuTv():
    if addon.getSetting(id="MajtvAuto")=="true":
        xbmc.log("Recherche mise a jour si première ouverture de la journée")
        DateDerMajTv = str(addon.getSetting(id="DateTvListe"))
        xbmc.log("Dernière Mise a jour: "+DateDerMajTv)
        if str(DateDerMajTv)!=strftime("%d-%m-%Y", gmtime()):
            Retour = cLiveSPOpt().RechercheChaine(AdressePlugin)
            if Retour=="OK":
                if addon.getSetting(id="CreerBouq")=="true":
                    cLiveSPOpt().CreerBouquet(AdressePlugin)
                addon.setSetting(id="DateTvListe", value=strftime("%d-%m-%Y", gmtime())) #%H:%M:%S"
    if addon.getSetting(id="CreerBouq")=="true":
        dbxAmAx = os.path.join(AdressePlugin, "resources", "xAmAx.db")
        xbmc.log("Ouverture Liste Bouquet de: "+dbxAmAx)
        NewDB = lite.connect(dbxAmAx)
        cUrl = NewDB.cursor()
        cUrl.execute("SELECT NomBouq FROM Bouquet ORDER BY Ordre ;")
        for NomBouq in cUrl:
            _MenuTV.update({"Bouquet "+str(NomBouq[0]): ("TV","Bouq"+str(NomBouq[0]),True)})
        cUrl.close()
        NewDB.close()
    AfficheMenu(_MenuTV)
    
def addDir(name,url,mode,iconimage,fanart,is_Folder,infos={},cat='',contextCommands=[]):
    u  =url
    ok =True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="Video", infoLabels=infos )
    liz.setProperty('Fanart_Image',fanart)
    if len(contextCommands)>0:
        liz.addContextMenuItems ( contextCommands, replaceItems=False)
        
    ok =xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_Folder)
    return ok

def AfichListeTS(ListeChaine=[], Colon="Nom, Url", Where="", Ordre="Nom", Bouquet=""):
    if len(ListeChaine)>0:
        for Nom, Url, Entete in ListeChaine:
            addDir(Nom,'{0}?action=Play&Url={1}&ElemMenu={2}'.format(_url, urlib.quote_plus(Url+"|"+Entete), "LireVideo"),1,_ArtMenu['thumb'],_ArtMenu['fanar'],True)
    else:
        dbxAmAx = os.path.join(AdressePlugin, "resources", "xAmAx.db")
        #xbmc.log("Ouverture Liste TV de: "+dbxAmAx+ " Table: "+Table+" Colon: "+Colon+" Where: "+Where+" Ordre: "+Ordre)
        NewDB = lite.connect(dbxAmAx)
        i = 0
        cUrl = NewDB.cursor()
        for numTab in range(1,5):
            Table="List"+str(numTab)
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
        try:
            with open(os.path.join(xbmc.translatePath('special://home/'),"userdata","addon_data",NomSkin,"settings.xml")) as f:
                Ret = f.read()
            f.closed
            ModifSkin = Ret.split('<setting id="UseCustomBackground" type="bool">')[1].split("</setting>")[0]
        except:
            ModifSkin = 'false'
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

def TelechargementZip(url,dest,DPAff=True):
    if DPAff:
        dp = xbmcgui.DialogProgress()
        dp.create("Telechargement Mise a jour:","Fichier en téléchargement",url)
    try:
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url=url: _pbhook(nb,bs,fs,url,dp))
    except:
        xbmc.log("Téléchargement de: " + url)
        xbmc.log("Téléchargement dans le dossier: " + dest)
        req = urllib.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; rv:22.0) Gecko/20100101 Firefox/22.0')
        essai = urllib.urlopen(req)
        fichier = open(dest, "wb")
        fichier.write(essai.read())
        fichier.close()

def DLFich(url,dest, DPView=True):
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

def RechercheMAJ():
    from resources.ziptools import ziptools
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

def MajAuto(NomMaj):
    if NomMaj=="default":
        resources = ""
        Ext=".py"
        AdresseFich = os.path.join(AdressePlugin, NomMaj+Ext)
    else:
        resources = "resources/"
        if NomMaj=="xAmAx":
            Ext=".db"
        elif NomMaj=="settings":
            Ext=".xml"
        else:
            Ext=".py"
        AdresseFich = os.path.join(AdressePlugin, "resources", NomMaj+Ext)
    try:
        AdresseVersion = "https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/plugin.video.xAmAx/"+resources+NomMaj
        VRech = urllib.urlopen(AdresseVersion).read()
        VLspopt = addon.getSetting(id=NomMaj)
        xbmc.log("Version "+NomMaj+": "+VLspopt+" Version sur internet: "+VRech)
        if VLspopt!=str(VRech):
            DL = urllib.urlopen("https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/plugin.video.xAmAx/"+resources+NomMaj+Ext).read()
            fichier = open(AdresseFich, "w")
            fichier.write(DL)
            fichier.close()
            addon.setSetting(id=NomMaj, value=str(VRech))
            xbmc.log("Mise a jour de "+NomMaj+" OK")
            return True
        else:
            return False
    except:
        xbmc.log("Erreur mise a jour: "+str(sys.exc_info()[0]))
        

    
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

def ConvAction(TitreCmd):
    FichSauv = ""
    dialog = xbmcgui.Dialog()
    
    for i in range(10):
        FichSauv += chr(randint(33,122))
    if TitreCmd == "ArretAuto":
        ret = dialog.yesno("Arrêt de l'arrêt automatique", "Voulez-vous vraiment arrêter l'arrêt automatique?","",nolabel="NON",yeslabel="OUI")
        if ret:
            return FichSauv+"ArretMyApp"
    elif TitreCmd == "HArret":
        Henvoi = ""
        HDemar = ""
        HArret = ""
        HArret = dialog.input("Entrer l'heure d'arret du pc", type=xbmcgui.INPUT_TIME) #, default="22.00"
        if HArret != "" and len(HArret)==5:
            HArret=HArret.replace(" ","0")
            HDemar = dialog.input("Entrer l'heure de démarrage du pc", type=xbmcgui.INPUT_TIME) #, default="09.00"
            if HDemar != "" and len(HDemar)==5:
                HDemar=HDemar.replace(" ","0")
                if HArret[:2]<HDemar[:2]:
                    Henvoi = HDemar+"."+HArret
                else:
                    Henvoi = HArret+"."+HDemar
                ret = dialog.yesno("Changer l'heure d'arrêt", "Voulez-vous vraiment que le PC s'arrête à "+HArret+" et ne puisse redémarrer que à "+HDemar+" ?","",nolabel="NON",yeslabel="OUI")
                if ret:
                    print "heure d'arret: "+HArret+"\r\n"+"heure de démarrage: "+HDemar
                    return FichSauv+"AjDateArret"+"\r\n1\r\n"+Henvoi
    elif TitreCmd == "DemarArret":
        ret = dialog.yesno("Redémarrer l'arrêt automatique", "Voulez-vous vraiment redémarrer l'arrêt automatique?","",nolabel="NON",yeslabel="OUI")
        if ret:
            return FichSauv+"DemarMyApp"
    elif TitreCmd == "ArretDirect":
        ret = dialog.yesno("Arrêt du PC", "Voulez-vous vraiment arrêter le PC maintenant?","",nolabel="NON",yeslabel="OUI")
        if ret:
            return FichSauv+"ArretPC"
    elif TitreCmd == "IHArret":
        ret = dialog.yesno("Interrogation Heure d'arrêt", "L'heure d'arrêt sera consutable dans le fichier Rep.xama de l'historique!", "Voulez-vous vraiment connaître l'heure d'arret?",nolabel="NON",yeslabel="OUI")
        if ret:
            return FichSauv+"HeureArret"
    elif TitreCmd == "HeurePC":
        ret = dialog.yesno("Interrogation Heure du pc", "L'heure du PC sera consutable dans le fichier Rep.xama de l'historique!", "Voulez-vous vraiment connaître l'heure du PC?",nolabel="NON",yeslabel="OUI")
        if ret:
            return FichSauv+"HeureEC"

    return ""

def router(paramstring):
    xbmc.log("dans router")
    # reception des paramètres du menu
    if len(paramstring)>=2:
        params = dict(parse_qsl(paramstring))
    else:
        params = None
    # Si aucun paramètre on ouvre le menu
    if params:
        xbmc.log(str(params))
        if params['action'] == 'Menu':
            
            if params['Option'] =="TV":#----------------------------------------------------------------------------------------
                if params['ElemMenu']=="VisuLiveStream":
                    AffichMenuTv()
                if params['ElemMenu']=='AffichTV':
                    AfficheMenu(MajMenuRegroup())
                if params['ElemMenu']=='MajTV':
                    VRech = urllib.urlopen("https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/plugin.video.xAmAx/resources/LSPOpt").read()
                    VLspopt = addon.getSetting(id="LSPOpt")
                    xbmc.log("Version Recherche TV: "+VLspopt+" Version sur internet: "+VRech)
                    if VLspopt!=str(VRech):
                        LSPOpt = urllib.urlopen("https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/plugin.video.xAmAx/resources/LSPOpt.py").read()
                        dest = os.path.join(AdressePlugin, "resources", "LSPOpt.py")
                        fichier = open(dest, "w")
                        fichier.write(LSPOpt)
                        fichier.close()
                        addon.setSetting(id="LSPOpt", value=str(VRech))
                        
                    Retour2 = cLiveSPOpt().RechercheChaine(AdressePlugin)
                    if Retour2=="OK":
                        AffichMenuTv()
                    else:
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Erreur chaines TV", Retour2)
                if params['ElemMenu'][:4]=="Bouq":
                    AfichListeTS(Bouquet=params['ElemMenu'][4:])
                if params['ElemMenu'][:13]=="ChaineRegroup":
                    if params['ElemMenu'][13:]=="LesAutres":
                        AfichListeTS(Where="IDLP NOT IN "+str(addon.getSetting(id="ListAutre")))
                    else:
                        dbxAmAx = os.path.join(AdressePlugin, "resources", "xAmAx.db")
                        NomChaine = base64.b64decode(str(params['ElemMenu'][13:]))
                        xbmc.log("Recherche "+NomChaine+" dans le Liste Regroup de: "+dbxAmAx)
                        NewDB = lite.connect(dbxAmAx)
                        cUrl = NewDB.cursor()
                        cUrl.execute("SELECT PasDansNom FROM RegroupChaine WHERE NomRegroup = '"+NomChaine+"' ;")
                        Retour = cUrl.fetchall()
                        ANDWHERE = ""
                        if len(Retour)==1:
                            if Retour[0][0] != None and Retour[0][0] != "":
                                ANDWHERE = " AND Nom NOT LIKE '%"+Retour[0][0]+"%' "
                        AfichListeTS(Where="Nom LIKE '"+NomChaine+"%'"+ANDWHERE)
                if params['ElemMenu']=="Adult":
                    try:
                        Url = params['Url']
                        ListAff = cLiveSPOpt().AdulteSources(base64.b64decode(Url))
                    except:
                        ListAff = cLiveSPOpt().AdulteSources()
                    if len(ListAff)>0:
                        i=0
                        _MenuRegroup={}
                        for Url,Thumb,Timag,Nom in ListAff:
                            i+=1
                            Nom2=base64.b64encode(Nom)
                            Nom3=base64.b64encode(Nom+str(i))
                            Url=base64.b64encode(Url)
                            Thumb=base64.b64encode(Thumb)
                            Tima=base64.b64encode(str(Timag))
                            _MenuRegroup.update({Nom: (Nom2, Url, False, Thumb, Tima)})
                        AfficheMenu(_MenuRegroup,True)

            if params['Option']=='vStream':#----------------------------------------------------------------------------------------
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
                
            if params['Option']=="Kodi": #----------------------------------------------------------------------------------------
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
            
            if params['Option']=="xAmAx": #----------------------------------------------------------------------------------------
                if params['ElemMenu']=="VisuxAmAx":
                    xbmc.log("Afficher menu xAmAx")
                    if addon.getSetting(id="stban")=="true":
                        if addon.getSetting(id="p")=="":
                            _MenuxAmAx.update({"PC distant: Ajouter un Mot de passe": ("PC","PssPc",True)})
                        else:
                            _MenuxAmAx.update({"PC distant: Changer le Mot de passe": ("PC","PssPc",True)})
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
                    dirs, files = xbmcvfs.listdir("smb://192.168.1.1/echange")
                    if len(files)>0:
                        i=0
                        _MenuRegroup={}
                        for fich in files:
                            i+=1
                            _MenuRegroup.update({fich: (fich, "ActPC",True)})
                        AfficheMenu(_MenuRegroup)
                if params['ElemMenu']=="ParamxAmAx":
                    addon.openSettings()
                if params['ElemMenu']=="LireUrl":
                    ListAff = cLiveSPOpt().LireM3u(CheminxAmAx=AdressePlugin)
                    i=0
                    MenuRegroup={}
                    for Nom,Url in ListAff:
                        i+=1
                        Nom=base64.b64encode(Nom)
                        Url=base64.b64encode(Url)
                        Thumb=base64.b64encode(_ArtMenu['lecture'])
                        MenuRegroup.update({"Video"+str(i): (Nom, Url, True, Thumb,[])})
                    AfficheMenu(MenuRegroup,True)
                if params['ElemMenu']=="LireF4m":
                    ListAff = cLiveSPOpt().LireM3u(CheminxAmAx=AdressePlugin, F4m=True)
                    i=0
                    _MenuRegroup={}
                    for Nom,Url in ListAff:
                        i+=1
                        Nom=base64.b64encode(Nom)
                        Url=base64.b64encode(Url)
                        Thumb=base64.b64encode(_ArtMenu['lecture'])
                        _MenuRegroup.update({"Video"+str(i): (Nom, Url, True, Thumb,[])})
                    AfficheMenu(_MenuRegroup,True)

            if params['Option']=="PC": #----------------------------------------------------------------------------------------
                from resources.Samba import EnvSamba
                if params['ElemMenu']=="stBan":
                    xbmc.log("Afficher menu xAmAx")
                    dialog = xbmcgui.Dialog()
                    d = dialog.input('Entrer votre mot de passe', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                    if d == base64.b64decode(addon.getSetting(id="p")):
                        AfficheMenu(_MenuPC)
                    elif d!="":
                        d = dialog.ok('Verrification du mot de passe', "Mot de passe incorrect")
                if params['ElemMenu']=="PssPc":
                    dialog = xbmcgui.Dialog()
                    d = dialog.input('Entrer votre mot de passe actuel', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                    if d == base64.b64decode(addon.getSetting(id="p")):
                        d = dialog.input('Entrer votre nouveau mot de passe', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                        if d != "":
                            e = dialog.input('Entrer votre nouveau mot de passe une seconde fois', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                            if e == d:
                                addon.setSetting(id='p', value=base64.b64encode(e))
                                d = dialog.ok('Verrification du mot de passe', "Votre Mot de passe a était changer!")
                            else:
                                dialog.ok('Verrification du mot de passe', "Le mot de passe saisi n'est pas le même!", "Recommencer pour pouvoir modifier votre mot de passe!")
                        else:
                            d = dialog.ok('Verrification du mot de passe', "Votre Mot de passe n'a pas était changer")
                    elif d!="":
                        d = dialog.ok('Verrification du mot de passe', "Mot de passe incorrect")
                if params['ElemMenu']=="AffichLog":
                    List = EnvSamba(dosEchange = "echange").ListFichier()
                    _MenuRegroup={}
                    for F in List:
                        Nom=base64.b64encode(F)
                        Url=base64.b64encode("LOG"+F)
                        Thumb=base64.b64encode(_ArtMenu['info'])
                        _MenuRegroup.update({Nom: (Nom, Url, True, Thumb,[])})
                    AfficheMenu(_MenuRegroup,True)
                if params['ElemMenu']=="ActPC":
                    xbmc.log("Afficher menu xAmAx")
                    AfficheMenu(_MenuActPC)
                if params['ElemMenu'][:3]=="Act" and params['ElemMenu']!="ActPC":
                    Retour = ConvAction(TitreCmd=params['ElemMenu'][3:])
                    if Retour != "":
                        xbmc.log("**** Retour action: "+Retour)
                        ret = EnvSamba(dosEchange = "echange").EnvoiFichier(txtEchang=Retour,NomFich="Act.xama")
                        dialog = xbmcgui.Dialog()
                        if ret:
                            d = dialog.ok("Enregistrement de l'action OK", "Votre Action à bien était enregistré, elle sera active dans 5min maximum", "Dans l'historique vous pourez retrouver le résultat de l'opération dans le fichier Rep.xama!")
                            xbmc.log("**** Retour action: "+Retour)
                        else:
                            d = dialog.ok("Erreur enregistrement de l'action", "Votre Action n'a pas peu être enregistré!", "Veuillez verrifier votre connection!")
                            xbmc.log("**** Retour action: Erreur d'enregistrement")
                    
        if params['action'] == 'Play':
            if params['ElemMenu']=="LireVideo":
                finalUrl=params['Url']
                xbmc.log("Lecture de: "+finalUrl) 
                xbmc.executebuiltin('XBMC.RunPlugin('+finalUrl+')')
            if params['ElemMenu']=="LireVideo2":
                if params['Adult']=="1":
                    html = cLiveSPOpt().TelechargPage('http://www.mrsexe.com/' + base64.b64decode(params['Url']))
                    videourl = re.compile(r"src='(/inc/clic\.php\?video=.+?&cat=mrsex.+?)'").findall(html)
                    xbmc.log("--videourl = "+str(videourl[0]))
                    html = cLiveSPOpt().TelechargPage('http://www.mrsexe.com/' + videourl[0])
                    #xbmc.log("--html = "+html)
                    videourls = re.compile(r"'file': \"(.+?)\",.+?'label': '(.+?)'", re.DOTALL).findall(html)
                    videourls = sorted(videourls, key=lambda tup: tup[1], reverse=True)
                    xbmc.log("--videourl.. = "+(str(videourl[0])))
                    videourl = "http:"+str(videourls[0][0])
                else:
                    videourl = base64.b64decode(params['Url'])
                xbmc.log("Adresse video: "+str(videourl))
                if videourl.startswith("plugin://"):
                    xbmc.executebuiltin('XBMC.RunPlugin('+videourl+')')
                else:
                    listitem = xbmcgui.ListItem("essai1")
                    listitem.setInfo('video', {'Title': "essai1", 'Genre': 'essai'})
                    xbmc.Player().play(videourl, listitem)
            if params['ElemMenu']=="DL":
                dialog = xbmcgui.Dialog()
                if dialog.yesno('Telechargement du fichier...', 'Voulez-vous télécharger le fichier?','','','Non', 'Oui'):
                    if params['Adult']=="1":
                        html = cLiveSPOpt().TelechargPage('http://www.mrsexe.com/' + base64.b64decode(params['Url']))
                        videourl = re.compile(r"src='(/inc/clic\.php\?video=.+?&cat=mrsex.+?)'").findall(html)
                        xbmc.log("--videourl_DL = "+str(videourl[0]))
                        html = cLiveSPOpt().TelechargPage('http://www.mrsexe.com/' + videourl[0])
                        #xbmc.log("--html = "+html)
                        videourls = re.compile(r"'file': \"(.+?)\",.+?'label': '(.+?)'", re.DOTALL).findall(html)
                        videourls = sorted(videourls, key=lambda tup: tup[1], reverse=True)
                        xbmc.log("--videourl_DL.. = "+(str(videourl[0])))
                        videourl = "http:"+str(videourls[0][0])
                    else:
                        videourl = base64.b64decode(params['Url'])
                    
                    xbmc.log("Adresse video DL: "+str(videourl))
                    for i in range(0,999):
                        if i < 10:
                            NomFichVid = "vid00"+str(i)+".mp4"
                        elif i < 100:
                            NomFichVid = "vid0"+str(i)+".mp4"
                        else:
                            NomFichVid = "vid"+str(i)+".mp4"
                        if not xbmcvfs.exists(os.path.join(profile,NomFichVid)):
                            break
                    DLFich(videourl,os.path.join(profile,NomFichVid), DPView=True)
        if params['action'] == 'OuvTxt':
            if params['ElemMenu']=="LogSamba":
                from resources.Samba import EnvSamba
                Fich = base64.b64decode(params['Url'])
                FichLu = EnvSamba(dosEchange = "echange").OuvrirFich(Fich)
                Affich=LogAffich()
                Affich.Fenetre(Chemin="",LabTitre="Journal d'action",Texte=FichLu)
        if params['action'] == 'SupFich':
            if params['ElemMenu']=="LogSamba":
                from resources.Samba import EnvSamba
                Fich = base64.b64decode(params['Url'])
                ret = EnvSamba(dosEchange = "echange").SupprimFich(Fich)
                dialog = xbmcgui.Dialog()
                if ret==1:
                    d = dialog.ok("Suppression du fichier OK", "Votre fichier "+Fich+" a bien était supprimer", "")
                    xbmc.log("**** Supprimer fichier: "+Fich)
                else:
                    d = dialog.ok("Erreur supression de fichier", "Votre fichier "+Fich+" n'a pas pu être supprimer", "Veuillez verrifier votre connection!")
                    xbmc.log("**** Erreur supression: "+Fich)
                xbmc.executebuiltin('XBMC.Container.Update')
                xbmc.executebuiltin('XBMC.Container.Refresh')
                xbmc.sleep(200)
                xbmc.log("****** Retour Supprim= "+str(ret))
        if params['action'] == 'FichierEnCour':
            if params['ElemMenu']=="Label":
                win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                curctl = win.getFocusId()
                cursel = win.getControl( curctl ).getSelectedItem()
                label = cursel.getLabel()
                xbmc.log("Label= "+str(label))
            if params['ElemMenu']=="Photo":
                listPhoto = ""
                ListeImage = base64.b64decode(params['timage']).replace("[","").replace("]","").replace(chr(39),"").split(",")
                i=0
                cheminPhoto=os.path.join(profile,"photo")
                xbmcvfs.mkdir(cheminPhoto)
                Dir,Phot = xbmcvfs.listdir(cheminPhoto)
                for ph in Phot:
                    xbmcvfs.delete(os.path.join(cheminPhoto,ph))
                for photo in ListeImage:
                    i+=1
                    CheminFich = os.path.join(cheminPhoto,"Photo"+str(i)+".jpg")
                    if photo.startswith(" "):
                        photo = photo[1:]
                    listPhoto = params['Icone'][:params['Icone'].rfind("_")+1]+photo+params['Icone'][-4:]
                    TelechargementZip(listPhoto,CheminFich)       
                xbmc.executebuiltin('xbmc.SlideShow(' + cheminPhoto + ')') 
    else:
        # Affichage du menu si aucune action
        if addon.getSetting(id="MajAuto")=="true":
            xbmc.log("Recherche auto de Mise a jour: ")
            ret = False
            Sret = False
            MajAuto("xAmAx")
            MajAuto("settings")
            MajAuto("vStreamOpt")
            MajAuto("LSPOpt")
            ret = MajAuto("default")
            if addon.getSetting(id="stban")=="true":
                MajAuto("Samba")
            if ret == True:
                xbmc.executebuiltin('XBMC.Container.Update')
                xbmc.sleep(200)
                xbmc.executebuiltin('XBMC.Container.Refresh')
                xbmc.sleep(200)
        AfficheMenu()
if __name__ == '__main__':
        xbmc.log("Demarrage xAmAx: commande = " + str(sys.argv[2]))
        # Envoi des paramètres du menu
        router(sys.argv[2][1:])

