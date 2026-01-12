from abc import ABC, abstractmethod

from api.v1.factories.interfaces.crud_interface import CrudInterface
from api.v1.factories.interfaces.auth_interface import AuthInterface

class APIFactory(ABC):
    
    @abstractmethod
    def crud(self, type) -> CrudInterface: 
        pass 

    @abstractmethod
    def authentication(self, type) -> AuthInterface:
        pass
