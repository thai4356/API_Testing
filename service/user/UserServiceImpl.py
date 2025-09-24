from typing import Optional
from passlib.hash import bcrypt
from entity.User import User
from repository.user.UserRepository import UserRepository
from service.user.UserService import UserService
from uuid import uuid4
from sqlmodel import SQLModel

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

    def create_user(self, email: str, password: str, name: str | None = None) -> User:
        # check trùng email
        if self.repo.exists_by_email(email):
            raise ValueError("Email already exists")

        hashed = bcrypt.hash(password)
        user = User(
            email=email,
            password=hashed,
            name=name,
            is_active=True,
            is_superuser=False,
            user_token=str(uuid4()),
        )
        return self.repo.create(user)
