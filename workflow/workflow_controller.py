STAGES = ["import","analyze","clean","engineer","train","deploy"]

class WorkflowController:
    """Prevents advancing to a stage before its prerequisites are met."""
    def __init__(self):
        self.current_stage = "import"

    def can_advance_to(self, stage: str) -> bool:
        return STAGES.index(stage) <= STAGES.index(self.current_stage) + 1

    def advance(self, stage: str):
        if not self.can_advance_to(stage):
            raise RuntimeError(f"Cannot jump to '{stage}' from '{self.current_stage}'.")
        self.current_stage = stage
        print(f"[WorkflowController] Stage → {self.current_stage}")
