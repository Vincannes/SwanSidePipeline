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

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from csv_parser import CSVParser

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

logger = logging.getLogger(__name__)


class Prism_SwanSidePlugins_Functions(object):
    APPS = ["Blender", "Nuke", "Standalone"]

    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.name = "Prism_SwanSidePlugins"

        if not self.isActive():
            return

        path = ""
        self._parser = CSVParser(path)

        if self.core.requestedApp == "Nuke":
            from nuke.swansideNuke import SwanSideNukePlugins
            self.swanside_nuke = SwanSideNukePlugins(self, core, plugin)

        self.core.registerCallback(
            "onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self.plugin
        )

    @err_catcher(name=__name__)
    def isActive(self):
        if not self.core.requestedApp in self.APPS:
            return False
        return True

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self):
        """Write Shots and Assets to pipeline.json
        """
        shots = self._parser.get_shots()
        for shot in shots:
            entity = {
                "sequence": "C010",
                "shot": shot,
            }
            shot_path = self.core.projects.getResolvedProjectStructurePath(
                "shots", entity
            )
            if not os.path.exists(shot_path):
                self.core.entities.createShot(entity)

