from abc import ABC, abstractmethod
from typing import Any, Dict, List

class CrudInterface(ABC):

    @abstractmethod
    def create(self, schema: Dict, session: Any,) -> Dict[str, str]: 
        pass 

    @abstractmethod
    def read(self, session: Any) -> Dict[str, str]:
        pass 

    @abstractmethod
    def update(self, session: Any, schema: List, **kwargs: Any):
        pass 

    @abstractmethod
    def delete(self, session: Any, schema: List):
        pass