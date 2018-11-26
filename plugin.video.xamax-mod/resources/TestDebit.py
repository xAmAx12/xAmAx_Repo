# -*- coding: UTF-8 -*-
# Module: TestDebit
# Author: xamax
# Created on: 08.04.2018

import os
import re
import sys
import math
import socket
import time
import timeit
import threading
from xbmcgui import DialogProgress, Dialog

try:
    import xml.etree.cElementTree as ET
    from xml.dom import minidom as DOM
except ImportError:
    try:
        import xml.etree.ElementTree as ET
    except ImportError:
        from xml.dom import minidom as DOM
        ET = None
        
try:
    from urllib2 import urlopen, Request, HTTPError, URLError
except ImportError:
    from urllib.request import urlopen, Request, HTTPError, URLError
    
try:
    from httplib import HTTPConnection, HTTPSConnection
except ImportError:
    from http.client import HTTPConnection, HTTPSConnection

try:
    from Queue import Queue
except ImportError:
    from queue import Queue

try:
    from urlparse import urlparse
except ImportError:
    from urllib.parse import urlparse

__version__ = '0.3.2'
UserAgent = 'speedtest-cli/%s' % __version__
Source = None
EvtSource = None

def RecherchePosition(origin, destination):
    OrigLatDegr, OrigLonDegr = origin
    DestLatDegr, DestLonDegr = destination
    LatRad = math.radians(DestLatDegr - OrigLatDegr)
    LongRad = math.radians(DestLonDegr - OrigLonDegr)
    ConvertAngle = (math.sin(LatRad / 2) * math.sin(LatRad / 2) +
                     math.cos(math.radians(OrigLatDegr)) *
                     math.cos(math.radians(DestLatDegr)) * math.sin(LongRad / 2) *
                     math.sin(LongRad / 2))
    Angle = 2 * math.atan2(math.sqrt(ConvertAngle), math.sqrt(1 - ConvertAngle))
    Position = 6371 * Angle
    return Position

def TelechargPage(url, data=None, headers={}):
    headers['User-Agent'] = UserAgent
    return Request(url, data=data, headers=headers)

def OuvrePage(request):
    try:
        Rep = urlopen(request)
        return Rep
    except (HTTPError, URLError, socket.error):
        return False

def DomXml(dom, tagName):
    Result = dom.getElementsByTagName(tagName)[0]
    return dict(list(Result.attributes.items()))

def DLConfigSpeedtest():
    PageDLL = TelechargPage('https://www.speedtest.net/speedtest-config.php')
    PageLu = OuvrePage(PageDLL)
    if PageLu is False:
        print 'Impossible de retrouver la configuration de speedtest.net'
        sys.exit(1)
    TabConfig = []
    while 1:
        TabConfig.append(PageLu.read(10240))
        if len(TabConfig[- 1]) == 0:
            break
    if int(PageLu.code) != 200:
        return None
    PageLu.close()
    try:
        try:
            XmlTab = ET.fromstring(''.encode().join(TabConfig))
            ConfigSpeedTest = {
                'client': XmlTab.find('client').attrib,
                'times': XmlTab.find('times').attrib,
                'download': XmlTab.find('download').attrib,
                'upload': XmlTab.find('upload').attrib}
        except Exception, Erreur:
            print 'Exception pour ET: ' + str(Erreur)
            XmlTab = DOM.parseString(''.join(TabConfig))
            ConfigSpeedTest = {
                'client': DomXml(XmlTab, 'client'),
                'times': DomXml(XmlTab, 'times'),
                'download': DomXml(XmlTab, 'download'),
                'upload': DomXml(XmlTab, 'upload')}
    except SyntaxError:
        print 'Erreur de partage de la configuration de speedtest.net'
        sys.exit(1)
    del XmlTab
    del TabConfig
    return ConfigSpeedTest

def RechSrvPlusProche(client, all=False):
    AdresseTest = [
        'https://www.speedtest.net/speedtest-servers-static.php',
        'http://c.speedtest.net/speedtest-servers-static.php',
    ]
    RepServ = {}
    for Lien in AdresseTest:
        try:
            Pagedl = TelechargPage(Lien)
            PageLU = OuvrePage(Pagedl)
            if PageLU is False:
                raise ErreurEnr
            TabServer = []
            while 1:
                TabServer.append(PageLU.read(10240))
                if len(TabServer[- 1]) == 0:
                    break
            if int(PageLU.code) != 200:
                PageLU.close()
                raise ErreurEnr
            PageLU.close()
            try:
                try:
                    XmlTab = ET.fromstring(''.encode().join(TabServer))
                    ListServer = XmlTab.getiterator('server')
                except Exception, Erreur:
                    print 'Exception pour ET: ' + str(Erreur)
                    XmlTab = DOM.parseString(''.join(TabServer))
                    ListServer = XmlTab.getElementsByTagName('server')
            except SyntaxError:
                raise ErreurEnr
            for SRV in ListServer:
                try:
                    SRVParam = SRV.attrib
                except AttributeError:
                    SRVParam = dict(list(SRV.attributes.items()))
                Position = RecherchePosition([float(client['lat']),float(client['lon'])],
                                                [float(SRVParam.get('lat')),float(SRVParam.get('lon'))])
                SRVParam['d'] = Position
                if Position not in RepServ:
                    RepServ[Position] = [SRVParam]
                else:
                    RepServ[Position].append(SRVParam)
            del XmlTab
            del TabServer
            del ListServer
        except ErreurEnr:
            continue
        if RepServ:
            break
    if not RepServ:
        print 'Erreur de recherche de la liste de serve de speedtest.net'
        sys.exit(1)
    OrdListServ = []
    for Position in sorted(RepServ.keys()):
        for Isrv in RepServ[Position]:
            OrdListServ.append(Isrv)
            if len(OrdListServ) == 5 and not all:
                break
        else:
            continue
        break
    del RepServ
    return OrdListServ

def RechLatencySrv(servers):
    Tab = {}
    for SRV in servers:
        ListTempsDeReponse = []
        UrlEnCour = '%s/latency.txt' % os.path.dirname(SRV['url'])
        UrlCouper = urlparse(UrlEnCour)
        for i in range(0, 3):
            try:
                if UrlCouper[0] == 'https':
                    ConnectionUrl = HTTPSConnection(UrlCouper[1])
                else:
                    ConnectionUrl = HTTPConnection(UrlCouper[1])
                ConnectionHead = {'User-Agent': UserAgent}
                TempsDeRef = timeit.default_timer()
                ConnectionUrl.request("GET", UrlCouper[2], headers=ConnectionHead)
                RepConnectEnCour = ConnectionUrl.getresponse()
                TempsDeReponse = (timeit.default_timer() - TempsDeRef)
            except (HTTPError, URLError, socket.error):
                ListTempsDeReponse.append(3600)
                continue
            TxtPageLu = RepConnectEnCour.read(9)
            if int(RepConnectEnCour.status) == 200 and TxtPageLu == 'test=test'.encode():
                ListTempsDeReponse.append(TempsDeReponse)
            else:
                ListTempsDeReponse.append(3600)
            ConnectionUrl.close()
        ArondTempsRep = round((sum(ListTempsDeReponse) / 6) * 1000, 3)
        Tab[ArondTempsRep] = SRV
    ListSrvTrier = sorted(Tab.keys())[0]
    ListeRetLatency = Tab[ListSrvTrier]
    ListeRetLatency['latency'] = ListSrvTrier
    return ListeRetLatency

class DlVitesseTaille(threading.Thread):
    def __init__(self, url, start):
        self.url = url
        self.result = None
        self.starttime = start
        threading.Thread.__init__(self)

    def run(self):
        self.result = [0]
        try:
            if (timeit.default_timer() - self.starttime) <= 10:
                PageDl = TelechargPage(self.url)
                PageLu = urlopen(PageDl)
                PageInfo = PageLu.info()
                TempsDebut = time.time()
                TailleFich = int(PageInfo.getheaders("Content-Length")[0])
                MB_Total = float(TailleFich) / (1024 * 1024)
                TailleDlEC = 0
                while 1 and not EvtSource.isSet():
                    TailleEC = len(PageLu.read(10240))
                    self.result.append(TailleEC)
                    if self.result[- 1] == 0:
                        break
                    TailleDlEC += TailleEC
                    MB_EC = TailleDlEC / (1024 * 1024)
                    VitesseBits = TailleDlEC / (time.time() - TempsDebut)
                    VitesseKBits = VitesseBits / 1024
                    AvancemenTxt = '%.02f MB of %.02f MB' % (MB_EC, MB_Total)
                    VitesseTxt = 'Speed: %.02f Kb/s ' % VitesseKBits
                PageLu.close()
        except IOError:
            pass

class UploadVitesseTaille(threading.Thread):
    def __init__(self, url, start, size):
        self.url = url
        Caractere = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        CaractEnv = Caractere * (int(round(int(size) / 36.0)))
        self.data = ('content1=%s' % CaractEnv[0: int(size) - 9]).encode()
        del CaractEnv
        self.result = None
        self.starttime = start
        threading.Thread.__init__(self)

    def run(self):
        try:
            if ((timeit.default_timer() - self.starttime) <= 10 and
                    not EvtSource.isSet()):
                PageDL = TelechargPage(self.url, data=self.data)
                PageLu = urlopen(PageDL)
                PageLu.read(11)
                PageLu.close()
                self.result = len(self.data)
            else:
                self.result = 0
        except IOError:
            self.result = 0

class TestVitesseDeb():

    def __init__(self): #, Dialog
        self.dp = DialogProgress()
        self.dp.create("Test du débit de votre connexion:")
        time.sleep(1)
        #self.dp = Dialog

    def __del__(self):
        self.dp.close()

    def MajProgression(self,Pourcentage,TextMessage):
        print TextMessage
        self.dp.update(Pourcentage,TextMessage)
        time.sleep(1)

    def downloadSpeed(self, files, quiet=False):
        TempsDeRef = timeit.default_timer()

        def FichierEC(q, files):
            for file in files:
                OperationEC = DlVitesseTaille(file, TempsDeRef)
                OperationEC.start()
                q.put(OperationEC, True)
                if not quiet and not EvtSource.isSet():
                    sys.stdout.write('.')
                    sys.stdout.flush()

        TempTotaleFichier = []

        def AffVitesseEC(q, total_files):
            while len(TempTotaleFichier) < total_files:
                OperationEC = q.get(True)
                while OperationEC.isAlive():
                    OperationEC.join(timeout=0.1)
                TempTotaleFichier.append(sum(OperationEC.result))
                #VitesseMbps = ((sum(TempTotaleFichier) / (timeit.default_timer() - TempsDeRef)) / 1000 / 1000) * 8
                #print 'Vitesse en cour: %.02f Mbps' % VitesseMbps
                del OperationEC

        TabFifo = Queue(6)
        ThFichEC = threading.Thread(target=FichierEC, args=(TabFifo, files))
        ThAffVitesse = threading.Thread(target=AffVitesseEC, args=(TabFifo, len(files)))
        TempsDeRef = timeit.default_timer()
        ThFichEC.start()
        ThAffVitesse.start()
        while ThFichEC.isAlive():
            ThFichEC.join(timeout=0.1)
        while ThAffVitesse.isAlive():
            ThAffVitesse.join(timeout=0.1)
        return (sum(TempTotaleFichier) / (timeit.default_timer() - TempsDeRef))

    def uploadSpeed(self, url, sizes, quiet=False):
        TempsDeRef = timeit.default_timer()
        TempTotaleFichier = []

        def FichierEC(q, sizes):
            for TailleEC in sizes:
                OperationEC = UploadVitesseTaille(url, TempsDeRef, TailleEC)
                OperationEC.start()
                q.put(OperationEC, True)
                if not quiet and not EvtSource.isSet():
                    sys.stdout.write('.')
                    sys.stdout.flush()

        def AffVitesseEC(q, total_sizes):
            while len(TempTotaleFichier) < total_sizes:
                OperationEC = q.get(True)
                while OperationEC.isAlive():
                    OperationEC.join(timeout=0.1)
                TempTotaleFichier.append(OperationEC.result)
                #VitesseMbps = ((sum(TempTotaleFichier) / (timeit.default_timer() - TempsDeRef)) / 1000 / 1000) * 8
                #print 'Vitesse en cour: %.02f Mbps' % VitesseMbps
                del OperationEC

        TabFifo = Queue(6)
        ThFichEC = threading.Thread(target=FichierEC, args=(TabFifo, sizes))
        ThAffVitesse = threading.Thread(target=AffVitesseEC, args=(TabFifo, len(sizes)))
        TempsDeRef = timeit.default_timer()
        ThFichEC.start()
        ThAffVitesse.start()
        while ThFichEC.isAlive():
            ThFichEC.join(timeout=0.1)
        while ThAffVitesse.isAlive():
            ThAffVitesse.join(timeout=0.1)
        return (sum(TempTotaleFichier) / (timeit.default_timer() - TempsDeRef))
    
    def Demare(self,timeout=10, units=('bit', 8)):
        try:
            global EvtSource, Source
            TxtFinal = ""
            EvtSource = threading.Event()
            socket.setdefaulttimeout(timeout)
            self.MajProgression(2,'Recherche configuration de speedtest.net...')
            try:
                ConfigSpeedTest = DLConfigSpeedtest()
            except URLError:
                TxtFinal = 'La configuration de speedtest.net est introuvable'
                self.MajProgression(100,TxtFinal)
                return TxtFinal
            
            self.MajProgression(10,'Recherche liste de serveurs de speedtest.net...')
            ListSrvOrd = RechSrvPlusProche(ConfigSpeedTest['client'])
            #self.MajProgression(15,str(ConfigSpeedTest))
            self.MajProgression(20,'Test connection depuis: %(isp)s (%(ip)s)...' % ConfigSpeedTest['client'])
            self.MajProgression(25,'Selection du meilleur server en fonction de la latence...')
            ServerUtiliser = RechLatencySrv(ListSrvOrd)
            try:
                TxtFinal = ('Heberger par %(sponsor)s (%(name)s) [%(d)0.2f km]: '
                          '%(latency)s ms' % ServerUtiliser).encode('utf-8', 'ignore')
                self.MajProgression(30,TxtFinal)
            except NameError:
                TxtFinal = ('Heberger par %(sponsor)s (%(name)s) [%(d)0.2f km]: '
                         '%(latency)s ms' % ServerUtiliser)
                self.MajProgression(30,TxtFinal)

            TabIndex = [350, 500, 750, 1000, 1500, 2000, 2500, 3000, 3500, 4000]
            TabUrlRandom = []
            for Taille in TabIndex:
                for i in range(0, 4):
                    TabUrlRandom.append('%s/random%sx%s.jpg' %
                                        (os.path.dirname(ServerUtiliser['url']), Taille, Taille))
            time.sleep(1)
            self.MajProgression(40, 'Test vitesse téléchargement...')
            VitesseDL = self.downloadSpeed(TabUrlRandom)

            VitesseDLAff = 'Vitesses téléchargement (Débit descendant): %0.2f M%s/s' % ((VitesseDL / 1000 / 1000) * units[1], units[0])
            TxtFinal += "\n"+VitesseDLAff
            self.MajProgression(60, VitesseDLAff)
            TailleUpl = [250000, 500000]
            TabTailleUpl = []
            for TaillEc in TailleUpl:
                for i in range(0, 25):
                    TabTailleUpl.append(TaillEc)
            self.MajProgression(80, "Test vitesse d'envoi...")
            VitesseUpload = self.uploadSpeed(ServerUtiliser['url'], TabTailleUpl)

            VitesseUpAff = "Vitesse d'envoi (Débit montant): %0.2f M%s/s" % ((VitesseUpload / 1000 / 1000) * units[1], units[0])
            TxtFinal += "\n"+VitesseUpAff
            self.MajProgression(100, VitesseUpAff)
            return TxtFinal
        except:
            return "Erreur lors de la recherche de votre débit!\nDésolé pour ce problème!"
