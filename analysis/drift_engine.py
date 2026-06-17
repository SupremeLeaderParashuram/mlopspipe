import numpy as np
class DriftEngine:
    """PSI / KL / JS divergence for telemetry drift detection."""
    def psi(self, expected, actual, bins=10) -> float:
        bp  = np.linspace(0, 1, bins + 1)
        exp = np.histogram(expected, bins=bp)[0] / len(expected) + 1e-8
        act = np.histogram(actual,   bins=bp)[0] / len(actual)   + 1e-8
        return float(np.sum((act - exp) * np.log(act / exp)))
