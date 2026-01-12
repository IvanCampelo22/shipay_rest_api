from abc import abstractmethod, ABC
from typing import Any, Optional

class FiltersInterface(ABC):

    @abstractmethod
    def filters(self, offset: Optional[Any], limit: Optional[Any], session: Any, args: Optional[Any], **kwargs):
        pass

    @abstractmethod
    def filter_by_id(self, object_id: Optional[int], args: Optional[Any], session: Any):
        pass