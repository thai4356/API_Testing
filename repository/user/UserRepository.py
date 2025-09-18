from typing import Optional
from sqlmodel import select
from repository.BaseRepository import BaseRepository
from entity.User import User

class UserRepository(BaseRepository):
    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.exec(stmt).first()
