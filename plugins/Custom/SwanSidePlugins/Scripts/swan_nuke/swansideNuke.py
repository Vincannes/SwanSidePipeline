#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import glob
import json
import nuke
import logging
import tempfile
from pprint import pprint

logger = logging.getLogger(__name__)

from swan_exceptions import PublishNukeFailed
from swan_nuke.nukePublisherUI import SwanSideNukePublisher
from swan_nuke.swanSideImportNukeLayersUi import ImportNukeLayers


class SwanSideNukePlugins(object):
    NUKE_STATUS = "wfa"

    def __init__(self, parent, core, plugin):
        self.core = core
        self.parent = parent
        self.plugin = plugin

        self._read_manager = ImportNukeLayers
        self.ui_publisher = SwanSideNukePublisher

        self.core.separateOutputVersionStack = False
        self.addCallBacks()

    def addCallBacks(self):
        nuke.addOnCreate(lambda : self._write_node(nuke.thisNode()), nodeClass="WritePrism")

    def read_manager(self, parent):
        data = self.parent.get_all_files_from_templates(last_only=True)
        return self._read_manager(data, parent)

    def publish_nuke(self, sequence_path, scene_path, comment=""):
        pattern_path = sequence_path
        if "####" in sequence_path:
            pattern_path = sequence_path.replace("####", "*")
        elif "%04d" in sequence_path:
            pattern_path = sequence_path.replace("%04d", "*")

        json_seq_path = self.core.getVersioninfoPath(os.path.dirname(sequence_path))
        json_scene_path = self.core.getVersioninfoPath(scene_path)

        if not os.path.exists(json_seq_path) or not glob.glob(pattern_path):
            return PublishNukeFailed("No render exist for {}".format(
                os.path.basename(sequence_path)), sequence_path
            )
        if not os.path.exists(json_scene_path):
            return PublishNukeFailed("No scene exist for {}".format(
                os.path.basename(scene_path)), scene_path
            )

        seq_data = json.load(open(json_seq_path, "r"))
        scene_data = json.load(open(json_scene_path, "r"))

        extension = os.path.basename(sequence_path).split(".")[-1]
        first_frame, last_frame = self.parent.media.get_first_last_frames(
            os.path.dirname(sequence_path), extension
        )

        _, filename = tempfile.mkstemp()
        tmp_mov = os.path.join(
            os.path.dirname(filename), os.path.basename(filename) + ".mov"
        )

        try:
            self.parent.media.process_mov_from_nuke(
                sequence_path, tmp_mov, first_frame, last_frame
            )
        except Exception as e:
            return PublishNukeFailed(str(e), sequence_path)

        path = os.path.realpath(tmp_mov)
        os.startfile(path)

        return "Publish Succeed for {}".format(os.path.basename(sequence_path))

    def _write_node(self, node):
        if not node:
            node = nuke.thisNode()
        node["identifier"].setValue("base")
        self.core.appPlugin.getOutputPath(node.node("WritePrismBase"), node)
