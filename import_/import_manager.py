from pathlib import Path
from .adapters import (CSVAdapter, ExcelAdapter, JSONAdapter, XMLAdapter,
                       TLogAdapter, ImageAdapter, ZipAdapter)

ADAPTER_MAP = {
    ".csv":  CSVAdapter,
    ".xlsx": ExcelAdapter,
    ".xls":  ExcelAdapter,
    ".json": JSONAdapter,
    ".xml":  XMLAdapter,
    ".tlog": TLogAdapter,
    ".zip":  ZipAdapter,
}

class ImportManager:
    def load(self, path: str):
        ext = Path(path).suffix.lower()
        cls = ADAPTER_MAP.get(ext)
        if not cls:
            raise ValueError(f"Unsupported file type: {ext}")
        return cls().load(path)
