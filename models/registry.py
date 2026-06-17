class ModelRegistry:
    def __init__(self):
        self._store = {}
    def register(self, name: str, model):
        self._store[name] = model
    def get(self, name: str):
        return self._store.get(name)
    def list_models(self) -> list:
        return list(self._store.keys())
