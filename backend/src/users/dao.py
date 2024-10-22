from base_dao import BaseDAO
from users.models import Users


class UsersDAO(BaseDAO[Users]):
    model = Users
