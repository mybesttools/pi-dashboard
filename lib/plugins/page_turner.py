# -*- coding: utf-8 -*-
"""
Clock Plugin
Provides the datetime
"""
import os
from lib import PLUGINDIR, log
from lib.plugin import BasePlugin, BaseConfig
from lib.decorators import never_raise, threaded_method

NAME = 'Page Interval'


class Plugin(BasePlugin):
    DEFAULT_INTERVAL = 10

    @threaded_method
    def enable(self):
        self.data['start_up'] = True
        self.data['next_page'] = False
        super(Plugin, self).enable()

    @never_raise
    def update(self):
        if not self.enabled:
            return
        # prevent firing wen starting up...
        if self.data['start_up']:
            self.data['start_up'] = False
            self.data['next_page'] = False
        else:
            # all plugin pages should be initialized now..
            self.data['next_page'] = True
        super(Plugin, self).update()


class Config(BaseConfig):
    TEMPLATE = os.path.join(PLUGINDIR, 'page_turner_config.html')
