from abc import ABC, abstractmethod
from typing import Optional
from entity.User import User

class UserService(ABC):
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        ...

    @abstractmethod
    def create_user(self, email: str, password: str, name: str | None = None) -> User:
        ...