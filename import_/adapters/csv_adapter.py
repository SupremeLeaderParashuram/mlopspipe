import pandas as pd
class CSVAdapter:
    def load(self, path: str):
        return pd.read_csv(path)
