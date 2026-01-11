from abc import ABC, abstractmethod

from api.v1.factories.interfaces.crud_interface import CrudInterface

class APIFactory(ABC):
    
    @abstractmethod
    def crud(self, type) -> CrudInterface: 
        pass 
