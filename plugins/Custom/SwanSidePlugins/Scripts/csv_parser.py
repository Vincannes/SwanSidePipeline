#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
from pprint import pprint

SWANSIDE_DIR = os.path.dirname(os.path.dirname(__file__))
EXT_MODULES_PATHS = os.path.join(SWANSIDE_DIR, "ExternalModules", "pandas_module")

class CSVParser(object):
    SHOTS = "Shots"
    ASSETS = "Assets"
    FRAME_RANGE_IN = "FRAMES RANGE"
    FRAME_RANGE_OUT = "Unnamed: 2"

    def __init__(self, path):
        self.path = path

        sys.path.append(EXT_MODULES_PATHS)

        import pandas as pd

        data = pd.read_csv(path, skiprows=0, delimiter=",")
        data = data.dropna(how="all")
        self._data_dict = data.to_dict(orient='records')


    def get_shots(self):
        import pandas as pd
        return [i.get(self.SHOTS) for i in self._data_dict if not pd.isnull(i.get(self.SHOTS))]

    def get_assets(self):
        import pandas as pd
        return [i.get(self.ASSETS) for i in self._data_dict if not pd.isnull(i.get(self.ASSETS))]

    def get_shots_framerange(self):
        import pandas as pd
        data = {}
        for i in self._data_dict:
            if not pd.isnull(i.get(self.SHOTS)):
                shot = i.get(self.SHOTS)
                frame_in = i.get(self.FRAME_RANGE_IN)
                frame_out = i.get(self.FRAME_RANGE_OUT)
                data[shot] = (frame_in, frame_out)
        return data

    def unset_env(self):
        if EXT_MODULES_PATHS in sys.path:
            sys.path.remove(EXT_MODULES_PATHS)


if __name__ == "__main__":
    path = "D:\\Desk\\armes\\BUENAS NOCHES - SWANSIDE SHOTS - SUIVI.csv"
    pprint(CSVParser(path).get_shots_framerange())
