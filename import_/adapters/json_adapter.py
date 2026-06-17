import pandas as pd
class JSONAdapter:
    def load(self, path: str):
        return pd.read_json(path)
