#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
from pprint import pprint

SWANSIDE_DIR = os.path.dirname(os.path.dirname(__file__))
EXT_MODULES_PATHS = os.path.join(SWANSIDE_DIR, "ExternalModules", "pandas_module")


class CSVParser(object):

    def __init__(self, path):
        self.path = path

        sys.path.append(EXT_MODULES_PATHS)

        import pandas as pd

        data = pd.read_csv(path, skiprows=0, delimiter=",")
        data = data.dropna(how="all")
        self._data_dict = data.to_dict(orient='records')

    def get_shots(self):
        import pandas as pd
        return [i.get("Shot") for i in self._data_dict if not pd.isnull(i.get("Shot"))]

    def unset_env(self):
        if EXT_MODULES_PATHS in sys.path:
            sys.path.remove(EXT_MODULES_PATHS)


if __name__ == "__main__":
    path = "C:\ProgramData\Prism2\plugins\Custom\SwanSidePlugins\VFX - MLS - SUIVI.csv"
    pprint(CSVParser(path).get_shots())
