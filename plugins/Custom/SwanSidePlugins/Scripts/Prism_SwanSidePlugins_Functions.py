#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import re
import os
import sys
import logging
import importlib
from pprint import pprint

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

logger = logging.getLogger(__name__)
SWANSIDE_DIR = os.path.dirname(os.path.dirname(__file__))
EXT_MODULES_PATHS = os.path.join(SWANSIDE_DIR, "ExternalModules")
sys.path.append(EXT_MODULES_PATHS)

## SWANSIDE PLUGIN
import utils
import constants
from swan_exceptions import *
from swan_kitsu.kitsuPublisher import Publisher
from swan_monkey_path import SwanSideMonkeyPatch
from customs.media import Media
from customs.login_ui import SwanSideLoginUI
from customs.publisher_ui import SwanSidePublisher
## END SWANSIDE PLUGIN

from PrismUtils.Decorators import err_catcher_plugin as err_catcher

DEBUG = False#os.environ.get("SWANSIDE_TD", False)


class Prism_SwanSidePlugins_Functions(object):
    APPS = ["Blender", "Nuke", "Standalone", "Cinema4D"]
    CSV_SHOTS = "csv_shots"
    CSV_ASSETS = "csv_assets"

    @err_catcher(name=__name__)
    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin
        self.name = "Prism_SwanSidePlugins"

        logger.debug("Current app: " + self.core.requestedApp)
        if not self.isActive():
            return

        self._publisher = None
        if not DEBUG:
            self.core.registerCallback(
                "onSetProjectStartup", self.onSetProjectStartup, plugin=self.plugin
            )
        self.core.registerCallback(
            "onProjectBrowserStartup", self.onProjectBrowserStartup, plugin=self.plugin
        )

        self._media = Media(self.core)
        user_pref_path = core.getUserPrefConfigPath()
        config_user_dict = self.core.configs.readJson(user_pref_path)
        self.prod_config_path = config_user_dict.get("globals").get("current project")
        self.config_prod_dict = self.core.configs.readJson(self.prod_config_path)

        self.register()

        monkey_path = SwanSideMonkeyPatch(core, plugin)
        monkey_path.run()

        if self.core.requestedApp == "Nuke":
            from swan_nuke.swansideNuke import SwanSideNukePlugins
            self.swanside_nuke = SwanSideNukePlugins(self, core, plugin)

        elif self.core.requestedApp == "Blender":
            from swan_blender.swansideBlender import SwanSideBlenderPlugins
            self.swanside_blender = SwanSideBlenderPlugins(self, core, plugin)

        elif self.core.requestedApp == "Cinema4D":
            from swan_cinema4d.swansideCinema4D import SwanSideCinema4DPlugins
            self.swan_cinema4d = SwanSideCinema4DPlugins(self, core, plugin)

    @property
    def media(self):
        return self._media

    @property
    def publisher(self):
        return self._publisher

    @err_catcher(name=__name__)
    def setPublisher(self, kitsu=None, mail=None, password=None):
        prjName = self.config_prod_dict.get("globals").get("project_name")
        if kitsu:
            self._publisher = Publisher(prjName, kitsu=self.kitsuPlugin)
        elif mail and password:
            url = constants.KITSU_URL
            self._publisher = Publisher(prjName, mail=mail, password=password, url=url)

    @err_catcher(name=__name__)
    def register(self):
        self.kitsuPlugin = self.core.getPlugin("Kitsu")
        if not self.kitsuPlugin:
            self.core.registerCallback("pluginLoaded", self.onPluginLoaded, plugin=self.plugin)
            return

    @err_catcher(name=__name__)
    def onPluginLoaded(self, plugin):
        if plugin.pluginName == "Kitsu":
            self.register()

    @err_catcher(name=__name__)
    def onSetProjectStartup(self, origin):
        inSwansideNAS = utils.is_nas_reachable(constants.SERVEUR_NAS_URL)
        mount_point = utils.is_mount_accessible(constants.SERVEUR_URL)
        if not inSwansideNAS and not mount_point:
            self.core.popup(
                "Vous n'etes pas connecté au serveur NAS.\n\n"\
                "Connectez vous au serveur {}.".format(constants.SERVEUR_NAS_URL)
            )

    @err_catcher(name=__name__)
    def isActive(self):
        if self.core.requestedApp not in self.APPS:
            return False
        return True

    @err_catcher(name=__name__)
    def onProjectBrowserStartup(self, origin):
        """Write Shots and Assets to pipeline.json
        """
        if self.core.requestedApp == "Standalone":
            self._updaterSwansideScripts(origin)
            if self.kitsuPlugin:
                self.setPublisher(kitsu=True)

    @err_catcher(name=__name__)
    def force_tasks_departments_from_kitsu(self):
        if not self._publisher and not self.kitsuPlugin:
            self.core.popup(
                "You need to install Kitsu plugin to process this."
            )
            return
        shots = self._publisher.get_all_shots()
        assets = self._publisher.get_all_assets()

        departments_shot = []
        for shot in shots:
            for task in self._publisher.get_tasks(shot):
                task_data = {"abbreviation": task.get("short_name"),
                             "defaultTasks": [task.get("name")],
                             "name": task.get("name")}
                if task_data in departments_shot:
                    continue
                departments_shot.append(task_data)

        departments_assets = []
        for asset in assets:
            for task in self._publisher.get_tasks(asset, entity="asset"):
                task_data = {"abbreviation": task.get("short_name"),
                             "defaultTasks": [task.get("name")],
                             "name": task.get("name")}
                if task_data in departments_assets:
                    continue
                departments_assets.append(task_data)

        self.config_prod_dict["globals"]["departments_shot"] = departments_shot
        self.config_prod_dict["globals"]["departments_asset"] = departments_assets
        self.core.configs.writeConfig(self.prod_config_path, self.config_prod_dict)

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
            assetData = self.core.projects.getMatchingPaths(template)
            for data in assetData:
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
    def get_asset_files_from_template(self, template_name="3drenders", last_only=False):
        """Get list all Paths from given template for Assets
        return[list] = {"asset_name": [path_to_render]}
        """
        all_files = {}
        version_pattern = re.compile(r'v(\d{4})')
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

            latest_paths = {}
            for identifier in os.listdir(template_dir):
                identifier_task = os.path.join(template_dir, identifier)

                for _f in sorted(self.get_files_from_task_path(identifier_task), reverse=True):
                    basename = os.path.basename(_f)
                    match = version_pattern.search(basename)

                    if last_only and match:
                        cur_version = int(match.group(1))
                        base_path = version_pattern.sub("v####", basename)

                        if base_path not in latest_paths or cur_version > latest_paths[base_path][0]:
                            latest_paths[base_path] = (cur_version, _f)
                    else:
                        all_files[asset_name].append(_f)

            if last_only:
                for _, path in latest_paths.values():
                    all_files[asset_name].append(path)

        return all_files

    @err_catcher(name=__name__)
    def get_shot_files_from_template(self, template_name="3drenders", last_only=False):
        """Get list all Paths from given template for Shots
        return[list] = {"shot_name": [path_to_render]}
        """
        all_files = {}
        version_pattern = re.compile(r'v(\d{4})')
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

            latest_paths = {}
            for identifier in os.listdir(template_dir):
                identifier_task = os.path.join(template_dir, identifier)

                for _f in sorted(self.get_files_from_task_path(identifier_task), reverse=True):
                    basename = os.path.basename(_f)
                    match = version_pattern.search(basename)

                    if last_only and match:
                        cur_version = int(match.group(1))
                        base_path = version_pattern.sub("v####", basename)

                        if base_path not in latest_paths or cur_version > latest_paths[base_path][0]:
                            latest_paths[base_path] = (cur_version, _f)
                    else:
                        all_files[shot_name].append(_f)

            if last_only:
                for _, path in latest_paths.values():
                    all_files[shot_name].append(path)

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
                all_files.append(utils.generate_pattern(files))
        return all_files

    @err_catcher(name=__name__)
    def get_fields_from_path(self, path):
        json_path = self.get_versioninfo_from_path(path)
        if not json_path:
            return {}
        return self.core.configs.readJson(json_path)

    @err_catcher(name=__name__)
    def get_versioninfo_from_path(self, path):
        json_path = None
        version_name = "versioninfo" + self.core.configs.getProjectExtension()
        if not os.path.isdir(path):
            dir_path = os.path.dirname(path)
            basename, ext = os.path.splitext(os.path.basename(path))
            basename_json = basename + "versioninfo" + self.core.configs.getProjectExtension()
            if basename_json in os.listdir(dir_path):
                json_path = os.path.join(dir_path, basename_json)
            else:
                if version_name in os.listdir(dir_path):
                    json_path = os.path.join(dir_path, version_name)
                else:
                    if version_name in os.listdir(os.path.dirname(dir_path)):
                        json_path = os.path.join(os.path.dirname(dir_path), version_name)
        else:
            if version_name in os.listdir(path):
                json_path = os.path.join(path, version_name)
            else:
                if version_name in os.listdir(os.path.dirname(path)):
                    json_path = os.path.join(os.path.dirname(path), version_name)
        return json_path

    @err_catcher(name=__name__)
    def get_all_files_from_templates(self, last_only=False):
        data = {"Assets": {}, "Shots": {}}
        assets_3d = self.get_asset_files_from_template("3drenders", last_only)
        assets_2d = self.get_asset_files_from_template("2drenders", last_only)
        shots_3d = self.get_shot_files_from_template("3drenders", last_only)
        shots_2d = self.get_shot_files_from_template("2drenders", last_only)

        def _process(sub_data, data_key, is_asset):
            for shot_name, paths in sub_data.items():
                if not shot_name in data[data_key].keys():
                    data[data_key][shot_name] = []
                for path in paths:
                    path_data = self.get_fields_from_path(path)
                    task = path_data.get("task")
                    version = path_data.get("version")
                    data[data_key][shot_name].append((path, task, "cmp", version))

        _process(assets_3d, "Assets", True)
        _process(assets_2d, "Assets", True)
        _process(shots_3d, "Shots", False)
        _process(shots_2d, "Shots", False)
        return data

    @err_catcher(name=__name__)
    def publisherUI(self):
        if not self._publisher and not self.kitsuPlugin:
            user_conf = self._get_user_config_file()
            if not os.path.exists(user_conf):
                login_ui = SwanSideLoginUI(user_conf)
                login_ui.show()
                login_ui.exec_()

            config = utils.readConfig(user_conf)
            mail = config.get("credentials", "mail")
            password = config.get("credentials", "password")
            self.setPublisher(kitsu=None, mail=mail, password=password)

        ui = SwanSidePublisher(parent=self)
        ui.show()
        ui.exec_()

    # PRIVATES

    @err_catcher(name=__name__)
    def _createShotsAssetsFolderAtStartup(self):
        if not hasattr(self.core, "projectPath"):
            return

        self._create_shots_folder()
        self._create_assets_folder()
        self._saveShotsAssetsToPipelineJson()

    def _create_shots_folder(self):

        for shot in self._publisher.get_all_shots():
            entity = {
                "sequence": shot.split("_")[0],
                "shot": shot,
            }
            shot_path = self.core.projects.getResolvedProjectStructurePath(
                "shots", entity
            )
            framerange = [0, 0]
            if not os.path.exists(shot_path):
                self.core.entities.createShot(entity, framerange)

    def _create_assets_folder(self):
        for asset in self._publisher.get_all_assets():
            name = asset.get("name")
            entity = {
                "entityType": "asset",
                "shot": name,
            }
            asset_path = self.core.projects.getResolvedProjectStructurePath(
                "assets", entity
            )
            if not os.path.exists(asset_path):
                self.core.entities.createAsset(entity)

    def _create_assets_folder_from_csv(self, csv_path):
        logger.info("Load csv:  {}".format(csv_path))
        from customs.csv_parser import CSVParser
        _parser = CSVParser(csv_path)

        assets = _parser.get_assets()
        for asset in assets:
            entity = {
                "entityType": "asset",
                "asset_path": asset
            }
            asset_path = self.core.projects.getResolvedProjectStructurePath(
                "assets", entity
            )
            if not os.path.exists(asset_path):
                self.core.entities.createAsset(entity)

        _parser.unset_env()

    def _create_shots_folder_from_csv(self, csv_path):
        logger.info("Load csv:  {}".format(csv_path))
        from customs.csv_parser import CSVParser
        _parser = CSVParser(csv_path)

        shots = _parser.get_shots()
        frame_range = _parser.get_shots_framerange()
        for shot in shots:
            entity = {
                "sequence": shot.split("_")[0],
                "shot": shot,
            }
            shot_path = self.core.projects.getResolvedProjectStructurePath(
                "shots", entity
            )
            framerange = frame_range.get(shot)
            if not os.path.exists(shot_path):
                self.core.entities.createShot(entity, framerange)

        _parser.unset_env()
        self._saveShotsAssetsToPipelineJson()

    def _saveShotsAssetsToPipelineJson(self):
        """Write Shots and Assets to pipeline.json
        """
        configPath = self.core.configs.getConfigPath("project")
        data = self.core.getConfig(configPath=configPath)
        _, shots = self.core.entities.getShots()
        assets = self.get_assets()

        data["shots"] = {}
        data["assets"] = {}
        for asset in assets:
            asset_name = asset.get("asset")
            type = asset.get("asset_path").split(os.sep)[0]
            if not type in data["assets"].keys():
                data["assets"][type] = []
            data["assets"][type].append(asset_name)

        for shot in shots:
            shot_name = shot.get("shot")
            sequence = shot.get("sequence")
            if not sequence in data["shots"].keys():
                data["shots"][sequence] = []
            data["shots"][sequence].append(shot_name)

        self.core.configs.writeConfig(configPath, data)

    def _updaterSwansideScripts(self, origin):

        if not getattr(origin, "menubar", None):
            return

        import swan_updatePrism
        if self.core.uiAvailable:
            icon_path = os.path.join(self.pluginDirectory, "resources", "logo_swan.png")
            swan_menu = QMenu("Swanside")
            swan_menu.setIcon(QPixmap(icon_path))
            # tools = swan_menu.addMenu("Load CSVs")
            # tools.addAction("Load Shots csv..", lambda: self._load_csv_path(isAsset=False))
            # tools.addAction("Load Assets csv..", lambda: self._load_csv_path(isAsset=True))
            swan_menu.addAction("Publish to Kitsu..", lambda: self.publisherUI())
            swan_menu.addAction("Synch Project Task from Kitsu", self.force_tasks_departments_from_kitsu)
            origin.menubar.addMenu(swan_menu)
            origin.myMenu = swan_menu

        if swan_updatePrism.has_to_run():
            from customs.update_ui import UpdateUi
            dialog = UpdateUi()
            dialog.exec_()

    def _load_csv_path(self, isAsset=False):
        configPath = self.core.configs.getConfigPath("project")
        data = self.core.configs.readJson(path=configPath)
        file_path, _ = QFileDialog.getOpenFileName(
            None, "Open File", "", "All Files (*);;Text Files (*.csv)"
        )
        if isAsset:
            data[self.CSV_ASSETS] = file_path
            self.core.configs.writeConfig(configPath, data)
            self._create_assets_folder_from_csv(file_path)
        else:
            data[self.CSV_SHOTS] = file_path
            self.core.configs.writeConfig(configPath, data)
            self._create_shots_folder_from_csv(file_path)

    def _get_user_config_file(self):
        user_dir = os.path.dirname(self.core.userini)
        user_conf_file = os.path.join(user_dir, constants.CONFIG_FILE_NAME)
        return user_conf_file
