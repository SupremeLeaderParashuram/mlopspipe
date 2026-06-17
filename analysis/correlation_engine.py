class CorrelationEngine:
    def compute(self, df) -> dict:
        n = df.select_dtypes(include="number")
        return {
            "pearson":  n.corr(method="pearson").to_dict(),
            "spearman": n.corr(method="spearman").to_dict(),
        }
