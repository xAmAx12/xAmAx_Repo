# -*- coding: utf-8 -*-
# Module: DB
# Author: xamax
# Created on: 14.07.2017

import sqlite3 as lite

class db():

    def __init__(self,Chemin):
        print "connexion a "+Chemin
        self.dbx = lite.connect(Chemin)
        self.dbx.text_factory = str

    def __del__(self):
        try:
            self.dbx.close()
        except:
            pass

    def Select(self, Table="", Colonnes="*", Where="", Order=""):
        curs = self.dbx.cursor()
        if Where!="":
            Where = " WHERE "+Where
        if Order!="":
            Order = " ORDER BY "+Order
        #print "-----SELECT "+Colonnes+" FROM "+Table+Where+Order+" ;"
        curs.execute("SELECT "+Colonnes+" FROM "+Table+Where+Order+" ;")
        ret = curs.fetchall()
        #print str(ret)
        try:
            curs.close()
        except:
            pass
        return ret

    def Update(self, Table="installed", Colonnes="enabled", Valeur="1", Where=""):
        curs = self.dbx.cursor()
        #print "-----SELECT "+Colonnes+" FROM "+Table+Where+Order+" ;"
        curs.execute("UPDATE `"+Table+"` SET `"+Colonnes+"`="+Valeur+" WHERE "+Where+" ;")
        self.dbx.commit()
        #print str(ret)
        try:
            curs.close()
        except:
            pass
        

    def Delete(self,Table):
        try:
            curs = self.dbx.cursor()
            curs.execute("DROP TABLE "+Table+" ;")
            self.dbx.commit()
            curs.close()
        except:
            pass

    def Insert(self,Table,Colonnes,Valeurs=()):
        curs = self.dbx.cursor()
        #print "----INSERT INTO "+Table+" ("+Colonnes+") VALUES "+str(Valeurs)+" ;"
        try:
            curs.execute("INSERT INTO "+Table+" ("+Colonnes+") VALUES "+str(Valeurs)+" ;")
            curs.close()
        except:
            pass

    def CreerTable(self,Table="", colonnes=""):
        curs = self.dbx.cursor()
        curs.execute("create table if not exists "+Table+" ("+colonnes+")")
        try:
            curs.close()
        except:
            pass

    def TableExist(self,Table):
        try:
            ret = self.Select(Table="sqlite_master",
                              Colonnes="name",
                              Where="type='table' AND name='"+Table+"'",
                              Order="")
            #print "TableExist "+Table+": "+str(ret)
            if len(ret)==1:
                return True
            else:
                return False
        except:
            return False
         
    def ExecutFichSQL(self,dirSQL):
        #print "sql execution de "+dirSQL
        curs = self.dbx.cursor()
        f = open(dirSQL, "r")
        sql = f.read()
        f.close()
        #print sql
        curs.executescript(sql)
        print "script sql executer"
        #self.dbx.commit()

    def text_factory(self,Type):
        self.dbx.text_factory = Type

    def FinEnregistrement(self):
        self.dbx.commit()

