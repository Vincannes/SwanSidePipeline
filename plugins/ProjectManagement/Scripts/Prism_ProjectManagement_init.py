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


from Prism_ProjectManagement_Variables import Prism_ProjectManagement_Variables
from Prism_ProjectManagement_Functions import Prism_ProjectManagement_Functions


class Prism_ProjectManagement(Prism_ProjectManagement_Variables, Prism_ProjectManagement_Functions):
    def __init__(self, core):
        Prism_ProjectManagement_Variables.__init__(self, core, self)
        Prism_ProjectManagement_Functions.__init__(self, core, self)
