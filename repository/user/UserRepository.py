from typing import Optional
from sqlmodel import select
from repository.BaseRepository import BaseRepository
from entity.User import User

class UserRepository(BaseRepository):
    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        return self.session.exec(stmt).first()

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
