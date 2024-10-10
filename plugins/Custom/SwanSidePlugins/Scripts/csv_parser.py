#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import os
import sys
import logging
from pprint import pprint

SWANSIDE_DIR = os.path.dirname(os.path.dirname(__file__))
EXT_MODULES_PATHS = os.path.join(SWANSIDE_DIR, "ExternalModules",)
EXT_PANDAS_MODULES_PATHS = os.path.join(SWANSIDE_DIR, "ExternalModules", "pandas_module")

sys.path.append(EXT_MODULES_PATHS)

import csv
logger = logging.getLogger(__name__)


class CSVParser(object):
    SHOTS = "Shots"
    ASSETS = "Assets"
    FRAME_RANGE_IN = "FRAMES RANGE"
    FRAME_RANGE_OUT = "Unnamed: 2"

    def __init__(self, path):
        self.path = path

        sys.path.append(EXT_PANDAS_MODULES_PATHS)

        try:
            import pandas as pd
            self.has_pandas = True
            data = pd.read_csv(path, skiprows=0, delimiter=",")
            data = data.dropna(how="all")
            self._data_dict = data.to_dict(orient='records')
        except:
            self.has_pandas = False
            self._data_dict = None

        logger.info("Has pandas : " + str(self.has_pandas))
        logger.info(path)

    def get_shots(self):
        if self.has_pandas:
            import pandas as pd
            shots = [i.get(self.SHOTS) for i in self._data_dict if not pd.isnull(i.get(self.SHOTS))]
        else:
            shots = self.read_csv(self.path, self.SHOTS)
        return shots

    def get_assets(self):
        if self.has_pandas:
            import pandas as pd
            assets = [i.get(self.ASSETS) for i in self._data_dict if not pd.isnull(i.get(self.ASSETS))]
        else:
            assets = self.read_csv(self.path, self.ASSETS)
        return assets

    def get_shots_framerange(self):
        if self.has_pandas:
            import pandas as pd
            data = {}
            for i in self._data_dict:
                if not pd.isnull(i.get(self.SHOTS)):
                    shot = i.get(self.SHOTS)
                    frame_in = i.get(self.FRAME_RANGE_IN)
                    frame_out = i.get(self.FRAME_RANGE_OUT)
                    data[shot] = (frame_in, frame_out)
        else:
            data = self.get_shots()
        return data

    def unset_env(self):
        if EXT_MODULES_PATHS in sys.path:
            sys.path.remove(EXT_MODULES_PATHS)

    def read_csv(self, fichier_csv, key="Shots"):
        dictionnaire = {}

        with open(fichier_csv, 'r', encoding='utf-8') as fichier:
            lecteur_csv = csv.reader(fichier)

            cles = next(lecteur_csv)

            for index, ligne in enumerate(lecteur_csv, start=1):
                if not ligne or all(cell.strip() == "" for cell in ligne):
                    continue

                entree = {}
                for i, cle in enumerate(enumerate(cles)):
                    if cle[1] == key:
                        dictionnaire[ligne[i].strip()] = (ligne[1].strip(), ligne[2].strip())
        return dictionnaire


if __name__ == "__main__":
    path = "D:\\Desk\\armes\\BUENAS NOCHES - SWANSIDE SHOTS - SUIVI.csv"
    pprint(CSVParser(path).get_shots_framerange())
