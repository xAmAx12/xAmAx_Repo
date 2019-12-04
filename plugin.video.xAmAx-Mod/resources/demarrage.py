# -*- coding: UTF-8 -*-
import xbmc,xbmcgui,xbmcvfs
import subprocess,os
from time import sleep

#control over player features    
class MyPlayer(xbmc.Player) :
    def __init__ (self):
        xbmc.Player.__init__(self)

    def onPlayBackStarted(self):
        if xbmc.Player().isPlayingVideo():
            #here you can input any command that tdtool would take like "tdtool -v 0 -d 1" to put a dimmable switch to off state
            #print "++++++++Lecture d'une vidéo: "
            xbmc.log("\t[PLUGIN] xAmAx-Mod: Lecture d'une vidéo", xbmc.LOGNOTICE)

            #os.system("tdtool -f 1")

    def onPlayBackEnded(self):
        if (VIDEO == 1):
            #print "++++++++Vidéo Fin!"
            xbmc.log("\t[PLUGIN] xAmAx-Mod: Lecture finit", xbmc.LOGNOTICE)
            #os.system("tdtool -n 1")

    def onPlayBackStopped(self):
        if (VIDEO == 1):
            xbmc.log("\t[PLUGIN] xAmAx-Mod: Lecture stopé", xbmc.LOGNOTICE)
            #print "++++++++Vidéo stoper!"
            #os.system("tdtool -n 1")

    def onPlayBackPaused(self):
        if xbmc.Player().isPlayingVideo():
            #print "++++++++Vidéo Pause!"
            xbmc.log("\t[PLUGIN] xAmAx-Mod: Lecture en pause", xbmc.LOGNOTICE)
            #os.system("tdtool -n 1")

    def onPlayBackResumed(self):
        if xbmc.Player().isPlayingVideo():
            #print "++++++++Vidéo Resume!"
            xbmc.log("\t[PLUGIN] xAmAx-Mod: Lecture redémarrer", xbmc.LOGNOTICE)
            #os.system("tdtool -f 1")


def ConvNom(Nom):
    Saison = ""
    Episode = ""
    Serie = ""
    Site = ""
    Table = Nom.upper().split("]")
    if len(Table)>2:
        Tab2 = Table[1].split("[")
        if ((Tab2[0].startswith("S")) and ("E" in Tab2[0]) and (len(Tab2[0])==6)):
            Saison = Tab2[0][1:3]
            Episode = Tab2[0][-2:]
        Tab2 = Table[2].split("[")
        if len(Tab2[0])>1:
            Serie = Tab2[0]
        if len(Table)>3:
            print str(Table)
            Tab2 = Table[3].split("[")
            if len(Tab2[0])>1:
                Site = Tab2[0]
    else:
        NomUp = Nom.upper()
        if "S" in NomUp and "E" in NomUp:
            i=0
            for lettre in NomUp:
                pass
                

    xbmc.log('\t[PLUGIN] xAmAx-Mod Serie: '+Serie+'\n\tSaison: '+Saison +'\n\tEpisode: '+Episode+'\n\tSite: '+Site, xbmc.LOGNOTICE)
            
            
            
#player=MyPlayer()
VIDEO = 0
InfoLecture = None
MemoInfo = None
MemoTitle = None
MemoOriginTitle = None

cached_Cache = "special://home/userdata/addon_data/plugin.video.vstream/video_cache.db"
#self.ClearDir2(cached_Cache, True)
try:
    xbmcvfs.delete(cached_Cache)
except:
    xbmc.log("\t[PLUGIN] xAmAx-Mod: Erreur de nettoyage de la cache de vstream", xbmc.LOGNOTICE)

path = "special://temp/archive_cache/"
try:
    xbmcvfs.rmdir(path, True)
except:
    pass

"""path = "special://temp/"
try:
    xbmcvfs.rmdir(path, True)
except:
    pass"""

xbmc.log("\t[PLUGIN] xAmAx-Mod: Démarrer", xbmc.LOGNOTICE)

"""while(1):
    if xbmc.Player().isPlaying():
        if xbmc.Player().isPlayingVideo():
            VIDEO = 1
            try:
                InfoLecture = xbmc.Player().getPlayingFile()
                if MemoInfo != InfoLecture:
                    xbmc.log('\t[PLUGIN] xAmAx-Mod Fichier: '+str(InfoLecture), xbmc.LOGNOTICE)
                    MemoInfo = InfoLecture
                try: LectureTitre = xbmc.Player().getVideoInfoTag().getTitle()
                except: LectureTitre = None 
                if MemoTitle != LectureTitre:
                    xbmc.log('\t[PLUGIN] xAmAx-Mod Titre: '+LectureTitre, xbmc.LOGNOTICE)
                    ConvNom(LectureTitre)
                    MemoTitle = LectureTitre
                try: LectureTitreOrigi = xbmc.Player().getVideoInfoTag().getOriginalTitle()
                except: LectureTitreOrigi = None
                if MemoOriginTitle != LectureTitreOrigi:
                    xbmc.log('\t[PLUGIN] xAmAx-Mod TitreOriginal: '+LectureTitreOrigi, xbmc.LOGNOTICE)
                    MemoOriginTitle = LectureTitreOrigi
            except:
                pass
        #print "++++++++Lecture d'une vidéo!"
    else:
        VIDEO = 0
    xbmc.sleep(3000)
"""

