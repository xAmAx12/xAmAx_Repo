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

    vStream = None
    adresseVstream = ""
    TableV = ""
    CreerTbl = ""
    InserTbl = ""
    InserTbl2 = ""
    FinAffich = ""

    def __init__(self):
        try:
            self.vStream  = xbmcaddon.Addon('plugin.video.vstream')
            self.adresseVstream=str(xbmc.translatePath(vStream.getAddonInfo('profile').decode('utf-8')))
        except:
            pass

    def TryConnectvStream(self):
        try:
            xbmc.log("TryConnectvStream")
            self.vStream  = xbmcaddon.Addon('plugin.video.vstream')
            self.adresseVstream=str(xbmc.translatePath(self.vStream.getAddonInfo('profile').decode('utf-8')))
            xbmc.log("TryConnectvStream adresse: " + self.adresseVstream)
            if xbmcvfs.exists(os.path.join(self.adresseVstream,'Vstream2.db')):
                os.remove(os.path.join(self.adresseVstream,'Vstream2.db'))
            return "OK"
        except:
            return "vStream non installer!"
    
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

