# -*- coding: utf-8 -*-
# Module: menu
# Author: xamax
# Created on: 23.07.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import os
import re
import sys
from xbmc import translatePath, executebuiltin, getSkinDir, Player
import xbmcgui
import xbmcplugin
from xbmcaddon import Addon
import xbmcvfs
import urllib as urlib
import base64
from urlparse import parse_qsl
from time import gmtime, strftime, sleep
from resources.vStreamOpt import cvStreamOpt
from resources.LSPOpt import cLiveSPOpt
from resources.DB import db
from resources.TxtAff import TxtAffich
from resources.Telecharg import cDL

class menu():

    def __init__(self):
        #Enregistrement des paramètres
        self.Param = {"Chemin":""}
        self.nomPlugin = 'plugin.video.xAmAx-Mod'
        self.adn = Addon(self.nomPlugin)

        self.__version__ = self.adn.getAddonInfo('version')
        self._vStream = cvStreamOpt().TryConnectvStream() # "vStream non installer!" TryConnectvStream()
        self._ChercheBackgroud = self.TryChercheBackgroud()

        # Récupération des info du plugin
        self._url = sys.argv[0]
        self.AdressePlugin = self.adn.getAddonInfo('path')
        
        self.UrlRepo = "https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/"
        self.Url_Plugin_Version = self.UrlRepo+"repo/"+self.nomPlugin+"/README.md"
        self._handle = int(sys.argv[1])
        self.profile = translatePath(self.adn.getAddonInfo('profile').decode('utf-8'))
        
        self.dbxAmAx = os.path.join(self.AdressePlugin, "resources", "xAmAx.db")
        self.addon_data_dir = os.path.join(translatePath("special://userdata/addon_data" ), self.nomPlugin)
        self.extpath = os.path.join(translatePath("special://home/addons/"))

        self._ArtMenu = {'thumb': os.path.join(self.AdressePlugin,'play.png'),
                'lecture': os.path.join(self.AdressePlugin,'menu.png'),
                'param': os.path.join(self.AdressePlugin,'param.png'),
                'fanar': os.path.join(self.AdressePlugin,'fanart.jpg'),
                'info': os.path.join(self.AdressePlugin,'info.png')}
        self._MenuList={"Ouvrir fichier m3u avec le lecteur de kodi":("xAmAx","LireUrl",True),
               "Ouvrir fichier m3u avec le lecteur F4m":("xAmAx","LireF4m",True),
               "Options de vStream (Film et séries)":("vStream","VisuVstream",True),
               "Options de Kodi":("Kodi","VisuKodi",True),
               "Options de xAmAx":("xAmAx",'VisuxAmAx',True)}
        self._MenuxAmAx={"Version "+self.__version__:("xAmAx","InfoVersion",False),
               "Mise a jour de xAmAx":("xAmAx",'MiseAJourxAmAx',True),
                "Paramètres de xAmAx":("xAmAx","ParamxAmAx",False)} #,"test":("xAmAx",'test',True)}
        self._MenuvStream={"Trier la liste de Recherche vStream":("vStream","RechercheVstream",True),
               "Trier les Marques-Pages vStream":("vStream","MPVstream",True),
               "Modifier la vitesse de téléchargement":("vStream","DownloadVstream",True)}
        self._MenuKodi={"Afficher le Journal d'erreur":("Kodi","AffichLog",False),
               "Effacer le fichiers temporaires":("Kodi","SupTemp",True),
               "Effacer les miniatures en mémoire":("Kodi","SupThumb",True)} #"Changer le Fond d'écran":("Kodi",'ChangeFonDecran',True),"
        self._MenuPC={"Afficher l'historique":("PC","AffichLog",True),
             "Réaliser une action":("PC","ActPC",True)}
        self._MenuActPC={"Changer heure d'arrêt":("PC","ActHArret",True),
                "Arrêter le pc":("PC","ActArretDirect",True),
                "Arrêt de l'arrêt automatique":("PC","ActArretAuto",True),
                "Re-démarrage de l'arrêt automatique":("PC","ActDemarArret",True),
                "Interrogation Heure d'arrêt":("PC","ActIHArret",True),
                "Interrogation Heure du pc":("PC","ActHeurePC",True)}
        self.Maj=[("xAmAx",".db","resources/"),
                  ("settings",".xml","resources/"),
                  ("vStreamOpt",".py","resources/"),
                  ("LSPOpt",".py","resources/"),
                  ("default",".py",""),
                  ("Samba",".py","resources/"),
                  ("Menu",".py","resources/")]
        self.MajPresente=True

    def AfficheMenu(self,Menu="", Icone=False):
        if Menu=="":
            Menu=self._MenuList
        # creation du menu
        print "Menu"
        # Création de la liste d'élément.
        if not Icone:
            for tag, (Titre, Act, is_folder) in Menu.items():
                if ((self._vStream == "OK" and Titre == "vStream")or
                (self._ChercheBackgroud == "OK" and Titre == "ChangeFonDecran")or
                (Titre != "vStream" and Titre != "ChangeFonDecran")):
                    if Titre == "TV":
                        icone = self._ArtMenu['lecture']
                    else:
                        icone = self._ArtMenu['param']
                    self.addDir(tag,'{0}?action=Menu&ElemMenu={1}&Option={2}'.format(self._url, Act, Titre),1,icone,icone,is_folder)
        else:
            for tag, (Titre, Url, is_folder, icone, Tmage) in Menu.items():
                if icone != "":
                    """text = base64.b64decode(str(Titre)).replace('&#8211;','-')
                    text = text.replace('&ndash;','-')
                    text = text.replace('&#038;','&')
                    text = text.replace('&#8217;','\'')
                    text = text.replace('&#8216;','\'')
                    text = text.replace('&#8230;','...')
                    text = text.replace('&quot;','"')
                    text = text.replace('&#039;','`')
                    text = text.replace('&amp;','&')
                    text = text.replace('&ntilde;','ñ')
                    Titre = text.replace('&rsquo;','\'')"""
                    Titre = cLiveSPOpt().ConvNom(base64.b64decode(str(Titre)))
                    #print "list m3u: "+Titre+' {0}?action=Play&Url={1}&ElemMenu={2}&Tmage={3}'.format(self._url,Url,"LireVideo2",Tmage)+" Icone= "+base64.b64decode(icone)
                    if base64.b64decode(icone)==self._ArtMenu['lecture']:
                        self.addDir(Titre,'{0}?action=Play&Url={1}&ElemMenu={2}&Adult=0'.format(self._url,Url,"LireVideo2"),1,self._ArtMenu['lecture'],self._ArtMenu['lecture'],is_folder)
                    elif base64.b64decode(icone)==self._ArtMenu['info']:
                        URL=base64.b64decode(str(Url))
                        cCommands=[]
                        cCommands.append(("Lire le Fichier",'XBMC.RunPlugin({0}?action=OuvTxt&Url={1}&ElemMenu={2})'.format(self._url,base64.b64encode(URL[3:]),"LogSamba")))
                        cCommands.append(("Supprimer le fichier",'XBMC.RunPlugin({0}?action=SupFich&Url={1}&ElemMenu={2})'.format(self._url,base64.b64encode(URL[3:]),"LogSamba")))
                        if URL.startswith("LOG"):
                            self.addDir(Titre,'{0}?action=OuvTxt&Url={1}&ElemMenu={2}'.format(self._url,base64.b64encode(URL[3:]),"LogSamba"),1,self._ArtMenu['lecture'],self._ArtMenu['lecture'],is_folder,contextCommands=cCommands)
                    else:
                        cCommands=[]
                        cCommands.append(("Telecharger vidéo",'XBMC.RunPlugin({0}?action=Play&Url={1}&ElemMenu={2}&Adult=1)'.format(self._url,Url,"DL")))
                        cCommands.append(("Afficher les photos",'XBMC.RunPlugin({0}?action=FichierEnCour&ElemMenu={1}&Adult=1&Icone={2}&timage={3})'.format(self._url,"Photo",base64.b64decode(icone),Tmage)))
                        self.addDir(Titre,'{0}?action=Play&Url={1}&ElemMenu={2}&Adult=1'.format(self._url,Url,"LireVideo2"),1,base64.b64decode(icone),self._ArtMenu['lecture'],is_folder,contextCommands=cCommands)
                else:
                    self.addDir(base64.b64decode(Titre),'{0}?action=Menu&ElemMenu={1}&Option={2}&Url={3}'.format(self._url,"Adult","TV",Url),1,self._ArtMenu['lecture'],self._ArtMenu['lecture'],True)
        if Menu==self._MenuList:
            # Création de chaque élément
            if self._vStream != "OK":
                self.addDir(self._vStream,
                            '{0}?action=Menu&ElemMenu={1}'.format(self._url, 'InstallvStream'),
                            1,
                            self._ArtMenu['info'],
                            self._ArtMenu['fanar'],
                            True)
            if self.adn.getSetting(id="Adult")=="true":
                self.addDir("Plus",
                            '{0}?action=Menu&ElemMenu={1}&Option={2}'.format(self._url, "Adult", 'TV'),
                            1,
                            self._ArtMenu['lecture'],
                            self._ArtMenu['fanar'],
                            True)
            if self.adn.getSetting(id="stban")=="true":
                self.addDir("PC distant",
                            '{0}?action=Menu&ElemMenu={1}&Option={2}'.format(self._url, "stBan", 'PC'),
                            1,
                            self._ArtMenu['lecture'],
                            self._ArtMenu['fanar'],
                            True)
                
        xbmcplugin.setPluginCategory( handle=int(sys.argv[1]), category="xAmAx" )
        xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
            

    def MajMenuRegroup(self):
        MenuRegroup={}
        print "Ouverture Liste Regroup:"
        DBxAmAx = db(self.dbxAmAx)
        AffichAutre = False
        listID=[]
        for numTab in range(1,5):
            if DBxAmAx.TableExist("List"+str(numTab)):
                cRegroup = DBxAmAx.Select(Table="RegroupChaine",
                                          Colonnes="NomAffiche,NomRegroup, PasDansNom",
                                          Where="",
                                          Order="NomAffiche ASC")
                for Affich, Nom, PasNom in cRegroup:
                    if PasNom != None and PasNom != "":
                        ANDWHERE = "AND Nom NOT LIKE '%"+PasNom+"%' "
                    else:
                        ANDWHERE = ""
                    cChaine = DBxAmAx.Select(Table="List"+str(numTab),
                                             Colonnes="IDLP",
                                             Where="Nom LIKE '"+str(Nom)+"%' "+ANDWHERE,
                                             Order="Nom ASC")
                    if len(cChaine)> 0:
                        for IDLP in cChaine:
                            listID.append(str(IDLP[0]))
                        MenuRegroup.update({str(Affich).replace("_"," "): ("TV","ChaineRegroup"+base64.b64encode(str(Nom)),True)})
                self.adn.setSetting(id="ListAutre", value=str(listID).replace("[","(").replace("]",")").replace("'",""))
                cChaine = DBxAmAx.Select(Table="List"+str(numTab),
                                         Colonnes="IDLP",
                                         Where="IDLP NOT IN "+str(listID).replace("[","(").replace("]",")").replace("'",""),
                                         Order="")
                if len(cChaine)>0:
                    AffichAutre = True
        if AffichAutre:
            MenuRegroup.update({"ZZZ Les autres chaines": ("TV","ChaineRegroupLesAutres",True)})
        return MenuRegroup
        
    def AffichMenuTv(self,MiseAJourOK=False):
        Retour=""
        MenuTV = self._MenuTV
        if self.adn.getSetting(id="MajtvAuto")=="true":
            print "Recherche mise a jour si première ouverture de la journée"
            DateDerMajTv = str(self.adn.getSetting(id="DateTvListe"))
            print "Dernière Mise a jour: "+DateDerMajTv
            if str(DateDerMajTv)!=strftime("%d-%m-%Y", gmtime()):
                Retour = cLiveSPOpt().RechercheChaine(self.AdressePlugin)
                if Retour=="OK":
                    self.adn.setSetting(id="DateTvListe", value=strftime("%d-%m-%Y", gmtime())) #%H:%M:%S"
        if self.adn.getSetting(id="CreerBouq")=="true":
            if Retour=="OK" or MiseAJourOK==True:
                cLiveSPOpt().CreerBouquet(self.AdressePlugin)
            print "Ouverture Liste Bouquet de: "+self.dbxAmAx
            cBouq = db(self.dbxAmAx).Select(Table="Bouquet", Colonnes="NomBouq", Where="", Order="Ordre ASC")
            for NomBouq in cBouq:
                MenuTV.update({"Bouquet "+str(NomBouq[0]): ("TV","Bouq"+str(NomBouq[0]),True)})
        self.AfficheMenu(MenuTV)
        
    def addDir(self,name,url,mode,iconimage,fanart,is_Folder,infos={},cat='',contextCommands=[]):
        u  =url
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infos )
        liz.setProperty('Fanart_Image',fanart)
        if len(contextCommands)>0:
            liz.addContextMenuItems ( contextCommands, replaceItems=False)
            
        ok =xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_Folder)

    def AfichListeTS(self,ListeChaine=[], Colon="Nom, Url", Where="", Ordre="Nom", Bouquet=""):
        if len(ListeChaine)>0:
            for Nom, Url, Entete in ListeChaine:
                self.addDir(Nom,
                       '{0}?action=Play&Url={1}&ElemMenu={2}'.format(self._url, urlib.quote_plus(Url+"|"+Entete), "LireVideo"),
                       1,
                       self._ArtMenu['thumb'],
                       self._ArtMenu['fanar'],
                       True)
        else:
            DBxAmAx = db(self.dbxAmAx)
            i = 0
            Table=""
            Rfin = 5
            if Bouquet!="":
                print "Ouverture Bouquet: "+Bouquet
                cBouq = DBxAmAx.Select(Table="Bouquet",
                                       Colonnes="IDBouquet, TriDesUrl",
                                       Where="NomBouq='"+Bouquet+"'",
                                       Order="")
                IdBouq=0
                OrdreB=""
                for IdBouquet,OrdreBouq in cBouq:
                    IdBouq=IdBouquet
                    OrdreB=OrdreBouq
                Where="IdBouquet="+str(IdBouq)
                Colon="NomAffichChaine, Url"
                Ordre=OrdreB
                Table="UrlBouquet"
                Rfin = 2
            for numTab in range(1,Rfin):
                if Table=="" or Table.startswith("List"):
                    Table="List"+str(numTab)
                print "Ouverture Liste TV de: "+self.dbxAmAx+ " Table: "+Table+" Colon: "+Colon+" Where: "+Where+" Ordre: "+Ordre
                cAffich = DBxAmAx.Select(Table, Colon, Where, Ordre)
                print "Creation Liste de chaine a afficher..."
                for Nom, Url in cAffich:
                    i += 1
                    self.addDir(str(i)+"-"+Nom,
                           '{0}?action=Play&Url={1}&ElemMenu={2}'.format(self._url, urlib.quote_plus(Url), "LireVideo"),
                           1,
                           self._ArtMenu['thumb'],
                           self._ArtMenu['fanar'],
                           True)
        xbmcplugin.setPluginCategory(handle=int(sys.argv[1]), category="lecture" )
        xbmcplugin.endOfDirectory(int(sys.argv[1]))

    def TryChercheBackgroud(self):
        try:
            NomSkin = getSkinDir()
            print "skindir: "+NomSkin
            Defaut = os.path.join(translatePath('special://home/addons/'),NomSkin,"backgrounds")
            if ((NomSkin == "skin.confluence")or(NomSkin == "skin.qonfluence")):
                try:
                    with open(os.path.join(translatePath('special://home/'),"userdata","addon_data",NomSkin,"settings.xml")) as f:
                        Ret = f.read()
                    f.closed
                    ModifSkin = Ret.split('<setting id="UseCustomBackground" type="bool">')[1].split("</setting>")[0]
                except:
                    ModifSkin = 'false'
                if ModifSkin == 'true':
                    ModifSkin = Retour.split('<setting id="CustomBackgroundPath" type="string">')[1].split("</setting>")[0]
                    if xbmcvfs.exists(ModifSkin):
                        self.Param["Chemin"]=ModifSkin
                        return "OK"
                    elif xbmcvfs.exists(os.path.join(Defaut,"SKINDEFAULT.jpg")):
                        self.Param["Chemin"]=os.path.join(Defaut,"SKINDEFAULT.jpg")
                        return "OK"
                    else:
                        return "Fond d'écran indisponible!"
                else:
                    if xbmcvfs.exists(os.path.join(Defaut,"SKINDEFAULT.jpg")):
                        self.Param["Chemin"]=os.path.join(Defaut,"SKINDEFAULT.jpg")
                        return "OK"
                    else:
                        return "Fond d'écran indisponible!"
            elif(NomSkin == "skin.aeon.nox.5"):
                if xbmcvfs.exists(os.path.join(Defaut,"default_bg.jpg")):
                    self.Param["Chemin"]=os.path.join(Defaut,"default_bg.jpg")
                    return "OK"
                else:
                    return "Fond d'écran indisponible!"
            else:
                return "Fond d'écran indisponible!"
        except:
            return "Fond d'écran indisponible!"

    def Efface_thumb(self,env):
        if (env == 'fi'):
            try:
                path = translatePath('special://temp/')
                filenames = next(os.walk(path))[2]
                for i in filenames:
                    if ".fi" in i:
                        os.remove(os.path.join(path, i))
                return "OK"
            except:
                return "Erreur de suppression des fichiers temporaires"

        elif (env == 'thumb'):
            try:
                path = translatePath('special://userdata/Thumbnails/')
                path2 = translatePath('special://userdata/Database/')
                for i in os.listdir(path):
                    folders = os.path.join(path, i)
                    if os.path.isdir(folders):
                        p = next(os.walk(folders))[2]
                        for x in p:
                            os.remove(os.path.join(folders, x))

                filenames = next(os.walk(path2))[2]
                for x in filenames:
                    if "exture" in x:
                        db(os.path.join(path2, x)).Delete("texture")
                return "OK"
            except:
                return "Erreur de suppression des miniatures"
            
    def RechercheMAJ(self):
        from resources.ziptools import ziptools
        print 'xAmAx Recherche mise a jour...'
        try:
            data = cDL().TelechargPage(self.Url_Plugin_Version)
            print 'Lecture de la version du plugin distant: ' + data
        except:
            data = ""
            print 'Erreur de la lecture de la version du plugin: ' + self.Url_Plugin_Version
            
        version_publique=data
        
        try:
            numVersionPub = version_publique.split(".")
            print 'xAmAx version publique:' + version_publique
            numVersionLoc = self.__version__.split(".")
            print 'xAmAx version locale:' + self.__version__
        except:
            version_publique = ""
            print 'xAmAx version locale:' + self.__version__
        print 'xAmAx version Publique: ' + str(numVersionPub) +  ' version locale: ' + str(numVersionLoc)
        if version_publique!="" and self.__version__!="" and len(numVersionPub)==3 and len(numVersionLoc)==3:
            if ((int(numVersionPub[0]) > int(numVersionLoc[0]))or
                ((int(numVersionPub[0]) == int(numVersionLoc[0]))and((int(numVersionPub[1]) > int(numVersionLoc[1]))or
                                                                    ((int(numVersionPub[2]) > int(numVersionLoc[2])))))):
                try:
                    xbmcvfs.mkdir(self.addon_data_dir)
                except: pass
                dest = os.path.join(self.addon_data_dir, 'DerMaj.zip')
                MAJ_URL = self.UrlRepo+self.nomPlugin+'/'+self.nomPlugin+'-' +str(int(numVersionPub[0]))+"."+str(int(numVersionPub[1]))+"."+str(int(numVersionPub[2])) + '.zip'
                print 'Démarrage du téléchargement de:' + MAJ_URL
                    
                cDL().TelechargementZip(MAJ_URL,dest)

                unzipper = ziptools()
                unzipper.extract(dest,self.extpath)
                    
                lign1 = 'Nouvelle version installer .....'
                lign2 = 'Version: ' + version_publique 
                xbmcgui.Dialog().ok('xAmAx', lign1, lign2)
                    
                if os.remove( dest ):
                    print 'Suppression du fichier télécharger'
                executebuiltin("UpdateLocalAddons")
                executebuiltin("UpdateAddonRepos")
                sleep(1.5)
                return "OK"
            else:
                return "Pas de mise à jour disponible! \nVersion Internet: " + version_publique + "Version Actuelle: " + self.__version__
        else:
            return "Pas de mise à jour disponible!"
        
    def MajAuto(self): #,NomMaj,Ext,resources=""
        for NomMaj,Ext,resources in self.Maj:
            if resources=="":
                AdresseFich = os.path.join(self.AdressePlugin, NomMaj+Ext)
            else:
                AdresseFich = os.path.join(self.AdressePlugin, "resources", NomMaj+Ext)
            try:
                ret = self.RechMajAuto(NomMaj,resources)
                if ret != "":
                    DL = cDL().TelechargPage(url=self.UrlRepo+self.nomPlugin+"/"+resources+NomMaj+Ext)
                    if not DL.startswith("Erreur"):
                        fichier = open(AdresseFich, "w")
                        fichier.write(DL)
                        fichier.close()
                        self.adn.setSetting(id=NomMaj, value=ret)
                        print "Mise a jour de "+NomMaj+" OK"
            except:
                print "Erreur mise a jour: "+str(sys.exc_info()[0])
                return "Erreur mise a jour: "+str(sys.exc_info()[0])
        self.adn.setSetting(id="MajV", value=self.vertionMaj)
        return "OK"
    
    def RechMajAuto(self,NomMaj,resources=""):
        #try:
        AdresseVersion = self.UrlRepo+self.nomPlugin+"/"+resources+NomMaj
        VRech = cDL().TelechargPage(AdresseVersion)
        if not VRech.startswith("Erreur"):
            VLspopt = self.adn.getSetting(id=NomMaj)
            print "Version "+NomMaj+": "+VLspopt+" Version sur internet: "+VRech
            if VLspopt!=str(VRech):
                return str(VRech)
            else:
                return ""
        #except:
        #    print "Erreur mise a jour: "+str(sys.exc_info()[0])
        #    return ""

    def router(self,paramstring):
        print "dans router"
        # reception des paramètres du menu
        if len(paramstring)>=2:
            params = dict(parse_qsl(paramstring))
        else:
            params = None
        # Si aucun paramètre on ouvre le menu
        if params:
            print str(params)
            if params['action'] == 'Menu':
                if params['Option'] =="TV":#----------------------------------------------------------------------------------------
                    if params['ElemMenu']=="Adult":
                        try:
                            Url = params['Url']
                            ListAff = cLiveSPOpt().AdulteSources(base64.b64decode(Url))
                        except:
                            ListAff = cLiveSPOpt().AdulteSources()
                        if len(ListAff)>0:
                            i=0
                            MenuRegroup={}
                            for Url,Thumb,Timag,Nom in ListAff:
                                i+=1
                                Nom2=base64.b64encode(Nom)
                                Nom3=base64.b64encode(Nom+str(i))
                                Url=base64.b64encode(Url)
                                Thumb=base64.b64encode(Thumb)
                                Tima=base64.b64encode(str(Timag))
                                MenuRegroup.update({Nom: (Nom2, Url, False, Thumb, Tima)})
                            self.AfficheMenu(MenuRegroup,True)

                if params['Option']=='vStream':#----------------------------------------------------------------------------------------
                    if params['ElemMenu']=="VisuVstream":
                        self.AfficheMenu(self._MenuvStream)
                    if params['ElemMenu']=='MPVstream':
                        Retour = cvStreamOpt().MiseAJourVstream("MarquePage")
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Trier les Marques-Pages vStream", Retour)
                    if params['ElemMenu']=='RechercheVstream':
                        Retour = cvStreamOpt().MiseAJourVstream("Recherche")
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Trier la liste de Recherche vStream", Retour)
                    if params['ElemMenu']=='DownloadVstream':
                        Retour = cvStreamOpt().LectureDownload()
                        if len(Retour)==5:
                            self.AfficheMenu(Retour)
                        else:
                            dialog = xbmcgui.Dialog()
                            ok = dialog.ok("Recherche de la vitesse de téléchargement de vStream", Retour)
                    if params['ElemMenu'].startswith("VstreamDl"):
                        Retour = cvStreamOpt().EcritureDownload(params['ElemMenu'][9:])
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Modification vitesse de téléchargement de vStream", Retour)
                        executebuiltin('XBMC.Container.Update')
                        executebuiltin('XBMC.Container.Refresh')
                    
                if params['Option']=="Kodi": #----------------------------------------------------------------------------------------
                    if params['ElemMenu']=="VisuKodi":
                        self.AfficheMenu(self._MenuKodi)
                    if params['ElemMenu']=="AffichLog":
                        print "AffichLog: "
                        Affich=TxtAffich()
                        Affich.Fenetre(Chemin=translatePath('special://logpath')+"kodi.log",
                                        line_number=0,Invertion=True,LabTitre="Journal d'erreur")
                    if params['ElemMenu']=='ChangeFonDecran':
                        print "ChangeFonDecran"
                        _ChercheBackgroud = self.TryChercheBackgroud()
                        if _ChercheBackgroud == "OK":
                            CheminSplit = self.Param["Chemin"][:self.Param["Chemin"].rfind("/")+1]
                            NomFichier = self.Param["Chemin"][self.Param["Chemin"].rfind("/")+1:]
                            Extension = NomFichier[-4:]
                            NomFichier = NomFichier[:-4]
                            print CheminSplit+" "+NomFichier+" "+Extension
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
                            ok = dialog.ok("Erreur de copy du fichier",self._ChercheBackgroud)
                    if params['ElemMenu']=="SupTemp":
                        print "SupTemp"
                        dialog = xbmcgui.Dialog()
                        if dialog.yesno('Effacer les fichier temporaires...', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                            Retour = self.Efface_thumb('fi')
                            if Retour=="OK":
                                executebuiltin("XBMC.Notification(Effacement des fichiers temporaires ,OK,2000,"")")
                            else:
                                executebuiltin("XBMC.Notification(Effacement des fichiers temporaires ," + Retour + ",2000,"")")

                    if params['ElemMenu']=="SupThumb":
                        print "SupThumb"
                        dialog = xbmcgui.Dialog()
                        if dialog.yesno('Effacer les miniatures...', 'Êtes-vous sûr ?','','','Non', 'Oui'):
                            Retour=self.Efface_thumb('thumb')
                            if Retour=="OK":
                                executebuiltin("XBMC.Notification(Effacement Miniatures ,OK,2000,"")")
                            else:
                                executebuiltin("XBMC.Notification(Effacement Miniatures ,"+Retour+",2000,"")")
                
                if params['Option']=="xAmAx": #----------------------------------------------------------------------------------------
                    if params['ElemMenu']=="VisuxAmAx":
                        print "Afficher menu xAmAx"
                        MenuxAmAx = self._MenuxAmAx
                        if self.adn.getSetting(id="stban")=="true":
                            if self.adn.getSetting(id="p")=="":
                                MenuxAmAx.update({"PC distant: Ajouter un Mot de passe": ("PC","PssPc",True)})
                            else:
                                MenuxAmAx.update({"PC distant: Changer le Mot de passe": ("PC","PssPc",True)})
                        self.AfficheMenu(MenuxAmAx)
                    if params['ElemMenu']=="InfoVersion":
                        print "InfoVersion: "
                        Affich=TxtAffich()
                        Affich.Fenetre(Chemin=os.path.join(self.AdressePlugin,"changelog.txt"),line_number=0)
                    if params['ElemMenu']=="MiseAJourxAmAx":
                        Retour = self.RechercheMAJ()
                        if Retour != "OK":
                            dialog = xbmcgui.Dialog()
                            ok = dialog.ok("Mise à jour xAmAx", Retour)
                    if params['ElemMenu']=="test":
                        print "test: "
                        Retour = cvStreamOpt().LectureDownload()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Temps de pause téléchargement vstream: ", Retour)
                        '''dirs, files = xbmcvfs.listdir("smb://192.168.1.1/echange")
                        if len(files)>0:
                            i=0
                            MenuRegroup={}
                            for fich in files:
                                i+=1
                                MenuRegroup.update({fich: (fich, "ActPC",True)})
                            self.AfficheMenu(MenuRegroup)'''
                        
                    if params['ElemMenu']=="ParamxAmAx":
                        self.adn.openSettings()
                    if params['ElemMenu']=="LireUrl":
                        ListAff = cLiveSPOpt().LireM3u(CheminxAmAx=self.AdressePlugin)
                        i=0
                        MenuRegroup={}
                        for Nom,Url in ListAff:
                            i+=1
                            Nom=base64.b64encode(Nom)
                            Url=base64.b64encode(Url)
                            Thumb=base64.b64encode(self._ArtMenu['lecture'])
                            MenuRegroup.update({"Video"+str(i): (Nom, Url, True, Thumb,[])})
                        self.AfficheMenu(MenuRegroup,True)
                    if params['ElemMenu']=="LireF4m":
                        ListAff = cLiveSPOpt().LireM3u(CheminxAmAx=self.AdressePlugin, F4m=True)
                        i=0
                        MenuRegroup={}
                        for Nom,Url in ListAff:
                            i+=1
                            Nom=base64.b64encode(Nom)
                            Url=base64.b64encode(Url)
                            Thumb=base64.b64encode(self._ArtMenu['lecture'])
                            MenuRegroup.update({"Video"+str(i): (Nom, Url, True, Thumb,[])})
                        self.AfficheMenu(MenuRegroup,True)

                if params['Option']=="PC": #----------------------------------------------------------------------------------------
                    from resources.Samba import EnvSamba
                    if params['ElemMenu']=="stBan":
                        print "Afficher menu xAmAx"
                        dialog = xbmcgui.Dialog()
                        d = dialog.input('Entrer votre mot de passe', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                        if d == base64.b64decode(self.adn.getSetting(id="p")):
                            self.AfficheMenu(self._MenuPC)
                        elif d!="":
                            d = dialog.ok('Verrification du mot de passe', "Mot de passe incorrect")
                    if params['ElemMenu']=="PssPc":
                        dialog = xbmcgui.Dialog()
                        d = dialog.input('Entrer votre mot de passe actuel', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                        if d == base64.b64decode(self.adn.getSetting(id="p")):
                            d = dialog.input('Entrer votre nouveau mot de passe', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                            if d != "":
                                e = dialog.input('Entrer votre nouveau mot de passe une seconde fois', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                                if e == d:
                                    self.adn.setSetting(id='p', value=base64.b64encode(e))
                                    d = dialog.ok('Verrification du mot de passe', "Votre Mot de passe a était changer!")
                                else:
                                    dialog.ok('Verrification du mot de passe', "Le mot de passe saisi n'est pas le même!", "Recommencer pour pouvoir modifier votre mot de passe!")
                            else:
                                d = dialog.ok('Verrification du mot de passe', "Votre Mot de passe n'a pas était changer")
                        elif d!="":
                            d = dialog.ok('Verrification du mot de passe', "Mot de passe incorrect")
                    if params['ElemMenu']=="AffichLog":
                        List = EnvSamba(dosEchange = "echange").ListFichier()
                        MenuRegroup={}
                        for F in List:
                            Nom=base64.b64encode(F)
                            Url=base64.b64encode("LOG"+F)
                            Thumb=base64.b64encode(self._ArtMenu['info'])
                            MenuRegroup.update({Nom: (Nom, Url, True, Thumb,[])})
                        self.AfficheMenu(MenuRegroup,True)
                    if params['ElemMenu']=="ActPC":
                        print "Afficher menu xAmAx"
                        self.AfficheMenu(self._MenuActPC)
                    if params['ElemMenu'][:3]=="Act" and params['ElemMenu']!="ActPC":
                        smb = EnvSamba(dosEchange = "echange")
                        ret1 = smb.ConvAction(TitreCmd=params['ElemMenu'][3:])
                        if ret1 != "":
                            print "**** Retour action: "+ret1
                            ret = smb.EnvoiFichier(txtEchang=ret1,NomFich="Act.xama")
                            dialog = xbmcgui.Dialog()
                            if ret:
                                d = dialog.ok("Enregistrement de l'action OK", "Votre Action à bien était enregistré, elle sera active dans 5min maximum", "Dans l'historique vous pourez retrouver le résultat de l'opération dans le fichier Rep.xama!")
                                print "**** Retour action: "+str(ret)
                            else:
                                d = dialog.ok("Erreur enregistrement de l'action", "Votre Action n'a pas peu être enregistré!", "Veuillez verrifier votre connection!")
                                print "**** Retour action: Erreur d'enregistrement"
                        
            if params['action'] == 'Play':
                if params['ElemMenu']=="LireVideo":
                    finalUrl=params['Url']
                    print "Lecture de: "+finalUrl
                    executebuiltin('XBMC.RunPlugin('+finalUrl+')')
                if params['ElemMenu']=="LireVideo2":
                    if params['Adult']=="1":
                        html = cDL().TelechargPage('http://www.mrsexe.com/' + base64.b64decode(params['Url']))
                        videourl = re.compile(r"src='(/inc/clic\.php\?video=.+?&cat=mrsex.+?)'").findall(html)
                        print "--videourl = "+str(videourl[0])
                        html = cDL().TelechargPage('http://www.mrsexe.com/' + videourl[0])
                        #print "--html = "+html
                        videourls = re.compile(r"'file': \"(.+?)\",.+?'label': '(.+?)'", re.DOTALL).findall(html)
                        videourls = sorted(videourls, key=lambda tup: tup[1], reverse=True)
                        print "--videourl.. = "+(str(videourl[0]))
                        videourl = str(videourls[0][0])
                    else:
                        videourl = base64.b64decode(params['Url'])
                    print "Adresse video: "+str(videourl)
                    if videourl.startswith("plugin://"):
                        executebuiltin('XBMC.RunPlugin('+videourl+')')
                    else:
                        listitem = xbmcgui.ListItem("essai1")
                        listitem.setInfo('video', {'Title': "essai1", 'Genre': 'essai'})
                        Player().play(videourl, listitem)
                if params['ElemMenu']=="DL":
                    dialog = xbmcgui.Dialog()
                    if dialog.yesno('Telechargement du fichier...', 'Voulez-vous télécharger le fichier?','','','Non', 'Oui'):
                        if params['Adult']=="1":
                            html = cDL().TelechargPage('http://www.mrsexe.com/' + base64.b64decode(params['Url']))
                            videourl = re.compile(r"src='(/inc/clic\.php\?video=.+?&cat=mrsex.+?)'").findall(html)
                            print "--videourl_DL = "+str(videourl[0])
                            html = cDL().TelechargPage('http://www.mrsexe.com/' + videourl[0])
                            #print "--html = "+html
                            videourls = re.compile(r"'file': \"(.+?)\",.+?'label': '(.+?)'", re.DOTALL).findall(html)
                            videourls = sorted(videourls, key=lambda tup: tup[1], reverse=True)
                            print "--videourl_DL.. = "+(str(videourl[0]))
                            videourl = str(videourls[0][0])
                        else:
                            videourl = base64.b64decode(params['Url'])
                        
                        print "Adresse video DL: "+str(videourl)
                        for i in range(0,999):
                            if i < 10:
                                NomFichVid = "vid00"+str(i)+".mp4"
                            elif i < 100:
                                NomFichVid = "vid0"+str(i)+".mp4"
                            else:
                                NomFichVid = "vid"+str(i)+".mp4"
                            if not xbmcvfs.exists(os.path.join(self.profile,NomFichVid)):
                                break
                        cDL().DLFich(videourl,os.path.join(self.profile,NomFichVid), DPView=True)
            if params['action'] == 'OuvTxt':
                if params['ElemMenu']=="LogSamba":
                    from resources.Samba import EnvSamba
                    Fich = base64.b64decode(params['Url'])
                    FichLu = EnvSamba(dosEchange = "echange").OuvrirFich(Fich)
                    Affich=TxtAffich()
                    Affich.Fenetre(Chemin="",LabTitre="Journal d'action",Texte=FichLu)
            if params['action'] == 'SupFich':
                if params['ElemMenu']=="LogSamba":
                    from resources.Samba import EnvSamba
                    Fich = base64.b64decode(params['Url'])
                    ret = EnvSamba(dosEchange = "echange").SupprimFich(Fich)
                    dialog = xbmcgui.Dialog()
                    if ret==1:
                        d = dialog.ok("Suppression du fichier OK", "Votre fichier "+Fich+" a bien était supprimer", "")
                        print "**** Supprimer fichier: "+Fich
                    else:
                        d = dialog.ok("Erreur supression de fichier", "Votre fichier "+Fich+" n'a pas pu être supprimer", "Veuillez verrifier votre connection!")
                        print "**** Erreur supression: "+Fich
                    executebuiltin('XBMC.Container.Update')
                    executebuiltin('XBMC.Container.Refresh')
                    sleep(0.2)
                    print "****** Retour Supprim= "+str(ret)
            if params['action'] == 'FichierEnCour':
                if params['ElemMenu']=="Label":
                    win = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                    curctl = win.getFocusId()
                    cursel = win.getControl( curctl ).getSelectedItem()
                    label = cursel.getLabel()
                    print "Label= "+str(label)
                if params['ElemMenu']=="Photo":
                    listPhoto = ""
                    ListeImage = base64.b64decode(params['timage']).replace("[","").replace("]","").replace(chr(39),"").split(",")
                    i=0
                    cheminPhoto=os.path.join(self.profile,"photo")
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
                        cDL().TelechargementZip(listPhoto,CheminFich)       
                    executebuiltin('xbmc.SlideShow(' + cheminPhoto + ')') 
        else:
            self.AfficheMenu()
            if self.adn.getSetting(id="MajAuto")=="true" and self.MajPresente:
                self.MajPresente = False
                print "Recherche auto de Mise a jour"
                self.vertionMaj = self.RechMajAuto("MajV")
                if self.vertionMaj != "":
                    Retour = self.MajAuto()
                    if Retour != "OK":
                        dialog = xbmcgui.Dialog()
                        dialog.ok("Mise à jour automatique", Retour, "")
                    else:
                        executebuiltin('XBMC.Container.Update')
                        executebuiltin('XBMC.Container.Refresh')
                    
            

