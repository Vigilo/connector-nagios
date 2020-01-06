# -*- coding: utf-8 -*-
# Copyright (C) 2011-2020 CS-SI
# License: GNU GPL v2 <http://www.gnu.org/licenses/gpl-2.0.html>

name = u'connector-nagios'

project = u'Vigilo %s' % name

pdf_documents = [
        ('admin', "admin-%s" % name, "Connector-nagios : Guide d'administration", u'Vigilo'),
        ('dev', "dev-%s" % name, "Connector-nagios : Guide de développement", u'Vigilo'),
]

latex_documents = [
        ('admin', 'admin-%s.tex' % name, u"Connector-nagios : Guide d'administration",
         'AA100004-2/ADM00002', 'vigilo'),
        ('dev', 'dev-%s.tex' % name, u"Connector-nagios : Guide de développement",
         'AA100004-2/DEV00006', 'vigilo'),
]

execfile("../buildenv/doc/conf.py")
