from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
SCALERS = {"standard": StandardScaler, "minmax": MinMaxScaler, "robust": RobustScaler}
class ScalingEngine:
    def scale(self, df, method: str = "standard"):
        scaler = SCALERS[method]()
        nums = df.select_dtypes(include="number").columns
        df = df.copy()
        df[nums] = scaler.fit_transform(df[nums])
        return df
