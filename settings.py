# vim: set fileencoding=utf-8 sw=4 ts=4 et :
import logging
LOGGING_PLUGINS = (
#        'vigilo.pubsub.logging',       
        )
LOGGING_SETTINGS = { 'level': logging.DEBUG, }
LOGGING_LEVELS = {}
LOGGING_SYSLOG = True
LOG_TRAFFIC = True


LOGGING_SETTINGS = {
        # 5 is the 'SUBDEBUG' level.
        'level': logging.DEBUG,
        'format': '%(levelname)s::%(name)s::%(message)s',
        }
LOGGING_LEVELS = {
        'multiprocessing': logging.DEBUG,
        'twisted': logging.DEBUG,
        'vigilo.pubsub': logging.DEBUG,
        'vigilo.connector': logging.DEBUG,
    }



#VIGILO_CONNECTOR_DAEMONIZE = True
VIGILO_CONNECTOR_DAEMONIZE = False
VIGILO_CONNECTOR_PIDFILE = '/home/smoignar/var/vigilo/connector-nagios/connector-nagios.pid'
VIGILO_CONNECTOR_XMPP_SERVER_HOST = 'localhost2'
VIGILO_CONNECTOR_XMPP_PUBSUB_SERVICE = 'pubsub.localhost'
# Respect the ejabberd namespacing, for now. It will be too restrictive soon.
VIGILO_CONNECTOR_JID = 'user-nagios@localhost'
VIGILO_CONNECTOR_PASS = 'user-nagios'

# listen on this node (écoute de ce noeud)
# pas initialisé le connector nagios n'as pas à recevoir des messages du BUS
# create this node (créer ce noeud)
VIGILO_CONNECTOR_TOPIC_OWNER = ['/home/localhost/user-nagios/BUS']

# publish on those node (publier sur ces noeuds)
VIGILO_CONNECTOR_TOPIC_PUBLISHER = { 
        'perf': '/home/localhost/user-nagios/BUS',
        'event': '/home/localhost/user-nagios/BUS',
        }


VIGILO_SOCKETR = '/var/lib/vigilo/connector-nagios/send.sock'
VIGILO_MESSAGE_BACKUP_FILE = '/var/lib/vigilo/connector-nagios/backup'
VIGILO_MESSAGE_BACKUP_TABLE_TOBUS = 'connector_tobus'

