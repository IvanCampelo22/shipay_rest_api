from abc import ABC, abstractmethod

from api.v1.factories.interfaces.crud_interface import CrudInterface
from api.v1.factories.interfaces.auth_interface import AuthInterface
from api.v1.factories.interfaces.filters_interface import FiltersInterface

class APIFactory(ABC):
    
    @abstractmethod
    def crud(self, type) -> CrudInterface: 
        pass 

    @abstractmethod
    def authentication(self, type) -> AuthInterface:
        pass

    @abstractmethod
    def filters(self, type) -> FiltersInterface:
        pass
