#!/usr/bin/env python
# #support	:Trolard Vincent
# copyright	:Vincannes
import pandas as pd
from pprint import pprint


class CSVParser(object):

    def __init__(self, path):
        self.path = path

        data = pd.read_csv(path, skiprows=0, delimiter=",")
        data = data.dropna(how="all")
        self._data_dict = data.to_dict(orient='records')

    def get_shots(self):
        return [i.get("Shot") for i in self._data_dict if not pd.isnull(i.get("Shot"))]


if __name__ == "__main__":
    path = "C:\ProgramData\Prism2\plugins\Custom\SwanSidePlugins\VFX - MLS - SUIVI.csv"
    pprint(CSVParser(path).get_shots())
