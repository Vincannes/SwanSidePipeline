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
import re
import os
import sys
import json
import logging
import subprocess
import platform
from pprint import pprint
from collections import OrderedDict

from kitsuPublisher import Publisher, EXT_MODULES_PATHS

from PrismUtils.Decorators import err_catcher_plugin as err_catcher


logger = logging.getLogger(__name__)


def convert_sequence_to_mov(path, first_frame):
    dir_name = os.path.dirname(path)

    output_path = convert_sequence_to_mov_path(path)
    cmd = "ffmpeg -apply_trc iec61966_2_1 -start_number {} -i {} {}".format(
        first_frame, path.replace(".####.", ".%04d."), output_path
    )
    return cmd


def convert_sequence_to_mov_path(path):
    return os.path.join(os.path.dirname(path), os.path.basename(path).split(".")[0] + ".mov")


def generate_pattern(file_list):
    first_file = file_list[0]
    dir_path, file_name = os.path.split(first_file)
    base_name, ext = os.path.splitext(file_name)
    parts = base_name.split('.')
    frame_number = parts[-1]
    base_pattern = '.'.join(parts[:-1])

    pattern = os.path.join(dir_path, f"{base_pattern}.%04d.{ext[1:]}")
    return pattern


class Prism_SwanSidePlugins_Functions(object):
    APPS = ["Blender", "Nuke"]
    NUKE_STATUS = "wfa"

    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.swanside_nuke = None
        self.prjMng = None
        self.name = "Prism_SwanSidePlugins"

        print(self.core.requestedApp)
        if not self.isActive():
            return
        self.register()

        user_pref_path = core.getUserPrefConfigPath()
        config_file_dict = json.load(open(user_pref_path)).get("globals").get("current project")
        prjName = json.load(open(config_file_dict)).get("globals").get("project_name")
        url = json.load(open(config_file_dict)).get("prjManagement").get("kitsu_url")
        email = os.getenv("PRISM_KITSU_EMAIL")
        password = os.getenv("PRISM_KITSU_PASSWORD")

        self._publisher = Publisher(prjName, url, email, password)

        if self.core.requestedApp == "Nuke":
            from swansideNuke import SwanSideNukePlugins
            self.swanside_nuke = SwanSideNukePlugins(self, core, plugin)

        self.core.plugins.monkeyPatch(self.core.media.getFFmpeg, self.getFFmpeg, self, force=True)
        self.core.plugins.monkeyPatch(self.core.media.convertMedia, self.convertMedia, self, force=True)

    # if returns true, the plugin will be loaded by Prism
    @err_catcher(name=__name__)
    def isActive(self):
        if not self.core.requestedApp in self.APPS:
            return False
        return True

    @err_catcher(name=__name__)
    def register(self):
        self.prjMng = self.core.getPlugin("ProjectManagement")
        if not self.prjMng:
            self.core.registerCallback("pluginLoaded", self.onPluginLoaded, plugin=self.plugin)
            return
        self.prjMng.registerManager(self)

    @err_catcher(name=__name__)
    def onPluginLoaded(self, plugin):
        if plugin.pluginName == "ProjectManagement":
            self.register()

    @err_catcher(name=__name__)
    def get_assets(self):
        """Get list all assets
        return[dict] = {}
        """
        location_paths = self.core.paths.getExportProductBasePaths()
        location_paths.update(self.core.paths.getRenderProductBasePaths())
        seqDirs = []

        for location in location_paths:
            seqDir = {"location": location, "path": location_paths[location]}
            seqDirs.append(seqDir)

        assets = []
        for seqDir in seqDirs:
            context = {"project_path": seqDir["path"]}
            template = self.core.projects.getResolvedProjectStructurePath(
                "assets", context=context
            )
            shotData = self.core.projects.getMatchingPaths(template)
            for data in shotData:
                path = data["path"]
                if "." in os.path.basename(path) and os.path.isfile(path):
                    continue
                if data["asset_path"].startswith("_"):
                    continue

                for asset_name in os.listdir(path):
                    data["location"] = seqDir["location"]
                    data["asset"] = asset_name
                    data["type"] = "assets"
                    data["asset_path"] = os.path.join(data["asset_path"], asset_name)
                    assets.append(data)

        assets = sorted(assets, key=lambda x: self.core.naturalKeys(x["asset"]))
        return assets

    @err_catcher(name=__name__)
    def get_first_last_frames(self, inputpathdir, inputExt):
        # self.core.paths.getFrameFromFilename()
        endNum = None
        startNum = None
        pattern = r'\.(\d+)\.[^.]+$'
        if any([inputExt in ext for ext in [".exr", ".jpg"]]):
            frames = []
            for filename in os.listdir(inputpathdir):
                match = re.search(pattern, filename)
                if match:
                    frames.append(int(match.group(1)))
            startNum = sorted(frames)[0] or 1001
            endNum = sorted(frames)[-1] or 1001
        return startNum, endNum

    @err_catcher(name=__name__)
    def get_json_files_from_template(self, template_name):

        files = []
        seqs, shots = self.core.entities.getShots()
        for shot_context in shots:
            shot_path = self.core.paths.getEntityPath(shot_context)
            if not os.path.exists(shot_path):
                continue

            shot_context["mediatype"] = template_name

            template = self.core.projects.getResolvedProjectStructurePath(
                template_name, context=shot_context
            )

            template_dir = os.path.dirname(template)
            if not os.path.exists(template_dir):
                continue

            for identifier in os.listdir(template_dir):
                identifier_task = os.path.join(template_dir, identifier)

                for root, dirs, iden_files in os.walk(identifier_task):
                    for _f in iden_files:
                        if not _f.endswith('.json'):
                            continue
                        files.append(os.path.join(root, _f))
        return files

    @err_catcher(name=__name__)
    def get_asset_files_from_template(self, template_name="3drenders"):
        """Get list all Paths from given template for Assets
        return[list] = {"asset_name": [path_to_render]}
        """
        all_files = {}
        for asset_context in self.get_assets():

            asset_name = asset_context.get("asset")
            asset_path = asset_context.get("path")

            if not os.path.exists(asset_path):
                continue

            if not asset_name in all_files.keys():
                all_files[asset_name] = []

            asset_context["mediatype"] = template_name
            template = self.core.projects.getResolvedProjectStructurePath(
                template_name, context=asset_context
            )

            template_dir = os.path.dirname(template)
            if not os.path.exists(template_dir):
                continue

            for identifier in os.listdir(template_dir):
                identifier_task = os.path.join(template_dir, identifier)
                all_files[asset_name].append(self.get_files_from_task_path(identifier_task))

        return all_files

    @err_catcher(name=__name__)
    def get_shot_files_from_template(self, template_name="3drenders"):
        """Get list all Paths from given template for Shots
        return[list] = {"shot_name": [path_to_render]}
        """
        all_files = {}
        seqs, shots = self.core.entities.getShots()
        for shot_context in shots:
            shot_name = shot_context.get("shot")
            shot_path = self.core.paths.getEntityPath(shot_context)
            if not os.path.exists(shot_path):
                continue

            if not shot_name in all_files.keys():
                all_files[shot_name] = []

            shot_context["mediatype"] = template_name
            template = self.core.projects.getResolvedProjectStructurePath(
                template_name, context=shot_context
            )
            template_dir = os.path.dirname(template)

            if not os.path.exists(template_dir):
                continue

            for identifier in os.listdir(template_dir):
                identifier_task = os.path.join(template_dir, identifier)
                all_files[shot_name].append(self.get_files_from_task_path(identifier_task))

        return all_files

    @err_catcher(name=__name__)
    def get_files_from_task_path(self, task_path):
        all_files = []
        for root, dirs, files in os.walk(task_path):
            for _f in files:
                if not _f.endswith("json") or not [item for item in os.listdir(root) if not item.endswith('.json')]:
                    continue

                json_path = os.path.join(root, _f)
                json_dict = self.core.configs.readJson(json_path)

                files = json_dict.get("path", [])
                if files:
                    all_files.append(files)
                    continue

                aovs = self.core.mediaProducts.getAOVsFromVersion(json_dict)
                if not aovs:
                    continue

                files = self.core.mediaProducts.getFilesFromContext(aovs[0])
                all_files.append(generate_pattern(files))
        return all_files

    @err_catcher(name=__name__)
    def convertMedia(self, inputpath, startNum, outputpath, settings=None):
        inputpath = inputpath.replace("\\", "/")
        inputExt = os.path.splitext(inputpath)[1].lower()
        logger.info(inputExt)
        logger.info(inputpath)

        ## SWANSIDE
        inputpathdir = os.path.dirname(inputpath)
        if inputExt == ".json":
            for i in os.listdir(inputpathdir):
                if i.endswith(".mp4"):
                    inputExt = ".mp4"
                    inputpath = os.path.join(inputpathdir, i)
                    break
                elif i.endswith(".exr") or i.endswith(".jpg"):
                    inputExt = "." + i.split(".")[-1]
                    logger.info("     " + inputExt)
                    i_name = "{}.%04d.{}".format(i.split(".")[0], inputExt.replace(".", ""))
                    inputpath = os.path.join(inputpathdir, i_name)
                    break

        # Get first frame if is not given
        tmpstartNum, endNum = self.get_first_last_frames(inputpathdir, inputExt)
        if not isinstance(startNum, int):
            startNum = tmpstartNum
        ## END SWANSIDE

        outputExt = os.path.splitext(outputpath)[1].lower()
        videoInput = inputExt in [".mp4", ".mov", ".m4v"]
        startNum = str(startNum) if startNum is not None else None

        ffmpegPath = self.getFFmpeg(validate=True)

        if not ffmpegPath:
            msg = "Could not find ffmpeg"
            if platform.system() == "Darwin":
                msg += (
                    '\n\nYou can install it with this command:\n"brew install ffmpeg"'
                )

            self.core.popup(msg, severity="critical")
            return

        if not os.path.exists(os.path.dirname(outputpath)):
            os.makedirs(os.path.dirname(outputpath))

        if videoInput:
            args = OrderedDict(
                [
                    ("-apply_trc", "iec61966_2_1"),
                    ("-i", inputpath),
                    ("-pix_fmt", "yuva420p"),
                    ("-start_number", startNum),
                ]
            )

        else:
            fps = "25"
            if self.core.getConfig(
                "globals", "forcefps", configPath=self.core.prismIni
            ):
                fps = self.core.getConfig(
                    "globals", "fps", configPath=self.core.prismIni
                )

            args = OrderedDict(
                [
                    ("-start_number", startNum),
                    ("-framerate", fps),
                    ("-apply_trc", "iec61966_2_1"),
                    ("-i", inputpath),
                    ("-pix_fmt", "yuva420p"),
                    ("-start_number_out", startNum),
                ]
            )

            if startNum is None:
                args.popitem(last=False)
                args.popitem(last=True)

        ## SWANSIDE
        if inputExt == ".exr":
            logger.info("Run Nuke processing for %s" % inputExt)
            return self.process_mov_from_nuke(
                inputpath, outputpath, startNum, endNum, self.core.requestedApp == "Blender"
            )
        ## END SWANSIDE

        if outputExt == ".jpg":
            quality = self.core.getConfig(
                "media", "jpgCompression", dft=4, config="project"
            )
            args["-qscale:v"] = str(quality)

        if outputExt == ".mp4":
            quality = self.core.getConfig(
                "media", "mp4Compression", dft=18, config="project"
            )
            args["-crf"] = str(quality)

        if settings:
            args.update(settings)

        argList = [ffmpegPath]

        for k in args.keys():
            if not args[k]:
                continue

            if isinstance(args[k], list):
                al = [k]
                al.extend([str(x) for x in args[k]])
            else:
                val = str(args[k])
                if k == "-start_number_out":
                    k = "-start_number"
                al = [k, val]

            argList += al

        argList += [outputpath, "-y"]
        logger.info("Run ffmpeg with this settings: " + str(argList))
        nProc = subprocess.Popen(
            argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )
        result = nProc.communicate()

        if sys.version[0] == "3":
            result = [x.decode("utf-8", "ignore") for x in result]

        return result

    @err_catcher(name=__name__)
    def process_mov_from_nuke(self, path, output_path, frame_in, frame_out, from_blender=False):
        nuke_path = self.core.getConfig("dccoverrides", "Nuke_path")
        scene_py = os.path.join(EXT_MODULES_PATHS, "process_mov_nk.py")

        data_dict = {
            "input_path": path,
            "output_path": output_path,
            "frame_in": int(frame_in),
            "frame_out": int(frame_out),
            "from_blender": from_blender,
        }

        json_path = os.path.join(
            os.path.dirname(output_path), os.path.basename(output_path) + ".json"
        )

        with open(json_path, 'w') as fp:
            json.dump(data_dict, fp, indent=4)
        argList = [nuke_path, "-x", scene_py, json_path]

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

    @err_catcher(name=__name__)
    def getFFmpeg(self, validate=False):
        ffmpegPath = "ffmpeg"
        if platform.system() == "Windows":
            # SwanSide Fix
            _ffmpeg_path = os.path.normpath(self.core.prismLibs)
            # End SwanSide Fix
            ffmpegPath = os.path.join(
                _ffmpeg_path, "Tools", "FFmpeg", "bin", "ffmpeg.exe"
            )
        elif platform.system() == "Linux":
            ffmpegPath = "ffmpeg"

        elif platform.system() == "Darwin":
            ffmpegPath = "ffmpeg"

        if validate:
            result = self.validateFFmpeg(ffmpegPath)
            if not result:
                return
        return ffmpegPath

    @err_catcher(name=__name__)
    def validateFFmpeg(self, path):
        ffmpegIsInstalled = False

        if platform.system() == "Windows":
            if os.path.exists(path):
                ffmpegIsInstalled = True
        elif platform.system() == "Linux":
            try:
                subprocess.Popen([path], shell=True)
                ffmpegIsInstalled = True
            except:
                pass

        elif platform.system() == "Darwin":
            try:
                subprocess.Popen([path], shell=True)
                ffmpegIsInstalled = True
            except:
                pass

        return ffmpegIsInstalled

    def postPlayblast(self, **kwargs):
        logger.info("kwargs: %s", str(kwargs))

    def postPublish(self, *args, **kwargs):
        logger.info("args: %s", args)
        logger.info("kwargs: %s", str(kwargs))

