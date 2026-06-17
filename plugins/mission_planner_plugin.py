class MissionPlannerPlugin:
    """Reads MAVLink / TLOG / Mission files directly — requires pymavlink."""
    def load(self, path: str):
        raise NotImplementedError("Install pymavlink.")
