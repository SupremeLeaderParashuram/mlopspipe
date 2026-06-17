class StatisticalEngine:
    def compute(self, df) -> dict:
        n = df.select_dtypes(include="number")
        return {
            "mean":     n.mean().to_dict(),
            "median":   n.median().to_dict(),
            "variance": n.var().to_dict(),
            "std":      n.std().to_dict(),
            "skew":     n.skew().to_dict(),
            "kurtosis": n.kurt().to_dict(),
        }
