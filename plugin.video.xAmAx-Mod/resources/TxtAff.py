# -*- coding: utf-8 -*-
# Module: TxtAff
# Author: xamax
# Created on: 23.07.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

import xbmcgui
from xbmc import executebuiltin
from time import sleep
import urllib2 as urllib

class TxtAffich():
    def Fenetre(self,Chemin="",line_number=0,Invertion=False,LabTitre="xAmAx-Mod",Texte=''):
        print "Fenetre de lecture de texte"
        executebuiltin("ActivateWindow(10147)") #10147
        window = xbmcgui.Window(10147)
        #window.getControl(1).setLabel(LabTitre)
        
        if Texte=='':
            Texte = self.getcontent(Chemin,line_number,Invertion)
        sleep(0.5)
        window.getControl(5).setText(Texte)
        sleep(0.2)
    def getcontent(self,Chemin="",line_number=0,Invertion=False):
        print "Récupération fichier texte"
        if Chemin!="":
            if ((Chemin[:8]=="https://")or(Chemin[:7]=="http://")):
                print "Ouverture du Fichier des modifications"
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
        print "Affichage du texte"
        return contents.replace(
            ' ERROR: ',' [COLOR red]ERREUR[/COLOR]: ').replace(
            ' WARNING: ',' [COLOR gold]AVERTISSEMENT[/COLOR]: ').replace(
            ' NOTICE: ',' [COLOR green]INFO[/COLOR]: ').replace(
            ' DEBUG: ',' [COLOR orange]DEBUG[/COLOR]: ').replace(
            '- Version ',' [COLOR green]- Version[/COLOR]: ').replace(
            '=======================================================================================',
            '[COLOR green]=======================================================================================[/COLOR]')
