# -*- coding: utf-8 -*-
# Module: vStreamOpt
# Author: xamax
# Created on: 20.11.2016
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html
import os
import xbmcvfs
import xbmcaddon
import xbmc
import sqlite3 as lite

class cvStreamOpt():    

    def __init__(self):

        self.vStream  = xbmcaddon.Addon('plugin.video.vstream')
        self.nomPlugin = 'plugin.video.xAmAx-Mod'
        self.adn = xbmcaddon.Addon(self.nomPlugin)
        self.adresseVstream=str(xbmc.translatePath(self.vStream.getAddonInfo('profile').decode('utf-8')))
        self.adresseResources = os.path.join(str(xbmc.translatePath(self.vStream.getAddonInfo('path').decode('utf-8'))),"resources","lib")
        self.TableV = ""
        self.CreerTbl = ""
        self.InserTbl = ""
        self.InserTbl2 = ""
        self.FinAffich = ""

    def TryConnectvStream(self):
        try:
            xbmc.log("TryConnectvStream adresse: " + self.adresseVstream)
            if xbmcvfs.exists(os.path.join(self.adresseVstream,'Vstream2.db')):
                os.remove(os.path.join(self.adresseVstream,'Vstream2.db'))
            if xbmcvfs.exists(os.path.join(self.adresseVstream,'vstream.db')):
                return "OK"
        except:
            return "vStream non installer!"

        return "vStream non présent!"
    
    def MiseAJourVstream(self, Tables):
        try:
            self.TryConnectvStream()
            self.selectTable(Tables)
            xbmc.log("Création de la nouvelle Base de donnée...")
            NewDB = lite.connect(os.path.join(self.adresseVstream,'Vstream2.db'))
            Curs = NewDB.cursor()
            xbmc.log("Création de la nouvelle Table: "+self.CreerTbl+"...")
            Curs.execute(self.CreerTbl)
            xbmc.log("Connection à la Base de donnée existante\n("+os.path.join(self.adresseVstream,'vstream.db')+")...")
            conn = lite.connect(os.path.join(self.adresseVstream,'vstream.db'))
            c = conn.cursor()
            xbmc.log('SELECT * FROM '+self.TableV)
            c.execute('SELECT * FROM '+self.TableV)
            xbmc.log("Enregistrement de tous les nouveaux Membres de la table...")

            if self.adn.getSetting(id="AjoutNomSite")=="true": AjNomSite = True
            else: AjNomSite = False
            
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
                while Nom[:1]==" ":
                    Nom=Nom[1:]
                if self.TableV=="favorite":
                    Nom2 = row[1]
                    
                    if AjNomSite:
                        site = " - [COLOR yellow]" + row[3] + "[/COLOR]"
                        if len(Nom2)>len(site):
                            if Nom2[len(Nom2)-len(site):]!=site:
                                Nom2=Nom2 + site
                        else:
                            Nom2=Nom2 + site
                    while Nom2[:1]==" ":
                        Nom2=Nom2[1:]
                    Curs.execute(self.InserTbl2,(row[0],Nom2,Nom,row[2],row[3],row[4],row[5],row[6],row[7]))
                else:
                    Curs.execute(self.InserTbl2,(row[0],row[1],Nom,row[2],row[3],row[4],row[5],row[6]))
        except lite.Error as e:
            if conn:
                conn.rollback()
            xbmc.log("Error %s:" % e.args[0])
            return "Erreur de connection à la base vstream!"
            xbmc.log("Erreur de connection à la base vstream!")
            # raise e
        except:
            return "Erreur de mise à jour de la liste!"
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

        xbmc.log("Sauv: "+'SELECT * FROM '+self.TableV+' ORDER BY `title2` ')
        try:
            conn = lite.connect(os.path.join(self.adresseVstream,'vstream.db'))
            c = conn.cursor()
            c.execute("DELETE FROM "+self.TableV)
            NewDB = lite.connect(os.path.join(self.adresseVstream,'Vstream2.db'))
            Curs = NewDB.cursor()
            Curs.execute('SELECT * FROM '+self.TableV+' ORDER BY `title2` ')
            i = 0
            if self.TableV=="favorite":
                for row in Curs:
                    i+=1
                    c.execute(self.InserTbl,(i,row[1],row[3],row[4],row[5],row[6],row[7],row[8]))
            else:
                for row in Curs:
                    i+=1
                    c.execute(self.InserTbl,(i,row[1],row[3],row[4],row[5],row[6],row[7]))
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

        os.remove(os.path.join(self.adresseVstream,'Vstream2.db'))
        xbmc.log(self.FinAffich)
        return self.FinAffich

    def selectTable(self, Table):
        xbmc.log("Selection table: "+Table)
        if Table=='Recherche':
            self.TableV="history"
            self.CreerTbl='''CREATE TABLE `history`
                (`addon_id` integer PRIMARY KEY AUTOINCREMENT,
                `title` TEXT,
                `title2` TEXT,
                `disp` TEXT,
                `icone` TEXT,
                `isfolder` TEXT,
                `level` TEXT,
                `lastwatched` TIMESTAMP);'''
            self.InserTbl='''INSERT INTO history (addon_id,title,disp,icone,isfolder,level,lastwatched)
                    VALUES (?,?,?,?,?,?,?)'''
            self.InserTbl2='''INSERT INTO history (addon_id,title,title2,disp,icone,isfolder,level,lastwatched)
                    VALUES (?,?,?,?,?,?,?,?)'''
            self.FinAffich='''
******************************************************
*   Fin de la sauvegarde des Recherches classés par nom!   *
******************************************************'''
        elif Table=='MarquePage':
            self.TableV="favorite"
            self.CreerTbl='''CREATE TABLE favorite
                    (`addon_id` integer PRIMARY KEY AUTOINCREMENT,
                    `title` TEXT,
                    `title2` TEXT,
                    `siteurl` TEXT,
                    `site` TEXT,
                    `fav` TEXT,
                    `cat` TEXT,
                    `icon` TEXT,
                    `fanart` TEXT);'''
            self.InserTbl='''INSERT INTO favorite (addon_id,title,siteurl,site,fav,cat,icon,fanart)
                            VALUES (?,?,?,?,?,?,?,?)'''
            self.InserTbl2='''INSERT INTO favorite (addon_id,title,title2,siteurl,site,fav,cat,icon,fanart)
                            VALUES (?,?,?,?,?,?,?,?,?)'''
            self.FinAffich='''
********************************************************
 Fin de la sauvegarde des Marques-Pages classés par nom! 
********************************************************'''
            
    def EcritureDownload(self, Vitesse="300"):
        FichDown = os.path.join(self.adresseResources,"download.py")
        FichNouv = os.path.join(self.adresseResources,"download2.py")
        ok = False
        MenuRegroup={}
        try:
            with open(FichDown,'r') as f:
                lines = f.readlines()
             
            with open(FichDown,'w') as f:
                for line in lines:
                    if "if not (self.__bFastMode):" in line:
                        print "_____OK"
                        ok = True 
                    elif ok:
                        Tab1=line.split("xbmc.sleep(")
                        if len(Tab1)>1:
                            line = Tab1[0] + "xbmc.sleep(" + Vitesse + ")\n"
                            ok = False
                    f.write(line)
            return "La modification de la rapiditée de téléchargement est terminée!\nBon téléchargement!"
        except lite.Error as e:
            if conn:
                conn.rollback()
            print "Error %s:" % e.args[0]
            return "Erreur de modification de la rapiditée du téléchargement!"
            # raise e
            
    def LectureDownload(self):
        FichDown = os.path.join(self.adresseResources,"download.py")
        ok = False
        MenuRegroup={}
        try:
            with open(FichDown) as f :
                for line in f :
                    if "if not (self.__bFastMode):" in line:
                        print "_____OK"
                        ok = True
                    elif ok:
                        Tab1=line.split("xbmc.sleep(")
                        if len(Tab1)>1:
                            Tab1=Tab1[1].split(")")
                            print "____Vitesse de téléchargement = "+str(Tab1[0])
                            if Tab1[0] == "300": Def=" - [COLOR yellow] Vitesse Actuelle [/COLOR]"
                            else: Def=""
                            MenuRegroup.update({"[COLOR orange]Vitesse de téléchargement: [/COLOR]": ("vStream","VstreamDl300",True)})
                            MenuRegroup.update({"-1 Par défaut"+Def: ("vStream","VstreamDl300",False)})
                            if Tab1[0] == "200": Def=" - [COLOR yellow] Vitesse Actuelle [/COLOR]"
                            else: Def=""
                            MenuRegroup.update({"-2 légère amélioration"+Def: ("vStream","VstreamDl200",False)})
                            if Tab1[0] == "100": Def=" - [COLOR yellow] Vitesse Actuelle [/COLOR]"
                            else: Def=""
                            MenuRegroup.update({"-3 Amélioration Moyenne"+Def: ("vStream","VstreamDl100",False)})
                            if Tab1[0] == "0": Def=" - [COLOR yellow] Vitesse Actuelle [/COLOR]"
                            else: Def=""
                            MenuRegroup.update({"-4 Téléchargement sans ralentissement"+Def: ("vStream","VstreamDl0",False)})
                            return MenuRegroup
            return "Erreur de recherche de la rapiditée du téléchargement!"
        except lite.Error as e:
            if conn:
                conn.rollback()
            print "Error %s:" % e.args[0]
            return "Erreur de recherche de la rapiditée du téléchargement!"
            print "Erreur de recherche de la rapiditée du téléchargement!"
            # raise e
        

                    
                    

            

