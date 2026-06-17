class CleaningPipeline:
    def run(self, df, strategy: dict = None):
        strategy = strategy or {}
        df = df.drop_duplicates()
        fill = strategy.get("fill_missing", "mean")
        if fill == "mean":
            df = df.fillna(df.mean(numeric_only=True))
        elif fill == "drop":
            df = df.dropna()
        df = df.loc[:, df.nunique() > 1]   # drop constants
        return df
