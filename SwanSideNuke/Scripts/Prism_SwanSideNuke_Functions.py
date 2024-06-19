# -*- coding: utf-8 -*-
#
####################################################
#
# PRISM - Pipeline for animation and VFX projects
#
# www.prism-pipeline.com
#
# contact: contact@prism-pipeline.com
#
####################################################
#
#
# Copyright (C) 2016-2023 Richard Frangenberg
# Copyright (C) 2023 Prism Software GmbH
#
# Licensed under GNU LGPL-3.0-or-later
#
# This file is part of Prism.
#
# Prism is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Prism is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Prism.  If not, see <https://www.gnu.org/licenses/>.

import os
import logging
# try:
    # import nuke
    # from PySide2.QtCore import *
    # from PySide2.QtGui import *
    # from PySide2.QtWidgets import *
    # from Prism_SwanSideNuke_UI import ReadManagerUI
# except:
#     pass

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

logger = logging.getLogger(__name__)

class Prism_SwanSideNuke_Functions(object):
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

        logger.info(core.requestedApp)
        logger.info(plugin)

    # @err_catcher(name=__name__)
    # def startup(self, origin):
    #     logger.info(origin)
    #     logger.info(self.core.uiAvailable)
        # if self.core.uiAvailable:
            # self.addMenus()

    # if returns true, the plugin will be loaded by Prism
    # @err_catcher(name=__name__)
    # def isActive(self):
        # if self.core.requestedApp == "Nuke":
        # return True
        # return False

    # def addMenus(self):
    #     nuke.menu("Nuke").addCommand(
    #         "Prism/Import Reads", self.import_read_ui, shortcut="ctrl+r"
    #     )

    def import_read_ui(self):
        seqs, shots = self.core.entities.getShots()
        for shot in shots:
            # pprint(shot)
            path = self.core.paths.getEntityPath(shot, "Compositing")
            print(os.path.exists(path))

        # read_manager = ReadManagerUI(QApplication.activeWindow())
        # read_manager.show()
