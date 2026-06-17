import zipfile, tempfile, os, pandas as pd
class ZipAdapter:
    def load(self, path: str):
        with tempfile.TemporaryDirectory() as tmp:
            with zipfile.ZipFile(path) as z:
                z.extractall(tmp)
            csvs = [os.path.join(tmp, f) for f in os.listdir(tmp) if f.endswith(".csv")]
            if csvs:
                return pd.concat([pd.read_csv(c) for c in csvs], ignore_index=True)
        raise ValueError("No CSV files found in zip.")
