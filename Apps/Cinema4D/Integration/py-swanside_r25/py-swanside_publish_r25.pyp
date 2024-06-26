import c4d
from c4d import plugins
from c4d import gui

PLUGIN1_ID = 999121031

class SwanSideDialog(c4d.gui.GeDialog):

    ID_FOLDER_BUTTON = 1001
    ID_PUBLISH_BUTTON = 1003
    ID_TEXTVIEW = 1002

    def CreateLayout(self):
        self.SetTitle("Swan Side Dialog")
        self.GroupBegin(1000, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, 1, 0, "Render Elements", 0)

        self.AddButton(self.ID_FOLDER_BUTTON, c4d.BFH_SCALE | c4d.BFV_SCALE, initw=100, inith=20, name='Select Folders')
        self.AddMultiLineEditText(self.ID_TEXTVIEW, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT, style=c4d.DR_MULTILINE_READONLY)
        self.AddButton(self.ID_PUBLISH_BUTTON, c4d.BFH_SCALE | c4d.BFV_SCALE, initw=100, inith=20, name='Publish')
        self.GroupEnd()
        return True

    def InitValues(self):
        return True

    def Command(self, id, msg):
        if id == self.ID_FOLDER_BUTTON:
            self.SelectFilesOrFolders()
        elif id == self.ID_PUBLISH_BUTTON:
            self.PublishElements()
        return True
    
    def SelectFilesOrFolders(self):
        selected_path = c4d.storage.LoadDialog(flags=c4d.FILESELECT_LOAD | c4d.FILESELECT_DIRECTORY)
        if selected_path:
            current_text = self.GetString(self.ID_TEXTVIEW)
            if current_text:
                current_elements = current_text.split('\n')
            else:
                current_elements = []
            
            current_elements.append(selected_path)
            self.UpdateTextView(current_elements)

    def UpdateTextView(self, elements):
        text = "\n".join(elements)
        self.SetString(self.ID_TEXTVIEW, text)

    def PublishElements(self):
        elements = self.GetString(self.ID_TEXTVIEW)
        print(elements)

class OpenSwanSideDialogCommand(plugins.CommandData):
    def Execute(self, doc):
        dlg = SwanSideDialog()
        dlg.Open(c4d.DLG_TYPE_MODAL, 0, -1, -1, 600, 250)
        return True

def main():
    plugins.RegisterCommandPlugin(
        PLUGIN1_ID,
        "Publish",
        0,
        None,
        "Publish",
        OpenSwanSideDialogCommand()
    )

if __name__ == '__main__':
    main()
