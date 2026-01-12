from api.v1.factories.factory import APIFactory
from api.v1.apps.users.services.claim_services import ClaimCrudService
from api.v1.apps.users.services.role_services import RoleCrudService 
from api.v1.apps.users.services.users_services import UserCrudService
from api.v1.apps.users.services.authentication import UsersAuthenticationService
from api.v1.apps.users.services.filters_services import UserFilterService


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
    
    def authentication(self, type):
        match type:
            case "authentication":
                return UsersAuthenticationService()
            
    def filters(self, type):
        match type:
            case "filters_users":
                return UserFilterService()