class TLogAdapter:
    """MAVLink / TLOG telemetry — requires pymavlink."""
    def load(self, path: str):
        raise NotImplementedError("Install pymavlink to enable TLog support.")
