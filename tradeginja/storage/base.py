import abc
import pandas as pd

class Storage(abc.ABC):
    @abc.abstractmethod
    def save(self, df: pd.DataFrame, key: str):
        pass

    @abc.abstractmethod
    def load(self, key: str) -> pd.DataFrame:
        pass