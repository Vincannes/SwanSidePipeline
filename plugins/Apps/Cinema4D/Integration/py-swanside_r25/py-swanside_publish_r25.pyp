import os
import c4d
import json
from c4d import plugins

PLUGIN1_ID = 999121031


def get_pipeline_json(scene_path_dir):
    prod_root = scene_path_dir.split("03_Production")[0]
    pipeline_json = os.path.join(prod_root, "00_Pipeline", "pipeline.json")
    if not os.path.exists(pipeline_json):
        raise ValueError("Pipeline json does not exist {}".format(pipeline_json))
    return pipeline_json


def get_shots_assets(path):
    json_path = get_pipeline_json(path)
    with open(json_path, "r") as f:
        jsonData = json.load(f)

    assets = jsonData.get("assets")
    shots = jsonData.get("shots")
    departments_shots = [i.get("name") for i in jsonData.get("globals").get("departments_shot")]
    departments_assets = [i.get("name") for i in jsonData.get("globals").get("departments_asset")]
    return assets, shots, departments_assets, departments_shots


class SwanSideDialog(c4d.gui.GeDialog):
    ID_FOLDER_BUTTON = 1001
    ID_PUBLISH_BUTTON = 1003
    ID_TEXTVIEW = 1002
    ID_PRINT_BUTTON = 1004
    ID_ENTITY_CB = 1005
    ID_NAME_CB = 1006
    ID_DEPART_CB = 1007

    # Create the Layout
    def CreateLayout(self):
        self.SetTitle("Render Elements")

        self.GroupBegin(2000, c4d.BFH_SCALEFIT, 2, 1)
        self.AddStaticText(3000, c4d.BFH_LEFT, name="        Shot or Asset:")
        self.AddComboBox(self.ID_ENTITY_CB, c4d.BFH_LEFT, initw=150, inith=20)
        self.GroupEnd()

        self.GroupBegin(2001, c4d.BFH_SCALEFIT, 2, 1)
        self.AddStaticText(3001, c4d.BFH_LEFT, name="Shot or Asset name:")
        self.AddComboBox(self.ID_NAME_CB, c4d.BFH_LEFT, initw=150, inith=20)
        self.GroupEnd()

        self.GroupBegin(2002, c4d.BFH_SCALEFIT, 2, 1)
        self.AddStaticText(3002, c4d.BFH_LEFT, name="        Departement:")
        self.AddComboBox(self.ID_DEPART_CB, c4d.BFH_LEFT, initw=150, inith=20)
        self.GroupEnd()

        self.AddButton(self.ID_FOLDER_BUTTON, c4d.BFH_SCALE | c4d.BFV_SCALE, initw=100, inith=20, name='Select Folders')
        self.AddMultiLineEditText(self.ID_TEXTVIEW, c4d.BFH_SCALEFIT | c4d.BFV_SCALEFIT,
                                  style=c4d.DR_MULTILINE_READONLY)
        self.AddButton(self.ID_PUBLISH_BUTTON, c4d.BFH_SCALE | c4d.BFV_SCALE, initw=100, inith=20, name='Publish')
        return True

    # Called after CreateLayout
    def InitValues(self):
        self.AddChild(self.ID_ENTITY_CB, 100, "Asset")
        self.AddChild(self.ID_ENTITY_CB, 102, "Shot")
        self.SetInt32(self.ID_ENTITY_CB, 100)

        self.UpdateNameComboBox(100)

        return True

    def Command(self, id, msg):
        if id == self.ID_FOLDER_BUTTON:
            self.SelectFilesOrFolders()
        elif id == self.ID_PUBLISH_BUTTON:
            self.PublishElements()
        elif id == self.ID_ENTITY_CB:
            entity_type = self.GetInt32(self.ID_ENTITY_CB)
            self.UpdateNameComboBox(entity_type)
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

    def UpdateNameComboBox(self, entity_type):
        self.FreeChildren(self.ID_NAME_CB)
        assets_entities, shots_entities, _, _ = get_shots_assets(
            c4d.documents.GetActiveDocument().GetDocumentPath()
        )

        counter = 200
        if entity_type == 100:  # Asset selected
            for _, values in assets_entities.items():
                for value in values:
                    self.AddChild(self.ID_NAME_CB, counter, value)
                    counter += 1
        elif entity_type == 102:  # Shot selected
            for _, values in shots_entities.items():
                for value in values:
                    self.AddChild(self.ID_NAME_CB, counter, value)
                    counter += 1

        if counter > 200:
            self.SetInt32(self.ID_NAME_CB, 200)

        self.UpdateDepartComboBox(entity_type)

    def UpdateDepartComboBox(self, entity_type):
        self.FreeChildren(self.ID_DEPART_CB)
        _, _, departments_assets, departments_shots = get_shots_assets(
            c4d.documents.GetActiveDocument().GetDocumentPath()
        )

        counter = 300
        if entity_type == 100:  # Asset selected
            for dept in departments_assets:
                self.AddChild(self.ID_DEPART_CB, counter, dept)
                counter += 1
        elif entity_type == 102:  # Shot selected
            for dept in departments_shots:
                self.AddChild(self.ID_DEPART_CB, counter, dept)
                counter += 1

        if counter > 300:
            self.SetInt32(self.ID_DEPART_CB, 300)

    def PublishElements(self):
        elements = self.GetString(self.ID_TEXTVIEW)
        for ele in elements.splitlines():
            print("Element:", ele)

            # argList = [
            #     python_path, publisher_py_path, ele
            # ]
            # nProc = subprocess.Popen(
            #     argList, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
            # )

            # result = nProc.communicate()
            # if sys.version[0] == "3":
            #     result = [x.decode("utf-8", "ignore") for x in result]
            print("ele")
            print(ele)


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
