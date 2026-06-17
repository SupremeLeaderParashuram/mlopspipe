import pandas as pd
class TaskDetector:
    def detect(self, df, target: str) -> str:
        if target not in df.columns:
            return "clustering"
        n = df[target].nunique()
        if pd.api.types.is_numeric_dtype(df[target]) and n > 20:
            return "regression"
        return "classification"
