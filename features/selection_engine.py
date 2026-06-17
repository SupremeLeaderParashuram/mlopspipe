from sklearn.feature_selection import VarianceThreshold, mutual_info_classif
class SelectionEngine:
    def select(self, df, target: str, method: str = "variance", k: int = 10) -> list:
        X = df.drop(columns=[target])
        y = df[target]
        nums = X.select_dtypes(include="number")
        if method == "variance":
            sel = VarianceThreshold()
            sel.fit(nums)
            return list(nums.columns[sel.get_support()])
        if method == "mutual_info":
            scores = mutual_info_classif(nums, y)
            ranked = sorted(zip(nums.columns, scores), key=lambda x: -x[1])
            return [c for c,_ in ranked[:k]]
        return list(X.columns)
