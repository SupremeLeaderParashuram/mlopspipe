import pandas as pd
from sklearn.preprocessing import LabelEncoder
class EncodingEngine:
    def encode(self, df, method: str = "onehot"):
        cats = df.select_dtypes(include=["object","category"]).columns.tolist()
        if method == "onehot":
            return pd.get_dummies(df, columns=cats)
        if method == "label":
            df = df.copy()
            le = LabelEncoder()
            for c in cats:
                df[c] = le.fit_transform(df[c].astype(str))
        return df
