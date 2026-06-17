from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

MODEL_MAP = {
    ("classification","RandomForest"): RandomForestClassifier,
    ("regression",    "RandomForest"): RandomForestRegressor,
}

class TrainingEngine:
    def train(self, df, target: str, task: str, model_name: str = "RandomForest", params: dict = None):
        X = df.drop(columns=[target])
        y = df[target]
        X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
        cls   = MODEL_MAP.get((task, model_name), RandomForestClassifier)
        model = cls(**(params or {}))
        model.fit(X_tr, y_tr)
        preds = model.predict(X_te)
        metrics = {}
        if task == "classification":
            metrics["accuracy"] = accuracy_score(y_te, preds)
        else:
            metrics["rmse"] = mean_squared_error(y_te, preds, squared=False)
        return model, metrics
