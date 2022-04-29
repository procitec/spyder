# -*- coding: utf-8 -*-
#
# Copyright © PROCITEC GmbH

from qtpy.QtGui import QFont
from qtpy.QtWidgets import QVBoxLayout

from spyder.api.config.decorators import on_conf_change
from spyder.api.shellconnect.main_widget import ShellConnectMainWidget

from .watchlist import WatchlistTableWidget


class WatchlistMainWidget(ShellConnectMainWidget):
    def __init__(self, name, plugin, parent=None):
        super().__init__(name, plugin, parent)

        layout = QVBoxLayout()
        layout.addWidget(self._stack)
        self.setLayout(layout)

        self.table_font: QFont

    # --- PluginMainWidget API ---
    def get_title(self):
        return "Watchlist"

    def setup(self):
        self.add_expression_action = self.create_action(
            "add_expression_action",  # name
            "Add expression",  # action’s text
            icon=self.create_icon("edit_add"),
            # icon_text="Clear",  # otherwise there is a tooltip with the action’s text
            triggered=self.add_expression,
        )
        self.remove_expression_action = self.create_action(
            "remove_expression_action",
            "Remove expression",
            icon=self.create_icon("edit_remove"),
            triggered=self.remove_expression,
        )
        self.remove_all_expressions_action = self.create_action(
            "remove_all_expressions_action",
            "Remove all expression",
            icon=self.create_icon("editdelete"),
            triggered=self.remove_all_expressions,
        )

        main_toolbar = self.get_main_toolbar()
        for item in [
            self.add_expression_action,
            self.remove_expression_action,
            self.remove_all_expressions_action,
        ]:
            self.add_item_to_toolbar(item, main_toolbar, "main_toolbar")

    def update_actions(self):
        pass

    # --- ShellConnectMainWidget API ---
    def create_new_widget(self, shellwidget):
        widget = WatchlistTableWidget(
            shellWidget=shellwidget,
            addAction=self.add_expression_action,
            removeAction=self.remove_expression_action,
            removeAllAction=self.remove_all_expressions_action,
        )
        widget.setTableFont(self.table_font)
        widget.setExpressions(self.get_conf("expressions"))

        return widget

    def close_widget(self, widget):
        self.set_conf("expressions", widget.getExpressions(), recursive_notification=False)
        widget.close()

    def switch_widget(self, widget, old_widget):
        pass

    # --- Public API ---
    def set_table_font(self, font: QFont) -> None:
        self.table_font = font

        for i in range(self._stack.count()):
            widget = self._stack.widget(i)
            widget.setTableFont(font)

    # --- Slots for Signals ---
    def add_expression(self):
        widget = self.current_widget()
        if widget:
            widget.onAddAction()

    def remove_expression(self):
        widget = self.current_widget()
        if widget:
            widget.onRemoveAction()

    def remove_all_expressions(self):
        widget = self.current_widget()
        if widget:
            widget.onRemoveAllAction()
