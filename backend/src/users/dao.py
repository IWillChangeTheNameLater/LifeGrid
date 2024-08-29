from backend.src.base_dao import BaseDAO
from backend.src.users.models import Users


class UsersDAO(BaseDAO):
    model = Users
