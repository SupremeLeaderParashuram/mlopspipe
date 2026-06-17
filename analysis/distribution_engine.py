class DistributionEngine:
    def classify(self, df) -> dict:
        result = {}
        for col in df.select_dtypes(include="number").columns:
            skew = df[col].skew()
            kurt = df[col].kurt()
            if abs(skew) < 0.5:
                label = "normal"
            elif abs(skew) >= 1:
                label = "skewed"
            elif kurt > 3:
                label = "heavy_tail"
            else:
                label = "uniform"
            result[col] = label
        return result
