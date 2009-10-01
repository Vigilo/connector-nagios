# -*- coding: utf-8 -*-
'''
Created on 30 sept. 2009

@author: smoignar
'''
# Teste la sauvegare d'un message nagios dans la database
from __future__ import absolute_import
import unittest
from subprocess import *
from os import kill, remove
import time
from socket import * 
from vigilo.common.conf import settings
import sqlite3

NS_EVENT = 'http://www.projet-vigilo.org/xmlns/event1'
NS_PERF = 'http://www.projet-vigilo.org/xmlns/perf1'


class TestSauveDB(unittest.TestCase):
    # Message from Socket impossible to forward(XMPP BUS not connected)
    # Vérification que le message est sauvegardé dans la database 
    def test_startconnector(self):
        # Demarrage en tâche de fond du connector nagios
        p = Popen(["python2.5", "/home/smoignar/workspace/connector-nagios/src/vigilo/connector_nagios/main.py"], 
            bufsize=1,stdin=PIPE, stdout=PIPE)
        time.sleep(1)
        pid = p.pid
        
        # connection à la database puis récupération du nombre d'enregistrement
        base = settings.get('VIGILO_MESSAGE_BACKUP_FILE',[])
        conn = sqlite3.connect(base)
        cur = conn.cursor()
        # récupération du nomnbre de message dans la table avant send
        requete = 'select count(*) from ' + settings.get('VIGILO_MESSAGE_BACKUP_TABLE_TOBUS',[])
        cur.execute(requete)
        raw_av = cur.fetchone()[0]

        # Création de la socket
        tsocket = socket(AF_UNIX, SOCK_STREAM)
        adr_socket = settings.get('VIGILO_SOCKETR', [])
        tsocket.connect(adr_socket) 
        dico = {'ns': NS_PERF}    
        b = tsocket.send("""<perf xmlns='%(ns)s'><timestamp>1165939739</timestamp><host>serveur1.example.com</host><datasource>Load</datasource><value>10</value></perf>\n""" % dico)
        time.sleep(1)      
    
        # récupération du nomnbre de message dans la table aprés send
        cur.execute(requete)
        raw_ap = cur.fetchone()[0]
             
        tsocket.close()
        cur.close()
        conn.close()
        kill(pid, 0)    # suppression du process connector nagios
        # suppression du fichier socket
        remove (adr_socket)
        
        # vérification que le message a été sauvegardé
        self.assertEqual(raw_av +1 ,raw_ap)      

    
if __name__ == "__main__": 
    unittest.main()
