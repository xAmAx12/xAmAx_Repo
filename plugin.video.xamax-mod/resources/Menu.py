# -*- coding: UTF-8 -*-
# Module: menu
# Author: xamax
# Created on: 23.07.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

#CreerBouquet

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
try:
    import resources.Config as Conf
except:
    Conf = None
try:
    import resources.KodiMod as Kmod
except:
    Kmod = None
try:
    import resources.TestDebit as Debi
except:
    Debi = None
from datetime import datetime

class menu():

    def __init__(self):
        #Enregistrement des paramètres
        self.nomPlugin = 'plugin.video.xamax-mod'
        self._IdAdn = sys.argv[0]

        # Récupération des info du plugin
        self.adn = Addon(self.nomPlugin)
        self.__version__ = self.adn.getAddonInfo('version')
        self.AdresseAdn = self.adn.getAddonInfo('path')
        
        self.UrlRepo = "https://raw.githubusercontent.com/xAmAx12/xAmAx_Repo/master/"
        self.AdresseAdnUtil = translatePath(self.adn.getAddonInfo('profile').decode('utf-8'))
        
        self.dbxAmAx = os.path.join(self.AdresseAdnUtil, "xAmAx.db")
        self.extpath = os.path.join(translatePath("special://home/addons/"))

        self._ArtMenu = {'thumb': os.path.join(self.AdresseAdn,'play.png'),
                'lecture': os.path.join(self.AdresseAdn,'menu.png'),
                'param': os.path.join(self.AdresseAdn,'param.png'),
                'fanar': os.path.join(self.AdresseAdn,'fanart.jpg'),
                'info': os.path.join(self.AdresseAdn,'info.png')}

        self.MajPresente=True

    def RechercheF4M(self):
        try:
            AdnF4m = Addon('plugin.video.f4mTester')
            print "f4m version = "+AdnF4m.getAddonInfo('version').decode('utf-8')
            if not os.path.exists(os.path.join(self.extpath,'plugin.video.f4mTester')):
                print "f4m tester dossier inexistant = "+os.path.join(self.extpath,'plugin.video.f4mTester')
                return False
            elif not os.path.exists(os.path.join(self.extpath,'script.video.F4mProxy')):
                print "f4m Proxy dossier inexistant = "+os.path.join(self.extpath,'script.video.F4mProxy')
                return False
            return True
        except:
            return False

    def AfficheMenu(self,Menu="", Icone=False, TriAuto=True):
        # creation du menu
        print "Menu"
        IdMenu = 0
        # Création de la liste d'élément.
        if not Icone:
            for tag, (Titre, Act, is_folder) in Menu.items():
                IdMenu += 1
                if Titre == "TV":
                    icone = self._ArtMenu['lecture']
                else:
                    icone = self._ArtMenu['param']
                self.addDir(tag,'{0}?action=Menu&ElemMenu={1}&Option={2}'.format(self._IdAdn, Act, Titre),1,icone,self._ArtMenu['fanar'],is_folder)
        else:
            for tag, (Titre, Url, is_folder, icone, Tmage) in Menu.items():
                if icone != "":
                    Titre = cLiveSPOpt().ConvNom(base64.b64decode(str(Titre)))
                    #print "list m3u: "+Titre+' {0}?action=Play&Url={1}&ElemMenu={2}&Tmage={3}'.format(self._IdAdn,Url,"LireVideo2",Tmage)+" Icone= "+base64.b64decode(icone)
                    if base64.b64decode(icone)==self._ArtMenu['lecture']:
                        self.addDir(Titre,'{0}?action=Play&Url={1}&ElemMenu={2}&Adult=0'.format(self._IdAdn,Url,"LireVideo2"),1,self._ArtMenu['lecture'],self._ArtMenu['fanar'],is_folder)
                    elif base64.b64decode(icone)==self._ArtMenu['info']:
                        URL=base64.b64decode(str(Url))
                        cCommands=[]
                        cCommands.append(("Lire le Fichier",'XBMC.RunPlugin({0}?action=OuvTxt&Url={1}&ElemMenu={2})'.format(self._IdAdn,base64.b64encode(URL[3:]),"LogSamba")))
                        cCommands.append(("Supprimer le fichier",'XBMC.RunPlugin({0}?action=SupFich&Url={1}&ElemMenu={2})'.format(self._IdAdn,base64.b64encode(URL[3:]),"LogSamba")))
                        if URL.startswith("LOG"):
                            self.addDir(Titre,'{0}?action=OuvTxt&Url={1}&ElemMenu={2}'.format(self._IdAdn,base64.b64encode(URL[3:]),"LogSamba"),1,self._ArtMenu['lecture'],self._ArtMenu['fanar'],is_folder,contextCommands=cCommands)
                    else:
                        cCommands=[]
                        cCommands.append(("Telecharger vidéo",'XBMC.RunPlugin({0}?action=Play&Url={1}&ElemMenu={2}&Adult=1)'.format(self._IdAdn,Url,"DL")))
                        cCommands.append(("Afficher les photos",'XBMC.RunPlugin({0}?action=FichierEnCour&ElemMenu={1}&Adult=1&Icone={2}&timage={3})'.format(self._IdAdn,"Photo",base64.b64decode(icone),Tmage)))
                        self.addDir(Titre,'{0}?action=Play&Url={1}&ElemMenu={2}&Adult=1'.format(self._IdAdn,Url,"LireVideo2"),1,base64.b64decode(icone),self._ArtMenu['fanar'],is_folder,contextCommands=cCommands)
                else:
                    self.addDir(base64.b64decode(Titre),'{0}?action=Menu&ElemMenu={1}&Option={2}&Url={3}'.format(self._IdAdn,"Adult","TV",Url),1,self._ArtMenu['lecture'],self._ArtMenu['fanar'],True)

        xbmcplugin.setPluginCategory( handle=int(sys.argv[1]), category="xAmAx" )
        if TriAuto: xbmcplugin.addSortMethod( handle=int(sys.argv[1]), sortMethod=xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
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
        _MenuTV={"Afficher Les chaines Tv":("TV","AffichTV",True),
                      "Mise A Jour Liste de chaines":("TV","MajTV",True)}
        MenuTV = _MenuTV
        if self.adn.getSetting(id="MajtvAuto")=="true":
            print "Recherche mise a jour si première ouverture de la journée"
            DateDerMajTv = str(self.adn.getSetting(id="DateTvListe"))
            print "Dernière Mise a jour: "+DateDerMajTv
            if str(DateDerMajTv)!=strftime("%d-%m-%Y", gmtime()):
                Retour = cLiveSPOpt().RechercheChaine(self.AdresseAdnUtil)
                if Retour=="OK":
                    self.adn.setSetting(id="DateTvListe", value=strftime("%d-%m-%Y", gmtime())) #%H:%M:%S"
        if self.adn.getSetting(id="CreerBouq")=="true":
            DBxAmAx = db(self.dbxAmAx)
            if Retour=="OK" or MiseAJourOK==True or not DBxAmAx.TableExist("UrlBouquet"):
                print "Création de bouquet"
                cLiveSPOpt().CreerBouquet(self.AdresseAdnUtil)
            print "Ouverture Liste Bouquet de: "+self.dbxAmAx
            cBouq = db(self.dbxAmAx).Select(Table="Bouquet", Colonnes="NomBouq", Where="", Order="Ordre ASC")
            for NomBouq in cBouq:
                MenuTV.update({"Bouquet "+str(NomBouq[0]): ("TV","Bouq"+str(NomBouq[0]),True)})
        self.AfficheMenu(MenuTV)

    def AfichListeTS(self,ListeChaine=[], Colon="Nom, Url", Where="", Ordre="Nom", Bouquet=""):
        if len(ListeChaine)>0:
            for Nom, Url, Entete in ListeChaine:
                self.addDir(Nom,
                       '{0}?action=Play&Url={1}&ElemMenu={2}&NomLu={3}'.format(self._IdAdn, base64.b64encode(urlib.quote_plus(Url+"|"+Entete)), "LireVideo", base64.b64encode(Nom)),
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
                    if Url.startswith("plugin://"): 
                        self.addDir(str(i)+"-"+Nom,
                           '{0}?action=Play&Url={1}&ElemMenu={2}&NomLu={3}'.format(self._IdAdn, base64.b64encode(urlib.quote_plus(Url)), "LireVideo",base64.b64encode(Nom)),
                           1,
                           self._ArtMenu['thumb'],
                           self._ArtMenu['fanar'],
                           True)
                    else:
                        self.addDir(str(i)+"-"+Nom,
                           '{0}?action=Play&Url={1}&ElemMenu={2}&NomLu={3}'.format(self._IdAdn, base64.b64encode(urlib.quote_plus(Url)), "LireVideo",base64.b64encode(Nom)),
                           1,
                           self._ArtMenu['thumb'],
                           self._ArtMenu['fanar'],
                           False)
        xbmcplugin.setPluginCategory(handle=int(sys.argv[1]), category="lecture" )
        xbmcplugin.endOfDirectory(int(sys.argv[1]))
    
    def addDir(self,name,url,mode,iconimage,fanart,is_Folder,infos={},cat='',contextCommands=[]):
        u  =url
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Video", infoLabels=infos )
        liz.setProperty('Fanart_Image',fanart)
        if len(contextCommands)>0:
            liz.addContextMenuItems ( contextCommands, replaceItems=False)
            
        ok =xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=is_Folder)


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
        Url_Plugin_Version = self.UrlRepo+"repo/"+self.nomPlugin+"/README.md"
        print 'xAmAx Recherche mise a jour...'
        try:
            data = cDL().TelechargPage(Url_Plugin_Version)
            print 'Lecture de la version du plugin distant: ' + data
        except:
            data = ""
            print 'Erreur de la lecture de la version du plugin: ' + Url_Plugin_Version
            
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
                    xbmcvfs.mkdir(self.AdresseAdnUtil)
                except: pass
                dest = os.path.join(self.AdresseAdnUtil, 'DerMaj.zip')
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
        
    def MajAuto(self,ForceMaj=False,TabMaj=[]): #,NomMaj,Ext,resources=""
        if len(TabMaj)==0:
            DL = cDL().TelechargPage(url=self.UrlRepo+self.nomPlugin+"/MajList")
            #DL = "RegroupChaine,.sql,resources/,1\nChaineBouquet,.sql,resources/,1"
            if not DL.startswith("Erreur"):
                Stab=DL.split("\n")
                if len(Stab)>1:
                    for Fich in Stab:
                        if "," in Fich:
                            TabMaj.append((Fich.split(",")))
        print "---Taille liste mise à jour:"+str(len(TabMaj))
        if len(TabMaj)>0:
            dp = xbmcgui.DialogProgress()
            dp.create("Recherche de mise à jour automatique:")
            sleep(0.5)
            increment = 100/len(TabMaj)
            total = 0
            for NomMaj,Ext,resources,Version in TabMaj:
                print "---Mise à jour de : "+NomMaj+Ext+" Version:"+Version
                total += increment
                dp.update(total,"Recherche mise à jour : "+NomMaj)
                sleep(0.2)
                try:
                    VersionAdn = self.adn.getSetting(id=NomMaj)
                    if VersionAdn=="": VersionAdn = 0
                        
                    if ((int(VersionAdn) != int(Version))or(ForceMaj)):
                        if resources==None:
                            DL = cDL().TelechargPage(url=self.UrlRepo+self.nomPlugin+"/"+NomMaj+Ext)
                        else:
                            DL = cDL().TelechargPage(url=self.UrlRepo+self.nomPlugin+"/"+resources+NomMaj+Ext)
                        if not DL.startswith("Erreur"):
                            if resources==None:
                                AdresseFich = os.path.join(self.AdresseAdn, NomMaj+Ext)
                            elif resources=="":
                                AdresseFich = os.path.join(self.AdresseAdn, NomMaj+Ext)
                            else:
                                TabResources = resources.split("/")
                                cheminRes = os.path.join(self.AdresseAdn,TabResources[0])
                                for x in range(1,len(TabResources)-1):
                                    if TabResources[x]!="": cheminRes = os.path.join(cheminRes,TabResources[x])
                                xbmcvfs.mkdirs(cheminRes)
                                AdresseFich = os.path.join(cheminRes, NomMaj+Ext)
                            fichier = open(AdresseFich, "w")
                            fichier.write(DL)
                            fichier.close()
                            if Ext==".sql":
                                print "---recherche de "+self.dbxAmAx+" = "+str(os.path.exists(self.dbxAmAx))
                                print "---recherche de la table " + NomMaj+" = "+str(db(self.dbxAmAx).TableExist(NomMaj))
                                if NomMaj=="xAmAxDB":
                                    print "---recherche de "+self.dbxAmAx
                                    if os.path.exists(self.dbxAmAx):
                                        xbmcvfs.delete(self.dbxAmAx)
                                elif db(self.dbxAmAx).TableExist(NomMaj):
                                    print "---delete table "+NomMaj
                                    db(self.dbxAmAx).Delete(NomMaj)
                                print "création de la table "+NomMaj
                                db(self.dbxAmAx).ExecutFichSQL(AdresseFich)
                            print "Maj= "+NomMaj+" : "+Version
                            self.adn.setSetting(id=NomMaj, value=str(int(Version)))
                            print "Mise a jour de "+NomMaj+" OK"
                except:
                    print "Erreur mise a jour: "+str(sys.exc_info()[0])
                    dp.close()
                    return "Erreur mise a jour: "+str(sys.exc_info()[0])
            dp.close()
            if not ForceMaj: self.adn.setSetting(id="MajV", value=self.vertionMaj)
            return "OK"
        else:
            if not ForceMaj: self.adn.setSetting(id="MajV", value=self.vertionMaj)
            return "OK"
        
    def RechMajAuto(self,NomMaj,resources="",ForceMaj=False):
        try:
            AdresseVersion = self.UrlRepo+self.nomPlugin+"/"+resources+NomMaj
            VRech = cDL().TelechargPage(AdresseVersion)
            if not VRech.startswith("Erreur"):
                VLspopt = self.adn.getSetting(id=NomMaj)
                print "Version "+NomMaj+": "+VLspopt+" Version sur internet: "+VRech
                if ((int(VLspopt)!=int(VRech)) or (ForceMaj)):
                    print "ForceMaj: "+str(ForceMaj)
                    return str(VRech)
                else:
                    return ""
        except:
            print "Erreur mise a jour: "+str(sys.exc_info()[0])
            return "Erreur mise a jour: "+str(sys.exc_info()[0])

    def InstallExt(self,NomExt, Repo="", DialogOK=False):
        from resources.ziptools import ziptools
        try:
            xbmcvfs.mkdir(self.AdresseAdnUtil)
        except: pass
        #try:
        dest = os.path.join(self.AdresseAdnUtil, 'ExtDl.zip')
        MAJ_URL = self.UrlRepo+"repo/"+NomExt+'/'+NomExt+'.zip'
        print 'Démarrage du téléchargement de:' + MAJ_URL
            
        if cDL().TelechargementZip(MAJ_URL,dest):
        
            unzipper = ziptools()
            unzipper.extract(dest,self.extpath)

            if DialogOK:  
                lign1 = 'Installation de '+NomExt+':'
                lign2 = "L'installation est terminé avec succés!"
                xbmcgui.Dialog().ok('xAmAx', lign1, lign2)
                
            if os.remove( dest ):
                print 'Suppression du fichier télécharger'
            executebuiltin("UpdateLocalAddons")
            executebuiltin("UpdateAddonRepos")
            sleep(1.5)
            path2 = translatePath('special://userdata/Database/')
            try:
                filenames = next(os.walk(path2))[2]
                for x in filenames:
                    if "ddons" in x:
                        tabAddon=db(os.path.join(path2, x)).Select(Table="installed", Colonnes="enabled", Where="addonID='"+NomExt+"'")
                        if len(tabAddon) == 1:
                            print '----Addon Activer : '+str(int(tabAddon[0][0]))
                            if Repo!="":
                                print "---repo: " + Repo
                                db(os.path.join(path2, x)).Update(Colonnes="enabled = ?, origin = ?",Valeur=("1",Repo),Where="addonID = '"+NomExt+"'")
                            else:
                                db(os.path.join(path2, x)).Update(Where="addonID = '"+NomExt+"'")
                        else:
                            db(os.path.join(path2, x)).Insert(Table="installed",
                                                              Colonnes="addonID,enable,installDate,lastUpdated,lastUsed,origin",
                                                              Valeurs=(NomExt,"1",datetime.now(),datetime.now(),datetime.now(),Repo))
                            print '----Creation Addon Activer : '+NomExt
            except:
                pass
            executebuiltin("UpdateLocalAddons")
            executebuiltin("UpdateAddonRepos")
            sleep(1.5)
            return True
        #except:
        #    pass
        if os.path.exists(dest):
            os.remove( dest )
        if os.path.exists(os.path.join(self.extpath, NomExt)):
            xbmcvfs.rmdir(os.path.join(self.extpath, NomExt))
        return False

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
                    if params['ElemMenu']=="VisuLiveStream":
                        self.AffichMenuTv()
                    if params['ElemMenu']=='AffichTV':
                        self.AfficheMenu(self.MajMenuRegroup())
                    if params['ElemMenu'][:4]=="Bouq":
                        self.AfichListeTS(Bouquet=params['ElemMenu'][4:])
                    if params['ElemMenu'][:13]=="ChaineRegroup":
                        if params['ElemMenu'][13:]=="LesAutres":
                            self.AfichListeTS(Where="IDLP NOT IN "+str(self.adn.getSetting(id="ListAutre")))
                        else:
                            NomChaine = base64.b64decode(str(params['ElemMenu'][13:]))
                            print "Recherche "+NomChaine+" dans le Liste Regroup de: "+self.dbxAmAx
                            Retour = db(self.dbxAmAx).Select(Table="RegroupChaine",
                                                             Colonnes="PasDansNom",
                                                             Where="NomRegroup = '"+NomChaine+"'",
                                                             Order="")
                            ANDWHERE = ""
                            if len(Retour)==1:
                                if Retour[0][0] != None and Retour[0][0] != "":
                                    ANDWHERE = " AND Nom NOT LIKE '%"+Retour[0][0]+"%' "
                            self.AfichListeTS(Where="Nom LIKE '"+NomChaine+"%'"+ANDWHERE)
                    if params['ElemMenu']=='MajTV':
                        Retour2 = cLiveSPOpt().RechercheChaine(self.AdresseAdnUtil)
                        if Retour2=="OK":
                            self.AffichMenuTv(MiseAJourOK=True)
                        else:
                            dialog = xbmcgui.Dialog()
                            ok = dialog.ok("Erreur chaines TV", Retour2)
                    if params['ElemMenu']=="Adult":
                        try:
                            Url = params['Url']
                            ListAff = cLiveSPOpt().AdulteSources(Url)
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
                    if params['ElemMenu']=="InstalF4m":
                        dialog = xbmcgui.Dialog()
                        if self.InstallExt("script.video.F4mProxy"):
                            if self.InstallExt("plugin.video.f4mTester"):
                                ok = dialog.ok("Installation de F4m",
                                               "F4mProxy et F4mTester ont était installer avec succés!",
                                               "Vous pourez profiter ensuite de mon menu Chaines TV et bouquet!")
                            else:
                                ok = dialog.ok("Installation de F4mTester",
                                               "Erreur d'installation de F4mTester!",
                                               "Désolé pour ce problème!")
                        else:
                            ok = dialog.ok("Installation de F4mProxy",
                                               "Erreur d'installation de F4mProxy!",
                                               "Désolé pour ce problème!")

                if params['Option']=='vStream':#----------------------------------------------------------------------------------------
                    if params['ElemMenu']=="VisuVstream":
                        if cvStreamOpt().RechercheBase():
                            MenuvStream={"1 - Modifier la vitesse de téléchargement":("vStream","DownloadVstream",True),
                                               "2 - Démarrer vStream":("vStream","DemarVstream",False),
                                               "3 - Tri Alphabétique des Marques-Pages vStream":("vStream","MPVstream",False),
                                               "4 - Tri Alphabétique de la liste de Recherche vStream":("vStream","RechercheVstream",False)}
                            IdMenu = 4
                        else:
                            MenuvStream={"1 - Modifier la vitesse de téléchargement":("vStream","DownloadVstream",True),
                                               "2 - Démarrer vStream":("vStream","DemarVstream",False)}
                            IdMenu = 2
                        if Kmod != None:
                            IdMenu += 1
                            KM = Kmod.KodiMod(Type='video', Nom='vStream', Plugin='plugin.video.vstream', Icon='icon.png')
                            if KM.LienExist():
                                MenuvStream.update({str(IdMenu)+" - Suppression du lien vers vStream dans le menu vidéo": ("vStream","SupprimLien",False)})
                            else:
                                MenuvStream.update({str(IdMenu)+" - Création du lien vers vStream dans le menu vidéo": ("vStream","CreerLien",False)})
                        self.AfficheMenu(MenuvStream)
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
                    if params['ElemMenu']=="InstallvStream":
                        dialog = xbmcgui.Dialog()
                        if self.InstallExt("repository.vstream"):
                            if self.InstallExt("plugin.video.vstream","repository.vstream"):
                                ok = dialog.ok("Installation de vStream",
                                               "vStream et sont dépo ont était installer avec succés!",
                                               "Vous pourez profiter de mon menu Option de vStream une fois que vStream aura démarrer!")
                            else:
                                ok = dialog.ok("Installation de vStream",
                                               "Erreur d'installation de vStream!",
                                               "Désolé pour ce problème!")
                        else:
                            ok = dialog.ok("Installation de vStream",
                                               "Erreur d'installation de vStream!",
                                               "Désolé pour ce problème!")
                    if params['ElemMenu']=="DemarVstream":
                        executebuiltin("ActivateWindow(10025,plugin://plugin.video.vstream/,return)") #RestartApp")
                    if params['ElemMenu']=="CreerLien":
                        KM = Kmod.KodiMod(Type='video', Nom="vStream", Plugin='plugin.video.vstream', Icon='icon.png')
                        Retour = KM.CreerLien()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Création du lien dans le menu video: ", Retour)
                        executebuiltin('XBMC.Container.Update')
                        executebuiltin('XBMC.Container.Refresh')
                    if params['ElemMenu']=="SupprimLien":
                        KM = Kmod.KodiMod(Type='video', Nom="vStream", Plugin='plugin.video.vstream', Icon='icon.png')
                        Retour = KM.SupprimLien()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Suppression du lien dans le menu video: ", Retour)
                        executebuiltin('XBMC.Container.Update')
                        executebuiltin('XBMC.Container.Refresh')
                if params['Option']=="Kodi": #----------------------------------------------------------------------------------------
                    if params['ElemMenu']=="VisuKodi":
                        MenuKodi={}
                        IdMenu = 0
                        if Conf:
                            IdMenu = 1
                            MenuKodi.update({str(IdMenu)+" - Configuration Connexion Kodi":("Kodi","Config",True)})
                        if Debi != None:
                            IdMenu += 1
                            MenuKodi.update({str(IdMenu)+" - Test de votre connexion internet avec speedtest.net":("Kodi","TestDebit",False)})
                        if Kmod != None:
                            IdMenu += 1
                            MenuKodi.update({str(IdMenu)+" - Activer/Désactiver le mode débugage! (plus d'info dans le journal d'erreur)": ("Kodi","Debug",False)})
                        IdMenu += 1
                        MenuKodi.update({str(IdMenu)+" - Afficher le Journal d'erreur":("Kodi","AffichLog",False)})
                        IdMenu += 1
                        MenuKodi.update({str(IdMenu)+" - Envoyer le journal d'erreur sur le site slexy.org":("Kodi","EnvoiLog",False)})
                        IdMenu += 1
                        MenuKodi.update({str(IdMenu)+" - Effacer le fichiers temporaires":("Kodi","SupTemp",False)})
                        IdMenu += 1
                        MenuKodi.update({str(IdMenu)+" - Effacer les miniatures en mémoire":("Kodi","SupThumb",False)})
                        self.AfficheMenu(MenuKodi)
                    if params['ElemMenu']=="AffichLog":
                        print "AffichLog: "
                        Affich=TxtAffich()
                        Affich.Fenetre(Chemin=translatePath('special://logpath')+"kodi.log",
                                        line_number=0,Invertion=True,LabTitre="Journal d'erreur")
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

                    if params['ElemMenu']=="EnvoiLog":
                        dialog = xbmcgui.Dialog()
                        if dialog.yesno("Envoi du journal d'erreur...", "Voulez vous envoyer votre journal d'erreur sur le site slexy.org ?",'','','Non', 'Oui'):
                            cheminLog = translatePath('special://logpath/')
                            retour = cDL().EnvoiLogKodi(cheminLog,next(os.walk(cheminLog))[2])
                            if retour.startswith("Erreur"):
                                dialog.ok("Envoi du journal d'erreur...",retour)
                            else:
                                dialog.ok("Envoi du journal d'erreur...","Voici le lien de votre journal d'erreur, veuillez le noter:" + '  ' + retour)

                    if params['ElemMenu']=="Config":
                        if Conf!= None: Conf.autoConfig()

                    if params['ElemMenu']=="Debug":
                        Kmod.KodiMod().ModeDebug()

                    if params['ElemMenu']=="TestDebit":
                        Resultat = Debi.TestVitesseDeb().Demare()
                        dialog = xbmcgui.Dialog()
                        dialog = dialog.ok("Résultat du test de débit de votre connexion:",Resultat)
                
                if params['Option']=="xAmAx": #----------------------------------------------------------------------------------------
                    if params['ElemMenu']=="VisuxAmAx":
                        print "Afficher menu xAmAx"
                        MenuxAmAx = {"1 - Mise a jour de la version de xAmAx-Mod":("xAmAx",'MiseAJourxAmAx',False),
                                     "2 - Mise à jour Manuelle de l'application":("xAmAx", 'MajAplixAmAx', False),
                                     "3 - Paramètres de xAmAx":("xAmAx","ParamxAmAx",False)} #,
                                     #"4 - test":("xAmAx",'test',True)}
                        IdMenu = 4
                        if self.adn.getSetting(id="stban")=="true":
                            IdMenu += 1
                            if self.adn.getSetting(id="p")=="":
                                MenuxAmAx.update({str(IdMenu)+" - PC distant: Ajouter un Mot de passe": ("PC","PssPc",True)})
                            else:
                                MenuxAmAx.update({str(IdMenu)+" - PC distant: Changer le Mot de passe": ("PC","PssPc",True)})
                        if Kmod != None:
                            IdMenu += 1
                            KM = Kmod.KodiMod(Type='video',Plugin='plugin.video.xamax-mod',Icon='icon.png')
                            if KM.LienExist():
                                MenuxAmAx.update({str(IdMenu)+" - Suppression du lien vers xAmAx-Mod dans le menu vidéo": ("xAmAx","SupprimLien",False)})
                            else:
                                MenuxAmAx.update({str(IdMenu)+" - Création du lien vers xAmAx-Mod dans le menu vidéo": ("xAmAx","CreerLien",False)})
                        IdMenu += 1
                        MenuxAmAx.update({str(IdMenu)+" - Version "+self.__version__:("xAmAx","InfoVersion",False)})
                        self.AfficheMenu(MenuxAmAx)
                    if params['ElemMenu']=="InfoVersion":
                        print "InfoVersion: "
                        Affich=TxtAffich()
                        Affich.Fenetre(Chemin=os.path.join(self.AdresseAdn,"changelog.txt"),line_number=0)
                    if params['ElemMenu']=="MiseAJourxAmAx":
                        Retour = self.RechercheMAJ()
                        if Retour != "OK":
                            dialog = xbmcgui.Dialog()
                            ok = dialog.ok("Mise à jour xAmAx", Retour)
                    if params['ElemMenu']=="MajAplixAmAx":
                        self.MajPresente = False
                        print "Recherche auto de Mise a jour"
                        ret = self.RechMajAuto("MajV")
                        if not ret.startswith("Erreur"):
                            print "Maj: "+ret
                            self.vertionMaj = ret
                            Retour = self.MajAuto(True)
                            dialog = xbmcgui.Dialog()
                            if Retour != "OK":
                                dialog.ok("Mise à jour automatique", Retour, "")
                            else:
                                dialog.ok("Mise à jour automatique", "Mise à jour réalisée avec succès!", "")
                                executebuiltin('XBMC.Container.Update')
                                executebuiltin('XBMC.Container.Refresh')
                    if params['ElemMenu']=="test":
                        print "test: "
                        Retour = Kmod.KodiMod().ModeDebug()
                        """dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Lancement du mode de débugage: ", Retour)
                        executebuiltin('XBMC.Container.Update')
                        executebuiltin('XBMC.Container.Refresh')"""
                        #executebuiltin('XBMC.ToggleDebug')
                    if params['ElemMenu']=="ParamxAmAx":
                        self.adn.openSettings()
                    if params['ElemMenu']=="LireUrl":
                        ListAff = cLiveSPOpt().LireM3u(CheminxAmAx=self.AdresseAdnUtil)
                        i=0
                        MenuRegroup={}
                        for Nom,Url in ListAff:
                            i+=1
                            Nom=base64.b64encode(Nom)
                            Url=base64.b64encode(Url)
                            Thumb=base64.b64encode(self._ArtMenu['lecture'])
                            MenuRegroup.update({"M3u"+str(i): (Nom, Url, True, Thumb,[])})
                        self.AfficheMenu(MenuRegroup,True)
                    if params['ElemMenu']=="LireF4m":
                        ListAff = cLiveSPOpt().LireM3u(CheminxAmAx=self.AdresseAdnUtil, F4m=True)
                        i=0
                        MenuRegroup={}
                        for Nom,Url in ListAff:
                            i+=1
                            Nom=base64.b64encode(Nom)
                            Url=base64.b64encode(Url)
                            Thumb=base64.b64encode(self._ArtMenu['lecture'])
                            MenuRegroup.update({"Video"+str(i): (Nom, Url, True, Thumb,[])})
                        self.AfficheMenu(MenuRegroup,True)
                    if params['ElemMenu']=="CreerLien":
                        KM = Kmod.KodiMod(Type='video',Plugin='plugin.video.xamax-mod',Icon='icon.png')
                        Retour = KM.CreerLien()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Création du lien dans le menu video: ", Retour)
                        executebuiltin('XBMC.Container.Update')
                        executebuiltin('XBMC.Container.Refresh')
                    if params['ElemMenu']=="SupprimLien":
                        KM = Kmod.KodiMod(Type='video',Plugin='plugin.video.xamax-mod',Icon='icon.png')
                        Retour = KM.SupprimLien()
                        dialog = xbmcgui.Dialog()
                        ok = dialog.ok("Suppression du lien dans le menu video: ", Retour)
                        executebuiltin('XBMC.Container.Update')
                        executebuiltin('XBMC.Container.Refresh')

                if params['Option']=="PC": #----------------------------------------------------------------------------------------
                    from resources.Samba import EnvSamba
                    if params['ElemMenu']=="stBan":
                        print "Afficher menu xAmAx"
                        dialog = xbmcgui.Dialog()
                        d = dialog.input('Entrer votre mot de passe', type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
                        if d == base64.b64decode(self.adn.getSetting(id="p")):
                            _MenuPC={"1 - Afficher l'historique":("PC","AffichLog",True),
                                     "2 - Réaliser une action":("PC","ActPC",True)}
                            self.AfficheMenu(_MenuPC)
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
                        _MenuActPC={"Changer heure d'arrêt":("PC","ActHArret",True),
                                        "Arrêter le pc":("PC","ActArretDirect",True),
                                        "Arrêt de l'arrêt automatique":("PC","ActArretAuto",True),
                                        "Re-démarrage de l'arrêt automatique":("PC","ActDemarArret",True),
                                        "Interrogation Heure d'arrêt":("PC","ActIHArret",True),
                                        "Interrogation Heure du pc":("PC","ActHeurePC",True)}
                        self.AfficheMenu(_MenuActPC)
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
                    print "----- xAmAx-Mod ----- lecture de " + params['Url']
                    finalUrl=base64.b64decode(params['Url'])
                    NomVideo=base64.b64decode(params["NomLu"])
                    if finalUrl.startswith("plugin://"):
                        executebuiltin('XBMC.RunPlugin('+urlib.unquote(finalUrl)+')')
                    else:
                        listitem = xbmcgui.ListItem(NomVideo)
                        listitem.setInfo('video', {'Title': NomVideo, 'Genre': 'TV'})
                        Player().play(urlib.unquote(finalUrl), listitem)
                if params['ElemMenu']=="LireVideo2":
                    if params['Adult']=="1":
                        html = cDL().TelechargPage('http://www.mrsexe.com/' + base64.b64decode(params['Url']))
                        videourl = re.compile(r"src='(/inc/clic\.php\?video=.+?&cat=mrsex.+?)'").findall(html)
                        print "--videourl = "+str(videourl[0])
                        html = cDL().TelechargPage('http://www.mrsexe.com/' + videourl[0])
                        #print "--html = "+html
                        videourls = re.compile(r".src.\"(.+?)\".+?'", re.DOTALL).findall(html)
                        videourls = sorted(videourls, key=lambda tup: tup[1], reverse=True)
                        print "--videourl.. = "+(str(videourl[0]))
                        videourl = str(videourls[0])
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
                            videourls = re.compile(r".src.\"(.+?)\".+?'", re.DOTALL).findall(html)
                            videourls = sorted(videourls, key=lambda tup: tup[1], reverse=True)
                            print "--videourl_DL.. = "+(str(videourl[0]))
                            videourl = str(videourls[0])
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
                            if not xbmcvfs.exists(os.path.join(self.AdresseAdnUtil,NomFichVid)):
                                break
                        cDL().DLFich(videourl,os.path.join(self.AdresseAdnUtil,NomFichVid), DPView=True)
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
                    cheminPhoto=os.path.join(self.AdresseAdnUtil,"photo")
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
            _MenuList={"1 - Options de Kodi":("Kodi","VisuKodi",True),
                        "2 - Options de xAmAx-Mod":("xAmAx",'VisuxAmAx',True)}
            # Création de chaque élément
            IdMenu = 2
            vStream = cvStreamOpt().TryConnectvStream() # "vStream non installer!" TryConnectvStream()
            if vStream != "OK":
                IdMenu += 1
                _MenuList.update({str(IdMenu)+" - "+vStream:("vStream", 'InstallvStream', True)})
            else:
                IdMenu += 1
                _MenuList.update({str(IdMenu)+" - Options de vStream":("vStream", "VisuVstream", True)})
            if self.RechercheF4M():
                IdMenu += 1
                _MenuList.update({str(IdMenu)+" - Chaines TV et bouquet":('TV', "VisuLiveStream", True)})

                IdMenu += 1
                _MenuList.update({str(IdMenu)+" - "+"Ouvrir fichier m3u avec le lecteur F4m":('xAmAx', "LireF4m", True)})
            else:
                IdMenu += 1
                _MenuList.update({str(IdMenu)+" - "+"Installation de F4mProxy et Tester":('TV', "InstalF4m", True)})
            IdMenu += 1
            _MenuList.update({str(IdMenu)+" - "+"Ouvrir fichier m3u avec le lecteur de kodi":('xAmAx', "LireUrl", True)})

            if self.adn.getSetting(id="Adult")=="true":
                IdMenu += 1
                _MenuList.update({str(IdMenu)+" - "+"Plus":('TV', "Adult", True)})
            if self.adn.getSetting(id="stban")=="true":
                IdMenu += 1
                _MenuList.update({str(IdMenu)+" - "+"PC distant":('PC', "stBan", True)})
            self.AfficheMenu(_MenuList)
            if self.adn.getSetting(id="MajAuto")=="true" and self.MajPresente:
                self.MajPresente = False
                print "Recherche auto de Mise a jour"
                ret = self.RechMajAuto("MajV")
                if ret != "" and not ret.startswith("Erreur"):
                    self.vertionMaj = ret
                    Retour = self.MajAuto()
                    sleep(2.0)
                    if Retour != "OK":
                        dialog = xbmcgui.Dialog()
                        dialog.ok("Mise à jour automatique", Retour, "")
                    """else:
                        executebuiltin('XBMC.Container.Update('+str(sys.argv[0])+')')
                        executebuiltin('XBMC.Container.Refresh')"""
                    
            if not os.path.exists(os.path.join(self.AdresseAdn,"resources","KodiMod.py")):
                print "---recherche Mise à jour avec KodiMod"
                self.MajAuto(True)
                print "---Mise à jour avec xAmAxdb"
                                  
            if not os.path.exists(os.path.join(self.AdresseAdn,"resources","skins","DefaultSkin","media","Background","Fenetre.png")):
                print "---recherche Mise à jour Skin"
                MajSkin=[("Fenetre",".png","resources/skins/DefaultSkin/media/Background/",1),
                  ("button-focus_grey",".png","resources/skins/DefaultSkin/media/Button/",1),
                  ("button-focus_lightxAm",".png","resources/skins/DefaultSkin/media/Button/",1),
                  ("MenuItemFOxAm",".png","resources/skins/DefaultSkin/media/RadioButton/",1),
                  ("MenuItemNF",".png","resources/skins/DefaultSkin/media/RadioButton/",1),
                  ("radiobutton-focus",".png","resources/skins/DefaultSkin/media/RadioButton/",1),
                  ("radiobutton-nofocus",".png","resources/skins/DefaultSkin/media/RadioButton/",1),
                  ("osd_slider_nibNFxAm",".png","resources/skins/DefaultSkin/media/Slider/",1),
                  ("osd_slider_nibxAm",".png","resources/skins/DefaultSkin/media/Slider/",1)]
                self.MajAuto(True,MajSkin)
                print "---Mise à jour avec Skin"
                    
