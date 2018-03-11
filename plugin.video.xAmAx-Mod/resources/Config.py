# -*- coding: UTF-8 -*-
import xbmc, xbmcgui, xbmcaddon, os, sys, xbmcvfs, glob
import xml.etree.ElementTree as ET

ADDON_ID       = "plugin.video.xAmAx-Mod"
ADDONTITLE     = "xAmAx Mod"
ADDON          = xbmcaddon.Addon(ADDON_ID)
DIALOG         = xbmcgui.Dialog()
HOME           = xbmc.translatePath('special://home/')
ADDONS         = os.path.join(HOME, 'addons')
USERDATA       = os.path.join(HOME, 'userdata')
ADDONPATH      = ADDON.getAddonInfo('path')
FANART         = os.path.join(ADDONPATH, 'FondFenetre.png')
SKINFOLD       = os.path.join(ADDONPATH,   'resources', 'skins', 'DefaultSkin', 'media')
ADVANCED       = os.path.join(USERDATA,  'advancedsettings.xml')
KODIV          = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
COLOR1         = 'firebrick'
COLOR2         = 'ghostwhite'

ACTION_PREVIOUS_MENU    =  10 ## ESCHAP
ACTION_NAV_BACK         =  92 ## Touche Retour
ACTION_SELECT_ITEM      =   7 ## ENTRER SUR PAD NUMERIQUE
ACTION_MOUSE_LEFT_CLICK = 100 ## CLICK GAUCHE

def artwork(file):
    if   file == 'button': return os.path.join(SKINFOLD, 'Button', 'button-focus_lightxAm.png'), os.path.join(SKINFOLD, 'Button', 'button-focus_grey.png')
    elif file == 'radio' : return os.path.join(SKINFOLD, 'RadioButton', 'MenuItemFOxAm.png'), os.path.join(SKINFOLD, 'RadioButton', 'MenuItemNF.png'), os.path.join(SKINFOLD, 'RadioButton', 'radiobutton-focus.png'), os.path.join(SKINFOLD, 'RadioButton', 'radiobutton-nofocus.png')
    elif file == 'slider': return os.path.join(SKINFOLD, 'Slider', 'osd_slider_nibxAm.png'), os.path.join(SKINFOLD, 'Slider', 'osd_slider_nibNFxAm.png')

def autoConfig(msg='', TxtColor='0xFFFFFFFF', Font='font12', BorderWidth=10):
    class MyWindow(xbmcgui.WindowDialog):
        scr={};
        def __init__(self,msg='',L=0,T=0,W=1280,H=720,TxtColor='0xFFFFFFFF',Font='font12',BorderWidth=10):
            buttonfocus, buttonnofocus = artwork('button')
            radiobgfocus, radiobgnofocus, radiofocus, radionofocus = artwork('radio')
            slidernibfocus, slidernibnofocus = artwork('slider')
            image_path = FANART
            boxbg = os.path.join(SKINFOLD, 'Background', 'Fenetre.png')
            self.border = xbmcgui.ControlImage(L,T,W,H, image_path)
            self.addControl(self.border); 
            self.BG=xbmcgui.ControlImage(L+BorderWidth,T+BorderWidth,W-(BorderWidth*2),H-(BorderWidth*2), FANART, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
            self.addControl(self.BG)
            top = T #+BorderWidth
            leftside = L #+BorderWidth
            rightside = L+(W/2) #-(BorderWidth*2)
            firstrow = top+30
            secondrow = firstrow+300+(BorderWidth/2)
            currentwidth = ((W/2)-(BorderWidth*4))/2

            header = '[COLOR %s][B]Configuration des paramètres Avancés de Kodi[/B][/COLOR]' % (COLOR2)
            self.Header=xbmcgui.ControlLabel(L, top, W, 30, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header)
            top += 30+BorderWidth
            self.bgarea = xbmcgui.ControlImage(leftside, firstrow, rightside-L, 300, boxbg, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
            self.addControl(self.bgarea)
            self.bgarea2 = xbmcgui.ControlImage(rightside, firstrow, rightside-L, 300, boxbg, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
            self.addControl(self.bgarea2)
            self.bgarea3 = xbmcgui.ControlImage(leftside, secondrow, rightside-L, 300, boxbg, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
            self.addControl(self.bgarea3)
            self.bgarea4 = xbmcgui.ControlImage(rightside, secondrow, rightside-L, 300, boxbg, aspectRatio=0, colorDiffuse='0xFFFFFFFF')
            self.addControl(self.bgarea4)

            header = '[COLOR %s]Taille de la mémoire video[/COLOR]' % (COLOR2)
            self.Header2=xbmcgui.ControlLabel(leftside+BorderWidth, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header2)
            freeMemory = int(float(xbmc.getInfoLabel('System.Memory(free)')[:-2])*.33)
            recMemory = int(float(xbmc.getInfoLabel('System.Memory(free)')[:-2])*.23)
            msg3 = "[COLOR %s]Taille de la mémoire tampon de kodi. Si on le met à [COLOR %s]0[/COLOR] la mémoire tampon est mise sur le disque dur et pas sur la RAM.  Note: Pour la taille de mémoire définie ici, Kodi nécessitera 3 fois la quantité de RAM libre. Si ce paramètre est trop élevé, Kodi risque de se bloquer s'il ne dispose pas de suffisamment de RAM (mémoire libre: [COLOR %s]%s[/COLOR])[/COLOR]" % (COLOR2, COLOR1, COLOR1, freeMemory)
            self.Support3=xbmcgui.ControlTextBox(leftside+int(BorderWidth*2), firstrow+30+BorderWidth, (W/2)-(BorderWidth*4), 220, font='font12', textColor=TxtColor)
            self.addControl(self.Support3)
            self.Support3.setText(msg3)
            try: self.videoCacheSize=xbmcgui.ControlSlider(leftside+int(BorderWidth*2.5), firstrow+240,(W/2)-(BorderWidth*5),20, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL) 
            except: self.videoCacheSize=xbmcgui.ControlSlider(leftside+int(BorderWidth*2.5), firstrow+240,(W/2)-(BorderWidth*5),20, texture=slidernibnofocus, texturefocus=slidernibfocus) 
            self.addControl(self.videoCacheSize)
            self.videomin = 0; self.videomax = freeMemory if freeMemory < 2000 else 2000
            self.recommendedVideo = recMemory if recMemory < 500 else 500; self.currentVideo = self.recommendedVideo
            videopos = 100 * float(self.currentVideo)/float(self.videomax)
            self.videoCacheSize.setPercent(videopos)
            current1 = '[COLOR %s]Votre Choix:[/COLOR] [COLOR %s]%s MB[/COLOR]' % (COLOR1, COLOR2, self.currentVideo)
            recommended1 = '[COLOR %s]Recommandé:[/COLOR] [COLOR %s]%s MB[/COLOR]' % (COLOR1, COLOR2, self.recommendedVideo)
            self.currentVideo1= xbmcgui.ControlTextBox(leftside+BorderWidth+20,firstrow+260,currentwidth,20,font=Font,textColor=TxtColor)
            self.addControl(self.currentVideo1)
            self.currentVideo1.setText(current1)
            self.recommendedVideo1=xbmcgui.ControlTextBox(leftside+BorderWidth+currentwidth,firstrow+260,currentwidth,20,font=Font,textColor=TxtColor)
            self.addControl(self.recommendedVideo1)
            self.recommendedVideo1.setText(recommended1)

            header = '[COLOR %s]Temps avant la déconnexion au site[/COLOR]' % (COLOR2)
            self.Header3=xbmcgui.ControlLabel(rightside, firstrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header3)
            msg3 = "[COLOR %s][B]curlclienttimeout[/B] est le temps en seconde pour arrêter la connexion au site internet sur dépassement du temps. \n[B]curllowspeedtime[/B] est le temps en seconde pour que le site soit considéré comme trop lent.\n\nPour les connexion lentes mettre 20s.[/COLOR]" % COLOR2
            self.Support3=xbmcgui.ControlTextBox(rightside+int(BorderWidth*2.5), firstrow+50+BorderWidth, (W/2)-(BorderWidth*4), 220, font='font12', textColor=TxtColor)
            self.addControl(self.Support3)
            self.Support3.setText(msg3)
            try: self.CURLTimeout=xbmcgui.ControlSlider(rightside+int(BorderWidth*2.5),firstrow+240,(W/2)-(BorderWidth*5),20, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL) 
            except: self.CURLTimeout=xbmcgui.ControlSlider(rightside+int(BorderWidth*2.5),firstrow+240,(W/2)-(BorderWidth*5),20, texture=slidernibnofocus, texturefocus=slidernibfocus)
            self.addControl(self.CURLTimeout)
            self.curlmin = 0; self.curlmax = 20
            self.recommendedCurl = 10; self.currentCurl = self.recommendedCurl
            curlpos = 100 * float(self.currentCurl)/float(self.curlmax)
            self.CURLTimeout.setPercent(curlpos)
            current2 = '[COLOR %s]Votre Choix:[/COLOR] [COLOR %s]%ss[/COLOR]' % (COLOR1, COLOR2, self.currentCurl)
            recommended2 = '[COLOR %s]Recommandé:[/COLOR] [COLOR %s]%ss[/COLOR]' % (COLOR1, COLOR2, self.recommendedCurl)
            self.currentCurl2=xbmcgui.ControlTextBox(rightside+(BorderWidth*3),firstrow+260,currentwidth,20,font=Font,textColor=TxtColor)
            self.addControl(self.currentCurl2)
            self.currentCurl2.setText(current2)
            self.recommendedCurl2=xbmcgui.ControlTextBox(rightside+(BorderWidth*3)+currentwidth,firstrow+260,currentwidth,20,font=Font,textColor=TxtColor)
            self.addControl(self.recommendedCurl2)
            self.recommendedCurl2.setText(recommended2)
            
            header = '[COLOR %s]Facteur de lecture de la mémoire tampon[/COLOR]' % (COLOR2)
            self.Header4=xbmcgui.ControlLabel(leftside, secondrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header4)
            msg3 = "[COLOR %s]Par défaut 4, Kodi remplira la mémoire tampon un peu au-dessus de ce qui est nécessaire pour la lecture. En augmentant cette valeur kodi prendra de l'avance sur le téléchargement et remplira la mémoire tampon! Donc en augmentant cette valeur la connexion internet sera monopoliser par kodi avec une augmentation de l'utilisation du processeur...[/COLOR]" % COLOR2
            self.Support3=xbmcgui.ControlTextBox(leftside+int(BorderWidth*2), secondrow+30+BorderWidth, (W/2)-(BorderWidth*4), 240, font='font12', textColor=TxtColor)
            self.addControl(self.Support3)
            self.Support3.setText(msg3)
            try: self.readBufferFactor=xbmcgui.ControlSlider(leftside+int(BorderWidth*2.5), secondrow+240,(W/2)-(BorderWidth*5),20, texture=slidernibnofocus, texturefocus=slidernibfocus, orientation=xbmcgui.HORIZONTAL) 
            except: self.readBufferFactor=xbmcgui.ControlSlider(leftside+int(BorderWidth*2.5), secondrow+240,(W/2)-(BorderWidth*5),20, texture=slidernibnofocus, texturefocus=slidernibfocus)
            self.addControl(self.readBufferFactor)
            self.readmin = 0; self.readmax = 30
            self.recommendedRead = 5; self.currentRead = self.recommendedRead
            readpos = 100 * float(self.currentRead)/float(self.readmax)
            self.readBufferFactor.setPercent(readpos)
            current3 = '[COLOR %s]Votre Choix:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, self.currentRead)
            recommended3 = '[COLOR %s]Recommandé:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, self.recommendedRead)
            self.currentRead3=xbmcgui.ControlTextBox(leftside+BorderWidth+30,secondrow+260,currentwidth,20,font=Font,textColor=TxtColor)
            self.addControl(self.currentRead3)
            self.currentRead3.setText(current3)
            self.recommendedRead3=xbmcgui.ControlTextBox(leftside+BorderWidth+currentwidth,secondrow+260,currentwidth,20,font=Font,textColor=TxtColor)
            self.addControl(self.recommendedRead3)
            self.recommendedRead3.setText(recommended3)

            header = '[COLOR %s]Mode mémoire tampon[/COLOR]' % (COLOR2)
            self.Header4=xbmcgui.ControlLabel(rightside, secondrow+5, (W/2)-(BorderWidth*2), 20, header, font='font13', textColor=TxtColor, alignment=0x00000002)
            self.addControl(self.Header4)
            msg4 = "[COLOR %s]Ce paramètre permet de choisir quels types de fichiers seront mis en mémoire tampon. La valeur  par défaut et 0, Cela permet de mettre et mémoire tampon tous les fichiers distants.[/COLOR]" % COLOR2
            self.Support4=xbmcgui.ControlTextBox(rightside+int(BorderWidth*2), secondrow+30+BorderWidth, (W/2)-(BorderWidth*4), 110, font='font12', textColor=TxtColor)
            self.addControl(self.Support4)
            self.Support4.setText(msg4)
            B1 = secondrow+140+BorderWidth; B2 = B1+35; B3 = B2+35; B4 = B3+35;
            self.Button0 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3)-22, B1, (W/2)-(BorderWidth*4)+20, 30, "0: Mémoriser les fichier d'internet et réseau local", font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
            self.Button1 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3)-22, B2, (W/2)-(BorderWidth*4)+20, 30, '1: Mémoriser tous les fichier', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus) 
            self.Button2 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3)-22, B3, (W/2)-(BorderWidth*4)+20, 30, "2: Mémoriser que les fichiers en streaming", font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus) 
            self.Button3 = xbmcgui.ControlRadioButton(rightside+(BorderWidth*3)-22, B4, (W/2)-(BorderWidth*4)+20, 30, '3: Pas de mémoire tampon', font='font12', focusTexture=radiobgfocus, noFocusTexture=radiobgnofocus, focusOnTexture=radiofocus, noFocusOnTexture=radiofocus, focusOffTexture=radionofocus, noFocusOffTexture=radionofocus)
            self.addControl(self.Button0)
            self.addControl(self.Button1)
            self.addControl(self.Button2)
            self.addControl(self.Button3)
            self.Button0.setSelected(False)
            self.Button1.setSelected(False)
            self.Button2.setSelected(True)
            self.Button3.setSelected(False)

            self.buttonWrite=xbmcgui.ControlButton(leftside,T+H-BorderWidth,(W/2)-(BorderWidth*2),35,"Ecrire le fichier de configuration",textColor="0xFFFFFFFF",focusedColor="0xFFFFFFFF",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
            self.buttonCancel=xbmcgui.ControlButton(rightside+BorderWidth*2,T+H-BorderWidth,(W/2)-(BorderWidth*2),35,"Annuler",textColor="0xFFFFFFFF",focusedColor="0xFFFFFFFF",alignment=2,focusTexture=buttonfocus,noFocusTexture=buttonnofocus)
            self.addControl(self.buttonWrite); self.addControl(self.buttonCancel)

            self.buttonWrite.controlLeft(self.buttonCancel); self.buttonWrite.controlRight(self.buttonCancel); self.buttonWrite.controlUp(self.Button3); self.buttonWrite.controlDown(self.videoCacheSize)
            self.buttonCancel.controlLeft(self.buttonWrite); self.buttonCancel.controlRight(self.buttonWrite); self.buttonCancel.controlUp(self.Button3); self.buttonCancel.controlDown(self.videoCacheSize)
            self.currentVideo1.controlUp(self.buttonWrite); self.currentVideo1.controlDown(self.CURLTimeout)
            self.videoCacheSize.controlUp(self.buttonWrite); self.videoCacheSize.controlDown(self.CURLTimeout)
            self.CURLTimeout.controlUp(self.videoCacheSize); self.CURLTimeout.controlDown(self.readBufferFactor)
            self.readBufferFactor.controlUp(self.CURLTimeout); self.readBufferFactor.controlDown(self.Button0)
            self.Button0.controlUp(self.CURLTimeout); self.Button0.controlDown(self.Button1); self.Button0.controlLeft(self.readBufferFactor); self.Button0.controlRight(self.readBufferFactor);
            self.Button1.controlUp(self.Button0); self.Button1.controlDown(self.Button2); self.Button1.controlLeft(self.readBufferFactor); self.Button1.controlRight(self.readBufferFactor);
            self.Button2.controlUp(self.Button1); self.Button2.controlDown(self.Button3); self.Button2.controlLeft(self.readBufferFactor); self.Button2.controlRight(self.readBufferFactor);
            self.Button3.controlUp(self.Button2); self.Button3.controlDown(self.buttonWrite); self.Button3.controlLeft(self.readBufferFactor); self.Button3.controlRight(self.readBufferFactor);
            self.setFocus(self.videoCacheSize)
                
        def doExit(self):
            self.CloseWindow()
                
        def updateCurrent(self, control):
            if control == self.videoCacheSize:
                self.currentVideo = (self.videomax)*self.videoCacheSize.getPercent()/100
                current = '[COLOR %s]Votre Choix:[/COLOR] [COLOR %s]%s MB[/COLOR]' % (COLOR1, COLOR2, int(self.currentVideo))
                self.currentVideo1.setText(current)
            elif control == self.CURLTimeout:
                self.currentCurl = (self.curlmax)*self.CURLTimeout.getPercent()/100
                current = '[COLOR %s]Votre Choix:[/COLOR] [COLOR %s]%ss[/COLOR]' % (COLOR1, COLOR2, int(self.currentCurl))
                self.currentCurl2.setText(current)
            elif control == self.readBufferFactor:
                self.currentRead = (self.readmax)*self.readBufferFactor.getPercent()/100
                current = '[COLOR %s]Votre Choix:[/COLOR] [COLOR %s]%s[/COLOR]' % (COLOR1, COLOR2, int(self.currentRead))
                self.currentRead3.setText(current)
            elif control in [self.Button0, self.Button1, self.Button2, self.Button3]:
                self.Button0.setSelected(False)
                self.Button1.setSelected(False)
                self.Button2.setSelected(False)
                self.Button3.setSelected(False)
                control.setSelected(True)

        def doWrite(self):
            if   self.Button0.isSelected(): buffermode = 0
            elif self.Button1.isSelected(): buffermode = 1
            elif self.Button2.isSelected(): buffermode = 2
            elif self.Button3.isSelected(): buffermode = 3
            TabLigneAEcrire = []
            TabLigneAEcrire.append(("advancedsettings","<advancedsettings>\n",0,""))
            if KODIV < 17:
                TabLigneAEcrire.append(("network",'   <network>\n',1,""))
                TabLigneAEcrire.append(("buffermode",'      <buffermode>%s</buffermode>\n',2,buffermode))
                TabLigneAEcrire.append(("cachemembuffersize",'      <cachemembuffersize>%s</cachemembuffersize>\n',2,int(self.currentVideo*1024*1024)))
                TabLigneAEcrire.append(("readbufferfactor",'      <readbufferfactor>%s</readbufferfactor>\n',2,int(self.currentRead)))
                TabLigneAEcrire.append(("curlclienttimeout",'      <curlclienttimeout>%s</curlclienttimeout>\n',2,int(self.currentCurl)))
                TabLigneAEcrire.append(("curllowspeedtime",'      <curllowspeedtime>%s</curllowspeedtime>\n',2,int(self.currentCurl)))
            else:
                TabLigneAEcrire.append(("cache",'   <cache>\n',1,""))
                TabLigneAEcrire.append(("buffermode",'      <buffermode>%s</buffermode>\n',2,buffermode))
                TabLigneAEcrire.append(("memorysize",'      <memorysize>%s</memorysize>\n',2,int(self.currentVideo*1024*1024)))
                TabLigneAEcrire.append(("readfactor",'      <readfactor>%s</readfactor>\n',2,int(self.currentRead)))
                TabLigneAEcrire.append(("/cache",'   </cache>\n',1,""))
                TabLigneAEcrire.append(("network",'   <network>\n',1,""))
                TabLigneAEcrire.append(("curlclienttimeout",'      <curlclienttimeout>%s</curlclienttimeout>\n',2,int(self.currentCurl)))
                TabLigneAEcrire.append(("curllowspeedtime",'      <curllowspeedtime>%s</curllowspeedtime>\n',2,int(self.currentCurl)))
            TabLigneAEcrire.append(("/network",'   </network>\n',1,""))
            TabLigneAEcrire.append(("/advancedsettings",'</advancedsettings>\n',0,""))
                                   
            #if os.path.exists(ADVANCED):
            #        choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]There is currently an active [COLOR %s]AdvancedSettings.xml[/COLOR], would you like to remove it and continue?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR green]Remove Settings[/COLOR][/B]", nolabel="[B][COLOR red]Cancel Write[/COLOR][/B]")
            #        if choice == 0: return
            #        try: os.remove(ADVANCED)
            #        except: f = open(ADVANCED, 'w'); f.close()
            #try:
            print TabLigneAEcrire
            if xbmcvfs.exists(ADVANCED):
                tree = ET.parse(ADVANCED)
                root = tree.getroot()
                
                if root.tag == 'advancedsettings':
                    for (Clef,AEcrire,Niveau,valeur) in TabLigneAEcrire:
                        if not Clef.startswith("/"):
                            print "Recherche de : "+Clef
                            if Niveau == 1:
                                TabTrouver=-1
                                ClefaCreer=Clef
                                for x in range(0,len(root)):
                                    if Clef == root[x].tag:
                                        print "Tag trouvé: "+Clef
                                        TabTrouver=x
                                        break
                                if TabTrouver==-1:
                                    a = ET.Element('advancedsettings')
                                    b = ET.SubElement(a,ClefaCreer)
                                    root.append(b)
                            if Niveau == 2:
                                if TabTrouver!=-1:
                                    TextModifier=False
                                    for y in range(0,len(root[TabTrouver])):
                                        
                                        if Clef == root[TabTrouver][y].tag:
                                            print "Tag trouvé: "+root[TabTrouver][y].text
                                            root[TabTrouver][y].text = str(valeur)
                                            print "Modifier: "+root[TabTrouver][y].text
                                            TextModifier=True
                                            break
                                    if not TextModifier:
                                        a = ET.Element(root[TabTrouver].tag)
                                        b = ET.SubElement(a, Clef)
                                        b.text=str(valeur)
                                        root[TabTrouver].append(b)
                                else:
                                    a = ET.Element(root[len(root)-1].tag)
                                    b = ET.SubElement(a, Clef)
                                    b.text=str(valeur)
                                    root[len(root)-1].append(b)
                                tree.write(ADVANCED)
                                        
            else:
                with open(ADVANCED,'w') as f:
                    for (Clef,AEcrire,Niveau,valeur) in TabLigneAEcrire:
                        print "xAmAx   Clef="+Clef+" AEcrire="+AEcrire+" Niveau="+str(Niveau)+" Valeur="+str(valeur)
                        if valeur!="":
                            AEcrire = AEcrire % valeur
                        f.write(AEcrire)
                f.close()
            choice = DIALOG.ok("Modification du fichier de configuration!", "[COLOR %s]Le fichier de configuration avancé de Kodi : [COLOR %s]AdvancedSettings.xml[/COLOR] vient d'être modifier\nPour que Kodi les prennent en compte il faut le redémarrer...\nBon visionnage à vous tous!!![/COLOR]" % (COLOR2, COLOR1))
            if choice == 0: return
            self.CloseWindow()

        def onControl(self, control):
            if   control==self.buttonWrite: self.doWrite()
            elif control==self.buttonCancel:  self.doExit()

        def onAction(self, action):
            try: F=self.getFocus()
            except: F=False
            if   F      == self.videoCacheSize:   self.updateCurrent(self.videoCacheSize)
            elif F      == self.CURLTimeout:      self.updateCurrent(self.CURLTimeout)
            elif F      == self.readBufferFactor: self.updateCurrent(self.readBufferFactor)
            elif F      in [self.Button0, self.Button1, self.Button2, self.Button3] and action in [ACTION_MOUSE_LEFT_CLICK, ACTION_SELECT_ITEM]: self.updateCurrent(F)
            elif action == ACTION_PREVIOUS_MENU:  self.doExit()
            elif action == ACTION_NAV_BACK:       self.doExit()
                
        def CloseWindow(self): self.close()

    maxW=1280; maxH=720; W=int(900); H=int(650); L=int((maxW-W)/2); T=int((maxH-H)/2); 
    TempWindow=MyWindow(L=L,T=T,W=W,H=H,TxtColor=TxtColor,Font=Font,BorderWidth=BorderWidth); 
    TempWindow.doModal() 
    del TempWindow
