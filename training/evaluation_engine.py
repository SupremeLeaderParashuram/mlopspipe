from sklearn.metrics import (accuracy_score, f1_score, precision_score, recall_score,
                              mean_squared_error, mean_absolute_error, r2_score)
class EvaluationEngine:
    def evaluate(self, y_true, y_pred, task: str) -> dict:
        if task == "classification":
            return {
                "accuracy":  accuracy_score(y_true, y_pred),
                "f1":        f1_score(y_true, y_pred, average="weighted", zero_division=0),
                "precision": precision_score(y_true, y_pred, average="weighted", zero_division=0),
                "recall":    recall_score(y_true, y_pred, average="weighted", zero_division=0),
            }
        return {
            "rmse": mean_squared_error(y_true, y_pred, squared=False),
            "mae":  mean_absolute_error(y_true, y_pred),
            "r2":   r2_score(y_true, y_pred),
        }
