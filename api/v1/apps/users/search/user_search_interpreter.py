from api.v1.apps.users.models.user_models import User

from datetime import datetime
import calendar
from enum import Enum

    
class SearchInterpreter:

    class SearchTypes(Enum):
        TRUE = "true"
        FALSE = "false"
        NOT_BOOL = "not_bool"

    def get_candidates_by_flag(self, flag):
        mapping = {
            "users": [
                User.name,
                User.email,
                User.is_active,
                User.created_at,
                User.id,
            ],
        }
        return mapping.get(flag, [])

    
    def detect_created_at_range(self, search: str):
        s = search.strip()

        if not s:
            return None

        
        if s.isdigit() and len(s) == 4:
            year = int(s)
            return {
                "type": "year",
                "year": year,
            }

        if s.isdigit():
            num = int(s)

            if 13 <= num <= 31:
                return {
                    "type": "day",
                    "day": num,
                }

            if 1 <= num <= 12:
                return {
                    "type": "day_or_month",
                    "value": num,
                }

        for fmt in ("%d/%m/%Y", "%d-%m-%Y"):
            try:
                dt = datetime.strptime(s, fmt)
                return {
                    "type": "range",
                    "start": dt.replace(hour=0, minute=0, second=0),
                    "end": dt.replace(hour=23, minute=59, second=59),
                }
            except ValueError:
                pass

        for fmt in ("%m/%Y", "%m-%Y"):
            try:
                dt = datetime.strptime(s, fmt)
                last_day = calendar.monthrange(dt.year, dt.month)[1]
                return {
                    "type": "range",
                    "start": datetime(dt.year, dt.month, 1),
                    "end": datetime(dt.year, dt.month, last_day, 23, 59, 59),
                }
            except ValueError:
                pass

        return None


    def detect_bool(self, search: str):
        search_lower = (search or "").strip().lower()

        true_values = {"true", "1", "t", "yes", "sim", "ativo", "active"}
        false_values = {"false", "0", "f", "no", "nao", "inativo", "inactive"}

        if search_lower in true_values:
            return self.SearchTypes.TRUE

        if search_lower in false_values:
            return self.SearchTypes.FALSE

        return self.SearchTypes.NOT_BOOL