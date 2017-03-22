# -*- coding: utf-8 -*-
"""
PiDashboard About
"""
import os
from lib import SHAREDIR, VERSION
from lib.pi_widgets import PiWidget
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QT_VERSION_STR, PYQT_VERSION_STR
from xml.etree import ElementTree


class AboutWindow(PiWidget):
    TEMPLATE = os.path.join(SHAREDIR, 'templates', 'about.html')

    def __init__(self, parent=None):
        with open(self.TEMPLATE) as tmpl:
            template = ElementTree.fromstring(tmpl.read())
        PiWidget.__init__(self, template, self, parent)
        self.setWindowTitle('About Pi Dashboard')
        self.setWindowFlags(Qt.Dialog)
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowIcon(QtGui.QIcon(QtGui.QPixmap('img:logo.png')))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self._init_stylesheet()
        self.manifest.version.setText('Version %s' % VERSION)
        self.manifest.qt.setText('QT v%s, PyQT v%s' % (QT_VERSION_STR, PYQT_VERSION_STR))

    def _init_stylesheet(self):
        stylepath = os.path.join(SHAREDIR, 'pi-dashboard.css')
        with open(stylepath) as handle:
            self.setStyleSheet(handle.read())
