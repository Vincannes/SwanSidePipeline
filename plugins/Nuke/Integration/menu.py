# >>>PrismStart
import sys
import nuke

if ((not nuke.env["studio"]) or nuke.env["indie"]) and nuke.env.get("gui"):
    if "pcore" in locals():
        nuke.message("Prism is loaded multiple times. This can cause unexpected errors. Please clean this file from all Prism related content:\n\n%s\n\nYou can add a new Prism integration through the Prism Settings dialog" % __file__)
    elif sys.version[0] == "2":
        nuke.message("Prism supports only Python 3 versions of Nuke.\nPython 3 is the default in Nuke 13 and later.")
    else:
        import os
        import sys

        prismRoot = os.getenv("PRISM_ROOT")
        if not prismRoot:
            prismRoot = "C:/Program Files/Prism2"

        scriptDir = os.path.join(prismRoot, "Scripts")
        if scriptDir not in sys.path:
            sys.path.append(scriptDir)

        import PrismCore

        pcore = PrismCore.PrismCore(app="Nuke")
        plugin_swanside = pcore.getPlugin("SwanSidePlugins")
        prism_menu = nuke.menu("Nuke").findItem("Prism")
        prism_menu.addCommand("Publish", "plugin_swanside.swanside_nuke.ui_publisher(pcore, QtWidgets.QApplication.activeWindow()).show()")
        prism_menu.addCommand("Read Manager", "plugin_swanside.swanside_nuke.read_manager(QtWidgets.QApplication.activeWindow()).show()")
# <<<PrismEnd
