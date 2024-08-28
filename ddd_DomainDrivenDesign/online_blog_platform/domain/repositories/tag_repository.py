from typing import List, Optional
from sqlalchemy.orm import Session
from domain.models.tag import Tag


class TagRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def save(self, tag: Tag) -> None:
        if tag.id is None:
            self.db_session.add(tag)
        self.db_session.commit()

    def find_by_id(self, tag_id: int) -> Optional[Tag]:
        return self.db_session.query(Tag).filter_by(id=tag_id).first()

    def find_all(self) -> List[Tag]:
        return self.db_session.query(Tag).all()

    def delete(self, tag: Tag) -> None:
        self.db_session.delete(tag)
        self.db_session.commit()
