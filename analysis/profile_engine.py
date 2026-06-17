class ProfileEngine:
    def profile(self, df) -> dict:
        return {
            "rows": len(df),
            "columns": len(df.columns),
            "missing_pct": df.isnull().mean().to_dict(),
            "duplicates": int(df.duplicated().sum()),
            "memory_mb": round(df.memory_usage(deep=True).sum() / 1e6, 2),
        }
