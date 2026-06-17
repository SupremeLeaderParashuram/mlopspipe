class ImbalanceEngine:
    def analyze(self, series) -> dict:
        dist = series.value_counts(normalize=True).to_dict()
        return {
            "distribution": dist,
            "minority_pct": min(dist.values()),
            "majority_pct": max(dist.values()),
        }
