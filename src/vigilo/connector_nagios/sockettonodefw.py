# vim: set fileencoding=utf-8 sw=4 ts=4 et :

"""
Extends pubsub clients to compute Socket message
"""

from __future__ import absolute_import

from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver
from wokkel.pubsub import PubSubClient, Item
from wokkel.generic import parseXml

from vigilo.connector import converttoxml 
from vigilo.connector.store import unstoremessage, storemessage, \
                initializeDB, sqlitevacuumDB
from vigilo.common.gettext import translate
_ = translate(__name__)
from vigilo.common.logging import get_logger
LOGGER = get_logger(__name__)

import os


class Forwarder(LineReceiver):
    """ Protocol used for each line received from the socket """
    
    delimiter = '\n'

    def lineReceived(self, line):
        """ redefinition of the lineReceived function"""
        if len(line) == 0:
            # empty line -> can't parse it
            return


        # already XML or not ?
        if line[0] != '<':
             Xml = converttoxml.text2xml(line)
        else:
            Xml = parseXml(line)

        if Xml is None:
            # Couldn't parse this line
            return
        self.factory.publishXml(Xml)


class SocketToNodeForwarder(PubSubClient):
    """
    Receives messages on the socket and passes them to the xmpp bus,
    Forward socket to Node.
    """

    def __init__(self, socket_filename, dbfilename, table, nodetopublish, service):
        self.__dbfilename = dbfilename
        self.__table = table

        initializeDB(self.__dbfilename, [self.__table])
        self.__backuptoempty = os.path.exists(self.__dbfilename)
        self.__factory = protocol.ServerFactory()

        self.__connector = reactor.listenUNIX(socket_filename, self.__factory)
        self.__factory.protocol = Forwarder
        self.__factory.publishXml = self.publishXml
        self.__service = service
        self.__nodetopublish = nodetopublish


    def connectionInitialized(self):
        """ redefinition of the function for flushing backup message """
        PubSubClient.connectionInitialized(self)
        LOGGER.info(_('ConnectionInitialized'))
        if self.__backuptoempty :
            while True:
                msg = unstoremessage(self.__dbfilename, self.__table)
                if msg == True:
                    break
                elif msg == False:
                    continue
                else:
                    Xml = parseXml(msg)
                    self.publishXml(Xml)
                
            self.__backuptoempty = False
            sqlitevacuumDB(self.__dbfilename)
        
    def publishXml(self, Xml):
        """ function to publish a XML msg to node """
        def eb(e, Xml):
            """errback"""
            LOGGER.error(_("errback publishStrXml %s") % e.__str__())
            msg = Xml.toXml()
            storemessage(self.__dbfilename, msg, self.__table)
            self.__backuptoempty = True
        
        item = Item(payload=Xml)
        node = self.__nodetopublish[Xml.name]
        try :
            result = self.publish(self.__service, node, [item])
            result.addErrback(eb, Xml)
        except AttributeError :
            LOGGER.error(_('Message from Socket impossible to forward' + \
                           ' (XMPP BUS not connected), the message is' + \
                           ' stored for later reemission'))
            msg = Xml.toXml()
            storemessage(self.__dbfilename, msg, self.__table)
            self.__backuptoempty = True
