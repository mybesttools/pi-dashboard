# -*- coding: utf-8 -*-
"""
Clock Plugin
Provides the datetime
"""
import datetime
from lib.decorators import never_raise
from lib.plugin import BasePlugin, BaseConfig

NAME = 'Clock'


class Plugin(BasePlugin):
    DEFAULT_INTERVAL = 5

    @never_raise
    def update(self):
        self.data['datetime'] = datetime.datetime.now()
        super(Plugin, self).update()


class Config(BaseConfig):
    pass