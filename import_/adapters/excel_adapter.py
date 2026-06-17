import pandas as pd
class ExcelAdapter:
    def load(self, path: str):
        return pd.read_excel(path)
