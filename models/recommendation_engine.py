class ModelRecommender:
    RULES = {
        ("classification","small"): ["RandomForest","XGBoost","LightGBM"],
        ("classification","large"): ["LightGBM","XGBoost"],
        ("regression","small"):     ["RandomForest","XGBoost"],
        ("regression","large"):     ["LightGBM","XGBoost"],
        ("clustering","small"):     ["KMeans","DBSCAN"],
    }
    def recommend(self, task: str, size: str = "small") -> list:
        return self.RULES.get((task, size), ["XGBoost"])
