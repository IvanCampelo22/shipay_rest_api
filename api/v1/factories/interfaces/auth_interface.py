from abc import abstractmethod, ABC
from typing import Dict, Any

class AuthInterface(ABC):

    @abstractmethod
    def login(self, schema: Dict, args, session: Any):
        pass 

    @abstractmethod
    def logout(self, args, session: Any):
        pass

    @abstractmethod
    def change_password(self, schema: Dict, session: Any):
        pass