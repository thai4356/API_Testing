from typing import Optional
from passlib.hash import bcrypt
from entity.User import User
from repository.user.UserRepository import UserRepository
from service.user.UserService import UserService

class UserServiceImpl(UserService):
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.repo.get_by_email(email)
        if not user:
            return None
        if not bcrypt.verify(password, user.password):
            return None
        if not user.is_active:
            return None
        return user
