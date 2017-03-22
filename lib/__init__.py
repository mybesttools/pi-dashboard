# -*- coding: utf-8 -*-
"""
Useful constants
"""
import logging, os, sys
from logging.handlers import RotatingFileHandler


# Basic Configuration
APPNAME = 'Pi Dashboard'
VERSION = '0.1'
CONFIGDIR = os.path.join(os.getenv('HOME'), '.config', 'pi-dashboard')
CONFIGPATH = os.path.join(CONFIGDIR, 'config.json')
STATUSFILE = os.path.join(CONFIGDIR, 'status.json')
WORKDIR = os.path.dirname(os.path.dirname(__file__))
PLUGINDIR = os.path.join(WORKDIR, 'lib', 'plugins')
SHAREDIR = os.path.join(WORKDIR, 'share')
THEMEDIR = os.path.join(SHAREDIR, 'themes')
HOMEPAGE = 'http://mybesttools.com'


# Logging Configuration
log = logging.getLogger('Pi-Dashboard')
log_file = os.path.join(CONFIGDIR, 'pi-dashboard.log')
log_format = logging.Formatter('%(asctime)s %(module)12s:%(lineno)-4s %(levelname)-9s %(message)s')
log_dir = os.path.dirname(log_file)
os.makedirs(log_dir, exist_ok=True)
file_handler = RotatingFileHandler(log_file, 'a', 512000, 3)
file_handler.setFormatter(log_format)
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(log_format)
log.addHandler(file_handler)
log.addHandler(stream_handler)
log.setLevel(logging.INFO)
