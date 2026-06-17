class ValidationEngine:
    def validate(self, df, target: str = None) -> list:
        errors = []
        if df.empty:
            errors.append("Empty dataset.")
        if target and target not in df.columns:
            errors.append(f"Target column '{target}' not found.")
        if df.isnull().values.all():
            errors.append("All values are null.")
        return errors
