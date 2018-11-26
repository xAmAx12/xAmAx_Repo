# -*- coding: utf-8 -*-
# Module: default
# Author: xamax
# Created on: 16.12.2017
# License: GPL v.3 https://www.gnu.org/copyleft/gpl.html

from resources.Menu import menu
import sys

if __name__ == '__main__':
    print "Demarrage xAmAx: commande = " + str(sys.argv[2])
    # Envoi des paramètres du menu
    menu().router(sys.argv[2][1:])

