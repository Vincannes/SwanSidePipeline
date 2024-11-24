#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import logging
from pprint import pprint

logger = logging.getLogger(__name__)

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


class SwanSideBlenderPlugins(object):

    @err_catcher(name=__name__)
    def __init__(self, parent, core, plugin):
        self.core = core
        self.parent = parent
        self.plugin = plugin

        _installLocPath = self.core.integration.installLocPath
        self.core.separateOutputVersionStack = False

        logger.info(plugin)

        self.core.registerCallback(
            "onStateCreated", self.onStateCreated, plugin=self.plugin
        )

    @err_catcher(name=__name__)
    def onStateCreated(self, origin, state, stateData):
        """Force Playblast to mp4
        """
        if state.className == "Playblast":
            state.cb_formats.setCurrentIndex(1)

        # if state.className == "ImageRender":
        #     state.cb_renderLayer.clear()