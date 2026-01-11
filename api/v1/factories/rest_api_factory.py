from api.v1.factories.factory import APIFactory
from api.v1.apps.users.services.claim_services import ClaimCrudService
from api.v1.apps.users.services.role_services import RoleCrudService 
from api.v1.apps.users.services.users_services import UserCrudService


class RestAPIFactory(APIFactory): 

    def __init__(self): 
        super().__init__()

    def crud(self, type):
        match type:
            case "claim":
                return ClaimCrudService()
            case "role":
                return RoleCrudService()
            case "users":
                return UserCrudService()