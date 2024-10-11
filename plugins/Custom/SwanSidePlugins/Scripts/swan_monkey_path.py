#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
import logging

from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *

from PrismUtils.Decorators import err_catcher_plugin as err_catcher
import utils
import constants

logger = logging.getLogger(__name__)


class SwanSideMonkeyPatch(object):

    def __init__(self, core, plugin):
        self.core = core
        self.plugin = plugin

    def run(self):
        self.core.plugins.monkeyPatch(self.core.projects.changeProject, self.changeProject, self, force=True)

    @err_catcher(name=__name__)
    def changeProject(self, configPath=None, openUi="", settingsTab=None, settingsType=None, unset=False):
        if not unset:
            if configPath is None:
                return

            if not self.core.isStr(configPath):
                return

            if self.core.projects.isPrism1Project(configPath):
                if not self.core.prism1Compatibility:
                    self.core.projects.setPrism1Compatibility(True)
            else:
                if self.core.prism1Compatibility:
                    self.core.projects.setPrism1Compatibility(False)

            if os.path.isdir(configPath):
                if os.path.basename(configPath) == self.core.projects.getDefaultPipelineFolder():
                    configPath = os.path.dirname(configPath)

                configPath = self.core.configs.getProjectConfigPath(configPath)

            configPath = (
                    self.core.configs.findDeprecatedConfig(configPath) or configPath
            )

            #SWANSIDE FIX
            if not os.path.exists(configPath) and not utils.is_nas_reachable(constants.SERVEUR_NAS_URL):
                self.core.popup(
                    "Cannot connect to SwanSide NAS. File doesn't exist:\n\n{path}\n\n"\
                    "Please connect you to Swanside NAS: {url}".format(
                        path=configPath,
                        url=constants.SERVEUR_NAS_URL
                    )
                )
                return
            #END SWANSIDE FIX
            elif not os.path.exists(configPath):
                self.core.popup(
                    "Cannot set project. File doesn't exist:\n\n%s" % configPath
                )
                return

            configPath = self.core.fixPath(configPath)
            projectPath = str(os.path.abspath(
                os.path.join(configPath, os.pardir, os.pardir)
            ))
            if not projectPath.endswith(os.sep):
                projectPath += os.sep

            configData = self.core.getConfig(configPath=configPath)
            if configData is None:
                logger.debug("unable to read project config: %s" % configPath)
                return

            projectName = self.core.getConfig(
                "globals", "project_name", configPath=configPath
            )
            projectVersion = (
                    self.core.getConfig("globals", "prism_version", configPath=configPath)
                    or ""
            )

            if not projectName:
                self.core.popup(
                    'The project config doesn\'t contain the "project_name" setting.\n\nCannot open project.'
                )
                return

            reqPlugins = (
                    self.core.getConfig("globals", "required_plugins", configPath=configPath)
                    or []
            )

            missing = []
            for reqPlugin in reqPlugins:
                if not reqPlugin:
                    continue

                if not self.core.getPlugin(reqPlugin):
                    unloadedPlugin = self.core.plugins.getUnloadedPlugin(reqPlugin)
                    if unloadedPlugin:
                        msg = "The plugin \"%s\" has to be loaded to open project \"%s\".\n\nDo you want to load plugin \"%s\" now?" % (
                            reqPlugin, projectName, reqPlugin)
                        result = self.core.popupQuestion(msg)
                        if result == "Yes":
                            loadedPlugin = self.core.plugins.loadPlugin(unloadedPlugin.pluginPath)
                            if loadedPlugin:
                                continue

                    missing.append(reqPlugin)

            if missing:
                msg = "Cannot open project \"%s\".\n\nThe following plugins are required to open this project:\n\n" % projectName
                msg += "\n".join(missing)
                self.core.popup(msg)
                return

        path = self.core.projects.changeProject(configPath=None, openUi="", settingsTab=None, settingsType=None,
                                                unset=False)

        delModules = []

        pipefolder = self.core.projects.getPipelineFolder()
        for path in sys.path:
            if pipefolder and pipefolder in path:
                delModules.append(path)

        for modulePath in delModules:
            sys.path.remove(modulePath)

        if hasattr(self.core, "projectPath"):
            modulePath = os.path.join(
                self.core.projects.getPipelineFolder(), "CustomModules", "Python"
            )
            if modulePath in sys.path:
                sys.path.remove(modulePath)

            curModules = list(sys.modules.keys())
            for i in curModules:
                if (
                        hasattr(sys.modules[i], "__file__")
                        and sys.modules[i].__file__ is not None
                        and modulePath in sys.modules[i].__file__
                ):
                    del sys.modules[i]

        self.core.unloadProjectPlugins()

        openPb = False
        openSm = False
        openPs = False

        quitOnLastWindowClosed = QApplication.quitOnLastWindowClosed()
        QApplication.setQuitOnLastWindowClosed(False)

        try:
            if getattr(self.core, "pb", None) and self.core.pb.isVisible():
                self.core.pb.close()
                openPb = True
        except:
            pass

        sm = self.core.getStateManager(create=False)
        if sm:
            if sm.isVisible():
                openSm = True

            self.core.closeSM()

        try:
            if hasattr(self, "dlg_setProject") and self.dlg_setProject.isVisible():
                self.dlg_setProject.close()
        except:
            pass

        try:
            if getattr(self.core, "ps", None) and self.core.ps.isVisible():
                if settingsTab is None:
                    settingsTab = self.core.ps.getCurrentCategory()

                if settingsType is None:
                    settingsType = self.core.ps.getCurrentSettingsType()

                self.core.ps.close()
                openPs = True
        except:
            pass

        try:
            if getattr(self, "dlg_settings", None) and self.core.projects.dlg_settings.isVisible():
                self.core.projects.dlg_settings.close()
        except:
            pass

        self.core.pb = None
        self.core.sm = None
        self.core.ps = None
        self.core.dv = None
        self.dlg_settings = None

        self.core.entities.removeEntityAction("masterVersionCheckProducts")
        self.core.entities.removeEntityAction("masterVersionCheckMedia")

        if unset:
            self.core.prismIni = ""
            self.core.setConfig("globals", "current project", "")
            if hasattr(self.core, "projectName"):
                del self.core.projectName
            if hasattr(self.core, "projectPath"):
                del self.core.projectPath
            if hasattr(self.core, "projectVersion"):
                del self.core.projectVersion
            self.core.useLocalFiles = False
            QApplication.setQuitOnLastWindowClosed(quitOnLastWindowClosed)
            return

        self.core.prismIni = configPath
        self.core.projectPath = projectPath
        self.core.projectName = projectName
        self.core.projectVersion = projectVersion

        self.core.configs.clearCache()
        result = self.core.projects.refreshLocalFiles()
        if not result:
            QApplication.setQuitOnLastWindowClosed(quitOnLastWindowClosed)
            return

        if configPath != self.core.getConfig("globals", "current project") and self.core.uiAvailable:
            self.core.setConfig("globals", "current project", configPath)

        self.core.versionPadding = self.core.getConfig(
            "globals",
            "versionPadding",
            dft=self.core.versionPadding,
            configPath=configPath,
        )
        self.core.framePadding = self.core.getConfig(
            "globals", "framePadding", dft=self.core.framePadding, configPath=configPath
        )
        self.core.versionFormatVan = self.core.getConfig(
            "globals",
            "versionFormat",
            dft=self.core.versionFormatVan,
            configPath=configPath,
        )
        self.core.versionFormat = self.core.versionFormatVan.replace(
            "#", "%0{}d".format(self.core.versionPadding)
        )
        self.core.separateOutputVersionStack = not self.core.getConfig(
            "globals",
            "matchScenefileVersions",
            dft=False,
            configPath=configPath,
        )
        expPath = self.core.getConfig(
            "globals",
            "expectedPrjPath",
            dft="",
            configPath=configPath,
        )
        if expPath and expPath.strip("\\") != self.core.projectPath.strip("\\") and os.getenv(
                "PRISM_SKIP_PROJECT_PATH_WARNING", "0") != "1":
            msg = "This project should be loaded from the following path:\n\n%s\n\nCurrently it is loaded from this path:\n\n%s\n\nContinuing can have unexpected consequences." % (
                expPath, self.core.projectPath)
            self.core.popup(msg)

        self.core._scenePath = None
        self.core._shotPath = None
        self.core._sequencePath = None
        self.core._assetPath = None
        self.core._texturePath = None

        self.core.callbacks.registerProjectHooks()
        self.core.projects.unloadProjectEnvironment(beforeRefresh=True)
        self.core.projects.refreshProjectEnvironment()
        if self.core.products.getUseMaster():
            self.core.entities.addEntityAction(
                key="masterVersionCheckProducts",
                types=["asset", "shot"],
                function=self.core.products.checkMasterVersions,
                label="Check Product Master Versions..."
            )
        else:
            self.core.entities.removeEntityAction("masterVersionCheckProducts")

        if self.core.mediaProducts.getUseMaster():
            self.core.entities.addEntityAction(
                key="masterVersionCheckMedia",
                types=["asset", "shot"],
                function=self.core.mediaProducts.checkMasterVersions,
                label="Check Media Master Versions..."
            )
        else:
            self.core.entities.removeEntityAction("masterVersionCheckMedia")

        logger.debug("Loaded project " + self.core.projectPath)

        modulePath = os.path.join(self.core.projects.getPipelineFolder(), "CustomModules", "Python")
        if not os.path.exists(modulePath):
            try:
                os.makedirs(modulePath)
            except FileExistsError:
                pass

        sys.path.append(modulePath)

        pluginPath = self.core.projects.getPluginFolder()
        if os.path.exists(pluginPath):
            self.core.plugins.loadPlugins(directories=[pluginPath], recursive=True)

        self.core.projects.setRecentPrj(configPath)
        self.core.checkCommands()
        self.core.updateProjectEnvironment()
        self.core.callback(
            name="onProjectChanged",
            args=[self.core],
        )

        if self.core.uiAvailable:
            if openPb or openUi == "projectBrowser":
                self.core.projectBrowser()

            if openSm or openUi == "stateManager":
                self.core.stateManager()

            if openPs or openUi == "prismSettings":
                self.core.prismSettings(tab=settingsTab, settingsType=settingsType, reload_module=False)

        structure = self.core.projects.getProjectStructure()
        result = self.core.projects.validateFolderStructure(structure)
        if result is not True:
            msg = "The project structure is invalid. Please update the project settings."
            r = self.core.popupQuestion(msg, buttons=["Open Project Settings...", "Close"],
                                        default="Open Project Settings...", escapeButton="Close",
                                        icon=QMessageBox.Warning)
            if r == "Open Project Settings...":
                self.core.prismSettings(tab="Folder Structure", settingsType="Project")

        QApplication.setQuitOnLastWindowClosed(quitOnLastWindowClosed)
        return self.core.projectPath
