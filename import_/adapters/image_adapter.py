import pandas as pd
from pathlib import Path
class ImageAdapter:
    def load(self, folder: str):
        files = list(Path(folder).rglob("*.*"))
        return pd.DataFrame({"filepath": [str(f) for f in files]})
