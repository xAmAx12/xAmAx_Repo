#-*-coding:utf8;-*-
#qpy:console
#qpy:2

# -*- coding:utf-8 -*-
import os
from base64 import b64decode
import xbmcvfs

class EnvSamba():
    
    def __init__(self,samba_ip = "192.168.1.1", dosEchange = "echange", Fich_present = "Ne/ pas/ supprimer.txt"):
        self.doss_dist = "smb://"+samba_ip+"/"+dosEchange
        self.ConnOK = xbmcvfs.listdir(self.doss_dist+"/"+Fich_present)

    def __del__(self):
        pass
        
    def CreerDossier(self):
        tempDir = randrange(111111,999999)
        command = 'mkdir /mnt/' + str(tempDir)
        if self.EnvoiCmdSud(command) == 0:
            #print ("Création répertoire OK")
            return "/mnt/"+str(tempDir)
        else:
            #print ("Erreur Création répertoire")
            return ""

    def ConvDoss(self, Dossier):
        return Dossier.replace(' ','\ ').replace('(','\(').replace(')','\)')

    def SupprimRep(self,path):
        if xbmcvfs.rmdir(path):
            print "Suppression répertoire OK"
            return True
        else:
            print "Erreur Suppression répertoire"
            return False

    def EnvoiFichier(self,txtEchang,NomFich):
        if txtEchang != "" :
            try:
                f = xbmcvfs.File(os.path.join(self.doss_dist,self.ConvDoss(NomFich)), 'w')
                result = f.write(txtEchang)
                f.close()
                return result
            except:
                print "Erreur ecriture fichier sur le disque samba"
                return False
        else:
            print "Pas d'action choisis..."

    def ListFichier(self, listDoss = False):
        dirs, files = xbmcvfs.listdir(self.doss_dist)
        if listDoss:
            return dirs
        else:
            return files

    def OuvrirFich(self, NomFich, CheminSauv=""):
        Fich = self.ConvDoss(os.path.join(self.doss_dist,NomFich))
        if CheminSauv != "":
            print "copy du fichier: "+Fich+" dans "+CheminSauv
            success = xbmcvfs.copy(Fich, CheminSauv)
            return success
        else:
            print "Ouveture du fichier: "+Fich
            f = xbmcvfs.File(Fich)
            b = f.read()
            f.close()
            
            textPrint = ''
            for l in b:
                if (ord(l) > 0 and ord(l)!=13 and ord(l) < 126):
                    textPrint += l
                elif (ord(l) > 191  and ord(l) < 198):
                    textPrint += "A" #chr(65)
                elif (ord(l) > 199  and ord(l) < 204):
                    textPrint += "E" #chr(69)
                elif (ord(l) > 203  and ord(l) < 208):
                    textPrint += "I" #chr(73)
                elif (ord(l) > 209  and ord(l) < 215):
                    textPrint += "O" #chr(79)
                elif (ord(l) > 216  and ord(l) < 221):
                    textPrint += "U" #chr(85)
                elif (ord(l) > 223  and ord(l) < 230):
                    textPrint += "a" #chr(97)
                elif (ord(l) > 231  and ord(l) < 236):
                    textPrint += "e" #chr(101)
                elif (ord(l) > 235  and ord(l) < 240):
                    textPrint += "i" #chr(105)
                elif (ord(l) > 241  and ord(l) < 247):
                    textPrint += "o" #chr(111)
                elif (ord(l) > 248  and ord(l) < 253):
                    textPrint += "u" #chr(117)
                elif ord(l) > 125:
                    textPrint += "?"
                    
            if textPrint.startswith(chr(10)):
                textPrint = textPrint[1:]
            return textPrint

    def SupprimFich(self, NomFich):
        Fich = self.ConvDoss(NomFich)
        #print("Suppression du fichier: "+Fich)
        return xbmcvfs.delete(os.path.join(self.doss_dist, Fich))

"""for r in EnvSamba().ListFichier():
    if not r.isDirectory:
        print r.filename"""

#print "lecture: "+EnvSamba().OuvrirFich("2017-06-17_Pg.xama")
