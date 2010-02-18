# vim: set fileencoding=utf-8 sw=4 ts=4 et :
""" Nagios connector Pubsub client. """
from __future__ import absolute_import, with_statement
import os

from twisted.application import app, service
from twisted.internet import reactor
from twisted.words.protocols.jabber.jid import JID
from wokkel import client

from vigilo.common.gettext import translate

_ = translate(__name__)

class ConnectorServiceMaker(object):
    """
    Creates a service that wraps everything the connector needs.
    """

    #implements(service.IServiceMaker, IPlugin)

    def makeService(self):
        """ the service that wraps everything the connector needs. """ 
        from vigilo.common.conf import settings
        settings.load_module(__name__)

        from vigilo.common.logging import get_logger
        LOGGER = get_logger(__name__)

        from vigilo.connector_nagios.xmpptopipefw import XMPPToPipeForwarder
        from vigilo.connector.sockettonodefw import SocketToNodeForwarder
        from vigilo.pubsub.checknode import VerificationNode

        xmpp_client = client.XMPPClient(
                JID(settings['bus']['jid']),
                settings['bus']['password'],
                settings['bus']['host'])
        xmpp_client.setName('xmpp_client')

        try:
            xmpp_client.logTraffic = settings['bus'].as_bool('log_traffic')
        except KeyError:
            xmpp_client.logTraffic = False


        try:
            list_nodeOwner = settings['bus'].as_list('owned_topics')
        except KeyError:
            list_nodeOwner = []

        try:
            list_nodeSubscriber = settings['bus'].as_list('watched_topics')
        except KeyError:
            list_nodeSubscriber = []

        verifyNode = VerificationNode(list_nodeOwner, list_nodeSubscriber, 
                                      doThings=True)
        verifyNode.setHandlerParent(xmpp_client)
        nodetopublish = settings.get('publications', {})
        _service = JID(settings['bus'].get('service', None))

        bkpfile = settings['connector'].get('backup_file', ":memory:")
        pw = settings['connector-nagios'].get('nagios_pipe', None)
        sr = settings['connector-nagios'].get('listen_unix', None)

        for i in bkpfile, pw, sr:
            if i != ':memory:' and i is not None:
                if not os.access(os.path.dirname(i), os.F_OK):
                    msg = _("Directory not found: '%(dir)s'") % \
                            {'dir': os.path.dirname(i)}
                    LOGGER.error(msg)
                    raise OSError(msg)
                if not os.access(os.path.dirname(i), os.R_OK):
                    msg = _("Directory not readable: '%(dir)s'") % \
                            {'dir': os.path.dirname(i)}
                    LOGGER.error(msg)
                    raise OSError(msg)
                if not os.access(os.path.dirname(i), os.W_OK):
                    msg = _("Directory not writable: '%(dir)s'") % \
                            {'dir': os.path.dirname(i)}
                    LOGGER.error(msg)
                    raise OSError(msg)
                if not os.access(os.path.dirname(i), os.X_OK):
                    msg = _("Directory not executable: '%(dir)s'") % \
                            {'dir': os.path.dirname(i)}
                    LOGGER.error(msg)
                    raise OSError(msg)

        if pw is not None:
            message_consumer = XMPPToPipeForwarder(
                    pw,
                    bkpfile,
                    settings['connector']['backup_table_from_bus'])
            message_consumer.setHandlerParent(xmpp_client)


        if sr is not None:
            message_publisher = SocketToNodeForwarder(
                    sr,
                    bkpfile,
                    settings['connector']['backup_table_to_bus'],
                    nodetopublish,
                    _service)
            message_publisher.setHandlerParent(xmpp_client)

        root_service = service.MultiService()
        xmpp_client.setServiceParent(root_service)
        return root_service

def do_main_program():
    """ main function designed to launch the program """
    application = service.Application('Vigilo Connector for Nagios')
    conn_service = ConnectorServiceMaker().makeService()
    conn_service.setServiceParent(application)
    app.startApplication(application, False)
    reactor.run()

def get_tac_path():
    # TODO: ajouter un test unitaire pour ça
    from vigilo import connector_nagios
    print os.path.join( os.path.dirname(connector_nagios.__file__),
                        "twisted_service.py")

def main(*args):
    """ main function designed to launch the program """

    from vigilo.common.daemonize import daemonize
    with daemonize():
        do_main_program()

if __name__ == '__main__':
    main()

