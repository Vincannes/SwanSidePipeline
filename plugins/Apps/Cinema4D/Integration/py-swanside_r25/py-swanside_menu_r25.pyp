import c4d
from c4d import gui


def EnhanceMainMenu():
    mainMenu = gui.GetMenuResource("M_EDITOR")
    pluginsMenu = gui.SearchPluginMenuResource()

    menu = c4d.BaseContainer()
    menu.InsData(c4d.MENURESOURCE_SUBTITLE, "Prism")
    menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_{}".format(999121031))
    # menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_{}".format(c4d.Osphere))
    # menu.InsData(c4d.MENURESOURCE_COMMAND, "PLUGIN_CMD_{}".format(c4d.Oplane))

    if pluginsMenu:
        mainMenu.InsDataAfter(c4d.MENURESOURCE_STRING, menu, pluginsMenu)
    else:
        mainMenu.InsData(c4d.MENURESOURCE_STRING, menu)

    gui.UpdateMenuBar()


def PluginMessage(id, data):
    if id == c4d.C4DPL_BUILDMENU:
        EnhanceMainMenu()
        return True
    return False
