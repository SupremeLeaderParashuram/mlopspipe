import pandas as pd
class XMLAdapter:
    def load(self, path: str):
        return pd.read_xml(path)
