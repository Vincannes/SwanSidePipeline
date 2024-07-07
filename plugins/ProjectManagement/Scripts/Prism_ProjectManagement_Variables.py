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
# Licensed under proprietary license. See license file in the directory of this plugin for details.
#
# This file is part of Prism-Plugin-ProjectManagement.
#
# Prism-Plugin-ProjectManagement is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.


class Prism_ProjectManagement_Variables(object):
    def __init__(self, core, plugin):
        self.version = "v2.0.9"
        self.pluginName = "ProjectManagement"
        self.pluginType = "Custom"
        self.platforms = ["Windows"]
