# -*- coding: utf-8 -*-
#
# Copyright © PROCITEC GmbH
# Licensed under the terms of the MIT License
# (see spyder/__init__.py for details)

from spyder.api.plugin_registration.decorators import on_plugin_available
from spyder.api.plugins import Plugins, SpyderDockablePlugin
from spyder.api.shellconnect.mixins import ShellConnectMixin

from .widgets.main_widget import WatchlistMainWidget


class Watchlist(SpyderDockablePlugin, ShellConnectMixin):
    # --- SpyderPluginV2 API ---
    NAME = "watchlist"
    REQUIRES = [Plugins.IPythonConsole]
    CONF_SECTION = NAME
    # CONF_FILE = True  # use separate configuration file (default)
    CONF_VERSION = "1.0.0"
    CONF_DEFAULTS = [(NAME, {"expressions": []})]

    # -- SpyderDockablePlugin API ---
    # TABIFY seems to be ignored if the plugin is added to a layout in
    # plugins/layout/layout.py. However, it seems to be respected when the plugin
    # is not in a layout and the user “manually” enables it using the Panes
    # menu.
    TABIFY = [Plugins.VariableExplorer]
    WIDGET_CLASS = WatchlistMainWidget

    # --- SpyderPluginV2 API ---
    @staticmethod
    def get_name():
        return "Watchlist"

    def get_description(self):
        return "Execute Python statements in the current namesapce and view the results"

    def get_icon(self):
        return self.create_icon("debug")

    def on_initialize(self):
        font = self.get_font()  # returns editor font
        self.get_widget().set_table_font(font)

    def update_font(self):
        font = self.get_font()  # returns editor font
        self.get_widget().set_table_font(font)

    # --- required by ShellConnectMixin ---
    def current_widget(self):
        return self.get_widget().current_widget()
