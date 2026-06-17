import pandas as pd
class SchemaDetector:
    def detect(self, df) -> dict:
        schema = {}
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                schema[col] = "numeric"
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                schema[col] = "datetime"
            elif df[col].dtype == object and df[col].astype(str).str.len().mean() > 50:
                schema[col] = "text"
            else:
                schema[col] = "categorical"
        return schema
