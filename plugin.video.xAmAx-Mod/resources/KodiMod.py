# -*- coding: UTF-8 -*-
# Module: KodiMod
# Author: xamax
# Created on: 17.03.2018

import os
from xbmc import translatePath,executebuiltin
import xbmcvfs

class KodiMod():

    def __init__(self, Type='video', Nom='xAmAx-Mod', Plugin='plugin.video.xAmAx-Mod', Icon='icon.png'):
        #Enregistrement des paramètres
        self.TypeExt = Type
        self.NomExt = Nom
        self.PlugExt = Plugin
        self.IconExt = os.path.join(translatePath("special://home/addons/".decode('utf-8')), self.PlugExt, Icon)
        self.AdresseLib = os.path.join(translatePath("special://profile".decode('utf-8')), "library", self.TypeExt)
        
    def copieRep(self, Destination, Origine):
        TabRep, TabFich = xbmcvfs.listdir(Origine)
        for Fichier in TabFich:
            Resultat = xbmcvfs.copy( os.path.join( Origine, Fichier ), os.path.join( Destination, Fichier ) )
        for dir in TabRep:
            self.copieRep(os.path.join( Destination, dir ), os.path.join( Origine, dir ) )

    def InitLibrairie(self):
        RepSource = self.AdresseLib
        if not os.path.exists(RepSource):
            xbmcvfs.mkdirs(RepSource)
            RepOrigine = os.path.join(translatePath("special://xbmc".decode( "utf-8" ) ), "system", "library", self.TypeExt)
            self.copieRep(RepSource, RepOrigine)

    def CreerLien(self):
        try:
            self.InitLibrairie()
            TextLien = "<?xml version='1.0' encoding='UTF-8'?>\n"
            TextLien += "<node type='folder'>\n"
            TextLien += "    <label>"+self.NomExt+"</label>\n"
            TextLien += "    <icon>"+self.IconExt+"</icon>\n"
            TextLien += "    <path>plugin://"+self.PlugExt+"/</path>\n"
            TextLien += "</node>"
            f = open(os.path.join(self.AdresseLib, self.NomExt+".xml"),'w')
            f.write(TextLien)
            f.close()
            return "Lien vers l'extension "+self.NomExt+" créer dans le menu vidéo!"
        except:
            return "Erreur lors de la création du lien de l'extension "+self.NomExt+" !"

    def SupprimLien(self):
        os.remove(os.path.join(self.AdresseLib, self.NomExt+".xml"))
        return "Lien vers l'extension "+self.NomExt+" supprimer dans le menu vidéo!"

    def LienExist(self):
        return os.path.exists(os.path.join(self.AdresseLib, self.NomExt+".xml"))

    def ModeDebug(self,valeur="true"):
        executebuiltin('XBMC.ToggleDebug')
                  
