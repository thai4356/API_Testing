from abc import ABC, abstractmethod
from typing import Optional
from entity.User import User

class UserService(ABC):
    @abstractmethod
    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        ...
