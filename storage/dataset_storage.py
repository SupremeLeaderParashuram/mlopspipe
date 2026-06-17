import pandas as pd
class DatasetStorage:
    def save(self, df, path: str):
        df.to_parquet(path, index=False)
    def load(self, path: str):
        return pd.read_parquet(path)
