#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import re
import sys
import json
import logging
import platform
import subprocess

PUBLISHER_DIR = os.path.dirname(os.path.dirname(__file__))
EXT_MODULES_PATHS = os.path.join(PUBLISHER_DIR, "ExternalModules")

logger = logging.getLogger(__name__)


class Media(object):

    def __init__(self):
        prism_json = ""
        user_dir = os.environ["userprofile"]
        if platform.system() == "Windows":
            prism_json = os.path.join(user_dir, "Documents", "Prism2", "Prism.json")

        self._nuke_path = json.load(open(prism_json)).get("dccoverrides").get("Nuke_path")

    def get_first_last_frames(self, inputpathdir, inputExt):
        # self.core.paths.getFrameFromFilename()
        endNum = None
        startNum = None
        pattern = r'\.(\d+)\.[^.]+$'
        inputpathdir = os.path.normpath(inputpathdir)
        if not os.path.isdir(inputpathdir):
            inputpathdir = os.path.dirname(inputpathdir)
        if any([inputExt in ext for ext in [".exr", ".jpg"]]):
            frames = []
            for filename in os.listdir(inputpathdir):
                match = re.search(pattern, filename)
                if match:
                    frames.append(int(match.group(1)))
            startNum = sorted(frames)[0] or 1001
            endNum = sorted(frames)[-1] or 1001
        return startNum, endNum

    def process_mov_from_nuke(self, path, output_path, frame_in, frame_out):
        import nuke
        read = nuke.createNode("Read")
        write = nuke.createNode("Write")
        read["file"].fromUserText("{} {}-{}".format(os.path.normpath(path), frame_in, frame_out))
        read["origfirst"].setValue(frame_in)
        read["origlast"].setValue(frame_out)
        read["first"].setValue(frame_in)
        read["last"].setValue(frame_out)
        write["file"].setValue(output_path)
        write["file_type"].setValue("mov")
        write.setInput(0, read)

        nuke.execute(write, frame_in, frame_out, 1)
        nuke.delete(read)
        nuke.delete(write)

    def process_mov_to_nuke(self, path, output_path, frame_in, frame_out, from_blender=False):
        scene_py = os.path.join(EXT_MODULES_PATHS, "process_mov_nk.py")

        data_dict = {
            "input_path": path,
            "output_path": output_path,
            "frame_in": int(frame_in),
            "frame_out": int(frame_out),
            "from_blender": from_blender,
        }
        if output_path.endswith(".mov"):
            output_path_file = output_path.replace(".mov", "")
        else:
            output_path_file = output_path
        json_path = os.path.join(
            os.path.dirname(output_path), os.path.basename(output_path_file) + ".json"
        )

        with open(json_path, 'w') as fp:
            json.dump(data_dict, fp, indent=4)
        argList = [self._nuke_path, "-x", scene_py, json_path]

        logger.info("Processing mov from path: {} to {} on frame {} {}".format(
            path, output_path, frame_in, frame_out)
        )

        nProc = subprocess.Popen(
            argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        result = nProc.communicate()
        if sys.version[0] == "3":
            result = [x.decode("utf-8", "ignore") for x in result]
        logger.info(result)

        return result
