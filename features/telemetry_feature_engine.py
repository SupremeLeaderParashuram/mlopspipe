class TelemetryFeatureEngine:
    """Creates lag, jitter, RSSI trends, entropy features from telemetry data."""
    def extract(self, df):
        df = df.copy()
        if "signal" in df.columns:
            df["lag_1"]        = df["signal"].shift(1)
            df["jitter"]       = df["signal"].diff().abs()
            df["rolling_mean"] = df["signal"].rolling(5).mean()
        return df.dropna()
