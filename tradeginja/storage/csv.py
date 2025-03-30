import os
import pandas as pd
from .base import Storage

class CSVStorage(Storage):
    """CSV-specific storage."""
    def __init__(self, base_path: str = "."):
        self.base_path = base_path

    def save(self, df: pd.DataFrame, key: str):
        file_path = os.path.join(self.base_path, key)
        df.to_csv(file_path, index=False)
        print(f"Data stored in {file_path}")

    def load(self, key: str) -> pd.DataFrame:
        file_path = os.path.join(self.base_path, key)
        if os.path.exists(file_path):
            return pd.read_csv(file_path)
        return pd.DataFrame()  # Return empty DataFrame if file doesn’t exist